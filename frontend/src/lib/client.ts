import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";
import type { paths } from "@/types/schema";
import { settings } from "./settings";

export const fetchClient = createFetchClient<paths>({
  baseUrl: settings.api_base_url,
  credentials: "include",
});

export const api = createClient<paths>(fetchClient);
