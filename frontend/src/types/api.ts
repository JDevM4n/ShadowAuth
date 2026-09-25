export interface Session {
  session_id: string;
  sources: string[];
  first_event_timestamp: string;
  last_event_timestamp: string;
  event_count: number;
  label: "attack" | "benign" | "unlabeled";
  attack_type: string | null;
  label_source: string | null;
  label_confidence: number | null;
  data_origin: string | null;
}

export interface SecurityEvent {
  event_id: string;
  source: string;
  event_type: string | null;
  rule_id: string | null;
  rule_name: string | null;
  event_timestamp: string;
  session_id: string | null;
  severity: number | null;
  severity_native: string | null;
  network: Record<string, unknown>;
  host: Record<string, unknown>;
  data: Record<string, unknown>;
}

export interface MLScore {
  score_id: number;
  session_id: string;
  model_name: string;
  model_version: string;
  prediction: string;
  attack_probability: number | null;
  anomaly_score: number | null;
  artifact_path: string | null;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface CorrelationResult {
  correlation_id: number;
  session_id: string;
  rule_id: string;
  rule_name: string;
  severity: string;
  score: number;
  threat_type: string;
  description: string;
  evidence: Record<string, unknown>;
  model_name: string;
  model_version: string;
  created_at: string;
  updated_at: string;
}
