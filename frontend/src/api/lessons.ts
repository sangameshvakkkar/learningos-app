import { api } from "./client";
import type { Lesson, LessonProgress } from "../types";

export async function getLessons(courseId: string): Promise<Lesson[]> {
  const { data } = await api.get<Lesson[]>(`/courses/${courseId}/lessons`);
  return data;
}

export async function getLesson(courseId: string, lessonId: string): Promise<Lesson> {
  const { data } = await api.get<Lesson>(`/courses/${courseId}/lessons/${lessonId}`);
  return data;
}

export async function markLessonComplete(courseId: string, lessonId: string): Promise<LessonProgress> {
  const { data } = await api.post<LessonProgress>(`/courses/${courseId}/lessons/${lessonId}/complete`);
  return data;
}

export async function getCourseProgress(courseId: string): Promise<LessonProgress[]> {
  const { data } = await api.get<LessonProgress[]>(`/courses/${courseId}/progress`);
  return data;
}

export async function getAllProgress(): Promise<LessonProgress[]> {
  const { data } = await api.get<LessonProgress[]>("/courses/me/progress");
  return data;
}
