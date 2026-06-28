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
  created_at: string;
};

export type Enrollment = {
  id: string;
  course: Course;
  enrolled_at: string;
};

export type AuthToken = {
  access_token: string;
  token_type: "bearer";
};
