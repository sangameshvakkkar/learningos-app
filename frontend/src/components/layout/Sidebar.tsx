import { BookOpen, LayoutDashboard, UserRound } from "lucide-react";
import { NavLink } from "react-router-dom";
import clsx from "clsx";

const links = [
  { to: "/app", label: "Dashboard", icon: LayoutDashboard },
  { to: "/app/catalog", label: "Catalog", icon: BookOpen },
  { to: "/app/profile", label: "Profile", icon: UserRound }
];

export function Sidebar() {
  return (
    <aside className="border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950 md:min-h-screen md:w-64">
      <div className="hidden h-16 items-center border-b border-slate-200 px-6 dark:border-slate-800 md:flex">
        <span className="text-lg font-bold text-ink dark:text-white">LearningOS</span>
      </div>
      <nav className="flex gap-2 overflow-x-auto p-3 md:flex-col md:p-4">
        {links.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/app"}
              className={({ isActive }) =>
                clsx(
                  "flex min-h-11 items-center gap-3 rounded-md px-3 py-2 text-sm font-semibold transition",
                  isActive
                    ? "bg-skyglass text-ink dark:bg-slate-800 dark:text-white"
                    : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-900"
                )
              }
            >
              <Icon size={18} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}
