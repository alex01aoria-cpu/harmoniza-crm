export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-zinc-50 px-6 py-10">
      <section className="mx-auto max-w-6xl space-y-6">
        <header className="space-y-2">
          <h1 className="text-3xl font-semibold tracking-tight text-zinc-950">
            Dashboard operacional
          </h1>
          <p className="text-sm text-zinc-600">
            Placeholder da V1 para as métricas de leads, qualificação,
            agendamento, compras e perdas por motivo.
          </p>
        </header>

        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[
            "Leads do período",
            "Taxa de qualificação",
            "Agendamentos",
            "Compras",
          ].map((label) => (
            <div
              key={label}
              className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm"
            >
              <p className="text-sm text-zinc-500">{label}</p>
              <p className="mt-3 text-3xl font-semibold text-zinc-950">--</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
