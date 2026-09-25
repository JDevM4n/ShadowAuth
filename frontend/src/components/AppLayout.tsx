import {
  Activity,
  Brain,
  LayoutDashboard,
  Link2,
  Shield,
} from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const links = [
  {
    to: "/dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    to: "/sessions",
    label: "Sessions",
    icon: Shield,
  },
  {
    to: "/events",
    label: "Events",
    icon: Activity,
  },
  {
    to: "/ml",
    label: "Machine Learning",
    icon: Brain,
  },
  {
    to: "/correlations",
    label: "Correlations",
    icon: Link2,
  },
];

export default function AppLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <img
              src="/logo-shadowauth.png"
              alt="ShadowAuth logo"
              className="brand-logo"
            />
          </div>

          <div>
            <h1>ShadowAuth</h1>
            <span>Threat Detection Platform</span>
          </div>
        </div>

        <nav>
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
