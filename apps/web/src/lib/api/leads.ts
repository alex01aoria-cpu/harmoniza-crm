export type LeadSource = {
  id: number;
  lead_id: number;
  canal: string;
  origem: string | null;
  campanha: string | null;
  conjunto: string | null;
  anuncio: string | null;
  utm_source: string | null;
  utm_medium: string | null;
  utm_campaign: string | null;
  utm_content: string | null;
  utm_term: string | null;
  landing_origem: string | null;
  capturado_em: string;
};

export type Lead = {
  id: number;
  nome: string;
  telefone: string;
  canal_principal: string;
  procedimento_entrada: string;
  objetivo_principal: string | null;
  interesse_principal: string | null;
  duvida_principal: string | null;
  conhece_clinica: boolean;
  conhece_procedimento: boolean;
  ja_fez_estetica: boolean;
  historico_estetico_curto: string | null;
  temperatura: string;
  qualificacao: string;
  status_atual: string;
  responsavel_atual: string;
  resumo_atual: string | null;
  proxima_acao: string | null;
  data_proxima_acao: string | null;
  created_at: string;
  updated_at: string;
  source: LeadSource | null;
};

export type LeadsFilters = {
  status_atual?: string;
  campanha?: string;
  limit?: number;
};

export type LeadsResult = {
  leads: Lead[];
  unavailable: boolean;
};

export const PIPELINE_STATUSES = [
  "Lead nova",
  "Resposta enviada",
  "Respondeu",
  "Triagem em andamento",
  "Triagem concluída",
  "Qualificada",
  "Não qualificada",
  "Passada para vendedora",
  "Agendamento em aberto",
  "Agendou",
  "Compareceu",
  "Comprou",
  "Não comprou",
  "Follow-up",
  "Perdida",
] as const;

export type PipelineStatus = (typeof PIPELINE_STATUSES)[number];

const API_BASE_URL = process.env.HARMONIZA_CRM_API_URL ?? "http://127.0.0.1:8000";
const API_TOKEN = process.env.HARMONIZA_CRM_API_TOKEN;
const API_EMAIL = process.env.HARMONIZA_CRM_API_EMAIL;
const API_PASSWORD = process.env.HARMONIZA_CRM_API_PASSWORD;

async function getApiToken(): Promise<string | null> {
  if (API_TOKEN) return API_TOKEN;
  if (!API_EMAIL || !API_PASSWORD) return null;

  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: API_EMAIL, password: API_PASSWORD }),
      cache: "no-store",
    });

    if (!response.ok) return null;
    const payload = (await response.json()) as { access_token?: string };
    return payload.access_token ?? null;
  } catch {
    return null;
  }
}

export async function fetchLeads(filters: LeadsFilters = {}): Promise<LeadsResult> {
  const params = new URLSearchParams();
  if (filters.status_atual) params.set("status_atual", filters.status_atual);
  if (filters.campanha) params.set("campanha", filters.campanha);
  params.set("limit", String(filters.limit ?? 50));

  try {
    const token = await getApiToken();
    const response = await fetch(`${API_BASE_URL}/leads?${params.toString()}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      cache: "no-store",
    });

    if (!response.ok) {
      return { leads: [], unavailable: true };
    }

    return { leads: (await response.json()) as Lead[], unavailable: false };
  } catch {
    return { leads: [], unavailable: true };
  }
}

export async function updateLeadStage(
  leadId: number,
  payload: { novo_status: string; observacao?: string },
): Promise<boolean> {
  const token = await getApiToken();
  if (!token) return false;

  try {
    const response = await fetch(`${API_BASE_URL}/leads/${leadId}/stage`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      cache: "no-store",
    });

    return response.ok;
  } catch {
    return false;
  }
}


export type LeadTask = {
  id: number;
  lead_id: number;
  titulo: string;
  descricao_curta: string | null;
  responsavel: string;
  data_limite: string;
  status_tarefa: string;
  prioridade: string;
  created_at: string;
  concluido_em: string | null;
};

export async function fetchLead(
  leadId: number,
): Promise<{ lead: Lead | null; unavailable: boolean }> {
  const token = await getApiToken();
  if (!token) return { lead: null, unavailable: true };
  try {
    const response = await fetch(`${API_BASE_URL}/leads/${leadId}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!response.ok) return { lead: null, unavailable: true };
    return { lead: (await response.json()) as Lead, unavailable: false };
  } catch {
    return { lead: null, unavailable: true };
  }
}

export async function fetchTasks(
  filters: { overdue?: boolean } = {},
): Promise<{ tasks: LeadTask[]; unavailable: boolean }> {
  const params = new URLSearchParams();
  if (filters.overdue) params.set("overdue", "true");
  try {
    const token = await getApiToken();
    const response = await fetch(`${API_BASE_URL}/tasks?${params.toString()}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      cache: "no-store",
    });
    if (!response.ok) return { tasks: [], unavailable: true };
    return { tasks: (await response.json()) as LeadTask[], unavailable: false };
  } catch {
    return { tasks: [], unavailable: true };
  }
}

export async function fetchDashboardSummary<T>(): Promise<{
  summary: T | null;
  unavailable: boolean;
}> {
  try {
    const token = await getApiToken();
    const response = await fetch(`${API_BASE_URL}/dashboard/summary`, {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      cache: "no-store",
    });
    if (!response.ok) return { summary: null, unavailable: true };
    return { summary: (await response.json()) as T, unavailable: false };
  } catch {
    return { summary: null, unavailable: true };
  }
}
