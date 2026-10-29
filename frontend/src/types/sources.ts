export type SourceStatus =
  | "recent"
  | "stale"
  | "supported";


export interface EventSource {
  source_id: string;
  name: string;
  source_type: string;
  protocol: string;
  format: string;
  integration: string;
  honeypot_linked: boolean;
  status: SourceStatus;
  events: number;
  first_event: string | null;
  last_event: string | null;
}


export interface SourcesSummary {
  total: number;
  with_telemetry: number;
  stale: number;
  honeypot_linked: number;
  sources: EventSource[];
}
