import { z } from "zod";

type EnvVar<T extends z.ZodType> = {
  type: T;
  value?: string;
  defaultValue?: z.infer<T>;
};

type EnvVars = Record<string, EnvVar<z.ZodType>>;

/** Helper to ensure that `defaultValue` is constrained to the same type as `type` */
const defineEnvVar = <T extends z.ZodType>(config: EnvVar<T>) => config;

const rawEnvInput = {
  gtm_id: defineEnvVar({
    type: z.string(),
    value: process.env.NEXT_PUBLIC_GTM_ID,
  }),
  api_base_url: defineEnvVar({
    type: z.string().transform((value) => value.replace(/\/+$/, "")),
    value: process.env.NEXT_PUBLIC_API_BASE_URL,
  }),
  gt_gateway_path: defineEnvVar({
    type: z.string().optional(),
    value: process.env.NEXT_PUBLIC_GT_GATEWAY_PATH,
  }),
} as const satisfies EnvVars;

const SettingsSchema = z.object(
  Object.fromEntries(
    Object.entries(rawEnvInput).map(([key, { type }]) => [key, type]),
  ),
);

type Settings = {
  [K in keyof typeof rawEnvInput]: z.infer<(typeof rawEnvInput)[K]["type"]>;
};

/**Environment variables */
export const settings = SettingsSchema.parse(
  Object.fromEntries(
    Object.entries(rawEnvInput).map(([key, { value, defaultValue }]) => [
      key,
      value ?? defaultValue,
    ]),
  ),
) as Settings;
