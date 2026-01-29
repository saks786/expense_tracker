// vite.config.mjs
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5413,
    host: "0.0.0.0",
    strictPort: true,
    watch: { usePolling: true },
  },
  build: { outDir: "dist" },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/test/setup.js",
    css: true,
  },
});

