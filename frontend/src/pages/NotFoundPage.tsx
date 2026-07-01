import { Link } from "react-router-dom";

import { Button } from "../components/ui/Button";

export function NotFoundPage() {
  return (
    <div className="grid min-h-screen place-items-center bg-[#f6f7f3] px-4 dark:bg-slate-900">
      <div className="text-center">
        <h1 className="text-4xl font-black text-ink dark:text-white">Page not found</h1>
        <Link className="mt-6 inline-flex" to="/">
          <Button>Go home</Button>
        </Link>
      </div>
    </div>
  );
}
