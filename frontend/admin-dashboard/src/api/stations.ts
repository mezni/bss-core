import { api } from "./client";
import type { Station, CreateStationInput, UpdateStationInput } from "../types";

export const stationsApi = {
  list: (partnerId?: string) =>
    api.get<Station[]>(`/stations${partnerId ? `?partner_id=${partnerId}` : ""}`),
  create: (input: CreateStationInput) => api.post<Station>("/stations", input),
  update: (id: string, input: UpdateStationInput) =>
    api.put<Station>(`/stations/${id}`, input),
  delete: (id: string) => api.delete(`/stations/${id}`),
};
