import { Clock, GraduationCap } from "lucide-react";

import { Button } from "../../components/ui/Button";
import type { Course } from "../../types";

type CourseCardProps = {
  course: Course;
  enrolled?: boolean;
  onEnroll?: (courseId: string) => void;
  isEnrolling?: boolean;
};

export function CourseCard({ course, enrolled, onEnroll, isEnrolling }: CourseCardProps) {
  return (
    <article className="flex h-full flex-col rounded-lg border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center justify-between gap-3">
        <span className="rounded-md bg-skyglass px-2.5 py-1 text-xs font-bold text-ink dark:bg-slate-800 dark:text-white">
          {course.level}
        </span>
        <span className="flex items-center gap-1 text-xs text-slate-500 dark:text-slate-400">
          <Clock size={14} />
          {Math.round(course.duration_minutes / 60)}h
        </span>
      </div>
      <h2 className="mt-4 text-lg font-bold text-ink dark:text-white">{course.title}</h2>
      <p className="mt-2 flex-1 text-sm leading-6 text-slate-600 dark:text-slate-300">{course.description}</p>
      <Button className="mt-5 w-full" disabled={enrolled || isEnrolling} onClick={() => onEnroll?.(course.id)}>
        <GraduationCap size={16} />
        {enrolled ? "Enrolled" : isEnrolling ? "Enrolling..." : "Enroll"}
      </Button>
    </article>
  );
}
