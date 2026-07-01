import { LogOut, Moon, Sun } from "lucide-react";

import { Button } from "../ui/Button";
import { useAuth } from "../../context/AuthContext";
import { useTheme } from "../../context/ThemeContext";

export function Navbar() {
  const { logout, user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">
      <div className="flex h-16 items-center justify-between px-4 md:px-8">
        <div>
          <p className="text-sm font-semibold text-ink dark:text-white">LearningOS</p>
          <p className="text-xs text-slate-500 dark:text-slate-400">{user?.email}</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" aria-label="Toggle dark mode" title="Toggle dark mode" onClick={toggleTheme}>
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </Button>
          <Button variant="secondary" onClick={logout}>
            <LogOut size={16} />
            Sign out
          </Button>
        </div>
      </div>
    </header>
  );
}
