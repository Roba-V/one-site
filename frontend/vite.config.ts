import react from '@vitejs/plugin-react-swc'
import { loadEnv } from 'vite'
import { createHtmlPlugin } from 'vite-plugin-html'
import { defineConfig } from 'vitest/config'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const PREFIX_ENV = 'APP_'
  const env = loadEnv(mode, '../', PREFIX_ENV)
  return {
    plugins: [
      react(),
      createHtmlPlugin({
        entry: 'src/main.tsx',
        template: 'index.html',
        inject: { data: { title: env.APP_NAME, lang: env.APP_LANGUAGE } },
      }),
    ],
    envDir: '../',
    envPrefix: [PREFIX_ENV],
    server: {
      watch: {
        usePolling: true,
      },
    },
    test: {
      globals: true,
      environment: 'jsdom',
      coverage: {
        provider: 'v8',
        exclude: [
          '**/*.d.ts',
          '**/*{.,-}{test,spec}.?(c|m)[jt]s?(x)',
          '**/{eslint,vite}.config.*',
          'src/main.tsx',
        ],
        thresholds: { '100': true },
      },
    },
  }
})
