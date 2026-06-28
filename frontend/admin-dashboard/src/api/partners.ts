import { api } from "./client";
import type { Partner, CreatePartnerInput } from "../types";

export const partnersApi = {
  list: () => api.get<Partner[]>("/partners"),
  create: (input: CreatePartnerInput) => api.post<Partner>("/partners", input),
};
