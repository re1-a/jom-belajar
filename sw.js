const CACHE_NAME = 'bijak-kafa-cache-v2';
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './modul_kuiz/sains/script.js',
  './modul_kuiz/sains/style.css',
  './modul_kuiz/sains/notes_data.js',
  './modul_kuiz/sains/audio_db.js',
  './modul_kuiz/akhlak/akhlak.html'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[ServiceWorker] Pre-caching fail');
        return Promise.all(
          PRECACHE_URLS.map(url => {
            return cache.add(url).catch(error => {
              console.error('[ServiceWorker] Gagal cache fail:', url, error);
            });
          })
        );
      })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keyList => {
      return Promise.all(keyList.map(key => {
        if (key !== CACHE_NAME) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    // Network-first untuk navigasi (HTML)
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          return caches.match('./index.html');
        })
    );
  } else {
    // Cache-first untuk aset (CSS, JS, Imej)
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          return response || fetch(event.request);
        })
    );
  }
});
