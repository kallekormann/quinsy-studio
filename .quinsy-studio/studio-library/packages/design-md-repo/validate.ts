import { load as loadYaml } from 'js-yaml';
import type {
  DesignMdDocument,
  DesignMdFrontmatter,
  DesignMdValidationError,
  DesignMdValidationResult,
} from './types';

function err(path: string, message: string): DesignMdValidationError {
  return { path, message };
}

function isRecord(v: unknown): v is Record<string, unknown> {
  return !!v && typeof v === 'object' && !Array.isArray(v);
}

function isStringArray(v: unknown): v is string[] {
  return Array.isArray(v) && v.every((x) => typeof x === 'string' && x.length > 0);
}

function isNumberMap(v: unknown): v is Record<string, number> {
  return (
    isRecord(v) && Object.keys(v).length > 0 && Object.values(v).every((x) => typeof x === 'number')
  );
}

/** Split Design.md into YAML frontmatter + narrative body. */
export function splitDesignMd(
  raw: string,
): { yaml: string; narrative: string } | { error: string } {
  const text = raw.replace(/^\uFEFF/, '');
  if (!text.startsWith('---')) {
    return { error: 'Design.md must start with YAML frontmatter (---)' };
  }
  const rest = text.slice(3);
  const end = rest.search(/\n---\s*(?:\n|$)/);
  if (end < 0) {
    return { error: 'Design.md frontmatter is missing closing ---' };
  }
  const yaml = rest.slice(0, end).trim();
  const after = rest.slice(end).replace(/^\n---\s*/, '');
  const narrative = after.replace(/^\n/, '');
  return { yaml, narrative };
}

const REQUIRED_TYPO_KEYS = [
  { label: 'Display/*', test: (k: string) => /^Display\//i.test(k) },
  { label: 'Heading/H1', test: (k: string) => /^Heading\/H1$/i.test(k) },
  { label: 'Heading/H2', test: (k: string) => /^Heading\/H2$/i.test(k) },
  { label: 'Heading/H3', test: (k: string) => /^Heading\/H3$/i.test(k) },
  { label: 'Body/Regular', test: (k: string) => /^Body\/Regular$/i.test(k) },
  { label: 'Utility/*', test: (k: string) => /Utility/i.test(k) },
] as const;

function validateFrontmatterObject(data: unknown): DesignMdValidationError[] {
  const errors: DesignMdValidationError[] = [];
  if (!isRecord(data)) {
    return [err('', 'Frontmatter must be a YAML mapping/object')];
  }

  if (data.schema_version !== '1.0') {
    errors.push(err('/schema_version', 'must be "1.0"'));
  }
  if (typeof data.id !== 'string' || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(data.id)) {
    errors.push(err('/id', 'must be a kebab-case id'));
  }
  if (typeof data.name !== 'string' || !data.name.trim()) {
    errors.push(err('/name', 'must be a non-empty string'));
  }

  if (!isRecord(data.token_hooks)) {
    errors.push(err('/token_hooks', 'required object'));
  } else {
    for (const key of ['color_primitives', 'color_semantic', 'spacing', 'radius'] as const) {
      if (!isStringArray(data.token_hooks[key])) {
        errors.push(err(`/token_hooks/${key}`, 'must be a non-empty string array'));
      }
    }
  }

  if (!isNumberMap(data.spacing_px)) {
    errors.push(err('/spacing_px', 'must be a non-empty map of numbers'));
  }
  if (!isNumberMap(data.radius_px)) {
    errors.push(err('/radius_px', 'must be a non-empty map of numbers'));
  }

  if (!isRecord(data.typography)) {
    errors.push(err('/typography', 'required object'));
  } else {
    const keys = Object.keys(data.typography);
    for (const req of REQUIRED_TYPO_KEYS) {
      if (!keys.some((k) => req.test(k))) {
        errors.push(err('/typography', `missing required typography key matching ${req.label}`));
      }
    }
    for (const [key, style] of Object.entries(data.typography)) {
      if (!isRecord(style)) {
        errors.push(err(`/typography/${key}`, 'must be an object'));
        continue;
      }
      if (typeof style.size !== 'number')
        errors.push(err(`/typography/${key}/size`, 'must be a number'));
      if (typeof style.lineHeight !== 'number') {
        errors.push(err(`/typography/${key}/lineHeight`, 'must be a number'));
      }
      if (typeof style.weight !== 'string' || !style.weight) {
        errors.push(err(`/typography/${key}/weight`, 'must be a non-empty string'));
      }
    }
  }

  if (!isRecord(data.layout)) {
    errors.push(err('/layout', 'required object'));
  } else {
    const dist = data.layout.color_distribution;
    if (!isRecord(dist)) {
      errors.push(err('/layout/color_distribution', 'required object'));
    } else {
      for (const k of ['tone', 'structure', 'accent'] as const) {
        if (typeof dist[k] !== 'number') {
          errors.push(err(`/layout/color_distribution/${k}`, 'must be a number'));
        }
      }
    }
    const borders = data.layout.borders;
    if (!isRecord(borders) || !['none', 'hairline', 'thick'].includes(String(borders.default))) {
      errors.push(err('/layout/borders/default', 'must be none | hairline | thick'));
    }
    const shadows = data.layout.shadows;
    if (!isRecord(shadows) || !['none', 'soft', 'hard-ink'].includes(String(shadows.default))) {
      errors.push(err('/layout/shadows/default', 'must be none | soft | hard-ink'));
    }
    const corners = data.layout.corners;
    if (!isRecord(corners) || !['rounded', 'sharp'].includes(String(corners.bias))) {
      errors.push(err('/layout/corners/bias', 'must be rounded | sharp'));
    }
    if (
      data.layout.whitespace_bias !== undefined &&
      !['generous', 'compact', 'dense'].includes(String(data.layout.whitespace_bias))
    ) {
      errors.push(err('/layout/whitespace_bias', 'must be generous | compact | dense'));
    }
  }

  if (!isRecord(data.modes) || data.modes.light_dark !== 'variable_modes') {
    errors.push(err('/modes/light_dark', 'must be "variable_modes"'));
  }

  if (
    isRecord(data.token_hooks) &&
    isNumberMap(data.spacing_px) &&
    isStringArray(data.token_hooks.spacing)
  ) {
    for (const key of data.token_hooks.spacing) {
      if (!(key in data.spacing_px)) {
        errors.push(
          err(`/spacing_px/${key}`, `token_hooks.spacing "${key}" missing from spacing_px`),
        );
      }
    }
  }
  if (
    isRecord(data.token_hooks) &&
    isNumberMap(data.radius_px) &&
    isStringArray(data.token_hooks.radius)
  ) {
    for (const key of data.token_hooks.radius) {
      if (!(key in data.radius_px)) {
        errors.push(err(`/radius_px/${key}`, `token_hooks.radius "${key}" missing from radius_px`));
      }
    }
  }

  return errors;
}

/**
 * Validate a Design.md string (YAML frontmatter + optional narrative).
 * Returns field-level errors — never a bare throw for schema failures.
 */
export function validateDesignMd(raw: string): DesignMdValidationResult {
  const split = splitDesignMd(raw);
  if ('error' in split) {
    return { ok: false, errors: [{ path: '', message: split.error }] };
  }

  let parsed: unknown;
  try {
    parsed = loadYaml(split.yaml);
  } catch (e) {
    return {
      ok: false,
      errors: [
        {
          path: '',
          message: `YAML parse error: ${e instanceof Error ? e.message : String(e)}`,
        },
      ],
    };
  }

  const errors = validateFrontmatterObject(parsed);
  if (errors.length) {
    return { ok: false, errors };
  }

  const document: DesignMdDocument = {
    frontmatter: parsed as DesignMdFrontmatter,
    narrative: split.narrative.trim(),
  };
  return { ok: true, document };
}

/** Validate an already-parsed frontmatter object (API / tests). */
export function validateDesignMdFrontmatter(data: unknown): DesignMdValidationResult {
  const errors = validateFrontmatterObject(data);
  if (errors.length) {
    return { ok: false, errors };
  }
  return {
    ok: true,
    document: {
      frontmatter: data as DesignMdFrontmatter,
      narrative: '',
    },
  };
}
