import { useState } from "react";
import { AppLayout } from "./components/layout/AppLayout";
import { useToast } from "./components/ui/Toast";
import { PartnersPage } from "./components/entities/PartnersPage";
import { StationsPage } from "./components/entities/StationsPage";
import { Building2, Zap } from "lucide-react";

type Page = "partners" | "stations";

export default function App() {
  const [page, setPage] = useState<Page>("partners");
  const [selectedPartnerId, setSelectedPartnerId] = useState<string | undefined>();
  const toast = useToast();

  const sidebarItems = [
    {
      label: "Partners",
      icon: <Building2 size={18} />,
      active: page === "partners",
      onClick: () => {
        setPage("partners");
        setSelectedPartnerId(undefined);
      },
    },
    {
      label: "Stations",
      icon: <Zap size={18} />,
      active: page === "stations",
      onClick: () => setPage("stations"),
    },
  ];

  const handleNavigate = (p: string, partnerId?: string) => {
    if (p === "stations") {
      setSelectedPartnerId(partnerId);
      setPage("stations");
    }
  };

  return (
    <AppLayout
      title={page === "partners" ? "Partners" : "Stations"}
      sidebarItems={sidebarItems}
      toast={toast}
    >
      {page === "partners" ? (
        <PartnersPage toast={toast} onNavigate={handleNavigate} />
      ) : (
        <StationsPage toast={toast} partnerId={selectedPartnerId} />
      )}
    </AppLayout>
  );
}
