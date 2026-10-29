import { useEffect, useState } from "react";
import {
  BellRing,
  CheckCircle2,
  RefreshCw,
  ShieldAlert,
  TriangleAlert,
  X,
  XCircle,
} from "lucide-react";

import LoadingScreen from "../components/LoadingScreen";

import {
  createIncidentFromAlert,
  getCorrelations,
  withMinimumDelay,
} from "../services/api";

import type { CorrelationResult } from "../types/api";

const MINIMUM_LOADING_TIME = 3000;

type ToastState = {
  type: "success" | "error";
  title: string;
  message: string;
} | null;

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<CorrelationResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [toast, setToast] = useState<ToastState>(null);
  const [creatingIncidentId, setCreatingIncidentId] = useState<number | null>(null);

  function showToast(
    type: "success" | "error",
    title: string,
    message: string
  ) {
    setToast({ type, title, message });

    setTimeout(() => {
      setToast((current) => {
        if (
          current &&
          current.type === type &&
          current.title === title &&
          current.message === message
        ) {
          return null;
        }

        return current;
      });
    }, 3500);
  }

  async function loadAlerts() {
    setLoading(true);
    setError(null);

    try {
      const data = await withMinimumDelay(
        getCorrelations(100),
        MINIMUM_LOADING_TIME
      );

      setAlerts(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load security alerts."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateIncident(correlationId: number) {
    setCreatingIncidentId(correlationId);

    try {
      await createIncidentFromAlert(correlationId);

      showToast(
        "success",
        "Incident created",
        "The incident was created successfully and is now available in the Incidents module."
      );
    } catch (err) {
      showToast(
        "error",
        "Incident creation failed",
        err instanceof Error
          ? err.message
          : "Could not create the incident."
      );
    } finally {
      setCreatingIncidentId(null);
    }
  }

  useEffect(() => {
    let cancelled = false;

    withMinimumDelay(
      getCorrelations(100),
      MINIMUM_LOADING_TIME
    )
      .then((data) => {
        if (!cancelled) {
          setAlerts(data);
          setError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load security alerts."
          );
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const ransomwareAlerts = alerts.filter(
    (item) => item.threat_type === "ransomware"
  ).length;

  const cryptojackingAlerts = alerts.filter(
    (item) => item.threat_type === "cryptojacking"
  ).length;

  const highSeverityAlerts = alerts.filter(
    (item) => item.severity.toLowerCase() === "high"
  ).length;

  if (loading) {
    return (
      <LoadingScreen
        title="Loading security alerts"
        message="Reviewing threat detections, correlation rules and security evidence."
      />
    );
  }

  return (
    <div className="data-page">
      {toast && (
        <div className={`custom-toast ${toast.type}`}>
          <div className="custom-toast-icon">
            {toast.type === "success" ? (
              <CheckCircle2 size={20} />
            ) : (
              <XCircle size={20} />
            )}
          </div>

          <div className="custom-toast-content">
            <strong>{toast.title}</strong>
            <span>{toast.message}</span>
          </div>

          <button
            className="custom-toast-close"
            onClick={() => setToast(null)}
            aria-label="Close notification"
          >
            <X size={16} />
          </button>
        </div>
      )}

      <header className="page-header">
        <div>
          <p className="eyebrow">SECURITY MONITORING</p>

          <h2>Security Alerts</h2>

          <p className="page-subtitle">
            Threat alerts generated from ShadowAuth correlation rules and
            machine learning analysis.
          </p>
        </div>

        <button className="refresh-button" onClick={loadAlerts}>
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>

      <section className="correlation-summary-grid">
        <article className="stat-card">
          <div className="stat-card-top">
            <span>Total alerts</span>

            <div className="stat-icon">
              <BellRing size={20} />
            </div>
          </div>

          <strong className="stat-value">{alerts.length}</strong>

          <span className="stat-subtitle">Security detections</span>
        </article>

        <article className="stat-card">
          <div className="stat-card-top">
            <span>High severity</span>

            <div className="stat-icon">
              <TriangleAlert size={20} />
            </div>
          </div>

          <strong className="stat-value">{highSeverityAlerts}</strong>

          <span className="stat-subtitle">Critical review required</span>
        </article>

        <article className="stat-card">
          <div className="stat-card-top">
            <span>Ransomware</span>

            <div className="stat-icon">
              <ShieldAlert size={20} />
            </div>
          </div>

          <strong className="stat-value">{ransomwareAlerts}</strong>

          <span className="stat-subtitle">Detected ransomware activity</span>
        </article>

        <article className="stat-card">
          <div className="stat-card-top">
            <span>Cryptojacking</span>

            <div className="stat-icon">
              <ShieldAlert size={20} />
            </div>
          </div>

          <strong className="stat-value">{cryptojackingAlerts}</strong>

          <span className="stat-subtitle">Detected mining activity</span>
        </article>
      </section>

      <section className="table-panel">
        {error && <div className="table-state error">{error}</div>}

        {!error && (
          <div className="correlation-list">
            {alerts.map((item) => (
              <article
                key={item.correlation_id}
                className="correlation-card"
              >
                <div className="correlation-card-top">
                  <div>
                    <div className="correlation-rule">
                      <span className="rule-id">{item.rule_id}</span>

                      <h3>{item.rule_name}</h3>
                    </div>

                    <p>{item.description}</p>
                  </div>

                  <span
                    className={`severity-badge ${item.severity.toLowerCase()}`}
                  >
                    {item.severity}
                  </span>
                </div>

                <div className="correlation-meta">
                  <div>
                    <span>Threat</span>
                    <strong>{item.threat_type}</strong>
                  </div>

                  <div>
                    <span>Session</span>
                    <strong className="mono-cell">{item.session_id}</strong>
                  </div>

                  <div>
                    <span>Confidence</span>
                    <strong>{(item.score * 100).toFixed(0)}%</strong>
                  </div>

                  <div>
                    <span>Detected</span>
                    <strong>
                      {new Date(item.created_at).toLocaleString()}
                    </strong>
                  </div>
                </div>

                <details className="evidence-box">
                  <summary>View alert evidence</summary>

                  <pre>{JSON.stringify(item.evidence, null, 2)}</pre>
                </details>

                <button
                  className="incident-create-button"
                  onClick={() => handleCreateIncident(item.correlation_id)}
                  disabled={creatingIncidentId === item.correlation_id}
                >
                  <ShieldAlert size={15} />
                  {creatingIncidentId === item.correlation_id
                    ? "Creating..."
                    : "Create incident"}
                </button>
              </article>
            ))}

            {alerts.length === 0 && (
              <div className="table-state">
                No security alerts detected.
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}