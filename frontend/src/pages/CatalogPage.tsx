import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { enrollInCourse, getCourses, getMyEnrollments } from "../api/courses";
import { CourseCard } from "../features/courses/CourseCard";

export function CatalogPage() {
  const queryClient = useQueryClient();
  const { data: courses = [], isLoading } = useQuery({ queryKey: ["courses"], queryFn: getCourses });
  const { data: enrollments = [] } = useQuery({ queryKey: ["enrollments"], queryFn: getMyEnrollments });
  const enrolledIds = new Set(enrollments.map((item) => item.course.id));

  const enrollmentMutation = useMutation({
    mutationFn: enrollInCourse,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["enrollments"] });
    }
  });

  return (
    <div className="space-y-6">
      <section>
        <p className="text-sm font-bold uppercase text-coral">Catalog</p>
        <h1 className="mt-2 text-3xl font-black text-ink dark:text-white">Course Catalog</h1>
      </section>
      {isLoading ? (
        <p className="text-slate-600 dark:text-slate-300">Loading courses...</p>
      ) : (
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {courses.map((course) => (
            <CourseCard
              key={course.id}
              course={course}
              enrolled={enrolledIds.has(course.id)}
              isEnrolling={enrollmentMutation.isPending && enrollmentMutation.variables === course.id}
              onEnroll={(courseId) => enrollmentMutation.mutate(courseId)}
            />
          ))}
        </section>
      )}
    </div>
  );
}
