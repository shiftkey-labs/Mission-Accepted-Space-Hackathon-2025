import * as z from "zod";

export const EnvSchema = z.object({
  VITE_API_BASE: z.string().url(),
  VITE_API_PREFIX: z.string(),
  VITE_ENABLE_MOCK_DATA: z.string().transform((val) => val === "true"),
  VITE_MAPBOX_TOKEN: z.string(),
});

export type ClientEnv = z.infer<typeof EnvSchema>;

const testEnv = EnvSchema.safeParse(import.meta.env);
if (!testEnv.success) {
  console.error("❌ Invalid environment variables:", testEnv.error.format());
  throw new Error("Invalid environment variables");
}

const parsedEnv: ClientEnv = EnvSchema.parse(import.meta.env);
console.log(parsedEnv) // DO NOT DELETE THIS

export default parsedEnv;