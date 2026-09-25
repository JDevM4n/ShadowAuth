import { useEffect, useState } from "react";
import {
  Activity,
  Brain,
  Bug,
  Database,
  Radar,
  ShieldAlert,
  ShieldCheck,
  Users,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { getDashboardSummary } from "../services/api";
import type { DashboardSummary } from "../types/dashboard";


export default function DashboardPage() {
  const [summary, setSummary] =
    useState<DashboardSummary | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    getDashboardSummary()
      .then((data) => {
        setSummary(data);
        setError(null);
      })
      .catch((err) => {
        setError(
          err instanceof Error
            ? err.message
            : "Could not load dashboard."
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);


  if (loading) {
    return (
      <div className="dashboard-state">
        Loading ShadowAuth data...
      </div>
    );
  }


  if (error || !summary) {
    return (
      <div className="dashboard-state error">
        {error ?? "Dashboard data unavailable."}
      </div>
    );
  }


  const attackData = [
    {
      name: "Ransomware",
      value:
        summary.attack_types.ransomware ?? 0,
    },
    {
      name: "Cryptojacking",
      value:
        summary.attack_types.cryptojacking ?? 0,
    },
  ];


  const sourceData = Object.entries(
    summary.events.by_source
  ).map(([name, value]) => ({
    name,
    value: value ?? 0,
  }));


  return (
    <div className="dashboard-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">
            SECURITY OPERATIONS
          </p>

          <h2>Dashboard</h2>

          <p className="page-subtitle">
            Real-time overview of ShadowAuth
            detection data.
          </p>
        </div>

        <div className="system-status">
          <span className="status-dot" />

          System operational
        </div>
      </header>


      <section className="stats-grid">
        <StatCard
          title="Sessions"
          value={summary.sessions.total}
          subtitle="Observed SSH sessions"
          icon={<Users size={20} />}
        />

        <StatCard
          title="Events"
          value={summary.events.total}
          subtitle="Normalized security events"
          icon={<Activity size={20} />}
        />

        <StatCard
          title="Attacks"
          value={summary.sessions.attack}
          subtitle="Labeled attack sessions"
          icon={<ShieldAlert size={20} />}
        />

        <StatCard
          title="Benign"
          value={summary.sessions.benign}
          subtitle="Labeled benign sessions"
          icon={<ShieldCheck size={20} />}
        />
      </section>


      <section className="stats-grid secondary">
        <StatCard
          title="Cowrie"
          value={
            summary.events.by_source.cowrie ?? 0
          }
          subtitle="SSH honeypot events"
          icon={<Bug size={20} />}
        />

        <StatCard
          title="Falco"
          value={
            summary.events.by_source.falco ?? 0
          }
          subtitle="Runtime security events"
          icon={<Radar size={20} />}
        />

        <StatCard
          title="Correlations"
          value={summary.correlations.total}
          subtitle="Matched correlation rules"
          icon={<Database size={20} />}
        />

        <StatCard
          title="ML Model"
          value={`v${summary.ml.model_version}`}
          subtitle={summary.ml.model_name}
          icon={<Brain size={20} />}
        />
      </section>


      <section className="dashboard-grid">
        <article className="panel">
          <div className="panel-header">
            <div>
              <h3>Detected attack types</h3>

              <p>
                Ground-truth labeled attack sessions.
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer
              width="100%"
              height={280}
            >
              <BarChart data={attackData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="name"
                  tickLine={false}
                />

                <YAxis
                  allowDecimals={false}
                  tickLine={false}
                />

                <Tooltip />

                <Bar
                  dataKey="value"
                  name="Sessions"
                  radius={[6, 6, 0, 0]}
                  fill="#38bdf8"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>


        <article className="panel">
          <div className="panel-header">
            <div>
              <h3>Telemetry sources</h3>

              <p>
                Events ingested by source.
              </p>
            </div>
          </div>

          <div className="source-list">
            {sourceData.map((source) => (
              <div
                className="source-item"
                key={source.name}
              >
                <div>
                  <span className="source-name">
                    {source.name}
                  </span>

                  <span className="source-label">
                    security telemetry
                  </span>
                </div>

                <strong>
                  {source.value.toLocaleString()}
                </strong>
              </div>
            ))}
          </div>


          <div className="model-summary">
            <span>Current detection model</span>

            <strong>
              {summary.ml.model_name}
              {" "}
              v{summary.ml.model_version}
            </strong>
          </div>
        </article>
      </section>


      <section className="panel correlation-panel">
        <div className="panel-header">
          <div>
            <h3>Correlation activity</h3>

            <p>
              Matches produced by the ShadowAuth
              correlation engine.
            </p>
          </div>

          <strong>
            {summary.correlations.total}
            {" "}
            total
          </strong>
        </div>

        <div className="correlation-types">
          {Object.entries(
            summary.correlations.by_type
          ).map(([type, count]) => (
            <div
              className="correlation-badge"
              key={type}
            >
              <span>{type}</span>
              <strong>{count}</strong>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}


function StatCard({
  title,
  value,
  subtitle,
  icon,
}: {
  title: string;
  value: number | string;
  subtitle: string;
  icon: React.ReactNode;
}) {
  return (
    <article className="stat-card">
      <div className="stat-card-top">
        <span>{title}</span>

        <div className="stat-icon">
          {icon}
        </div>
      </div>

      <strong className="stat-value">
        {typeof value === "number"
          ? value.toLocaleString()
          : value}
      </strong>

      <span className="stat-subtitle">
        {subtitle}
      </span>
    </article>
  );
}
