import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";

export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="grid min-h-screen place-items-center bg-[#f6f7f3] text-ink dark:bg-slate-900 dark:text-white">
        Loading workspace...
      </div>
    );
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}
