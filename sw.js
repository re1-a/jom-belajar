const CACHE_NAME = 'bijak-kafa-cache-v1';
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  './icon.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache dibuka');
        // Gunakan catch bagi mengelakkan error jika fail tiada
        return Promise.all(
          urlsToCache.map(url => {
            return cache.add(url).catch(error => {
              console.error('Gagal cache fail:', url, error);
            });
          })
        );
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Pulangkan cache jika ada
        if (response) {
          return response;
        }
        
        // Buat fetch jika tiada dalam cache, jika offline fallback kepada index.html
        return fetch(event.request).catch(() => caches.match('./index.html'));
      })
  );
});
