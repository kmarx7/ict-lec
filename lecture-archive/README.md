# Lecture Archive

Lecture Archive is a macOS desktop utility for archiving Zoom recordings that the user is
authorized to download. It uses an explicit observe → plan → act → evaluate loop and stops
normally when the host has disabled downloads.

## Development

```bash
uv sync --extra dev
uv run playwright install chromium   # only needed for browser integration
uv run python app.py
uv run pytest -q
uv run ruff check .
```

## Build a macOS app bundle

```bash
./scripts/build-macos.sh
open "dist/Lecture Archive.app"
```

The resulting bundle is unsigned. Distribution to other Macs additionally requires an Apple
Developer ID, hardened-runtime signing, and notarization.

The packaged app uses Playwright's standard per-user browser cache. Run
`uv run playwright install chromium` once on a new Mac before analyzing Zoom links.

The default archive is `~/Downloads/LectureArchive`. OAuth credentials, passcodes, cookies,
authorization headers, and signed URLs are never written to metadata or logs.

## Zoom integration status

The deterministic core, downloader, verifier, local import, SQLite library, and desktop UI are
implemented. Browser observation uses a centralized, conservative selector registry. Zoom can
change its DOM at any time, so selectors must be validated against a recording the user is
legally allowed to access. No stream interception, playlist extraction, cache scraping, or
hidden media URL discovery is performed. The API strategy accepts only an official download URL
already resolved by an authenticated API integration; OAuth/Keychain setup is intentionally a
future integration boundary.
