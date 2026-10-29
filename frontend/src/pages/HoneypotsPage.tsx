import { useEffect, useState } from "react";
import {
  Activity,
  Clock,
  RefreshCw,
  Server,
  Shield,
  Terminal,
} from "lucide-react";

import LoadingScreen from "../components/LoadingScreen";

import {
  getDashboardSummary,
  getEvents,
  withMinimumDelay,
} from "../services/api";

import type { DashboardSummary } from "../types/dashboard";
import type { SecurityEvent } from "../types/api";


const MINIMUM_LOADING_TIME = 3000;
const RECENT_THRESHOLD_MINUTES = 15;


export default function HoneypotsPage() {
  const [summary, setSummary] =
    useState<DashboardSummary | null>(null);

  const [events, setEvents] =
    useState<SecurityEvent[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  async function loadHoneypotData() {
    setLoading(true);
    setError(null);

    try {
      const [dashboardData, eventData] =
        await withMinimumDelay(
          Promise.all([
            getDashboardSummary(),
            getEvents(10, "cowrie"),
          ]),
          MINIMUM_LOADING_TIME,
        );

      setSummary(dashboardData);
      setEvents(eventData);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load honeypot data."
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadHoneypotData();
  }, []);


  if (loading) {
    return (
      <LoadingScreen
        title="Loading honeypots"
        message="Reviewing Cowrie telemetry, captured sessions and recent honeypot activity."
      />
    );
  }


  const lastEvent =
    events.length > 0
      ? events[0]
      : null;

  const lastEventDate =
    lastEvent
      ? new Date(lastEvent.event_timestamp)
      : null;

  const minutesSinceLastEvent =
    lastEventDate
      ? (
          Date.now()
          - lastEventDate.getTime()
        ) / 60000
      : null;

  const telemetryRecent =
    minutesSinceLastEvent !== null
    && minutesSinceLastEvent <=
      RECENT_THRESHOLD_MINUTES;

  const cowrieEvents =
    summary?.events.by_source?.cowrie ?? 0;

  const totalSessions =
    summary?.sessions.total ?? 0;


  return (
    <div className="data-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">
            HONEYPOT MONITORING
          </p>

          <h2>Honeypots</h2>

          <p className="page-subtitle">
            Monitor deception sensors,
            captured sessions and telemetry
            received by ShadowAuth.
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={loadHoneypotData}
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>


      <section className="correlation-summary-grid">
        <article className="stat-card">
          <div className="stat-card-top">
            <span>Configured honeypots</span>

            <div className="stat-icon">
              <Server size={20} />
            </div>
          </div>

          <strong className="stat-value">
            1
          </strong>

          <span className="stat-subtitle">
            Cowrie SSH sensor
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>Captured sessions</span>

            <div className="stat-icon">
              <Shield size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {totalSessions}
          </strong>

          <span className="stat-subtitle">
            Current experimental dataset
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>Cowrie events</span>

            <div className="stat-icon">
              <Activity size={20} />
            </div>
          </div>

          <strong className="stat-value">
            {cowrieEvents}
          </strong>

          <span className="stat-subtitle">
            Normalized telemetry
          </span>
        </article>


        <article className="stat-card">
          <div className="stat-card-top">
            <span>Telemetry status</span>

            <div className="stat-icon">
              <Clock size={20} />
            </div>
          </div>

          <strong className="ml-card-value">
            {
              telemetryRecent
                ? "Recent"
                : "Stale"
            }
          </strong>

          <span className="stat-subtitle">
            Based on last received event
          </span>
        </article>
      </section>


      {error && (
        <section className="table-panel">
          <div className="table-state error">
            {error}
          </div>
        </section>
      )}


      {!error && (
        <>
          <section className="honeypot-card">
            <div className="honeypot-card-header">
              <div className="honeypot-title">
                <div className="honeypot-icon">
                  <Terminal size={22} />
                </div>

                <div>
                  <h3>
                    Cowrie SSH Honeypot
                  </h3>

                  <p>
                    Interactive SSH deception
                    sensor integrated with
                    ShadowAuth.
                  </p>
                </div>
              </div>


              <span
                className={
                  telemetryRecent
                    ? "honeypot-status recent"
                    : "honeypot-status stale"
                }
              >
                {
                  telemetryRecent
                    ? "RECENT TELEMETRY"
                    : "TELEMETRY STALE"
                }
              </span>
            </div>


            <div className="honeypot-details-grid">
              <div>
                <span>Sensor type</span>
                <strong>SSH Honeypot</strong>
              </div>

              <div>
                <span>Technology</span>
                <strong>Cowrie</strong>
              </div>

              <div>
                <span>Listening port</span>
                <strong>2222</strong>
              </div>

              <div>
                <span>Source ID</span>
                <strong className="mono-cell">
                  cowrie
                </strong>
              </div>

              <div>
                <span>Captured sessions</span>
                <strong>
                  {totalSessions}
                </strong>
              </div>

              <div>
                <span>Captured events</span>
                <strong>
                  {cowrieEvents}
                </strong>
              </div>

              <div>
                <span>Last telemetry</span>
                <strong>
                  {
                    lastEventDate
                      ? lastEventDate
                          .toLocaleString()
                      : "No telemetry"
                  }
                </strong>
              </div>

              <div>
                <span>Integration</span>
                <strong>
                  NormalizedEvent
                </strong>
              </div>
            </div>
          </section>


          <section className="table-panel">
            <div className="table-toolbar">
              <div>
                <strong>
                  Recent Honeypot Activity
                </strong>

                <div className="event-counter">
                  Latest Cowrie events received
                  by ShadowAuth
                </div>
              </div>
            </div>


            <div className="table-wrapper">
              <table className="security-table">
                <thead>
                  <tr>
                    <th>Event</th>
                    <th>Session</th>
                    <th>Severity</th>
                    <th>Timestamp</th>
                  </tr>
                </thead>

                <tbody>
                  {events.map((event) => (
                    <tr key={event.event_id}>
                      <td>
                        <div className="event-name">
                          <Activity size={15} />

                          {event.event_type}
                        </div>
                      </td>

                      <td className="mono-cell">
                        {
                          event.session_id
                          ?? "—"
                        }
                      </td>

                      <td>
                        {
                          event.severity_native
                          ?? (
                            event.severity !== null
                              ? String(
                                  event.severity
                                )
                              : "—"
                          )
                        }
                      </td>

                      <td>
                        {
                          new Date(
                            event.event_timestamp
                          ).toLocaleString()
                        }
                      </td>
                    </tr>
                  ))}


                  {events.length === 0 && (
                    <tr>
                      <td
                        colSpan={4}
                        className="table-state"
                      >
                        No Cowrie events found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
