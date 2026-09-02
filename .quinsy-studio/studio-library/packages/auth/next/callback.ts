import { NextResponse } from 'next/server';
import { readSupabasePublicEnv } from './env';
import { createServerSupabaseClient } from './server';

export interface AuthCallbackOptions {
  loginPath?: string;
  defaultNext?: string;
}

/** Use in `app/auth/callback/route.ts` — exchanges magic-link/OAuth code for session. */
export async function handleAuthCallback(request: Request, options: AuthCallbackOptions = {}) {
  const loginPath = options.loginPath ?? '/login';
  const defaultNext = options.defaultNext ?? '/';

  if (!readSupabasePublicEnv()) {
    return NextResponse.redirect(new URL(loginPath, request.url));
  }

  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get('code');
  const next = searchParams.get('next') ?? defaultNext;

  if (code) {
    const supabase = await createServerSupabaseClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) {
      return NextResponse.redirect(`${origin}${next}`);
    }
  }

  return NextResponse.redirect(`${origin}${loginPath}?error=auth_callback`);
}
