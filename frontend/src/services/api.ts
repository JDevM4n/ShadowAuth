import type {
  SourcesSummary,
} from "../types/sources";


import type {
  ReportSummary,
} from "../types/reports";

import type { DashboardSummary } from "../types/dashboard";

import type {
  CorrelationResult,
  Incident,
  MLScore,
  SecurityEvent,
  Session,
} from "../types/api";


const API_URL =
  import.meta.env.VITE_API_URL ?? "";


async function apiFetch<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(
    `${API_URL}${path}`,
    {
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers ?? {}),
      },
      ...options,
    }
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


export function getIncidents(
  limit = 100,
  status?: string,
) {
  const params =
    new URLSearchParams();

  params.set(
    "limit",
    String(limit)
  );

  if (status) {
    params.set(
      "status",
      status
    );
  }

  return apiFetch<Incident[]>(
    `/api/incidents?${params.toString()}`
  );
}


export function createIncidentFromAlert(
  correlationId: number,
) {
  return apiFetch<Incident>(
    `/api/incidents/from-alert/${correlationId}`,
    {
      method: "POST",
    }
  );
}


export function updateIncidentStatus(
  incidentId: number,
  status:
    | "open"
    | "investigating"
    | "resolved",
) {
  return apiFetch<Incident>(
    `/api/incidents/${incidentId}/status`,
    {
      method: "PATCH",

      body: JSON.stringify({
        status,
      }),
    }
  );
}



export function getReportSummary(
  startDate?: string,
  endDate?: string,
) {
  const params = new URLSearchParams();

  if (startDate) {
    params.set(
      "start_date",
      startDate
    );
  }

  if (endDate) {
    params.set(
      "end_date",
      endDate
    );
  }

  const query =
    params.toString();

  return apiFetch<ReportSummary>(
    `/api/reports/summary${
      query ? `?${query}` : ""
    }`
  );
}



export function getSourcesSummary() {
  return apiFetch<SourcesSummary>(
    "/api/sources"
  );
}


export async function withMinimumDelay<T>(
  promise: Promise<T>,
  milliseconds = 3000,
): Promise<T> {
  const [result] =
    await Promise.all([
      promise,

      new Promise<void>(
        (resolve) => {
          setTimeout(
            resolve,
            milliseconds
          );
        }
      ),
    ]);

  return result;
}
