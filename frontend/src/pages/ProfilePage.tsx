import { Mail, ShieldCheck, UserRound } from "lucide-react";

import { useAuth } from "../context/AuthContext";

export function ProfilePage() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <section>
        <p className="text-sm font-bold uppercase text-coral">Profile</p>
        <h1 className="mt-2 text-3xl font-black text-ink dark:text-white">Your account</h1>
      </section>
      <section className="rounded-lg border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-950">
        <div className="grid gap-5 md:grid-cols-3">
          <ProfileItem icon={<UserRound size={18} />} label="Name" value={user?.full_name ?? ""} />
          <ProfileItem icon={<Mail size={18} />} label="Email" value={user?.email ?? ""} />
          <ProfileItem icon={<ShieldCheck size={18} />} label="Status" value={user?.is_active ? "Active" : "Inactive"} />
        </div>
      </section>
    </div>
  );
}

function ProfileItem({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div>
      <div className="flex items-center gap-2 text-coral">{icon}</div>
      <p className="mt-3 text-sm text-slate-500 dark:text-slate-400">{label}</p>
      <p className="mt-1 font-bold text-ink dark:text-white">{value}</p>
    </div>
  );
}
