import { Header } from "./Header";
import { Sidebar } from "./Sidebar";
import { ToastContainer } from "../ui/Toast";
import type { UseToastResult } from "../ui/Toast";

interface AppLayoutProps {
  title: string;
  sidebarItems: Parameters<typeof Sidebar>[0]["items"];
  children: React.ReactNode;
  toast: UseToastResult;
}

export type { SidebarItem } from "./Sidebar";

export function AppLayout({ title, sidebarItems, children, toast }: AppLayoutProps) {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar items={sidebarItems} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header title={title} />
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
      <ToastContainer toasts={toast.toasts} />
    </div>
  );
}
