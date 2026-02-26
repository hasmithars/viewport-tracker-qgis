# Viewport Tracker - Activation Mode Guide

## 🎯 New Behavior Summary

The plugin now works in **ACTIVATION MODE**:
- Click toolbar button to **turn ON** (button stays highlighted)
- Press 'P' to capture boxes (only works when ON)
- Click toolbar button again to **turn OFF**

---

## 🔘 Visual Indicator

### Plugin ACTIVE (ON)
```
[🔴] ← Button is HIGHLIGHTED
```
- 'P' key works
- Captures boxes
- Message: "Viewport Tracker ACTIVATED. Press 'P' to capture view extents."

### Plugin INACTIVE (OFF)
```
[⚪] ← Button is NORMAL
```
- 'P' key does nothing (or shows warning)
- No boxes captured
- Message: "Viewport Tracker DEACTIVATED."

---

## 📋 Step-by-Step Usage

### First Time Use

1. **Load a map layer** in QGIS (any layer)

2. **Click the toolbar button** (red box icon)
   - Button becomes **highlighted**
   - Message: "Viewport Tracker ACTIVATED..."
   - "progress" layer appears in Layers panel

3. **Press 'P'** to capture current view
   - Red box appears on map
   - Message shows: "Captured view extent at [time] (Total: 1 boxes)"

4. **Pan/zoom** to a different area

5. **Press 'P'** again
   - Another box appears
   - Message shows: "Total: 2 boxes"

6. **Click toolbar button** to deactivate
   - Button becomes **normal** (not highlighted)
   - Message: "Viewport Tracker DEACTIVATED."

---

## 🔄 File Management

### When You Activate
- **First activation**: Creates fresh GPKG file
- **Already have progress layer**: Reuses existing file
- **Removed progress layer manually**: Creates fresh file

### When You Deactivate
- Progress layer stays visible
- Boxes remain on map
- Can still see your progress

### When You Close QGIS
- **Normal close** (File → Exit): Temp file deleted automatically
- **Crash**: Temp file preserved for recovery

### When You Reopen QGIS
- After crash: Progress restored
- After normal exit: Fresh start

---

## 💡 Common Scenarios

### Scenario 1: Start Fresh
1. Remove the "progress" layer from Layers panel
2. Click toolbar button to activate
3. New empty progress file created

### Scenario 2: Continue Work
1. Keep the "progress" layer
2. Click toolbar button to activate
3. Existing file reused, add more boxes

### Scenario 3: QGIS Crashed
1. Reopen QGIS
2. Reopen your project
3. Progress layer automatically restored
4. Click toolbar to activate and continue

### Scenario 4: Accidentally Pressed 'P' When Inactive
- Message shows: "Plugin is not active. Click the toolbar button to activate it first."
- Click toolbar button to activate, then press 'P'

---

## ⚠️ Important Notes

### ✅ DO THIS:
- **Always activate first** (click toolbar button until it's highlighted)
- **Press 'P'** only when button is highlighted
- **Look for messages** at the top of QGIS screen

### ❌ AVOID:
- Pressing 'P' when plugin is not active (won't work)
- Wondering why nothing happens (check if button is highlighted!)
- Forgetting to activate after QGIS restart

---

## 🆚 Old vs New Behavior

### OLD (Original Plugin):
- Press 'P' → Box appears (always)
- No activation needed
- No visual indicator of plugin state

### NEW (Activation Mode):
- Click button to activate (button highlighted)
- Press 'P' → Box appears (only when active)
- Clear visual indicator (highlighted = active)
- Click button again to deactivate

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| 'P' does nothing | Click toolbar button to activate (make it highlighted) |
| Button not highlighted | Click it once to activate |
| "Plugin is not active" message | Click toolbar button first |
| Layer disappeared | Press 'P' - plugin will recreate it |
| Want fresh start | Remove progress layer, then activate |

---

## 💾 File Locations

### Saved Project (`mymap.qgs`)
```
C:\projects\mymap.qgs
C:\projects\qgis_viewport_tracker_mymap.gpkg  ← Progress file
```

### Unsaved Project
```
C:\Users\YourName\AppData\Local\Temp\qgis_viewport_tracker_temp.gpkg
```
(Deleted on normal exit, kept on crash)

---

## 🎨 Customization

### Change Keyboard Shortcut
1. Settings → Keyboard Shortcuts
2. Search: "Toggle Viewport Tracker"
3. Change from 'P' to your preferred key

### Change Box Color
1. Right-click "progress" layer
2. Properties → Symbology
3. Change color and effects

---

## ✨ Benefits of Activation Mode

1. **Clear Status**: Button shows if plugin is on or off
2. **Intentional Capture**: Won't accidentally create boxes
3. **Better Control**: Turn on only when needed
4. **Fresh Start**: Easy to start with clean slate
5. **Crash Recovery**: Preserves work if QGIS crashes

---

## 📞 Quick Reference

| Action | Result |
|--------|--------|
| Click toolbar (OFF→ON) | Activate, button highlighted |
| Click toolbar (ON→OFF) | Deactivate, button normal |
| Press 'P' (when ON) | Capture box |
| Press 'P' (when OFF) | Warning message |
| Remove layer (when ON) | Auto-recreate layer |
| Exit QGIS normally | Delete temp file |
| QGIS crashes | Keep temp file |

---

**Remember: Button HIGHLIGHTED = Plugin ACTIVE = 'P' works!** ✨

