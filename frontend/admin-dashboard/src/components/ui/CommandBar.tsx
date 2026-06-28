import { Search, Plus } from "lucide-react";

interface CommandBarProps {
  onCreateLabel: string;
  onCreate: () => void;
  searchPlaceholder?: string;
  searchValue?: string;
  onSearchChange?: (value: string) => void;
  filters?: React.ReactNode;
}

export function CommandBar({
  onCreateLabel,
  onCreate,
  searchPlaceholder = "Search...",
  searchValue,
  onSearchChange,
  filters,
}: CommandBarProps) {
  return (
    <div className="flex items-center justify-between gap-4 mb-6">
      <div className="flex items-center gap-3 flex-1">
        {onSearchChange && (
          <div className="relative flex-1 max-w-sm">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-surface-400" />
            <input
              type="text"
              placeholder={searchPlaceholder}
              value={searchValue}
              onChange={(e) => onSearchChange(e.target.value)}
              className="input pl-9"
            />
          </div>
        )}
        {filters}
      </div>
      <button onClick={onCreate} className="btn-primary">
        <Plus size={16} />
        {onCreateLabel}
      </button>
    </div>
  );
}
