export interface Partner {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface Station {
  id: string;
  partner_id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  created_at: string;
  updated_at: string;
}

export interface Connector {
  id: string;
  station_id: string;
  connector_type: string;
  power_kw: number;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  data: T | null;
  error: { code: string; message: string } | null;
}

export interface CreatePartnerInput {
  name: string;
}

export interface CreateStationInput {
  partner_id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
}

export interface UpdateStationInput {
  name: string;
  address: string;
  latitude: number;
  longitude: number;
}

export interface CreateConnectorInput {
  station_id: string;
  connector_type: string;
  power_kw: number;
}
