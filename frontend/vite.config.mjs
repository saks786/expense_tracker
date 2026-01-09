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
    proxy: {
      // in docker-compose dev we want browser requests to /api -> backend service
      "/api": {
        target: "http://backend:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: { outDir: "dist" },
});

