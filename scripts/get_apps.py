"""Download the open-source Sauce Labs "My Demo App" builds used by the mobile suite.

Usage:
    python scripts/get_apps.py android     # apps/mda-<version>.apk
    python scripts/get_apps.py ios         # apps/SauceLabs-Demo-App.app (simulator build)
"""

from __future__ import annotations

import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS = ROOT / "apps"
RELEASES = {
    "android": (
        "https://github.com/saucelabs/my-demo-app-android/releases/download/2.3.0/mda-2.3.0-27.apk",
        "mda-2.3.0-27.apk",
    ),
    "ios": (
        "https://github.com/saucelabs/my-demo-app-ios/releases/download/2.3.0/SauceLabs-Demo-App.Simulator.zip",
        "SauceLabs-Demo-App.Simulator.zip",
    ),
}


def download(platform: str) -> Path:
    url, filename = RELEASES[platform]
    APPS.mkdir(exist_ok=True)
    target = APPS / filename
    if not target.exists():
        print(f"Downloading {url}")
        urllib.request.urlretrieve(url, target)
    if target.suffix == ".zip":
        with zipfile.ZipFile(target) as archive:
            archive.extractall(APPS)
        app = next(APPS.rglob("*.app"))
        final = APPS / "SauceLabs-Demo-App.app"
        if app != final and not final.exists():
            app.rename(final)
        target = final
    print(f"Ready: {target.relative_to(ROOT)}")
    return target


if __name__ == "__main__":
    platforms = sys.argv[1:] or ["android"]
    for p in platforms:
        if p not in RELEASES:
            sys.exit(f"Unknown platform '{p}'. Use: android, ios")
        download(p)
