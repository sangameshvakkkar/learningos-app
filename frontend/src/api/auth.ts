import { api } from "./client";
import type { AuthToken, User } from "../types";

export type LoginInput = {
  email: string;
  password: string;
};

export type RegisterInput = LoginInput & {
  full_name: string;
};

export async function login(payload: LoginInput): Promise<AuthToken> {
  const { data } = await api.post<AuthToken>("/auth/login", payload);
  return data;
}

export async function register(payload: RegisterInput): Promise<User> {
  const { data } = await api.post<User>("/auth/register", payload);
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await api.get<User>("/auth/me");
  return data;
}
