export default function Home() {
  return (
    <main className="min-h-screen bg-zinc-50 text-zinc-950">
      <section className="mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-16">
        <div className="max-w-3xl space-y-6">
          <span className="inline-flex rounded-full bg-zinc-900 px-3 py-1 text-sm font-medium text-white">
            Harmoniza CRM V1
          </span>
          <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
            Motor operacional de pré-venda e conversão da Harmoniza.
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-zinc-600">
            Esta aplicação concentra origem rastreável do lead, triagem,
            handoff, follow-up, perdas, vendas e leitura gerencial mínima para a
            operação comercial da clínica.
          </p>
        </div>

        <div className="mt-10 flex flex-col gap-4 sm:flex-row">
          <a
            href="/login"
            className="inline-flex items-center justify-center rounded-xl bg-zinc-950 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-800"
          >
            Entrar no CRM
          </a>
          <a
            href="/leads"
            className="inline-flex items-center justify-center rounded-xl border border-zinc-300 bg-white px-5 py-3 text-sm font-medium text-zinc-900 transition hover:bg-zinc-100"
          >
            Ver inbox de leads
          </a>
          <a
            href="/pipeline"
            className="inline-flex items-center justify-center rounded-xl border border-zinc-300 bg-white px-5 py-3 text-sm font-medium text-zinc-900 transition hover:bg-zinc-100"
          >
            Ver pipeline comercial
          </a>
          <a
            href="/dashboard"
            className="inline-flex items-center justify-center rounded-xl border border-zinc-300 bg-white px-5 py-3 text-sm font-medium text-zinc-900 transition hover:bg-zinc-100"
          >
            Ver dashboard inicial
          </a>
        </div>
      </section>
    </main>
  );
}
