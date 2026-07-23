import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router-dom";
import { Search } from "lucide-react";

import { enrollInCourse, getCourses, getMyEnrollments } from "../api/courses";
import { CourseCard } from "../features/courses/CourseCard";
import { Input } from "../components/ui/Input";
import { CardSkeleton } from "../components/ui/Skeleton";

export function CatalogPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [level, setLevel] = useState("");

  const { data: courses = [], isLoading } = useQuery({ 
    queryKey: ["courses", { search, level }], 
    queryFn: () => getCourses({ search, level }) 
  });
  
  const { data: enrollments = [] } = useQuery({ 
    queryKey: ["enrollments"], 
    queryFn: getMyEnrollments 
  });
  
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

      <section className="flex flex-col gap-4 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label htmlFor="search" className="sr-only">Search</label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input
              id="search"
              type="text"
              placeholder="Search courses..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="block w-full rounded-md border border-slate-300 bg-white py-2 pl-10 pr-3 text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-coral focus:ring-2 focus:ring-coral/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            />
          </div>
        </div>
        <div className="w-full sm:w-48">
          <label htmlFor="level" className="sr-only">Level</label>
          <select
            id="level"
            value={level}
            onChange={(e) => setLevel(e.target.value)}
            className="block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm outline-none transition focus:border-coral focus:ring-2 focus:ring-coral/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
          >
            <option value="">All levels</option>
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
        </div>
      </section>

      {isLoading ? (
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <CardSkeleton />
          <CardSkeleton />
          <CardSkeleton />
        </section>
      ) : courses.length === 0 ? (
        <div className="rounded-lg border border-slate-200 bg-white p-12 text-center dark:border-slate-800 dark:bg-slate-950">
          <p className="text-slate-600 dark:text-slate-400">No courses match your filters.</p>
        </div>
      ) : (
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {courses.map((course) => (
            <Link key={course.id} to={`/app/courses/${course.id}`} className="block h-full transition hover:-translate-y-1">
              <CourseCard
                course={course}
                enrolled={enrolledIds.has(course.id)}
                isEnrolling={enrollmentMutation.isPending && enrollmentMutation.variables === course.id}
                onEnroll={(courseId) => {
                  // Ignore click on link when clicking the button
                  enrollmentMutation.mutate(courseId);
                }}
              />
            </Link>
          ))}
        </section>
      )}
    </div>
  );
}
