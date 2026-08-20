#!/usr/bin/env node
/**
 * Generic Playwright smoke runner — reads docs/smoke-routes.json (or --config path).
 * Studio library: packages/qa-smoke/bin/run-smoke-routes.mjs
 */
import { spawn } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

function parseArgs(argv) {
  const args = { config: resolve(process.cwd(), 'docs/smoke-routes.json') };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--config' && argv[i + 1]) {
      args.config = resolve(process.cwd(), argv[++i]);
    }
  }
  return args;
}

function loadConfig(configPath) {
  if (!existsSync(configPath)) {
    throw new Error(`Smoke config not found: ${configPath}`);
  }
  const raw = readFileSync(configPath, 'utf8');
  const config = JSON.parse(raw);
  if (!Array.isArray(config.routes) || config.routes.length === 0) {
    throw new Error(`${configPath}: "routes" must be a non-empty array`);
  }
  return config;
}

function expandCommand(template, vars) {
  return template.map((part) =>
    part.replace(/\{(\w+)\}/g, (_, key) => String(vars[key] ?? '')),
  );
}

function startServer(command, cwd, env) {
  return new Promise((resolveStart, reject) => {
    const child = spawn(command[0], command.slice(1), {
      cwd,
      env: { ...process.env, ...env },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let ready = false;
    const timeoutMs = 60_000;
    const timer = setTimeout(() => {
      if (!ready) {
        child.kill('SIGTERM');
        reject(new Error(`Server did not become ready within ${timeoutMs}ms`));
      }
    }, timeoutMs);

    const onData = (chunk) => {
      const text = chunk.toString();
      process.stderr.write(text);
      if (!ready && /ready|started server|listening/i.test(text)) {
        ready = true;
        clearTimeout(timer);
        resolveStart(child);
      }
    };

    child.stdout?.on('data', onData);
    child.stderr?.on('data', onData);
    child.on('error', reject);

    setTimeout(() => {
      if (!ready) {
        ready = true;
        clearTimeout(timer);
        resolveStart(child);
      }
    }, 3000);
  });
}

async function runRoute(page, baseUrl, route) {
  const url = `${baseUrl}${route.path}`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30_000 });

  if (route.waitForUrl) {
    const pattern =
      typeof route.waitForUrl === 'string'
        ? new RegExp(route.waitForUrl)
        : route.waitForUrl;
    await page.waitForURL(pattern, { timeout: 15_000 });
  }

  if (route.expectSelector) {
    await page.waitForSelector(route.expectSelector, { timeout: 15_000 });
  }

  if (route.expectText) {
    const body = await page.textContent('body');
    if (!body?.includes(route.expectText)) {
      throw new Error(`Expected text "${route.expectText}" on ${route.path}`);
    }
  }
}

async function main() {
  const { config: configPath } = parseArgs(process.argv);
  const config = loadConfig(configPath);

  const host = config.host ?? '127.0.0.1';
  const port = config.port ?? 3456;
  const baseUrl = config.baseUrl ?? `http://${host}:${port}`;
  const startCwd = resolve(process.cwd(), config.startCwd ?? '.');
  const startCommand = config.startCommand ?? [
    'npx',
    'next',
    'start',
    '-p',
    '{port}',
    '-H',
    '{host}',
  ];
  const command = expandCommand(startCommand, { port, host });

  console.log(`[smoke] config: ${configPath}`);
  console.log(`[smoke] server: ${command.join(' ')} (cwd=${startCwd})`);

  const server = await startServer(command, startCwd, config.env ?? {});
  const browser = await chromium.launch({ headless: true });

  try {
    const page = await browser.newPage();
    for (const route of config.routes) {
      console.log(`[smoke] ${route.path}`);
      await runRoute(page, baseUrl, route);
    }
    console.log(`[smoke] OK — ${config.routes.length} route(s)`);
  } finally {
    await browser.close();
    server.kill('SIGTERM');
  }
}

main().catch((err) => {
  console.error('[smoke] FAILED:', err.message ?? err);
  process.exit(1);
});
