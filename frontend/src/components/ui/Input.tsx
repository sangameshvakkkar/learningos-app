import { InputHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  error?: string;
};

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const inputId = id ?? props.name;
    return (
      <label className="block text-sm font-medium text-slate-700 dark:text-slate-200" htmlFor={inputId}>
        {label}
        <input
          ref={ref}
          id={inputId}
          className={clsx(
            "mt-2 block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-coral focus:ring-2 focus:ring-coral/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white",
            error && "border-coral",
            className
          )}
          {...props}
        />
        {error ? <span className="mt-1 block text-xs text-coral">{error}</span> : null}
      </label>
    );
  }
);

Input.displayName = "Input";
