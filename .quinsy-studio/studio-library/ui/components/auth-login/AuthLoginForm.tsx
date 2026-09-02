'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import type { SupabaseClient } from '@supabase/supabase-js';
import { Button } from '@ui/components/atoms/Button';
import { Input } from '@ui/components/atoms/Input';

type AuthMode = 'signin' | 'signup' | 'magic';

export interface AuthLoginFormProps {
  createClient: () => SupabaseClient;
  isConfigured: () => boolean;
  welcomeApiPath?: string;
  defaultNext?: string;
  homeHref?: string;
  homeLabel?: string;
}

export function AuthLoginForm({
  createClient,
  isConfigured,
  welcomeApiPath = '/api/auth/welcome',
  defaultNext = '/',
  homeHref = '/',
  homeLabel = 'Back',
}: AuthLoginFormProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const next = searchParams.get('next') ?? defaultNext;
  const invitedEmail = searchParams.get('email');

  const [mode, setMode] = useState<AuthMode>('signin');
  const [email, setEmail] = useState(invitedEmail ?? '');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (invitedEmail) {
      setEmail(invitedEmail);
    }
  }, [invitedEmail]);

  useEffect(() => {
    if (!isConfigured()) {
      return;
    }
    let cancelled = false;
    void (async () => {
      try {
        const supabase = createClient();
        const { data } = await supabase.auth.getSession();
        if (cancelled || !data.session) {
          return;
        }
        // Already signed in — honor ?next= (Figma plugin connected handoff).
        router.replace(next);
        router.refresh();
      } catch {
        // stay on form
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [createClient, isConfigured, next, router]);

  if (!isConfigured()) {
    return (
      <div className="rounded-lg border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
        <p className="font-medium">Supabase not configured</p>
        <p className="mt-2">
          Set <code className="rounded bg-black/5 px-1">NEXT_PUBLIC_SUPABASE_URL</code> and{' '}
          <code className="rounded bg-black/5 px-1">NEXT_PUBLIC_SUPABASE_ANON_KEY</code>, then
          restart the dev server.
        </p>
      </div>
    );
  }

  async function handlePasswordSubmit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);

    const supabase = createClient();

    if (mode === 'signup') {
      const { data, error: signUpError } = await supabase.auth.signUp({ email, password });
      if (signUpError) {
        setError(signUpError.message);
        setLoading(false);
        return;
      }
      if (data.user) {
        await fetch(welcomeApiPath, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email }),
        });
      }
      setMessage('Account created. You can sign in now.');
      setMode('signin');
      setLoading(false);
      return;
    }

    const { error: signInError } = await supabase.auth.signInWithPassword({ email, password });
    if (signInError) {
      setError(signInError.message);
      setLoading(false);
      return;
    }

    router.push(next);
    router.refresh();
  }

  async function handleMagicLink(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);

    const supabase = createClient();
    const redirectTo = `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`;

    const { error: otpError } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: redirectTo },
    });

    setLoading(false);
    if (otpError) {
      setError(otpError.message);
      return;
    }
    setMessage('Check your email for a magic link.');
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-2">
        {(['signin', 'signup', 'magic'] as const).map((tab) => (
          <Button
            key={tab}
            type="button"
            variant={mode === tab ? 'primary' : 'secondary'}
            buttonSize="sm"
            onClick={() => {
              setMode(tab);
              setError(null);
              setMessage(null);
            }}
          >
            {tab === 'signin' ? 'Sign in' : tab === 'signup' ? 'Sign up' : 'Magic link'}
          </Button>
        ))}
      </div>

      {mode === 'magic' ? (
        <form className="space-y-4" onSubmit={(e) => void handleMagicLink(e)}>
          <Input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Sending…' : 'Email me a link'}
          </Button>
        </form>
      ) : (
        <form className="space-y-4" onSubmit={(e) => void handlePasswordSubmit(e)}>
          <Input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            autoComplete={mode === 'signup' ? 'new-password' : 'current-password'}
          />
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Working…' : mode === 'signup' ? 'Create account' : 'Sign in'}
          </Button>
        </form>
      )}

      {error ? <p className="text-sm text-red-600">{error}</p> : null}
      {message ? <p className="text-sm text-emerald-600">{message}</p> : null}
      {invitedEmail ? (
        <p className="text-xs text-neutral-500">
          Use <strong>{invitedEmail}</strong> to accept this invitation.
        </p>
      ) : null}

      <p className="text-center text-sm text-neutral-500">
        <Link href={homeHref} className="underline">
          {homeLabel}
        </Link>
      </p>
    </div>
  );
}
