# Viewport Tracker (QGIS Plugin)

A QGIS plugin that helps you keep track of areas of a map you have already viewed by creating boxes around your viewport.

![QGIS 3.0+](https://img.shields.io/badge/QGIS-3.0+-green) ![Python 3](https://img.shields.io/badge/Python-3.x-blue) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Toggle activation** — Toolbar button turns the plugin on/off (highlighted when active)
- **Quick capture** — Press **P** while active to capture the current view as a red box
- **Smart file management** — Fresh progress file per session; GPKG in project folder (saved) or temp (unsaved)
- **Crash recovery** — Progress boxes restored when you reopen QGIS after a crash
- **Auto cleanup** — Temp files removed on normal QGIS exit
- **Neon-style boxes** — Red polygons with a glow for clear visibility
- **Customizable** — Keyboard shortcuts and symbology via QGIS settings and layer properties

## Installation

### From GitHub (ZIP)

1. Download the repo: **Code → Download ZIP** (or clone).
2. Copy the `progress_tracker` folder into your QGIS plugins directory:
   - **Windows**: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. In QGIS: **Plugins → Manage and Install Plugins → Installed** → enable **Viewport Tracker**.

### From ZIP in QGIS

1. **Plugins → Manage and Install Plugins → Install from ZIP**.
2. Select a ZIP of the `progress_tracker` folder (or of this repo).
3. Enable **Viewport Tracker** in the Installed tab.

## Quick Start

1. **Activate** — Click the Viewport Tracker toolbar button (it stays highlighted when active).
2. **Capture** — Press **P** to add a red box for the current view.
3. **Deactivate** — Click the toolbar button again to turn off.

See **[progress_tracker/README.md](progress_tracker/README.md)** for full usage, file locations, and troubleshooting.  
See **[progress_tracker/ACTIVATION_GUIDE.md](progress_tracker/ACTIVATION_GUIDE.md)** for activation mode details.

## Requirements

- QGIS 3.0 or higher  
- Python 3.x  
- PyQt5 (included with QGIS)

## Repository structure

```
github/
├── README.md                 ← You are here
├── LICENSE
├── .gitignore
├── CONTRIBUTING.md
└── progress_tracker/         ← Viewport Tracker plugin
    ├── __init__.py
    ├── progress_tracker.py
    ├── metadata.txt
    ├── resources.qrc
    ├── icon.png              (required; add your own if missing)
    ├── README.md
    └── ACTIVATION_GUIDE.md
```

**Note:** The plugin expects `progress_tracker/icon.png`. If you built from source and the icon is missing, add a small PNG (e.g. 24×24) named `icon.png` in `progress_tracker/`.

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Hasmitha Rayasam** — [hasmitha.rs@gmail.com](mailto:hasmitha.rs@gmail.com)
