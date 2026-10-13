'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@ui/components/atoms/Button';
import { Input } from '@ui/components/atoms/Input';

type AuthMode = 'signin' | 'signup' | 'reset';

export interface AuthLoginFormProps {
  loginPath?: string;
  registerPath?: string;
  mePath?: string;
  forgotPath?: string;
  defaultNext?: string;
  homeHref?: string;
  homeLabel?: string;
}

async function postJson(path: string, body: Record<string, string>): Promise<{ ok: boolean; message: string }> {
  const response = await fetch(path, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const payload = (await response.json().catch(() => ({}))) as { message?: string; errors?: { message?: string }[] };
  const message = payload.message || payload.errors?.[0]?.message || response.statusText;
  return { ok: response.ok, message };
}

export function AuthLoginForm({
  loginPath = '/api/users/login',
  registerPath = '/api/users',
  mePath = '/api/users/me',
  forgotPath = '/api/users/forgot-password',
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
    let cancelled = false;
    void (async () => {
      try {
        const response = await fetch(mePath, { credentials: 'include' });
        if (!response.ok || cancelled) {
          return;
        }
        const payload = (await response.json()) as { user?: { id?: string } | null };
        if (!payload.user?.id) {
          return;
        }
        router.replace(next);
        router.refresh();
      } catch {
        // stay on the form
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [mePath, next, router]);

  async function handlePasswordSubmit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);

    if (mode === 'signup') {
      const created = await postJson(registerPath, { email, password });
      if (!created.ok) {
        setError(created.message);
        setLoading(false);
        return;
      }
      setMessage('Account created. You can sign in now.');
      setMode('signin');
      setLoading(false);
      return;
    }

    const signedIn = await postJson(loginPath, { email, password });
    if (!signedIn.ok) {
      setError(signedIn.message);
      setLoading(false);
      return;
    }
    router.push(next);
    router.refresh();
  }

  async function handleReset(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);
    const sent = await postJson(forgotPath, { email });
    setLoading(false);
    if (!sent.ok) {
      setError(sent.message);
      return;
    }
    setMessage('Check your email for a reset link.');
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-2">
        {(['signin', 'signup', 'reset'] as const).map((tab) => (
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
            {tab === 'signin' ? 'Sign in' : tab === 'signup' ? 'Sign up' : 'Reset'}
          </Button>
        ))}
      </div>

      {mode === 'reset' ? (
        <form className="space-y-4" onSubmit={(e) => void handleReset(e)}>
          <Input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Sending…' : 'Email me a reset link'}
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
