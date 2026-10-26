# BetterPlayblast-Blender Restructured Code

## Overview
Unified addon combining BetterPlayblast engine with Easy Playblast features. Uses ONLY addon-defined settings for playblast rendering.

Code generated from Corentin BILEAU's usage of Claude

## Architecture

### Settings Layer
- **`preferences.py`**: AddonPreferences with 4 tabs (Output, Video, Render, Burn-In)
- **`quick_settings.py`**: Scene-level PropertyGroup for per-scene overrides

### Operator Layer
- **`ops/playblast.py`**: Main rendering operator using addon settings only
- **`ops/quick_ops.py`**: Quick Settings management (version, replay, open folder, preferences)

### UI Layer
- **`ui/panel.py`**: Main 3D View panel with playblast controls and Quick Settings UI

### Utilities
- **`playblast_utils.py`**: Helper functions for file/folder management
- **`addon.py`**: Addon initialization and dependency management

## Settings Hierarchy

### Addon Preferences (Default)
Read from `AddonPreferences`:
- Output folder mode (VIDEOS, PROJECT, SYSTEM)
- Playblast naming (FILENAME vs CUSTOM)
- Video codec and bitrate
- Resolution percentage
- Frame rate
- Viewport shading settings
- Burn-in options

### Quick Settings Overrides (Per-Scene)
When enabled in scene, overrides addon preferences:
- `resolution_override_enabled` → Uses custom resolution %
- `shading_override_enabled` → Uses custom viewport shading
- `frame_range_override_enabled` → Uses custom frame start/end
- `burnin_override_enabled` → Uses custom burn-in settings

## Playblast Operator Flow

1. **Input Validation**
   - Check addon preferences accessible
   - Check BetterPlayblast dependencies installed
   - Verify .blend file saved

2. **Settings Preparation**
   - Resolve output folder from addon prefs
   - Determine output filename
   - Apply Quick Settings overrides if enabled
   - Save current render settings for restoration

3. **Rendering**
   - Set viewport shading if using OpenGL
   - Capture frame data via handler
   - Render using `bpy.ops.render.opengl()` or `bpy.ops.render.render()`
   - Save metadata JSON

4. **Post-Processing**
   - Apply burn-in overlay via BetterPlayblast engine
   - Move to final output location
   - Update last playblast name in Quick Settings

5. **Restoration**
   - Restore render settings
   - Restore viewport shading

## Key Design Decisions

### Settings Isolation
- Operator **does NOT** access `bpy.context.scene.render` directly
- All render parameters sourced from addon preferences + Quick Settings
- Prevents interference with Blender's default render settings

### Quick Settings System
- Each override has `*_enabled` boolean flag
- When enabled, override completely replaces addon setting
- Supports version numbering, resolution, shading, frame range, burn-in

### Backward Compatibility
- `BP_QuickSettings` maintains legacy property names
- `playblast_utils.py` uses both old and new property names
- Existing .blend files with old Quick Settings continue to work

## Files Modified

| File | Changes |
|------|---------|
| `preferences.py` | 4 tabs (Output/Video/Render/Burn-In), cleaned structure |
| `quick_settings.py` | Unified settings with legacy compatibility |
| `ops/playblast.py` | Complete rewrite: addon-only settings, viewport override |
| `ops/quick_ops.py` | Version management operators (no changes) |
| `ui/panel.py` | Updated imports, simplified Quick Settings UI |
| `playblast_utils.py` | Added `get_playblast_filename()`, fixed refs |
| `__init__.py` | Property names: `ep_*` → `bp_*` |

## Testing Checklist

- [ ] Addon loads without errors in Blender 4.2+
- [ ] Playblast button renders successfully
- [ ] Quick Settings resolution override works
- [ ] Quick Settings shading override works
- [ ] Quick Settings frame range override works
- [ ] Replay button plays latest playblast
- [ ] Open Folder button opens output folder
- [ ] Preferences button opens addon preferences
- [ ] Version increment/decrement operators work
- [ ] Burn-in overlay renders correctly
