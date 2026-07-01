import { Outlet } from "react-router-dom";

import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";

export function AppLayout() {
  return (
    <div className="min-h-screen bg-[#f6f7f3] text-ink dark:bg-slate-900 dark:text-white">
      <div className="md:flex">
        <Sidebar />
        <div className="min-w-0 flex-1">
          <Navbar />
          <main className="mx-auto max-w-6xl px-4 py-8 md:px-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
