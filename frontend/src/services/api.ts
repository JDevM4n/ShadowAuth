import type { DashboardSummary } from "../types/dashboard";
import type {
  CorrelationResult,
  MLScore,
  SecurityEvent,
  Session,
} from "../types/api";

const API_URL =
  import.meta.env.VITE_API_URL ??
  "http://127.0.0.1:8000";


async function apiFetch<T>(
  path: string,
): Promise<T> {
  const response = await fetch(
    `${API_URL}${path}`
  );

  if (!response.ok) {
    throw new Error(
      `API error ${response.status}: ${path}`
    );
  }

  return response.json();
}


export function getDashboardSummary() {
  return apiFetch<DashboardSummary>(
    "/api/dashboard/summary"
  );
}


export function getSessions(
  limit = 50,
  label?: string,
) {
  const params = new URLSearchParams();

  params.set("limit", String(limit));

  if (label) {
    params.set("label", label);
  }

  return apiFetch<Session[]>(
    `/api/sessions?${params.toString()}`
  );
}


export function getEvents(
  limit = 50,
  source?: string,
) {
  const params = new URLSearchParams();

  params.set("limit", String(limit));

  if (source) {
    params.set("source", source);
  }

  return apiFetch<SecurityEvent[]>(
    `/api/events?${params.toString()}`
  );
}


export function getMLScores(
  limit = 50,
) {
  return apiFetch<MLScore[]>(
    `/api/ml/scores?limit=${limit}`
  );
}


export function getCorrelations(
  limit = 50,
) {
  return apiFetch<CorrelationResult[]>(
    `/api/correlations?limit=${limit}`
  );
}
