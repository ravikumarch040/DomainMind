import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// GitHub project pages: https://<user>.github.io/DomainMind/
const base = process.env.VITE_BASE_PATH ?? "/";

export default defineConfig({
  base,
  plugins: [react()],
  server: {
    port: 5174,
  },
});
