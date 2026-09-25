import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import DashboardPage from "./pages/DashboardPage";
import SessionsPage from "./pages/SessionsPage";
import EventsPage from "./pages/EventsPage";
import MachineLearningPage from "./pages/MachineLearningPage";
import CorrelationsPage from "./pages/CorrelationsPage";
import AppLayout from "./components/AppLayout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/sessions" element={<SessionsPage />} />
          <Route path="/events" element={<EventsPage />} />
          <Route path="/ml" element={<MachineLearningPage />} />
          <Route path="/correlations" element={<CorrelationsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;