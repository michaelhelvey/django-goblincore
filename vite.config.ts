import path from "node:path";
import { fileURLToPath } from "node:url";
import vitePlusDefaults from "@michaelhelvey/vite-config";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite-plus";

const APP_STATIC_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "app/static/");

export default defineConfig({
  staged: {
    "*": "vp check --fix",
  },
  ...vitePlusDefaults,
  plugins: [tailwindcss()],
  clearScreen: false,
  base: "/static/",
  root: APP_STATIC_DIR,
  build: {
    rollupOptions: {
      input: [
        // add other entrypoints as required:
        path.resolve(APP_STATIC_DIR, "css/globals.css"),
        path.resolve(APP_STATIC_DIR, "js/entry.ts"),
        path.resolve(APP_STATIC_DIR, "js/icons.ts"),
      ],
    },
    manifest: "manifest.json",
    outDir: path.resolve(APP_STATIC_DIR, "build"),
  },
  test: {
    ...vitePlusDefaults.test,
    environment: "happy-dom",
    setupFiles: ["./js/tests/test-setup.ts"],
  },
});
