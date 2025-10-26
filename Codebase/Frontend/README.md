# SatelLocator - Realistic Satellite Orbit Visualization

A Next.js 16 application that visualizes satellite orbits in 3D with a photorealistic Earth, day/night terminator, clouds, atmosphere glow, and real-time time-controlled satellite tracking using TLE (Two-Line Element) data.

## Features

### Visual Enhancements
- 🌍 **Photorealistic Earth** with day/night texture blending
- 🌤️ **Dynamic cloud layer** with slow rotation
- 🌟 **Atmosphere glow** using Fresnel shader effects
- ✨ **Starfield background** (textured or procedural)
- 💫 **Bloom post-processing** for glowing orbits and atmosphere
- 🎨 **SMAA anti-aliasing** for crisp rendering

### Orbit & Satellite Features
- 🛰️ **High-quality orbit paths** using Line2 (fat lines)
- 📍 **Animated satellite marker** with glowing sprite
- ⏱️ **Time control system** - play/pause, speed up to 1024x
- 🎯 **Real-time position updates** based on TLE propagation
- 📊 150+ point orbit visualization for smooth curves

### UI/UX
- 🔍 **Satellite search** with real-time filtering
- 🎛️ **Visual toggles** for atmosphere, clouds, and bloom
- ⏰ **Time playback controls** with speed slider
- 📱 **Responsive dark-themed UI** with modern design

## Tech Stack

- **Next.js 16** (App Router, React 19)
- **Three.js** - Core 3D rendering with PBR pipeline
- **three-stdlib** - Line2 for fat orbit lines
- **postprocessing** - Bloom and SMAA effects
- **satellite.js** - TLE orbit propagation
- **Custom shaders** - Day/night blending, atmosphere glow

## Project Structure

```
satellocator-frontend/
├── app/
│   ├── layout.js          # Root layout with metadata
│   ├── page.js            # Main page with satellite selector
│   └── globals.css        # Global styles
├── components/
│   └── GlobeScene.jsx     # Three.js scene with orbit rendering
├── lib/
│   ├── orbit.js           # Orbit propagation utilities
│   └── store.js           # Global mesh store
└── public/
    └── data/
        └── Satellite-TLE-Data.json  # Satellite TLE data
```

## Getting Started

### Prerequisites

- **Node.js 20.9.0 or higher** (required for Next.js 16)
- npm or yarn
- Modern GPU-capable browser (Chrome, Firefox, Edge, Safari)

### Installation

```bash
# Install Node 20 (if using nvm)
nvm install 20
nvm use 20

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Adding Earth Textures (Optional but Recommended)

For the best visual experience, download high-quality Earth textures:

1. Visit [Solar System Scope Textures](https://www.solarsystemscope.com/textures/)
2. Download the following textures (4K or 2K):
   - Earth Day Map
   - Earth Night Lights
   - Earth Clouds (with alpha)
   - Earth Normal Map (optional)
   - Earth Specular Map (optional)
   - Star Field

3. Rename and place them in `/public/textures/earth/`:
   ```
   public/textures/earth/
   ├── earth_day_4k.jpg
   ├── earth_night_4k.jpg
   ├── earth_clouds_4k.png
   ├── earth_normal_4k.jpg (optional)
   ├── earth_spec_4k.jpg (optional)
   └── stars_4k.jpg
   ```

**Note**: The app works without textures using fallback materials, but textures significantly enhance the visual quality.

## How It Works

### 1. Orbit Propagation (`lib/orbit.js`)

**`getOrbitPositions(tle1, tle2, numPoints)`**:
- Parses TLE data using `satellite.js`
- Calculates orbital period from mean motion
- Propagates 150 future positions around one complete orbit
- Converts ECI coordinates to geodetic (lat/lon/alt)

**`getPositionAtTime(tle1, tle2, date)`**:
- Calculates satellite position at a specific time
- Used for animating the satellite marker in real-time

**`getGroundTrack(tle1, tle2, durationMin, stepSec)`** (optional):
- Generates ground track points for extended visualization

### 2. Realistic Earth Rendering

**Day/Night Shader**:
```glsl
// Blends day and night textures based on sun angle
float lambert = max(dot(normal, lightDir), 0.0);
float terminator = smoothstep(-0.1, 0.1, lambert);
color = mix(nightTexture * 1.2, dayTexture, terminator);
```

**Atmosphere Glow**:
- Fresnel effect using view angle
- Additive blending for glowing rim
- BackSide rendering for proper depth

**Cloud Layer**:
- Transparent sphere slightly larger than Earth
- Slow rotation for dynamic effect
- Alpha-blended for realistic transparency

### 3. High-Quality Orbit Rendering

Uses `Line2` from `three-stdlib` instead of basic `THREE.Line`:
- Consistent screen-space width
- Better visibility at all zoom levels
- Smooth anti-aliased curves

### 4. Time Control System

**Playback Loop**:
```javascript
// Updates simTime based on playbackSpeed
deltaMs = (now - lastTime) * playbackSpeed;
setSimTime(prev => new Date(prev.getTime() + deltaMs));
```

**Marker Updates**:
- Every frame, recalculates satellite position
- Uses `getPositionAtTime(tle1, tle2, simTime)`
- Updates 3D sprite position in scene

### 5. Post-Processing Pipeline

```
Scene → RenderPass → SMAAEffect → BloomEffect → Screen
```

- **SMAA**: Removes jagged edges
- **Bloom**: Makes orbits and atmosphere glow
- **Tone Mapping**: ACESFilmic for realistic HDR

### 6. Data Flow

```
User selects satellite
  ↓
Extract TLE1, TLE2, NORAD ID
  ↓
Generate orbit path (150 points)
  ↓
Create Line2 mesh with gradient color
  ↓
Create glowing sprite marker
  ↓
User controls time (play/pause/speed)
  ↓
Update marker position every frame
  ↓
Render with bloom and effects
```

## Customization

### Change Orbit Color

Edit `components/GlobeScene.jsx` in the `drawOrbitPath` function:
```javascript
const lineMaterial = new LineMaterial({
  color: 0x00ffff, // Change to desired color (hex)
  linewidth: 3,    // Adjust thickness
  // ...
});
```

### Adjust Orbit Resolution

Edit `components/GlobeScene.jsx`:
```javascript
const pts = getOrbitPositions(tle1, tle2, 150); // Change 150 to desired count
// More points = smoother curve but more computation
```

### Modify Time Speed Range

Edit `app/page.js`:
```javascript
<input
  type="range"
  min="-10"  // 2^-10 = 0.001x speed
  max="10"   // 2^10 = 1024x speed
  step="0.5"
  // Change min/max for different speed ranges
/>
```

### Toggle Effects by Default

Edit `app/page.js`:
```javascript
const [showAtmosphere, setShowAtmosphere] = useState(true);  // Change to false
const [showClouds, setShowClouds] = useState(true);          // Change to false
const [showBloom, setShowBloom] = useState(true);            // Change to false
```

### Adjust Bloom Intensity

Edit `components/GlobeScene.jsx`:
```javascript
const bloomEffect = new BloomEffect({
  intensity: 0.4,           // Increase for stronger glow
  luminanceThreshold: 0.3,  // Lower = more objects glow
  luminanceSmoothing: 0.7   // Smoothness of bloom
});
```

### Switch to Backend API

Edit `app/page.js`:
```javascript
// Replace:
fetch('/data/Satellite-TLE-Data.json')

// With:
fetch('https://your-backend-api.com/api/satellite-positions')
```

## Data Format

Expected JSON structure for satellite data:

```json
[
  {
    "name": "SAPPHIRE",
    "norad_id": 39088,
    "tle1": "1 39088U 13009C   25297.72717685  .00000254  00000-0  10395-3 0  9991",
    "tle2": "2 39088  98.4172 117.8868 0010342 226.4031 133.6297 14.35131764662806",
    "operator": "DND/CAF",
    "launch_date": "Feb 25, 2013",
    "mission": "Space surveillance in MEO/GEO",
    "status": "Active"
  }
]
```

## Backend Integration (Future)

When your Flask backend is ready:

1. Update the API endpoint in `app/page.js`
2. Ensure the backend returns `tle1` and `tle2` fields
3. No changes needed to orbit calculation logic

### Example Flask Response

```python
@app.route('/api/satellite-positions')
def get_satellites():
    return jsonify([
        {
            'name': 'SAPPHIRE',
            'norad_id': 39088,
            'tle1': '1 39088U 13009C...',
            'tle2': '2 39088  98.4172...',
            # ... other fields
        }
    ])
```

## Troubleshooting

### "Node.js version >= 20.9.0 is required"
```bash
nvm install 20
nvm use 20
npm run dev
```

### "Cannot find module 'satellite.js'" or other dependencies
```bash
npm install
```

### Textures not loading (Earth appears as basic blue sphere)
- Check that texture files are in `/public/textures/earth/`
- Verify file names match exactly (case-sensitive)
- Check browser console for 404 errors
- **Note**: App works without textures using fallback materials

### Orbit line not showing
- Check browser console for errors
- Verify TLE data format is correct
- Ensure `tle1` and `tle2` are valid strings
- Try selecting a different satellite

### Performance issues / Low FPS
**Option 1 - Reduce quality**:
- Toggle off Bloom effect
- Use 2K textures instead of 4K
- Reduce orbit points from 150 to 75-100
- Lower Earth sphere segments (128 → 64)

**Option 2 - Optimize rendering**:
```javascript
// In GlobeScene.jsx, adjust pixel ratio
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5)); // Lower from 2
```

### Satellite marker not moving
- Ensure time playback is enabled (Play button)
- Check playback speed isn't set to 0x
- Verify satellite TLE data is valid

### WebGL context lost errors
- Too many satellites selected at once
- GPU memory exhausted
- Solution: Refresh page and select fewer satellites

## License

MIT

## Team

- **Frontend**: This implementation
- **Backend**: Flask API (teammate integration pending)

## References

- [satellite.js Documentation](https://github.com/shashwatak/satellite-js)
- [Three.js Documentation](https://threejs.org/docs/)
- [Next.js App Router](https://nextjs.org/docs/app)
