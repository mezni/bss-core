import { api } from "./client";
import type { Connector, CreateConnectorInput } from "../types";

export const connectorsApi = {
  listByStation: (stationId: string) =>
    api.get<Connector[]>(`/connectors?station_id=${stationId}`),
  create: (input: CreateConnectorInput) => api.post<Connector>("/connectors", input),
  delete: (id: string) => api.delete(`/connectors/${id}`),
};
