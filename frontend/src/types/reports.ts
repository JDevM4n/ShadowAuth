export interface ReportSummary {
  period: {
    start_date: string | null;
    end_date: string | null;
  };

  sessions: {
    total: number;
    attack: number;
    benign: number;
    unlabeled: number;
  };

  attack_types: {
    [key: string]: number;
  };

  events: {
    total: number;
    by_source: {
      [key: string]: number;
    };
  };

  alerts: {
    total: number;
    high: number;
    by_threat: {
      [key: string]: number;
    };
  };

  incidents: {
    total: number;
    open: number;
    investigating: number;
    resolved: number;
  };

  ml: {
    scores: number;
    model_name: string;
    model_version: string;
  };
}
