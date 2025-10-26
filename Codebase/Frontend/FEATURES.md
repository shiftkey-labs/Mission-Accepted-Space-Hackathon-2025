# Feature Guide

Quick reference for all features in SatelLocator.

## 🌍 Visual Features

### Earth Rendering
| Feature | Description | Toggle |
|---------|-------------|--------|
| **Day/Night Shader** | Realistic sun illumination with terminator | Always on |
| **Cloud Layer** | Rotating transparent clouds | ☑️ Cloud Layer |
| **Atmosphere Glow** | Blue rim lighting effect | ☑️ Atmosphere Glow |
| **Starfield** | Background stars (textured or procedural) | Always on |
| **Bloom Effect** | Glowing orbits and atmosphere | ☑️ Bloom Effect |

### Orbit & Satellite
| Feature | Description | Status |
|---------|-------------|--------|
| **Orbit Path** | 150-point closed loop using Line2 | Cyan, 3px wide |
| **Satellite Marker** | Glowing yellow sprite | Animated |
| **Real-time Position** | Updates based on simulation time | Live |
| **TLE Propagation** | Accurate orbital mechanics | satellite.js |

## 🎮 Controls

### Camera Controls (Mouse/Trackpad)
- **Rotate**: Left-click + drag
- **Zoom**: Scroll wheel
- **Pan**: Right-click + drag (or two-finger drag)

### Time Controls
| Control | Function | Range |
|---------|----------|-------|
| **Play/Pause** | Start/stop time progression | ▶️ / ⏸ |
| **Speed Slider** | Adjust playback speed | 0.001× to 1024× |
| **Now Button** | Reset to current time | Instant |

### Visual Toggles
- ☑️ **Atmosphere Glow** - Blue outer glow
- ☑️ **Cloud Layer** - White clouds
- ☑️ **Bloom Effect** - Post-processing glow

## 🔍 Search & Selection

### Satellite Search
- **Type to filter**: Search by name or NORAD ID
- **Real-time results**: Instant filtering
- **Case insensitive**: Works with any case

### Satellite Info Display
When selected, shows:
- Satellite name
- NORAD ID
- Operator
- Launch date

## ⌨️ Keyboard Shortcuts (Potential Future Addition)

Currently not implemented, but could add:
- `Space` - Play/Pause
- `R` - Reset to Now
- `←/→` - Decrease/Increase speed
- `1-3` - Toggle atmosphere/clouds/bloom
- `F` - Focus on satellite

## 📊 Performance Tips

### High Performance Mode
1. Disable **Bloom Effect**
2. Use 2K textures instead of 4K
3. Reduce orbit points to 100

### Quality Mode
1. Enable all visual toggles
2. Use 4K textures
3. Keep orbit points at 150

### Balanced Mode (Default)
- All toggles enabled
- 4K textures (or fallback)
- 150 orbit points
- Should run at 60 FPS on most hardware

## 🎨 Color Scheme

### Current Colors
- **Earth Day**: Blue/green (from texture)
- **Earth Night**: Orange/yellow city lights
- **Clouds**: White (semi-transparent)
- **Atmosphere**: Blue (#4488ff)
- **Orbit**: Cyan (#00ffff)
- **Satellite Marker**: Yellow/orange gradient
- **Stars**: White
- **UI Background**: Dark blue (#0a0e1a → #0d1321)
- **UI Accent**: Blue (#4488ff)

### Customizing Colors
See `README.md` → Customization section

## 🚀 Speed Reference

| Speed | Description | Use Case |
|-------|-------------|----------|
| 0.001× | Extreme slow motion | Debug precise positions |
| 0.1× | Slow motion | Watch terminator movement |
| 1× | Real-time | Observe actual speed |
| 10× | Fast forward | See orbit progress |
| 100× | Very fast | Complete orbit in minutes |
| 1024× | Maximum | Fastest time progression |

## 🛰️ Supported Satellites

All satellites with valid TLE data in:
```
/public/data/Satellite-TLE-Data.json
```

Common types:
- LEO (Low Earth Orbit): 200-2000 km
- MEO (Medium Earth Orbit): 2000-35,786 km
- GEO (Geostationary): ~35,786 km

## 📐 Technical Specifications

### Rendering
- **Engine**: Three.js (WebGL 2.0)
- **Resolution**: Adaptive (up to 2× device pixel ratio)
- **Tone Mapping**: ACESFilmic
- **Color Space**: sRGB

### Orbit Calculation
- **Method**: SGP4/SDP4 (satellite.js)
- **Input**: Two-Line Element (TLE) sets
- **Accuracy**: ~1-5 km typical error
- **Update Rate**: Every frame (60 FPS)

### Camera Limits
- **Min Distance**: 1.5× Earth radius (~9,556 km)
- **Max Distance**: 50× Earth radius (~318,550 km)
- **FOV**: 60°
- **Damping**: 0.05 (smooth motion)

## 🎯 Best Practices

### For Smooth Experience
1. Select one satellite at a time
2. Use moderate playback speeds (1-50×)
3. Enable damping on camera controls
4. Keep browser tab active for best FPS

### For Best Visuals
1. Download and install 4K Earth textures
2. Enable all visual toggles
3. Use modern GPU-capable device
4. View in fullscreen mode

### For Learning
1. Start at 1× speed to observe real motion
2. Use 10× to see complete orbits faster
3. Toggle atmosphere/clouds to see effects
4. Compare different satellite altitudes

## 🔧 Advanced Features

### Developer Console Access
All Three.js objects accessible via:
```javascript
// In browser console after scene loads
sceneRef.current // THREE.Scene object
orbitLineMeshes   // Orbit line meshes
satelliteMarkers  // Satellite sprite objects
```

### Custom Shader Uniforms
Day/night shader uniforms:
- `uDayMap` - Day texture
- `uNightMap` - Night texture
- `uLightDirection` - Sun direction vector

Atmosphere shader uniforms:
- `uAtmosphereColor` - Glow color

## 📱 Mobile Support

Currently optimized for desktop. Mobile considerations:
- Touch controls work (pinch to zoom, drag to rotate)
- Performance may vary on mobile GPUs
- Recommended: Disable bloom on mobile
- UI may need scrolling on small screens

## 🌐 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Full support |
| Firefox | 88+ | ✅ Full support |
| Safari | 14+ | ✅ Full support |
| Edge | 90+ | ✅ Full support |
| Mobile Safari | 14+ | ⚠️ Performance varies |
| Mobile Chrome | 90+ | ⚠️ Performance varies |

## 📚 Related Documentation

- `README.md` - Installation and setup
- `ENHANCEMENTS.md` - Implementation details
- `ARCHITECTURE.md` - System design
- `QUICKSTART.md` - Quick start guide

---

**Tip**: Press `F11` for fullscreen immersive experience!

