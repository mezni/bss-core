import { useState, useCallback } from "react";
import { CheckCircle, XCircle } from "lucide-react";

interface Toast {
  id: number;
  type: "success" | "error";
  message: string;
}

let toastId = 0;

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const toast = useCallback((type: Toast["type"], message: string) => {
    const id = ++toastId;
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  }, []);

  return { toasts, toast };
}

export type UseToastResult = ReturnType<typeof useToast>;

interface ToastContainerProps {
  toasts: Toast[];
}

export function ToastContainer({ toasts }: ToastContainerProps) {
  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-6 right-6 z-[100] flex flex-col gap-3">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`flex items-center gap-3 px-4 py-3 rounded-lg shadow-2xl border backdrop-blur-sm text-sm min-w-[320px] animate-in slide-in-from-right ${
            t.type === "success"
              ? "bg-brand-500/10 border-brand-500/20 text-brand-400"
              : "bg-danger-500/10 border-danger-500/20 text-danger-400"
          }`}
        >
          {t.type === "success" ? <CheckCircle size={18} /> : <XCircle size={18} />}
          <span className="flex-1">{t.message}</span>
        </div>
      ))}
    </div>
  );
}
