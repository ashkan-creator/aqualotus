const CACHE = 'aqualotus-v2'
const STATIC = [
  '/',
  '/index.html',
  '/logo.png',
  '/rubika.png',
]
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(STATIC))
  )
  self.skipWaiting()
})
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  )
  self.clients.claim()
})
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return
  if (e.request.url.includes('/api/')) return

  // Navigation requests (HTML pages) must always be network-first: the HTML
  // references hashed JS/CSS filenames, so serving a stale cached HTML can
  // point at old/broken/missing bundle files after a new deploy.
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request)
        .then((res) => {
          if (res && res.status === 200) {
            caches.open(CACHE).then((c) => c.put(e.request, res.clone()))
          }
          return res
        })
        .catch(() => caches.match(e.request))
    )
    return
  }

  // Static hashed assets (JS/CSS/images): cache-first with background
  // revalidation is safe here, since Vite gives each build's files unique
  // hashed filenames -- a cached asset for a given URL never goes stale.
  e.respondWith(
    caches.match(e.request).then((cached) => {
      const fresh = fetch(e.request).then((res) => {
        if (res && res.status === 200) {
          caches.open(CACHE).then((c) => c.put(e.request, res.clone()))
        }
        return res
      }).catch(() => cached)
      return cached || fresh
    })
  )
})
