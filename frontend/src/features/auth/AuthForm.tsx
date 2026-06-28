import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";

import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { useAuth } from "../../context/AuthContext";

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

const registerSchema = loginSchema.extend({
  full_name: z.string().min(2, "Enter your full name")
});

type AuthFormProps = {
  mode: "login" | "register";
};

type AuthFormValues = z.infer<typeof registerSchema>;

export function AuthForm({ mode }: AuthFormProps) {
  const navigate = useNavigate();
  const { login, register } = useAuth();
  const [serverError, setServerError] = useState("");
  const schema = mode === "login" ? loginSchema : registerSchema;

  const {
    register: registerField,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<AuthFormValues>({
    resolver: zodResolver(schema),
    defaultValues: { email: "", password: "", full_name: "" }
  });

  async function onSubmit(values: AuthFormValues) {
    setServerError("");
    try {
      if (mode === "login") {
        await login({ email: values.email, password: values.password });
      } else {
        await register(values);
      }
      navigate("/app");
    } catch {
      setServerError(mode === "login" ? "Check your email and password." : "Unable to create this account.");
    }
  }

  return (
    <div className="mx-auto w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-soft dark:border-slate-800 dark:bg-slate-950">
      <h1 className="text-2xl font-bold text-ink dark:text-white">
        {mode === "login" ? "Welcome back" : "Create your workspace"}
      </h1>
      <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">
        {mode === "login" ? "Sign in to continue learning." : "Start tracking courses and progress."}
      </p>
      <form className="mt-6 space-y-4" onSubmit={handleSubmit(onSubmit)}>
        {mode === "register" ? (
          <Input label="Full name" autoComplete="name" error={errors.full_name?.message} {...registerField("full_name")} />
        ) : null}
        <Input label="Email" type="email" autoComplete="email" error={errors.email?.message} {...registerField("email")} />
        <Input
          label="Password"
          type="password"
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          error={errors.password?.message}
          {...registerField("password")}
        />
        {serverError ? <p className="text-sm text-coral">{serverError}</p> : null}
        <Button className="w-full" disabled={isSubmitting}>
          {isSubmitting ? "Please wait..." : mode === "login" ? "Sign in" : "Create account"}
        </Button>
      </form>
      <p className="mt-5 text-center text-sm text-slate-600 dark:text-slate-300">
        {mode === "login" ? "New to LearningOS?" : "Already registered?"}{" "}
        <Link className="font-semibold text-coral" to={mode === "login" ? "/register" : "/login"}>
          {mode === "login" ? "Create account" : "Sign in"}
        </Link>
      </p>
    </div>
  );
}
