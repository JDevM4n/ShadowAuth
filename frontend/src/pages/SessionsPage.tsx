import { useEffect, useState } from "react";
import {
  RefreshCw,
  Search,
  ShieldAlert,
} from "lucide-react";

import LoadingScreen from "../components/LoadingScreen";

import {
  getSessions,
  withMinimumDelay,
} from "../services/api";

import type {
  Session,
} from "../types/api";


const MINIMUM_LOADING_TIME = 3000;


export default function SessionsPage() {
  const [sessions, setSessions] =
    useState<Session[]>([]);

  const [label, setLabel] =
    useState("");

  const [search, setSearch] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  async function loadSessions() {
    setLoading(true);
    setError(null);

    try {
      const data = await withMinimumDelay(
        getSessions(
          100,
          label || undefined,
        ),
        MINIMUM_LOADING_TIME,
      );

      setSessions(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load sessions."
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    let cancelled = false;

    withMinimumDelay(
      getSessions(
        100,
        label || undefined,
      ),
      MINIMUM_LOADING_TIME,
    )
      .then((data) => {
        if (!cancelled) {
          setSessions(data);
          setError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load sessions."
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
  }, [label]);


  const filteredSessions =
    sessions.filter((session) =>
      session.session_id
        .toLowerCase()
        .includes(
          search.trim().toLowerCase()
        )
    );


  if (loading) {
    return (
      <LoadingScreen
        title="Loading sessions"
        message="Retrieving observed SSH sessions and classification information."
      />
    );
  }


  return (
    <div className="data-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">
            HONEYPOT ACTIVITY
          </p>

          <h2>Sessions</h2>

          <p className="page-subtitle">
            SSH sessions observed and classified
            by ShadowAuth.
          </p>
        </div>


        <button
          className="refresh-button"
          onClick={loadSessions}
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>


      <section className="table-panel">
        <div className="table-toolbar">
          <div className="search-box">
            <Search size={17} />

            <input
              type="text"
              placeholder="Search session ID..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />
          </div>


          <select
            value={label}
            onChange={(event) =>
              setLabel(event.target.value)
            }
          >
            <option value="">
              All labels
            </option>

            <option value="attack">
              Attack
            </option>

            <option value="benign">
              Benign
            </option>

            <option value="unlabeled">
              Unlabeled
            </option>
          </select>
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
                  <th>Session</th>
                  <th>Source</th>
                  <th>Events</th>
                  <th>Label</th>
                  <th>Threat</th>
                  <th>Origin</th>
                  <th>Last activity</th>
                </tr>
              </thead>


              <tbody>
                {filteredSessions.map(
                  (session) => (
                    <tr key={session.session_id}>
                      <td>
                        <div className="session-id">
                          <ShieldAlert size={15} />

                          {session.session_id}
                        </div>
                      </td>


                      <td>
                        {session.sources.join(", ")}
                      </td>


                      <td>
                        {session.event_count}
                      </td>


                      <td>
                        <span
                          className={
                            `label-badge ${session.label}`
                          }
                        >
                          {session.label}
                        </span>
                      </td>


                      <td>
                        {session.attack_type ?? "—"}
                      </td>


                      <td>
                        {session.data_origin ?? "—"}
                      </td>


                      <td>
                        {formatDate(
                          session.last_event_timestamp
                        )}
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>


            {filteredSessions.length === 0 && (
              <div className="table-state">
                No sessions found.
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}


function formatDate(
  value: string,
) {
  return new Date(
    value
  ).toLocaleString();
}