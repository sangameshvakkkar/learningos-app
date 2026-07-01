import { createContext, useContext, useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import { getMe, login as loginRequest, register as registerRequest } from "../api/auth";
import type { LoginInput, RegisterInput } from "../api/auth";
import type { User } from "../types";

type AuthContextValue = {
  user: User | undefined;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginInput) => Promise<void>;
  register: (payload: RegisterInput) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);
const TOKEN_KEY = "learningos_token";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const queryClient = useQueryClient();
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY));

  const { data: user, isLoading } = useQuery({
    queryKey: ["me", token],
    queryFn: getMe,
    enabled: Boolean(token),
    retry: false
  });

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: Boolean(token),
      isLoading,
      async login(payload) {
        const result = await loginRequest(payload);
        localStorage.setItem(TOKEN_KEY, result.access_token);
        setToken(result.access_token);
        await queryClient.invalidateQueries({ queryKey: ["me"] });
      },
      async register(payload) {
        await registerRequest(payload);
        const result = await loginRequest({ email: payload.email, password: payload.password });
        localStorage.setItem(TOKEN_KEY, result.access_token);
        setToken(result.access_token);
        await queryClient.invalidateQueries({ queryKey: ["me"] });
      },
      logout() {
        localStorage.removeItem(TOKEN_KEY);
        setToken(null);
        queryClient.clear();
      }
    }),
    [isLoading, queryClient, token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
