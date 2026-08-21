/** Env keys Next.js App Router + Supabase SSR expect (browser needs NEXT_PUBLIC_*). */
export const SUPABASE_URL_ENV = 'NEXT_PUBLIC_SUPABASE_URL';
export const SUPABASE_ANON_KEY_ENV = 'NEXT_PUBLIC_SUPABASE_ANON_KEY';
export const SUPABASE_SERVICE_ROLE_ENV = 'SUPABASE_SERVICE_ROLE_KEY';

export function readSupabasePublicEnv(): { url: string; anonKey: string } | null {
  // Literal property names — Next.js only inlines NEXT_PUBLIC_* for static access (not process.env[variable]).
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !anonKey) {
    return null;
  }
  return { url, anonKey };
}

export function isSupabaseConfigured(): boolean {
  return readSupabasePublicEnv() !== null;
}
