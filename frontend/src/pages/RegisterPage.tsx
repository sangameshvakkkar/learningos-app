import { Link } from "react-router-dom";

import { AuthForm } from "../features/auth/AuthForm";

export function RegisterPage() {
  return (
    <div className="grid min-h-screen bg-[#f6f7f3] px-4 py-10 dark:bg-slate-900">
      <Link className="mb-8 text-center text-xl font-black text-ink dark:text-white" to="/">
        LearningOS
      </Link>
      <AuthForm mode="register" />
    </div>
  );
}
