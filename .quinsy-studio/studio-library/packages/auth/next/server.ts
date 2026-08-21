import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';
import { readSupabasePublicEnv, SUPABASE_ANON_KEY_ENV, SUPABASE_URL_ENV } from './env';

export async function createServerSupabaseClient() {
  const cookieStore = await cookies();
  const env = readSupabasePublicEnv();
  if (!env) {
    throw new Error(`Missing ${SUPABASE_URL_ENV} or ${SUPABASE_ANON_KEY_ENV}`);
  }

  return createServerClient(env.url, env.anonKey, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(cookiesToSet) {
        try {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options);
          });
        } catch {
          // setAll from Server Component — middleware refreshes session
        }
      },
    },
  });
}
