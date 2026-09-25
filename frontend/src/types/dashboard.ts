export interface DashboardSummary {
  sessions: {
    total: number;
    attack: number;
    benign: number;
    unlabeled: number;
  };

  attack_types: {
    ransomware?: number;
    cryptojacking?: number;
    [key: string]: number | undefined;
  };

  events: {
    total: number;
    by_source: {
      cowrie?: number;
      falco?: number;
      [key: string]: number | undefined;
    };
  };

  correlations: {
    total: number;
    by_type: {
      [key: string]: number;
    };
  };

  ml: {
    model_name: string;
    model_version: string;
  };
}
