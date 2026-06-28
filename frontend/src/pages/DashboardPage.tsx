import { useQuery } from "@tanstack/react-query";
import { BookOpen, CheckCircle2, Clock3 } from "lucide-react";
import { Link } from "react-router-dom";

import { getCourses, getMyEnrollments } from "../api/courses";
import { Button } from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";

export function DashboardPage() {
  const { user } = useAuth();
  const { data: courses = [] } = useQuery({ queryKey: ["courses"], queryFn: getCourses });
  const { data: enrollments = [] } = useQuery({ queryKey: ["enrollments"], queryFn: getMyEnrollments });
  const nextCourse = courses.find((course) => !enrollments.some((item) => item.course.id === course.id));

  return (
    <div className="space-y-8">
      <section>
        <p className="text-sm font-bold uppercase text-coral">Dashboard</p>
        <h1 className="mt-2 text-3xl font-black text-ink dark:text-white">Good to see you, {user?.full_name}.</h1>
      </section>
      <section className="grid gap-4 md:grid-cols-3">
        <Metric icon={<BookOpen size={20} />} label="Catalog courses" value={courses.length} />
        <Metric icon={<CheckCircle2 size={20} />} label="Your enrollments" value={enrollments.length} />
        <Metric icon={<Clock3 size={20} />} label="Learning minutes" value={enrollments.reduce((sum, item) => sum + item.course.duration_minutes, 0)} />
      </section>
      <section className="rounded-lg border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-950">
        <h2 className="text-xl font-bold text-ink dark:text-white">Next useful action</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300">
          {nextCourse
            ? `Continue with ${nextCourse.title}, a ${nextCourse.level.toLowerCase()} module.`
            : "You are enrolled in every available v0.1 course."}
        </p>
        <Link className="mt-5 inline-flex" to="/app/catalog">
          <Button>Open catalog</Button>
        </Link>
      </section>
    </div>
  );
}

function Metric({ icon, label, value }: { icon: React.ReactNode; label: string; value: number }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center gap-3 text-coral">{icon}</div>
      <p className="mt-4 text-3xl font-black text-ink dark:text-white">{value}</p>
      <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">{label}</p>
    </div>
  );
}
