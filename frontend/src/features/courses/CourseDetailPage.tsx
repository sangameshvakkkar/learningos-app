import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, BookOpen, CheckCircle2, Clock, GraduationCap, Layers } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { getCourse, enrollInCourse } from "../../api/courses";
import { getCourseProgress } from "../../api/lessons";
import { Button } from "../../components/ui/Button";
import { CardSkeleton } from "../../components/ui/Skeleton";
import { useToast } from "../../context/ToastContext";

export function CourseDetailPage() {
  const { courseId } = useParams<{ courseId: string }>();
  const queryClient = useQueryClient();
  const toast = useToast();

  const { data: course, isLoading } = useQuery({
    queryKey: ["course", courseId],
    queryFn: () => getCourse(courseId!),
    enabled: Boolean(courseId)
  });

  const { data: progress = [] } = useQuery({
    queryKey: ["progress", courseId],
    queryFn: () => getCourseProgress(courseId!),
    enabled: Boolean(courseId)
  });

  const { data: enrollments = [] } = useQuery({
    queryKey: ["enrollments"],
    queryFn: async () => {
      const { getMyEnrollments } = await import("../../api/courses");
      return getMyEnrollments();
    }
  });

  const isEnrolled = enrollments.some((e) => e.course.id === courseId);
  const completedLessonIds = new Set(progress.map((p) => p.lesson_id));

  const enrollMutation = useMutation({
    mutationFn: () => enrollInCourse(courseId!),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["enrollments"] });
      toast.success("Enrolled successfully!");
    },
    onError: () => toast.error("Failed to enroll. Please try again.")
  });

  if (isLoading) {
    return (
      <div className="space-y-6">
        <CardSkeleton />
      </div>
    );
  }

  if (!course) {
    return (
      <div className="space-y-4">
        <h1 className="text-2xl font-bold text-ink dark:text-white">Course not found</h1>
        <Link to="/app/catalog"><Button variant="secondary">Back to catalog</Button></Link>
      </div>
    );
  }

  const lessonsCompleted = course.lessons.filter((l) => completedLessonIds.has(l.id)).length;
  const progressPercent = course.lessons.length > 0 ? Math.round((lessonsCompleted / course.lessons.length) * 100) : 0;

  return (
    <div className="space-y-8">
      <div>
        <Link to="/app/catalog" className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-coral dark:text-slate-400">
          <ArrowLeft size={14} /> Back to catalog
        </Link>
      </div>

      <section>
        <div className="flex flex-wrap items-center gap-3">
          <span className="rounded-md bg-skyglass px-2.5 py-1 text-xs font-bold text-ink dark:bg-slate-800 dark:text-white">
            {course.level}
          </span>
          {course.category && (
            <span className="rounded-md border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-600 dark:border-slate-700 dark:text-slate-300">
              {course.category}
            </span>
          )}
        </div>
        <h1 className="mt-4 text-3xl font-black text-ink dark:text-white">{course.title}</h1>
        <p className="mt-3 max-w-2xl text-lg leading-7 text-slate-600 dark:text-slate-300">{course.description}</p>
      </section>

      <section className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-950">
          <div className="flex items-center gap-2 text-coral"><Clock size={16} /><span className="text-sm font-medium">Duration</span></div>
          <p className="mt-2 text-2xl font-bold text-ink dark:text-white">{Math.round(course.duration_minutes / 60)}h {course.duration_minutes % 60}m</p>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-950">
          <div className="flex items-center gap-2 text-coral"><Layers size={16} /><span className="text-sm font-medium">Lessons</span></div>
          <p className="mt-2 text-2xl font-bold text-ink dark:text-white">{course.lessons.length}</p>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-950">
          <div className="flex items-center gap-2 text-coral"><CheckCircle2 size={16} /><span className="text-sm font-medium">Progress</span></div>
          <p className="mt-2 text-2xl font-bold text-ink dark:text-white">{progressPercent}%</p>
          {isEnrolled && course.lessons.length > 0 && (
            <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
              <div className="h-full rounded-full bg-coral transition-all" style={{ width: `${progressPercent}%` }} />
            </div>
          )}
        </div>
      </section>

      {!isEnrolled && (
        <Button onClick={() => enrollMutation.mutate()} disabled={enrollMutation.isPending}>
          <GraduationCap size={16} />
          {enrollMutation.isPending ? "Enrolling..." : "Enroll in this course"}
        </Button>
      )}

      {course.lessons.length > 0 && (
        <section className="rounded-lg border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
          <div className="border-b border-slate-200 px-6 py-4 dark:border-slate-800">
            <h2 className="text-lg font-bold text-ink dark:text-white">
              <BookOpen size={18} className="mr-2 inline text-coral" />
              Course Lessons
            </h2>
          </div>
          <ul className="divide-y divide-slate-200 dark:divide-slate-800">
            {course.lessons
              .sort((a, b) => a.order_index - b.order_index)
              .map((lesson, i) => {
                const completed = completedLessonIds.has(lesson.id);
                return (
                  <li key={lesson.id}>
                    <Link
                      to={`/app/courses/${course.id}/lessons/${lesson.id}`}
                      className="flex items-center gap-4 px-6 py-4 transition hover:bg-slate-50 dark:hover:bg-slate-900"
                    >
                      <span className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                        completed
                          ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300"
                          : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300"
                      }`}>
                        {completed ? <CheckCircle2 size={14} /> : i + 1}
                      </span>
                      <div className="min-w-0 flex-1">
                        <p className="font-semibold text-ink dark:text-white">{lesson.title}</p>
                        <p className="text-xs text-slate-500 dark:text-slate-400">{lesson.duration_minutes} min</p>
                      </div>
                    </Link>
                  </li>
                );
              })}
          </ul>
        </section>
      )}
    </div>
  );
}
