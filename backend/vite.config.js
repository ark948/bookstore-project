import { resolve } from 'path';
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
    base: "/static/",
    resolve: {
      alias: {
        '@': resolve('./static')
      }
    },
    build: {
      manifest: "manifest.json",
      outDir: resolve("./assets"),
      assetsDir: "frontend-assets",
      rollupOptions: {
        input: {
          test: resolve('./static/js/main.js'),
        }
      }
    },
    plugins: [
      tailwindcss(),
    ]
  })