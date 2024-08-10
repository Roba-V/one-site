import react from '@vitejs/plugin-react-swc'
import { defineConfig } from 'vitest/config'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
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
    },
  },
})
