export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-zinc-50 px-6 py-16">
      <section className="w-full max-w-md rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
        <div className="space-y-2">
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-950">
            Entrar no Harmoniza CRM
          </h1>
          <p className="text-sm text-zinc-600">
            Tela inicial de autenticação da V1. O login funcional será conectado
            ao backend nas próximas etapas.
          </p>
        </div>

        <form className="mt-8 space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-zinc-900" htmlFor="email">
              E-mail
            </label>
            <input
              id="email"
              type="email"
              placeholder="voce@harmoniza.com"
              className="w-full rounded-xl border border-zinc-300 px-4 py-3 text-sm outline-none transition focus:border-zinc-950"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-zinc-900" htmlFor="password">
              Senha
            </label>
            <input
              id="password"
              type="password"
              placeholder="********"
              className="w-full rounded-xl border border-zinc-300 px-4 py-3 text-sm outline-none transition focus:border-zinc-950"
            />
          </div>

          <button
            type="button"
            className="w-full rounded-xl bg-zinc-950 px-4 py-3 text-sm font-medium text-white transition hover:bg-zinc-800"
          >
            Entrar
          </button>
        </form>
      </section>
    </main>
  );
}
