# QGIS Viewport Tracker Plugin

A QGIS plugin that helps you keep track of areas of a map you have already viewed by creating boxes around your viewport.

## Features

- **Toggle Activation**: Click the toolbar button to activate/deactivate the plugin (button stays highlighted when active)
- **Quick Capture**: Press 'P' while plugin is active to capture your current view as a red box
- **Smart File Management**: 
  - Creates fresh progress file each activation session
  - Saved projects: GPKG stored in project folder
  - Unsaved projects: GPKG stored in temp directory
- **Crash Recovery**: If QGIS crashes, your progress boxes will be restored when you reopen
- **Auto Cleanup**: Temp files are automatically deleted on normal QGIS exit
- **Neon Effect Styling**: Red boxes with a neon glow effect for clear visibility
- **Customizable**: Change keyboard shortcuts and symbology through QGIS settings and layer properties

## Installation

1. Copy the plugin folder to your QGIS plugins directory:
   - **Windows**: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\progress_tracker\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

2. **OR** Install from ZIP:
   - Open QGIS and go to **Plugins > Manage and Install Plugins**
   - Click **Install from ZIP** tab
   - Browse to the `progress_tracker.zip` file and install

3. Enable the plugin:
   - Find "Viewport Tracker" in the **Installed** tab
   - Check the box to enable it

4. You should see a toolbar icon appear in QGIS

## Usage

### Step 1: Activate the Plugin
Click the Viewport Tracker toolbar button to activate it. The button will stay **highlighted** to show it's active.

### Step 2: Capture Views
While the plugin is active:
- Press **'P'** on your keyboard, OR
- Click the toolbar button again to toggle off

A red box will be created around your current viewport each time you press 'P'.

### Step 3: View Progress
- The "progress" layer appears in your Layers panel
- All captured boxes are stored in this layer
- Box count is shown in the success message

### Step 4: Deactivate
Click the toolbar button again to deactivate. The button will no longer be highlighted.

## Behavior Details

### Activation/Deactivation
- **Click toolbar button once**: Activates plugin (button highlighted)
- **Click toolbar button again**: Deactivates plugin (button normal)
- **'P' key only works when plugin is ACTIVE**

### File Management
- **Each activation**: Creates a fresh progress file (unless one already exists in the session)
- **Layer removed by user**: Plugin automatically recreates it if still active
- **Normal QGIS exit**: Temp file is deleted automatically
- **QGIS crash**: Temp file is preserved for recovery

### File Storage Locations

**Saved Projects**:
```
{project_folder}/qgis_viewport_tracker_{project_name}.gpkg
```
Example: `C:\projects\mymap.qgs` → `C:\projects\qgis_viewport_tracker_mymap.gpkg`

**Unsaved Projects**:
```
{temp_folder}/qgis_viewport_tracker_temp.gpkg
```
Example: `C:\Users\YourName\AppData\Local\Temp\qgis_viewport_tracker_temp.gpkg`

## Tips

- **Activate first**: Make sure the toolbar button is highlighted before pressing 'P'
- **Visual feedback**: Button stays highlighted when active = you can capture boxes
- **Multiple boxes**: Zoom/pan to different areas and press 'P' each time
- **Crash recovery**: If QGIS crashes, reopen it and your progress will be restored
- **Clean slate**: Each time you activate, if you removed the old progress layer, a fresh one is created
- **Manual editing**: You can toggle layer editing to manually add/remove/modify boxes

## Troubleshooting

### "Plugin is not active" message when pressing 'P'
**Solution**: Click the toolbar button to activate the plugin first (it should be highlighted)

### Button not highlighted
**Solution**: Click the toolbar button once to activate it

### Boxes don't appear
1. Make sure plugin is activated (toolbar button highlighted)
2. Make sure you have at least one layer loaded in your project
3. Check that the "progress" layer is visible in the Layers panel

### Layer disappeared
**Solution**: The plugin will automatically recreate it if it's still active. Just press 'P' again.

## Export Progress

To save your progress permanently:
1. Right-click the "progress" layer in the Layers panel
2. Select "Export > Save Features As..."
3. Choose your desired format and location

## Requirements

- QGIS 3.0 or higher
- Python 3.x
- PyQt5 (included with QGIS)

## Keyboard Shortcuts

- **'P'**: Capture current view extent (only works when plugin is active)
- To customize: Go to Settings > Keyboard Shortcuts, search for "Toggle Viewport Tracker"

## Technical Details

- **File Format**: GeoPackage (.gpkg)
- **Geometry Type**: Polygon
- **Attributes**: ID (integer), Timestamp (string)
- **CRS**: Automatically uses the map canvas CRS
- **Temp File Cleanup**: Uses Python's atexit handler for normal shutdown

## License

This plugin is provided as-is for use with QGIS.
