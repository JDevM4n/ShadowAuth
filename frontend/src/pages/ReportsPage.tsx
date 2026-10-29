import {
  useEffect,
  useState,
} from "react";

import {
  Activity,
  BellRing,
  Brain,
  Download,
  RefreshCw,
  Siren,
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

import LoadingScreen
  from "../components/LoadingScreen";

import {
  getReportSummary,
  withMinimumDelay,
} from "../services/api";

import type {
  ReportSummary,
} from "../types/reports";


const MINIMUM_LOADING_TIME = 1500;


export default function ReportsPage() {
  const [
    report,
    setReport,
  ] = useState<ReportSummary | null>(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState<string | null>(null);

  const [
    startDate,
    setStartDate,
  ] = useState("");

  const [
    endDate,
    setEndDate,
  ] = useState("");


  async function loadReport(
    start = startDate,
    end = endDate,
  ) {
    setLoading(true);
    setError(null);

    try {
      const data =
        await withMinimumDelay(
          getReportSummary(
            start || undefined,
            end || undefined,
          ),
          MINIMUM_LOADING_TIME,
        );

      setReport(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load report."
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadReport("", "");
  }, []);


  function resetFilters() {
    setStartDate("");
    setEndDate("");

    loadReport("", "");
  }


  function downloadCsv() {
    if (!report) {
      return;
    }

    const rows = [
      ["Metric", "Value"],

      [
        "Total Sessions",
        report.sessions.total,
      ],
      [
        "Attack Sessions",
        report.sessions.attack,
      ],
      [
        "Benign Sessions",
        report.sessions.benign,
      ],
      [
        "Unlabeled Sessions",
        report.sessions.unlabeled,
      ],
      [
        "Total Events",
        report.events.total,
      ],
      [
        "Security Alerts",
        report.alerts.total,
      ],
      [
        "High Severity Alerts",
        report.alerts.high,
      ],
      [
        "Total Incidents",
        report.incidents.total,
      ],
      [
        "Open Incidents",
        report.incidents.open,
      ],
      [
        "Investigating Incidents",
        report.incidents.investigating,
      ],
      [
        "Resolved Incidents",
        report.incidents.resolved,
      ],
      [
        "ML Scores",
        report.ml.scores,
      ],
      [
        "ML Model",
        `${report.ml.model_name} v${report.ml.model_version}`,
      ],
    ];

    Object.entries(
      report.attack_types
    ).forEach(
      ([type, count]) => {
        rows.push([
          `Attack Type: ${type}`,
          count,
        ]);
      }
    );

    Object.entries(
      report.events.by_source
    ).forEach(
      ([source, count]) => {
        rows.push([
          `Telemetry Source: ${source}`,
          count,
        ]);
      }
    );

    const csv = rows
      .map(
        row =>
          row
            .map(
              value =>
                `"${String(value)
                  .replaceAll(
                    '"',
                    '""'
                  )}"`
            )
            .join(",")
      )
      .join("\n");

    const blob = new Blob(
      [csv],
      {
        type:
          "text/csv;charset=utf-8;",
      }
    );

    const url =
      URL.createObjectURL(blob);

    const link =
      document.createElement("a");

    link.href = url;

    link.download =
      "shadowauth-security-report.csv";

    link.click();

    URL.revokeObjectURL(url);
  }


  if (loading) {
    return (
      <LoadingScreen
        title="Generating security report"
        message="Aggregating sessions, telemetry, alerts, incidents and machine learning results."
      />
    );
  }


  if (error || !report) {
    return (
      <div className="dashboard-state error">
        {
          error
          ?? "Report unavailable."
        }
      </div>
    );
  }


  const attackData =
    Object.entries(
      report.attack_types
    ).map(
      ([name, value]) => ({
        name,
        value,
      })
    );


  const sourceData =
    Object.entries(
      report.events.by_source
    ).map(
      ([name, value]) => ({
        name,
        value,
      })
    );


  const incidentData = [
    {
      name: "Open",
      value:
        report.incidents.open,
    },
    {
      name: "Investigating",
      value:
        report.incidents
          .investigating,
    },
    {
      name: "Resolved",
      value:
        report.incidents.resolved,
    },
  ];


  return (
    <div className="data-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">
            SECURITY ANALYTICS
          </p>

          <h2>
            Reports
          </h2>

          <p className="page-subtitle">
            Historical security analysis
            across ShadowAuth telemetry,
            detections and incidents.
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={() =>
            loadReport()
          }
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>


      <section className="report-filter-panel">
        <div className="report-date-field">
          <label>
            Start date
          </label>

          <input
            type="date"
            value={startDate}
            onChange={
              event =>
                setStartDate(
                  event.target.value
                )
            }
          />
        </div>


        <div className="report-date-field">
          <label>
            End date
          </label>

          <input
            type="date"
            value={endDate}
            onChange={
              event =>
                setEndDate(
                  event.target.value
                )
            }
          />
        </div>


        <button
          className="report-filter-button"
          onClick={() =>
            loadReport()
          }
        >
          Apply filter
        </button>


        <button
          className="report-reset-button"
          onClick={resetFilters}
        >
          Reset
        </button>


        <button
          className="report-export-button"
          onClick={downloadCsv}
        >
          <Download size={16} />
          Export CSV
        </button>
      </section>


      <section className="correlation-summary-grid">
        <ReportCard
          title="Sessions"
          value={report.sessions.total}
          subtitle="Observed sessions"
          icon={<Users size={20} />}
        />

        <ReportCard
          title="Security Events"
          value={report.events.total}
          subtitle="Normalized telemetry"
          icon={<Activity size={20} />}
        />

        <ReportCard
          title="Security Alerts"
          value={report.alerts.total}
          subtitle="Correlation detections"
          icon={<BellRing size={20} />}
        />

        <ReportCard
          title="Incidents"
          value={report.incidents.total}
          subtitle="Registered investigations"
          icon={<Siren size={20} />}
        />
      </section>


      <section className="report-overview-grid">
        <article className="panel">
          <div className="panel-header">
            <div>
              <h3>
                Session classification
              </h3>

              <p>
                Dataset classification
                summary.
              </p>
            </div>
          </div>

          <div className="report-metric-list">
            <ReportMetric
              label="Attack"
              value={
                report.sessions.attack
              }
            />

            <ReportMetric
              label="Benign"
              value={
                report.sessions.benign
              }
            />

            <ReportMetric
              label="Unlabeled"
              value={
                report.sessions.unlabeled
              }
            />
          </div>
        </article>


        <article className="panel">
          <div className="panel-header">
            <div>
              <h3>
                Detection overview
              </h3>

              <p>
                Current detection and
                investigation status.
              </p>
            </div>
          </div>

          <div className="report-metric-list">
            <ReportMetric
              label="High severity alerts"
              value={
                report.alerts.high
              }
            />

            <ReportMetric
              label="Open incidents"
              value={
                report.incidents.open
              }
            />

            <ReportMetric
              label="Resolved incidents"
              value={
                report.incidents.resolved
              }
            />
          </div>
        </article>


        <article className="panel">
          <div className="panel-header">
            <div>
              <h3>
                Machine Learning
              </h3>

              <p>
                Detection model used by
                ShadowAuth.
              </p>
            </div>
          </div>

          <div className="report-model">
            <Brain size={30} />

            <strong>
              {report.ml.model_name}
              {" "}
              v{report.ml.model_version}
            </strong>

            <span>
              {report.ml.scores}
              {" "}
              persisted predictions
            </span>
          </div>
        </article>
      </section>


      <section className="dashboard-grid">
        <ReportChart
          title="Attack types"
          subtitle="Labeled attack sessions by threat type."
          data={attackData}
        />

        <ReportChart
          title="Telemetry sources"
          subtitle="Normalized security events by source."
          data={sourceData}
        />
      </section>


      <section className="panel report-incidents-panel">
        <div className="panel-header">
          <div>
            <h3>
              Incident lifecycle
            </h3>

            <p>
              Current security incident
              distribution.
            </p>
          </div>
        </div>

        <div className="chart-container">
          <ResponsiveContainer
            width="100%"
            height={260}
          >
            <BarChart
              data={incidentData}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
                stroke="#dbe5ef"
              />

              <XAxis
                dataKey="name"
                tickLine={false}
                axisLine={{
                  stroke: "#cbd5e1",
                }}
              />

              <YAxis
                allowDecimals={false}
                tickLine={false}
                axisLine={false}
              />

              <Tooltip />

              <Bar
                dataKey="value"
                name="Incidents"
                radius={[
                  6,
                  6,
                  0,
                  0,
                ]}
                fill="#0ea5e9"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>


      <section className="panel">
        <div className="panel-header">
          <div>
            <h3>
              Report metadata
            </h3>

            <p>
              Selected analysis period
              and current model.
            </p>
          </div>
        </div>

        <div className="report-metadata">
          <div>
            <span>
              Start date
            </span>

            <strong>
              {
                report.period.start_date
                ?? "All data"
              }
            </strong>
          </div>

          <div>
            <span>
              End date
            </span>

            <strong>
              {
                report.period.end_date
                ?? "All data"
              }
            </strong>
          </div>

          <div>
            <span>
              Report type
            </span>

            <strong>
              Security operations
            </strong>
          </div>

          <div>
            <span>
              Platform
            </span>

            <strong>
              ShadowAuth
            </strong>
          </div>
        </div>
      </section>
    </div>
  );
}


function ReportCard({
  title,
  value,
  subtitle,
  icon,
}: {
  title: string;
  value: number;
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
        {value.toLocaleString()}
      </strong>

      <span className="stat-subtitle">
        {subtitle}
      </span>
    </article>
  );
}


function ReportMetric({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="report-metric">
      <span>{label}</span>

      <strong>
        {value.toLocaleString()}
      </strong>
    </div>
  );
}


function ReportChart({
  title,
  subtitle,
  data,
}: {
  title: string;
  subtitle: string;
  data: {
    name: string;
    value: number;
  }[];
}) {
  return (
    <article className="panel">
      <div className="panel-header">
        <div>
          <h3>{title}</h3>
          <p>{subtitle}</p>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer
          width="100%"
          height={280}
        >
          <BarChart data={data}>
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="#dbe5ef"
            />

            <XAxis
              dataKey="name"
              tickLine={false}
              axisLine={{
                stroke: "#cbd5e1",
              }}
            />

            <YAxis
              allowDecimals={false}
              tickLine={false}
              axisLine={false}
            />

            <Tooltip />

            <Bar
              dataKey="value"
              radius={[
                6,
                6,
                0,
                0,
              ]}
              fill="#0ea5e9"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </article>
  );
}
