const C = "codigo-v1",
  F = [
    "./",
    "index.html",
    "style.css",
    "icons.css",
    "manifest.webmanifest",
    "icon-192.png",
    "icon-512.png",
    "apple-touch-icon.png",
  ];
self.addEventListener("install", (e) =>
  e.waitUntil(
    caches
      .open(C)
      .then((c) => Promise.all(F.map((u) => c.add(u).catch(() => {}))))
      .then(() => self.skipWaiting()),
  ),
);
self.addEventListener("activate", (e) =>
  e.waitUntil(
    caches
      .keys()
      .then((k) =>
        Promise.all(k.filter((x) => x != C).map((x) => caches.delete(x))),
      )
      .then(() => clients.claim()),
  ),
);
self.addEventListener("fetch", (e) => {
  if (e.request.method != "GET") return;
  e.respondWith(
    fetch(e.request, { cache: "no-cache" })
      .then((r) => {
        const k = r.clone();
        caches.open(C).then((c) => c.put(e.request, k));
        return r;
      })
      .catch(() => caches.match(e.request)),
  );
});
