import { Building2, Zap } from "lucide-react";

export interface SidebarItem {
  label: string;
  icon: React.ReactNode;
  active: boolean;
  onClick: () => void;
}

interface SidebarProps {
  items: SidebarItem[];
}

export function Sidebar({ items }: SidebarProps) {
  return (
    <aside className="w-60 border-r border-surface-700/50 bg-surface-800/30 flex flex-col">
      <div className="flex items-center gap-2.5 px-5 h-16 border-b border-surface-700/50">
        <Zap size={20} className="text-brand-400" />
        <span className="font-semibold text-surface-50 tracking-tight">BorneMap</span>
      </div>
      <nav className="flex-1 p-3 space-y-1">
        {items.map((item) => (
          <button
            key={item.label}
            onClick={item.onClick}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              item.active
                ? "bg-brand-500/10 text-brand-400"
                : "text-surface-400 hover:text-surface-50 hover:bg-surface-700/50"
            }`}
          >
            {item.icon}
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}
