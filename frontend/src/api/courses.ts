import { api } from "./client";
import type { Course, Enrollment } from "../types";

export async function getCourses(): Promise<Course[]> {
  const { data } = await api.get<Course[]>("/courses");
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
