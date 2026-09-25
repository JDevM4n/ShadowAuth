import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  RefreshCw,
  Search,
} from "lucide-react";

import LoadingScreen from "../components/LoadingScreen";

import {
  getEvents,
  withMinimumDelay,
} from "../services/api";

import type {
  SecurityEvent,
} from "../types/api";


type SourceFilter = "" | "cowrie" | "falco";

const MINIMUM_LOADING_TIME = 3000;


export default function EventsPage() {
  const [events, setEvents] =
    useState<SecurityEvent[]>([]);

  const [source, setSource] =
    useState<SourceFilter>("");

  const [search, setSearch] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  async function loadEvents() {
    setLoading(true);
    setError(null);

    try {
      const data = await withMinimumDelay(
        getEvents(
          100,
          source || undefined,
        ),
        MINIMUM_LOADING_TIME,
      );

      setEvents(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load events."
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    let cancelled = false;

    withMinimumDelay(
      getEvents(
        100,
        source || undefined,
      ),
      MINIMUM_LOADING_TIME,
    )
      .then((data) => {
        if (!cancelled) {
          setEvents(data);
          setError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load events."
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
  }, [source]);


  const filteredEvents = useMemo(() => {
    const value =
      search.trim().toLowerCase();

    return events.filter((event) => {
      return (
        event.event_type
          ?.toLowerCase()
          .includes(value) ||
        event.session_id
          ?.toLowerCase()
          .includes(value) ||
        event.source
          .toLowerCase()
          .includes(value)
      );
    });
  }, [events, search]);


  if (loading) {
    return (
      <LoadingScreen
        title="Loading security events"
        message="Retrieving normalized Cowrie and Falco telemetry."
      />
    );
  }


  return (
    <div className="data-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">
            SECURITY TELEMETRY
          </p>

          <h2>Events</h2>

          <p className="page-subtitle">
            Normalized Cowrie and Falco
            security events.
          </p>
        </div>


        <button
          className="refresh-button"
          onClick={loadEvents}
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>


      <section className="source-filter-grid">
        <SourceButton
          label="All"
          active={source === ""}
          onClick={() => setSource("")}
        />

        <SourceButton
          label="Cowrie"
          active={source === "cowrie"}
          onClick={() => setSource("cowrie")}
        />

        <SourceButton
          label="Falco"
          active={source === "falco"}
          onClick={() => setSource("falco")}
        />
      </section>


      <section className="table-panel">
        <div className="table-toolbar">
          <div className="search-box">
            <Search size={17} />

            <input
              value={search}
              placeholder="Search event type or session..."
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />
          </div>


          <div className="event-counter">
            {filteredEvents.length}
            {" "}
            events displayed
          </div>
        </div>


        {error && (
          <div className="table-state error">
            {error}
          </div>
        )}


        {!error && (
          <div className="table-wrapper">
            <table className="security-table">
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Event</th>
                  <th>Severity</th>
                  <th>Session</th>
                  <th>Host / Process</th>
                  <th>Timestamp</th>
                </tr>
              </thead>

              <tbody>
                {filteredEvents.map(
                  (event) => (
                    <tr key={event.event_id}>
                      <td>
                        <span
                          className={
                            `source-badge ${event.source}`
                          }
                        >
                          {event.source}
                        </span>
                      </td>


                      <td>
                        <div className="event-name">
                          <Activity size={14} />

                          {event.event_type ??
                            "Unknown event"}
                        </div>
                      </td>


                      <td>
                        {event.severity_native ??
                          event.severity ??
                          "—"}
                      </td>


                      <td className="mono-cell">
                        {event.session_id ??
                          "—"}
                      </td>


                      <td>
                        {getHostDescription(
                          event
                        )}
                      </td>


                      <td>
                        {formatDate(
                          event.event_timestamp
                        )}
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>


            {filteredEvents.length === 0 && (
              <div className="table-state">
                No events found.
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}


function SourceButton({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      className={
        active
          ? "source-filter active"
          : "source-filter"
      }
      onClick={onClick}
    >
      {label}
    </button>
  );
}


function getHostDescription(
  event: SecurityEvent,
) {
  const hostname =
    typeof event.host.hostname === "string"
      ? event.host.hostname
      : null;

  const process =
    typeof event.host.process_name === "string"
      ? event.host.process_name
      : null;

  if (hostname && process) {
    return `${hostname} / ${process}`;
  }

  return hostname ?? process ?? "—";
}


function formatDate(
  value: string,
) {
  return new Date(
    value
  ).toLocaleString();
}