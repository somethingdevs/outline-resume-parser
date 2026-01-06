import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/health": "http://127.0.0.1:8000",
      "/parse": "http://127.0.0.1:8000",
      "/match": "http://127.0.0.1:8000",
    },
  },
});
