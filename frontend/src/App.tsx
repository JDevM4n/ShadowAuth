import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import DashboardPage from "./pages/DashboardPage";
import SessionsPage from "./pages/SessionsPage";
import EventsPage from "./pages/EventsPage";
import HoneypotsPage from "./pages/HoneypotsPage";
import MachineLearningPage from "./pages/MachineLearningPage";
import AlertsPage from "./pages/AlertsPage";
import IncidentsPage from "./pages/IncidentsPage";
import ReportsPage from "./pages/ReportsPage";
import SourcesPage from "./pages/SourcesPage";
import AppLayout from "./components/AppLayout";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route
            path="/"
            element={
              <Navigate
                to="/dashboard"
                replace
              />
            }
          />

          <Route
            path="/dashboard"
            element={<DashboardPage />}
          />

          <Route
            path="/sessions"
            element={<SessionsPage />}
          />

          <Route
            path="/events"
            element={<EventsPage />}
          />

          <Route
            path="/honeypots"
            element={<HoneypotsPage />}
          />

          <Route
            path="/ml"
            element={<MachineLearningPage />}
          />

          <Route
            path="/alerts"
            element={<AlertsPage />}
          />

          <Route
            path="/incidents"
            element={<IncidentsPage />}
          />

          <Route
            path="/reports"
            element={<ReportsPage />}
          />

          <Route
            path="/sources"
            element={<SourcesPage />}
          />

          <Route
            path="/correlations"
            element={
              <Navigate
                to="/alerts"
                replace
              />
            }
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
