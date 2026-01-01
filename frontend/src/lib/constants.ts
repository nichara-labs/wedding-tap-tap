import type { paths } from "@/types/schema";
import { settings } from "./settings";

const _GOOGLE_AUTH_PATH: keyof paths = "/v1/oauth/google/authorize";
export const GOOGLE_AUTH_PATH = `${settings.api_base_url}${_GOOGLE_AUTH_PATH}`;

const _LOGOUT_PATH: keyof paths = "/v1/auth/logout";
export const LOGOUT_PATH = `${settings.api_base_url}${_LOGOUT_PATH}`;

/**Query parameter name */
export const CHAT_PARAM = "chat";

/**Query parameter name */
export const STORY_PARAM = "story";
