export type User = {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
};

export type Course = {
  id: string;
  title: string;
  slug: string;
  description: string;
  level: string;
  duration_minutes: number;
  category: string | null;
  lessons_count: number;
  created_at: string;
};

export type CourseDetail = Course & {
  lessons: LessonSummary[];
};

export type LessonSummary = {
  id: string;
  title: string;
  slug: string;
  order_index: number;
  duration_minutes: number;
};

export type Lesson = LessonSummary & {
  course_id: string;
  content: string;
  created_at: string;
};

export type Enrollment = {
  id: string;
  course: Course;
  enrolled_at: string;
};

export type LessonProgress = {
  id: string;
  lesson_id: string;
  completed_at: string;
};

export type AuthToken = {
  access_token: string;
  token_type: "bearer";
};
