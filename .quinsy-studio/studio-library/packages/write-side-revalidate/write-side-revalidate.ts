const PUBLIC_PREFIX = "NEXT_PUBLIC_";

/** Env names that ship in the browser bundle cannot hold write-side secrets. */
export function isClientExposedEnvName(name: string): boolean {
  return name.startsWith(PUBLIC_PREFIX);
}

/**
 * First non-empty value among server-only keys.
 * Skips `NEXT_PUBLIC_*` even when set — those keys are visible to `"use client"`
 * and must never be the source of a revalidate secret.
 */
export function pickServerOnlySecret(
  env: Record<string, string | undefined>,
  keys: string[],
): string {
  for (const key of keys) {
    if (isClientExposedEnvName(key)) {
      continue;
    }
    const value = env[key]?.trim() ?? "";
    if (value) {
      return value;
    }
  }
  return "";
}

export type WriteSideRevalidateInput = {
  origin: string;
  secret: string;
  path?: string;
  headerName?: string;
  payload?: Record<string, unknown>;
  fetchImpl?: typeof fetch;
};

export type WriteSideRevalidateResult = "ok" | "skipped" | "failed";

/**
 * Bust a delivery cache after a write. Call only from the plane that already
 * holds the secret (admin worker, server action, route handler). A `"use client"`
 * module cannot see admin-only env: Saved can look true while the public host
 * stays stale.
 */
export async function revalidateAfterWrite(
  input: WriteSideRevalidateInput,
): Promise<WriteSideRevalidateResult> {
  const origin = input.origin.replace(/\/$/, "");
  const secret = input.secret.trim();
  if (!origin || !secret) {
    return "skipped";
  }

  const rawPath = input.path ?? "/api/revalidate";
  const path = rawPath.startsWith("/") ? rawPath : `/${rawPath}`;
  const headerName = input.headerName ?? "x-revalidate-secret";
  const fetchImpl = input.fetchImpl ?? fetch;

  try {
    const response = await fetchImpl(`${origin}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        [headerName]: secret,
      },
      body: JSON.stringify(input.payload ?? {}),
    });
    return response.ok ? "ok" : "failed";
  } catch {
    return "failed";
  }
}
