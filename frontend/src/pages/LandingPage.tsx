import { ArrowRight, BookOpen, Compass, Moon, Sun } from "lucide-react";
import { Link } from "react-router-dom";

import { Button } from "../components/ui/Button";
import { useTheme } from "../context/ThemeContext";

export function LandingPage() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-[#f6f7f3] text-ink dark:bg-slate-900 dark:text-white">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-5">
        <Link to="/" className="text-xl font-black">
          LearningOS
        </Link>
        <div className="flex items-center gap-2">
          <Button variant="ghost" aria-label="Toggle dark mode" title="Toggle dark mode" onClick={toggleTheme}>
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </Button>
          <Link to="/login">
            <Button variant="secondary">Sign in</Button>
          </Link>
          <Link to="/register">
            <Button>Start</Button>
          </Link>
        </div>
      </nav>
      <main className="mx-auto grid max-w-6xl gap-10 px-4 py-12 md:grid-cols-[1.05fr_0.95fr] md:items-center md:py-20">
        <section>
          <span className="inline-flex rounded-md bg-skyglass px-3 py-1 text-sm font-bold text-ink dark:bg-slate-800 dark:text-white">
            Release v0.1
          </span>
          <h1 className="mt-6 max-w-3xl text-5xl font-black leading-tight text-ink dark:text-white md:text-6xl">
            LearningOS
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600 dark:text-slate-300">
            A focused learning workspace for discovering courses, tracking enrollments, and building a repeatable path
            through complex topics.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link to="/register">
              <Button>
                Create account <ArrowRight size={16} />
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="secondary">Open workspace</Button>
            </Link>
          </div>
        </section>
        <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-soft dark:border-slate-800 dark:bg-slate-950">
          <div className="grid gap-4">
            {[
              ["Course Catalog", "Browse curated modules by level and time commitment.", BookOpen],
              ["Personal Dashboard", "See active learning activity and next useful actions.", Compass],
              ["Profile", "Keep identity and account details visible in one place.", ArrowRight]
            ].map(([title, text, Icon]) => (
              <div key={String(title)} className="rounded-md border border-slate-200 p-4 dark:border-slate-800">
                <div className="flex items-center gap-3">
                  <Icon className="text-coral" size={20} />
                  <h2 className="font-bold">{title as string}</h2>
                </div>
                <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{text as string}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
