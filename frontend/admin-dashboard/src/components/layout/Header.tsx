export function Header({ title }: { title: string }) {
  return (
    <header className="h-16 border-b border-surface-700/50 flex items-center px-6">
      <h1 className="text-xl font-semibold text-surface-50">{title}</h1>
    </header>
  );
}
