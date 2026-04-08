import { ui, defaultLang } from './ui';

export function getLangFromUrl(url: URL) {
  const parts = url.pathname.split('/').filter(Boolean);
  
  // Look for language in the parts. In a subpath like /zlota-pasieka/pl/, 
  // 'pl' might be at index 1. In /pl/, it's at index 0.
  for (const part of parts) {
    if (part in ui) {
      return part as keyof typeof ui;
    }
  }
  
  return defaultLang;
}

export function useTranslations(lang: keyof typeof ui) {
  return function t(key: keyof typeof ui[typeof defaultLang]) {
    return ui[lang][key] || ui[defaultLang][key];
  }
}

export function useTranslatedPath(lang: keyof typeof ui) {
  return function translatePath(path: string, l: string = lang) {
    const base = import.meta.env.BASE_URL; // Includes trailing slash, e.g., '/zlota-pasieka/' or '/'
    const cleanPath = path.startsWith('/') ? path.substring(1) : path;
    
    if (path === '' || path === '/') {
        return `${base}${l}/`;
    }
    return `${base}${l}/${cleanPath}`;
  }
}
