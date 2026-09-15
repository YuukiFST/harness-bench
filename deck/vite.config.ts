import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  base: "./",
  plugins: [viteSingleFile()],
  build: {
    outDir: "../dist/apresentacao",
    emptyOutDir: true,
    assetsInlineLimit: 100000000,
    sourcemap: false,
    chunkSizeWarningLimit: 2400,
  },
});
