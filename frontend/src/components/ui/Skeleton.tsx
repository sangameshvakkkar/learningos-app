import clsx from "clsx";

type SkeletonProps = {
  className?: string;
  count?: number;
};

export function Skeleton({ className, count = 1 }: SkeletonProps) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className={clsx(
            "animate-pulse rounded-md bg-slate-200 dark:bg-slate-800",
            className ?? "h-4 w-full"
          )}
        />
      ))}
    </>
  );
}

export function CardSkeleton() {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
      <div className="flex justify-between">
        <Skeleton className="h-6 w-20" />
        <Skeleton className="h-4 w-12" />
      </div>
      <Skeleton className="mt-4 h-6 w-3/4" />
      <Skeleton className="mt-3 h-4 w-full" />
      <Skeleton className="mt-2 h-4 w-2/3" />
      <Skeleton className="mt-5 h-10 w-full" />
    </div>
  );
}

export function MetricSkeleton() {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
      <Skeleton className="h-5 w-5" />
      <Skeleton className="mt-4 h-8 w-16" />
      <Skeleton className="mt-2 h-4 w-24" />
    </div>
  );
}

export function LessonSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="h-8 w-2/3" />
      <Skeleton className="h-4 w-full" count={8} />
    </div>
  );
}
