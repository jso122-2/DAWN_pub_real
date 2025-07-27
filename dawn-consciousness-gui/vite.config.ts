import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  // Vite options tailored for Tauri development and only applied in `tauri dev` or `tauri build`
  //
  // 1. prevent vite from obscuring rust errors
  clearScreen: false,
  // 2. Local development server configuration
  server: {
    port: 1422,
    strictPort: false,
    host: "localhost", // Only bind to localhost
    open: false, // Don't open browser automatically
    watch: {
      // 3. tell vite to ignore watching `src-tauri` and runtime data
      ignored: [
        "**/src-tauri/**",
        "**/runtime/**",
        "**/*.log",
        "**/*.jsonl",
        "**/*.mmap"
      ],
    },
  },
  // 4. Build configuration for native app
  build: {
    target: "esnext",
    minify: "esbuild",
    sourcemap: true,
  },
}); 