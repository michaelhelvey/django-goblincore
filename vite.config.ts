import path from "node:path";
import { fileURLToPath } from "node:url";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

const APP_STATIC_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "app/static/");

export default defineConfig({
  plugins: [tailwindcss()],
  clearScreen: false,
  base: "/static/",
  root: APP_STATIC_DIR,
  build: {
    rollupOptions: {
      input: [path.resolve(APP_STATIC_DIR, "js/entry.ts")],
    },
    manifest: "manifest.json",
    outDir: path.resolve(APP_STATIC_DIR, "build"),
  },
});
