import { useCallback, useEffect, useRef } from "react";
import { X } from "lucide-react";

interface SideDrawerProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  width?: string;
}

export function SideDrawer({ open, onClose, title, children, width = "w-[480px]" }: SideDrawerProps) {
  const ref = useRef<HTMLDivElement>(null);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    },
    [onClose]
  );

  useEffect(() => {
    if (open) {
      document.addEventListener("keydown", handleKeyDown);
      return () => document.removeEventListener("keydown", handleKeyDown);
    }
  }, [open, handleKeyDown]);

  return (
    <>
      {open && (
        <div className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      )}
      <div
        ref={ref}
        className={`fixed top-0 right-0 z-50 h-full ${width} bg-surface-900 border-l border-surface-700 shadow-2xl transition-transform duration-300 ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between px-6 h-16 border-b border-surface-700">
          <h2 className="text-lg font-semibold text-surface-50">{title}</h2>
          <button onClick={onClose} className="btn-ghost p-1.5 rounded-md">
            <X size={18} />
          </button>
        </div>
        <div className="overflow-y-auto h-[calc(100%-4rem)] p-6">{children}</div>
      </div>
    </>
  );
}
