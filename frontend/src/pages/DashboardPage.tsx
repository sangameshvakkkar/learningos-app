import { useQuery } from "@tanstack/react-query";
import { BookOpen, CheckCircle2, Clock3 } from "lucide-react";
import { Link } from "react-router-dom";

import { getCourses, getMyEnrollments } from "../api/courses";
import { getAllProgress } from "../api/lessons";
import { Button } from "../components/ui/Button";
import { MetricSkeleton, CardSkeleton } from "../components/ui/Skeleton";
import { useAuth } from "../context/AuthContext";

export function DashboardPage() {
  const { user } = useAuth();
  
  const { data: courses = [], isLoading: isLoadingCourses } = useQuery({ queryKey: ["courses"], queryFn: () => getCourses() });
  const { data: enrollments = [], isLoading: isLoadingEnrollments } = useQuery({ queryKey: ["enrollments"], queryFn: getMyEnrollments });
  const { data: progress = [], isLoading: isLoadingProgress } = useQuery({ queryKey: ["progress", "all"], queryFn: getAllProgress });

  const nextCourse = courses.find((course) => !enrollments.some((item) => item.course.id === course.id));
  
  const isLoading = isLoadingCourses || isLoadingEnrollments || isLoadingProgress;

  return (
    <div className="space-y-8">
      <section>
        <p className="text-sm font-bold uppercase text-coral">Dashboard</p>
        <h1 className="mt-2 text-3xl font-black text-ink dark:text-white">Good to see you, {user?.full_name}.</h1>
      </section>
      
      <section className="grid gap-4 md:grid-cols-3">
        {isLoading ? (
          <>
            <MetricSkeleton />
            <MetricSkeleton />
            <MetricSkeleton />
          </>
        ) : (
          <>
            <Metric icon={<BookOpen size={20} />} label="Catalog courses" value={courses.length} />
            <Metric icon={<CheckCircle2 size={20} />} label="Lessons completed" value={progress.length} />
            <Metric icon={<Clock3 size={20} />} label="Learning minutes" value={enrollments.reduce((sum, item) => sum + item.course.duration_minutes, 0)} />
          </>
        )}
      </section>

      {enrollments.length > 0 && (
        <section>
          <h2 className="mb-4 text-xl font-bold text-ink dark:text-white">Your Enrollments</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {enrollments.map((enrollment) => {
              const courseProgress = progress.filter(p => courses.find(c => c.id === enrollment.course.id)?.lessons_count).length; // simple approximation or actual data
              // The accurate way is to get the course.id's lessons from progress but progress only has lesson_id.
              // To simplify, we just show the course card without progress percentage unless we calculate it.
              return (
                <Link key={enrollment.id} to={`/app/courses/${enrollment.course.id}`} className="block rounded-lg border border-slate-200 bg-white p-5 transition hover:shadow-md dark:border-slate-800 dark:bg-slate-950">
                  <div className="flex items-center justify-between">
                    <span className="rounded-md bg-skyglass px-2.5 py-1 text-xs font-bold text-ink dark:bg-slate-800 dark:text-white">{enrollment.course.level}</span>
                  </div>
                  <h3 className="mt-3 text-lg font-bold text-ink dark:text-white">{enrollment.course.title}</h3>
                  <p className="mt-1 text-sm text-slate-500">{enrollment.course.lessons_count} lessons</p>
                </Link>
              );
            })}
          </div>
        </section>
      )}

      <section className="rounded-lg border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-950">
        <h2 className="text-xl font-bold text-ink dark:text-white">Next useful action</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300">
          {isLoading ? (
            "Loading recommendations..."
          ) : nextCourse ? (
            `Continue with ${nextCourse.title}, a ${nextCourse.level.toLowerCase()} module.`
          ) : (
            "You are enrolled in every available course."
          )}
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
