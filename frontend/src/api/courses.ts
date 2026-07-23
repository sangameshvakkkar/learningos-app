import { api } from "./client";
import type { Course, CourseDetail, Enrollment } from "../types";

export async function getCourses(params?: {
  search?: string;
  level?: string;
  skip?: number;
  limit?: number;
}): Promise<Course[]> {
  const cleanParams = Object.fromEntries(
    Object.entries(params || {}).filter(([_, v]) => v !== undefined && v !== "")
  );
  const { data } = await api.get<Course[]>("/courses", { params: cleanParams });
  return data;
}

export async function getCourse(courseId: string): Promise<CourseDetail> {
  const { data } = await api.get<CourseDetail>(`/courses/${courseId}`);
  return data;
}

export async function enrollInCourse(courseId: string): Promise<Enrollment> {
  const { data } = await api.post<Enrollment>(`/courses/${courseId}/enroll`);
  return data;
}

export async function getMyEnrollments(): Promise<Enrollment[]> {
  const { data } = await api.get<Enrollment[]>("/courses/me/enrollments");
  return data;
}
