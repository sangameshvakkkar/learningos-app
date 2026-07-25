import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, ArrowRight, CheckCircle2 } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { Link, useNavigate, useParams } from "react-router-dom";

import { getCourse } from "../../api/courses";
import { getLesson, getCourseProgress, markLessonComplete } from "../../api/lessons";
import { Button } from "../../components/ui/Button";
import { LessonSkeleton } from "../../components/ui/Skeleton";
import { useToast } from "../../context/ToastContext";

export function LessonViewerPage() {
  const { courseId, lessonId } = useParams<{ courseId: string; lessonId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const toast = useToast();

  const { data: course } = useQuery({
    queryKey: ["course", courseId],
    queryFn: () => getCourse(courseId!),
    enabled: Boolean(courseId)
  });

  const { data: lesson, isLoading } = useQuery({
    queryKey: ["lesson", courseId, lessonId],
    queryFn: () => getLesson(courseId!, lessonId!),
    enabled: Boolean(courseId) && Boolean(lessonId)
  });

  const { data: progress = [] } = useQuery({
    queryKey: ["progress", courseId],
    queryFn: () => getCourseProgress(courseId!),
    enabled: Boolean(courseId)
  });

  const completeMutation = useMutation({
    mutationFn: () => markLessonComplete(courseId!, lessonId!),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["progress", courseId] });
      toast.success("Lesson completed!");
    },
    onError: () => toast.error("Failed to mark lesson complete.")
  });

  if (isLoading) {
    return <LessonSkeleton />;
  }

  if (!lesson || !course) {
    return (
      <div className="space-y-4 text-center py-12">
        <h1 className="text-2xl font-bold text-ink dark:text-white">Lesson not found</h1>
        <Link to={`/app/courses/${courseId}`}>
          <Button variant="secondary">Back to course</Button>
        </Link>
      </div>
    );
  }

  const isCompleted = progress.some((p) => p.lesson_id === lessonId);
  
  const sortedLessons = [...course.lessons].sort((a, b) => a.order_index - b.order_index);
  const currentIndex = sortedLessons.findIndex((l) => l.id === lessonId);
  const previousLesson = currentIndex > 0 ? sortedLessons[currentIndex - 1] : null;
  const nextLesson = currentIndex < sortedLessons.length - 1 ? sortedLessons[currentIndex + 1] : null;

  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <div>
        <Link to={`/app/courses/${courseId}`} className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-coral dark:text-slate-400">
          <ArrowLeft size={14} /> Back to {course.title}
        </Link>
      </div>

      <article className="prose prose-slate max-w-none dark:prose-invert prose-headings:font-bold prose-a:text-coral hover:prose-a:text-coral/80 prose-img:rounded-lg">
        <ReactMarkdown>{lesson.content}</ReactMarkdown>
      </article>

      <div className="flex flex-col gap-4 border-t border-slate-200 pt-8 dark:border-slate-800 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex gap-3">
          {previousLesson && (
            <Button variant="secondary" onClick={() => navigate(`/app/courses/${courseId}/lessons/${previousLesson.id}`)}>
              <ArrowLeft size={16} /> Previous
            </Button>
          )}
          {nextLesson && (
            <Button variant="secondary" onClick={() => navigate(`/app/courses/${courseId}/lessons/${nextLesson.id}`)}>
              Next <ArrowRight size={16} />
            </Button>
          )}
        </div>

        <Button
          onClick={() => completeMutation.mutate()}
          disabled={isCompleted || completeMutation.isPending}
          className={isCompleted ? "bg-emerald-600 hover:bg-emerald-700 disabled:opacity-100" : ""}
        >
          {isCompleted ? (
            <>
              <CheckCircle2 size={16} /> Completed
            </>
          ) : completeMutation.isPending ? (
            "Marking complete..."
          ) : (
            "Mark as complete"
          )}
        </Button>
      </div>
    </div>
  );
}
