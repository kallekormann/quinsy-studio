/** Studio Library page type stub — comparison / alternatives layout. */
export function ComparisonPageLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="mx-auto max-w-4xl space-y-8 p-8">
      <header>
        <h1 className="text-2xl font-bold text-slate-900">Comparison</h1>
        <p className="mt-2 text-slate-600">Base page type — customize in project.</p>
      </header>
      <section className="grid gap-4 md:grid-cols-2">{children}</section>
    </main>
  );
}
