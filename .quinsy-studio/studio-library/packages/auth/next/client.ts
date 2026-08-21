import { createBrowserClient } from '@supabase/ssr';
import { readSupabasePublicEnv, SUPABASE_ANON_KEY_ENV, SUPABASE_URL_ENV } from './env';

export function createBrowserSupabaseClient() {
  const env = readSupabasePublicEnv();
  if (!env) {
    throw new Error(`Missing ${SUPABASE_URL_ENV} or ${SUPABASE_ANON_KEY_ENV}`);
  }
  return createBrowserClient(env.url, env.anonKey);
}

export { isSupabaseConfigured, readSupabasePublicEnv } from './env';
