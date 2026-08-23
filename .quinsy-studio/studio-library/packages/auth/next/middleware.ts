import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';
import { readSupabasePublicEnv } from './env';

export interface SessionMiddlewareOptions {
  /** Path prefixes that require an authenticated user. */
  protectedPathPrefixes?: string[];
  loginPath?: string;
}

const DEFAULT_PROTECTED = ['/settings', '/api/account'];

async function runSessionMiddleware(
  request: NextRequest,
  protectedPathPrefixes: string[],
  loginPath: string,
) {
  let supabaseResponse = NextResponse.next({ request });
  const env = readSupabasePublicEnv();
  if (!env) {
    return supabaseResponse;
  }

  const supabase = createServerClient(env.url, env.anonKey, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(cookiesToSet) {
        cookiesToSet.forEach(({ name, value }) => {
          request.cookies.set(name, value);
        });
        supabaseResponse = NextResponse.next({ request });
        cookiesToSet.forEach(({ name, value, options }) => {
          supabaseResponse.cookies.set(name, value, options);
        });
      },
    },
  });

  const {
    data: { user },
  } = await supabase.auth.getUser();

  const isProtected = protectedPathPrefixes.some((prefix) =>
    request.nextUrl.pathname.startsWith(prefix),
  );

  if (!user && isProtected) {
    const loginUrl = request.nextUrl.clone();
    loginUrl.pathname = loginPath;
    loginUrl.searchParams.set('next', request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  return supabaseResponse;
}

export function createSessionMiddleware(options: SessionMiddlewareOptions = {}) {
  const protectedPathPrefixes = options.protectedPathPrefixes ?? DEFAULT_PROTECTED;
  const loginPath = options.loginPath ?? '/login';
  return (request: NextRequest) => runSessionMiddleware(request, protectedPathPrefixes, loginPath);
}

/** Default middleware — protected /settings and /api/account. */
export async function updateSession(request: NextRequest) {
  return runSessionMiddleware(request, DEFAULT_PROTECTED, '/login');
}
