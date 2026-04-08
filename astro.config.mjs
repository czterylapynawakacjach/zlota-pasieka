import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://czterylapynawakacjach.github.io',
  base: '/zlota-pasieka',
  integrations: [tailwind()],
  output: 'static'
});
