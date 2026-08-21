/** Env keys Next.js App Router + Supabase SSR expect (browser needs NEXT_PUBLIC_*). */
export const SUPABASE_URL_ENV = 'NEXT_PUBLIC_SUPABASE_URL';
export const SUPABASE_ANON_KEY_ENV = 'NEXT_PUBLIC_SUPABASE_ANON_KEY';
export const SUPABASE_SERVICE_ROLE_ENV = 'SUPABASE_SERVICE_ROLE_KEY';

export function readSupabasePublicEnv(): { url: string; anonKey: string } | null {
  const url = process.env[SUPABASE_URL_ENV];
  const anonKey = process.env[SUPABASE_ANON_KEY_ENV];
  if (!url || !anonKey) {
    return null;
  }
  return { url, anonKey };
}

export function isSupabaseConfigured(): boolean {
  return readSupabasePublicEnv() !== null;
}
