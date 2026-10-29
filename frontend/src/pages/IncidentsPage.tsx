import {
  useEffect,
  useState,
} from "react";

import {
  CheckCircle2,
  CircleDot,
  RefreshCw,
  Search,
  ShieldAlert,
} from "lucide-react";

import LoadingScreen
  from "../components/LoadingScreen";

import {
  getIncidents,
  updateIncidentStatus,
  withMinimumDelay,
} from "../services/api";

import type {
  Incident,
} from "../types/api";


const MINIMUM_LOADING_TIME = 3000;


export default function IncidentsPage() {
  const [
    incidents,
    setIncidents,
  ] = useState<Incident[]>([]);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState<string | null>(null);


  async function loadIncidents() {
    setLoading(true);
    setError(null);

    try {
      const data =
        await withMinimumDelay(
          getIncidents(100),
          MINIMUM_LOADING_TIME,
        );

      setIncidents(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load incidents."
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadIncidents();
  }, []);


  async function changeStatus(
    incidentId: number,
    status:
      | "open"
      | "investigating"
      | "resolved",
  ) {
    try {
      const updated =
        await updateIncidentStatus(
          incidentId,
          status,
        );

      setIncidents(
        current =>
          current.map(
            incident =>
              incident.incident_id ===
              incidentId
                ? updated
                : incident
          )
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not update incident."
      );
    }
  }


  if (loading) {
    return (
      <LoadingScreen
        title="Loading incidents"
        message="Reviewing security investigations and incident status."
      />
    );
  }


  const open =
    incidents.filter(
      item =>
        item.status === "open"
    ).length;

  const investigating =
    incidents.filter(
      item =>
        item.status ===
        "investigating"
    ).length;

  const resolved =
    incidents.filter(
      item =>
        item.status === "resolved"
    ).length;


  return (
    <div className="data-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">
            INCIDENT MANAGEMENT
          </p>

          <h2>
            Security Incidents
          </h2>

          <p className="page-subtitle">
            Investigate and track security
            incidents generated from
            ShadowAuth alerts.
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={loadIncidents}
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>


      <section className="correlation-summary-grid">
        <article className="stat-card">
          <div className="stat-card-top">
            <span>
              Total incidents
            </span>

            <div className="stat-icon">
              <ShieldAlert size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {incidents.length}
          </strong>

          <span className="stat-subtitle">
            Registered investigations
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>Open</span>

            <div className="stat-icon">
              <CircleDot size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {open}
          </strong>

          <span className="stat-subtitle">
            Awaiting investigation
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>
              Investigating
            </span>

            <div className="stat-icon">
              <Search size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {investigating}
          </strong>

          <span className="stat-subtitle">
            Active investigations
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>Resolved</span>

            <div className="stat-icon">
              <CheckCircle2 size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {resolved}
          </strong>

          <span className="stat-subtitle">
            Closed investigations
          </span>
        </article>
      </section>


      <section className="table-panel">
        {error && (
          <div className="table-state error">
            {error}
          </div>
        )}


        {!error && incidents.length === 0 && (
          <div className="table-state">
            No incidents have been created yet.
            Create an incident from a security alert.
          </div>
        )}


        {!error && (
          <div className="incident-list">
            {incidents.map(
              incident => (
                <article
                  key={
                    incident.incident_id
                  }
                  className="incident-card"
                >
                  <div className="incident-card-header">
                    <div>
                      <div className="incident-heading">
                        <span className="incident-id">
                          INC-
                          {
                            String(
                              incident.incident_id
                            ).padStart(
                              4,
                              "0"
                            )
                          }
                        </span>

                        <h3>
                          {incident.title}
                        </h3>
                      </div>

                      <p>
                        {
                          incident.description
                          ?? "No description."
                        }
                      </p>
                    </div>

                    <span
                      className={
                        `severity-badge ${incident.severity}`
                      }
                    >
                      {incident.severity}
                    </span>
                  </div>


                  <div className="incident-meta">
                    <div>
                      <span>Threat</span>
                      <strong>
                        {
                          incident.threat_type
                          ?? "unknown"
                        }
                      </strong>
                    </div>

                    <div>
                      <span>Session</span>

                      <strong className="mono-cell">
                        {incident.session_id}
                      </strong>
                    </div>

                    <div>
                      <span>Created</span>

                      <strong>
                        {
                          new Date(
                            incident.created_at
                          ).toLocaleString()
                        }
                      </strong>
                    </div>

                    <div>
                      <span>Status</span>

                      <select
                        className={
                          `incident-status ${incident.status}`
                        }
                        value={incident.status}
                        onChange={
                          event =>
                            changeStatus(
                              incident.incident_id,
                              event.target.value as
                                | "open"
                                | "investigating"
                                | "resolved"
                            )
                        }
                      >
                        <option value="open">
                          Open
                        </option>

                        <option value="investigating">
                          Investigating
                        </option>

                        <option value="resolved">
                          Resolved
                        </option>
                      </select>
                    </div>
                  </div>


                  <details className="evidence-box">
                    <summary>
                      View incident evidence
                    </summary>

                    <pre>
                      {
                        JSON.stringify(
                          incident.evidence,
                          null,
                          2
                        )
                      }
                    </pre>
                  </details>
                </article>
              )
            )}
          </div>
        )}
      </section>
    </div>
  );
}
