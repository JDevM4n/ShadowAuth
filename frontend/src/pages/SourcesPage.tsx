import {
  useEffect,
  useState,
} from "react";

import {
  Activity,
  Database,
  RefreshCw,
  Server,
  Shield,
} from "lucide-react";

import LoadingScreen
  from "../components/LoadingScreen";

import {
  getSourcesSummary,
  withMinimumDelay,
} from "../services/api";

import type {
  SourcesSummary,
} from "../types/sources";


const MINIMUM_LOADING_TIME = 1500;


export default function SourcesPage() {
  const [
    summary,
    setSummary,
  ] = useState<SourcesSummary | null>(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState<string | null>(null);


  async function loadSources() {
    setLoading(true);
    setError(null);

    try {
      const data =
        await withMinimumDelay(
          getSourcesSummary(),
          MINIMUM_LOADING_TIME,
        );

      setSummary(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load event sources."
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadSources();
  }, []);


  if (loading) {
    return (
      <LoadingScreen
        title="Loading event sources"
        message="Reviewing registered telemetry sources and ingestion activity."
      />
    );
  }


  if (error || !summary) {
    return (
      <div className="dashboard-state error">
        {
          error
          ?? "Source data unavailable."
        }
      </div>
    );
  }


  return (
    <div className="data-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">
            TELEMETRY MANAGEMENT
          </p>

          <h2>
            Event Sources
          </h2>

          <p className="page-subtitle">
            Monitor ShadowAuth telemetry
            integrations and the latest
            information received from each
            source.
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={loadSources}
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>


      <section className="correlation-summary-grid">
        <article className="stat-card">
          <div className="stat-card-top">
            <span>
              Total sources
            </span>

            <div className="stat-icon">
              <Database size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {summary.total}
          </strong>

          <span className="stat-subtitle">
            Supported integrations
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>
              With telemetry
            </span>

            <div className="stat-icon">
              <Activity size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {summary.with_telemetry}
          </strong>

          <span className="stat-subtitle">
            Sources with stored events
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>
              Stale telemetry
            </span>

            <div className="stat-icon">
              <Server size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {summary.stale}
          </strong>

          <span className="stat-subtitle">
            No recent events received
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>
              Honeypot linked
            </span>

            <div className="stat-icon">
              <Shield size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {summary.honeypot_linked}
          </strong>

          <span className="stat-subtitle">
            Deception telemetry sources
          </span>
        </article>
      </section>


      <section className="table-panel">
        <div className="sources-panel-header">
          <div>
            <h3>
              Registered integrations
            </h3>

            <p>
              Status is based on telemetry
              stored by ShadowAuth, not on
              remote process availability.
            </p>
          </div>
        </div>


        <div className="table-wrapper">
          <table className="security-table">
            <thead>
              <tr>
                <th>Source</th>
                <th>Type</th>
                <th>Protocol</th>
                <th>Format</th>
                <th>Status</th>
                <th>Events</th>
                <th>Last activity</th>
                <th>Honeypot</th>
              </tr>
            </thead>

            <tbody>
              {summary.sources.map(
                source => (
                  <tr key={source.source_id}>
                    <td>
                      <div className="source-main">
                        <div className="source-main-icon">
                          <Database size={15} />
                        </div>

                        <div>
                          <strong>
                            {source.name}
                          </strong>

                          <span>
                            {source.source_id}
                          </span>
                        </div>
                      </div>
                    </td>

                    <td>
                      {source.source_type}
                    </td>

                    <td>
                      {source.protocol}
                    </td>

                    <td>
                      <span className="source-format">
                        {source.format}
                      </span>
                    </td>

                    <td>
                      <span
                        className={
                          `source-status ${source.status}`
                        }
                      >
                        {
                          source.status === "recent"
                            ? "Recent"
                            : source.status === "stale"
                              ? "Telemetry stale"
                              : "Supported"
                        }
                      </span>
                    </td>

                    <td>
                      <strong>
                        {
                          source.events
                            .toLocaleString()
                        }
                      </strong>
                    </td>

                    <td>
                      {
                        source.last_event
                          ? new Date(
                              source.last_event
                            ).toLocaleString()
                          : "—"
                      }
                    </td>

                    <td>
                      {
                        source.honeypot_linked
                          ? "Yes"
                          : "—"
                      }
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </section>


      <section className="sources-detail-grid">
        {summary.sources.map(
          source => (
            <article
              className="source-detail-card"
              key={source.source_id}
            >
              <div className="source-detail-top">
                <div>
                  <span className="source-detail-id">
                    {source.source_id}
                  </span>

                  <h3>
                    {source.name}
                  </h3>
                </div>

                <span
                  className={
                    `source-status ${source.status}`
                  }
                >
                  {source.status}
                </span>
              </div>

              <div className="source-detail-meta">
                <div>
                  <span>Integration</span>
                  <strong>
                    {source.integration}
                  </strong>
                </div>

                <div>
                  <span>Events</span>
                  <strong>
                    {
                      source.events
                        .toLocaleString()
                    }
                  </strong>
                </div>

                <div>
                  <span>First event</span>
                  <strong>
                    {
                      source.first_event
                        ? new Date(
                            source.first_event
                          ).toLocaleString()
                        : "No telemetry"
                    }
                  </strong>
                </div>

                <div>
                  <span>Last event</span>
                  <strong>
                    {
                      source.last_event
                        ? new Date(
                            source.last_event
                          ).toLocaleString()
                        : "No telemetry"
                    }
                  </strong>
                </div>
              </div>
            </article>
          )
        )}
      </section>
    </div>
  );
}
