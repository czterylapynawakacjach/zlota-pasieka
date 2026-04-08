import { ui, defaultLang } from './ui';

export function getLangFromUrl(url: URL) {
  const parts = url.pathname.split('/').filter(Boolean);
  
  // Check for /zlota-pasieka/pl/ pattern if hosted on subpath
  // parts might be ['zlota-pasieka', 'pl', ...]
  const langIndex = parts.indexOf('zlota-pasieka') + 1;
  if (langIndex > 0 && parts[langIndex] in ui) {
    return parts[langIndex] as keyof typeof ui;
  }
  
  // Fallback for /[lang]/
  if (parts[0] in ui) return parts[0] as keyof typeof ui;
  
  return defaultLang;
}

export function useTranslations(lang: keyof typeof ui) {
  return function t(key: keyof typeof ui[typeof defaultLang]) {
    return ui[lang][key] || ui[defaultLang][key];
  }
}

export function useTranslatedPath(lang: keyof typeof ui) {
  return function translatePath(path: string, l: string = lang) {
    const cleanPath = path.startsWith('/') ? path : '/' + path;
    if (path === '' || path === '/') {
        return `/${l}/`;
    }
    return `/${l}${cleanPath}`;
  }
}
