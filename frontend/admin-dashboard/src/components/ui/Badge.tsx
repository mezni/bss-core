import { MapPin, PlugZap } from "lucide-react";

interface BadgeProps {
  variant?: "default" | "brand" | "danger" | "warning";
  children: React.ReactNode;
}

export function Badge({ variant = "default", children }: BadgeProps) {
  const variants = {
    default: "bg-surface-700 text-surface-200",
    brand: "bg-brand-500/10 text-brand-400",
    danger: "bg-danger-500/10 text-danger-400",
    warning: "bg-yellow-500/10 text-yellow-400",
  };

  return <span className={`badge ${variants[variant]}`}>{children}</span>;
}

export { MapPin, PlugZap };
