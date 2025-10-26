# SatelLocator Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (localhost:3000)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Next.js App                        │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │           app/page.js (Client)              │  │  │
│  │  │  • Satellite selector                        │  │  │
│  │  │  • Data fetching                            │  │  │
│  │  │  • Metadata display                         │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                      ▼                                 │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │    components/GlobeScene.jsx (Client)       │  │  │
│  │  │  • Three.js scene                           │  │  │
│  │  │  • Earth rendering                          │  │  │
│  │  │  • Orbit path drawing                       │  │  │
│  │  │  • Camera controls                          │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                      ▼                                 │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │         lib/orbit.js (Utility)              │  │  │
│  │  │  • TLE propagation                          │  │  │
│  │  │  • Coordinate conversion                    │  │  │
│  │  │  • satellite.js wrapper                     │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ HTTP GET
                            │
                ┌───────────┴────────────┐
                │                        │
        ┌───────▼───────┐       ┌───────▼────────┐
        │   Local JSON  │   OR  │   Flask API    │
        │   (Current)   │       │   (Future)     │
        └───────────────┘       └────────────────┘
```

## Data Flow

```
User Action (Select Satellite)
    │
    ▼
app/page.js
    │
    ├─→ Fetch satellite data (JSON/API)
    │
    ▼
Set selected satellite state
    │
    ▼
GlobeScene.jsx receives selectedSatellite prop
    │
    ├─→ Extract tle1, tle2, norad_id
    │
    ▼
Call lib/orbit.js → getOrbitPositions(tle1, tle2, 100)
    │
    ├─→ satellite.js propagates orbit
    ├─→ Convert ECI → Geodetic
    ├─→ Convert Geodetic → Cartesian
    │
    ▼
Return array of 100 [x, y, z] points
    │
    ▼
drawOrbitPath() creates THREE.Line
    │
    ├─→ Create BufferGeometry
    ├─→ Add to scene
    ├─→ Store in orbitLineMeshes
    │
    ▼
Render magenta orbit path in 3D
```

## Component Hierarchy

```
RootLayout (app/layout.js)
│
└─── Page (app/page.js) [Client Component]
     ├─── Sidebar
     │    ├─── <select> Satellite selector
     │    └─── Metadata display
     │
     └─── Main
          └─── GlobeScene (components/GlobeScene.jsx) [Client]
               ├─── THREE.Scene
               ├─── THREE.PerspectiveCamera
               ├─── THREE.WebGLRenderer
               ├─── OrbitControls
               │
               ├─── Earth Mesh
               │    ├─── SphereGeometry (6371 km)
               │    └─── MeshPhongMaterial
               │
               ├─── Lighting
               │    ├─── DirectionalLight
               │    └─── AmbientLight
               │
               └─── Orbit Line Mesh (dynamic)
                    ├─── BufferGeometry
                    └─── LineBasicMaterial (magenta)
```

## File Responsibilities

### `app/layout.js` (Server Component)
- **Role:** Root HTML structure
- **Responsibilities:**
  - Define HTML, body tags
  - Set metadata (title, description)
  - Load global fonts
  - Import global CSS

### `app/page.js` (Client Component)
- **Role:** Main page logic
- **State:**
  - `sats` - Array of satellites
  - `selected` - Currently selected satellite
- **Responsibilities:**
  - Fetch satellite data
  - Render satellite selector
  - Display metadata
  - Pass selected satellite to GlobeScene

### `components/GlobeScene.jsx` (Client Component)
- **Role:** 3D visualization
- **State:**
  - `mountRef` - DOM mount point
  - `sceneRef` - Three.js scene reference
- **Responsibilities:**
  - Initialize Three.js scene
  - Render Earth sphere
  - Draw/remove orbit paths
  - Handle camera controls
  - Cleanup on unmount

### `lib/orbit.js` (Utility Module)
- **Role:** Orbit calculations
- **Functions:**
  - `getOrbitPositions(tle1, tle2, numPoints)`
  - `geoToCartesianKm(lat, lon, alt)`
- **Responsibilities:**
  - Parse TLE data
  - Propagate satellite positions
  - Convert coordinate systems

### `lib/store.js` (State Module)
- **Role:** Global state management
- **Data:**
  - `orbitLineMeshes` - Object storing orbit line meshes
- **Purpose:**
  - Track orbit lines for cleanup
  - Prevent memory leaks

## Key Algorithms

### 1. Orbit Propagation

```
Input: TLE1, TLE2, numPoints (100)

Step 1: Parse TLE with satellite.js
  → satrec = twoline2satrec(tle1, tle2)

Step 2: Calculate orbital period
  → period = (2π) / satrec.no
  → where satrec.no is mean motion (rad/min)

Step 3: Calculate time step
  → dtMs = (period × 60 × 1000) / numPoints
  → evenly distribute points over one orbit

Step 4: Propagate positions
  FOR i = 0 TO numPoints-1:
    time = startTime + (i × dtMs)
    posVel = propagate(satrec, time)
    
    IF posVel.position exists:
      gmst = gstime(time)
      geodetic = eciToGeodetic(posVel.position, gmst)
      APPEND {lat, lon, altKm} to points
      
Output: Array of 100 geodetic positions
```

### 2. Coordinate Conversion

```
Input: latitude (rad), longitude (rad), altitude (km)

Step 1: Calculate radius
  r = EARTH_RADIUS (6371 km) + altitude

Step 2: Trigonometric conversions
  cosLat = cos(latitude)
  sinLat = sin(latitude)
  cosLon = cos(longitude)
  sinLon = sin(longitude)

Step 3: Spherical to Cartesian
  x = r × cosLat × cosLon
  y = r × sinLat              (Y-up coordinate system)
  z = r × cosLat × sinLon

Output: [x, y, z] in kilometers
```

### 3. Orbit Path Drawing

```
Input: noradId, tle1, tle2, scene

Step 1: Get orbit positions
  points = getOrbitPositions(tle1, tle2, 100)

Step 2: Convert to cartesian coordinates
  positions = Float32Array(points.length × 3)
  FOR each point in points:
    [x, y, z] = geoToCartesianKm(point.lat, point.lon, point.altKm)
    positions[i++] = x
    positions[i++] = y
    positions[i++] = z

Step 3: Create Three.js geometry
  geometry = new BufferGeometry()
  geometry.setAttribute('position', new BufferAttribute(positions, 3))

Step 4: Create line material and mesh
  material = new LineBasicMaterial({ color: 0xff00ff })
  line = new Line(geometry, material)

Step 5: Add to scene and store
  scene.add(line)
  orbitLineMeshes[noradId] = line
```

### 4. Orbit Path Cleanup

```
Input: scene

Step 1: Iterate over stored meshes
  FOR each key in orbitLineMeshes:
    line = orbitLineMeshes[key]
    
    IF line exists:
      Step 2a: Remove from scene
        scene.remove(line)
      
      Step 2b: Dispose geometry (free GPU memory)
        line.geometry.dispose()
      
      Step 2c: Dispose material (free GPU memory)
        line.material.dispose()
      
      Step 2d: Delete reference
        delete orbitLineMeshes[key]
```

## State Management

### React State (app/page.js)
```javascript
const [sats, setSats] = useState([])         // All satellites
const [selected, setSelected] = useState(null) // Current selection
```

### Module-Level State (lib/store.js)
```javascript
export const orbitLineMeshes = {}  // { noradId: THREE.Line }
```

**Why module-level?**
- Shared across component instances
- Survives re-renders
- Enables cleanup across renders

## Performance Optimizations

### 1. Efficient Rendering
- **RequestAnimationFrame loop** for smooth 60 FPS
- **OrbitControls** for optimized camera updates
- **Phong material** (cheaper than PBR materials)

### 2. Memory Management
- **Dispose geometries** when removing orbit paths
- **Dispose materials** to free GPU memory
- **Store references** for efficient cleanup

### 3. Calculation Efficiency
- **Pre-calculate** orbital period
- **Batch coordinate conversions** using Float32Array
- **Single geometry** for entire orbit path (not 100 points)

### 4. Render Optimization
- **BufferGeometry** instead of Geometry (faster)
- **LineBasicMaterial** (no lighting calculations needed)
- **Simple sphere** for Earth (64×64 segments)

## Coordinate Systems

### 1. TLE → ECI (Earth-Centered Inertial)
- **Origin:** Earth's center
- **Axes:** Fixed in inertial space
- **Units:** Kilometers
- **Used by:** satellite.js propagation

### 2. ECI → Geodetic
- **Components:** Latitude, longitude, altitude
- **Latitude/Longitude:** Radians
- **Altitude:** Kilometers above sea level
- **Used for:** Human-readable coordinates

### 3. Geodetic → Cartesian (Three.js)
- **Origin:** Earth's center
- **X-axis:** Through prime meridian
- **Y-axis:** Through north pole (up)
- **Z-axis:** Completes right-hand system
- **Units:** Kilometers
- **Used by:** Three.js rendering

## Dependencies

```
next@16.0.0
├─ react@19.2.0
├─ react-dom@19.2.0

three@0.180.0
├─ Used for: 3D rendering
└─ Includes: OrbitControls, geometries, materials

satellite.js@6.0.1
├─ Used for: TLE parsing and propagation
└─ Functions: twoline2satrec, propagate, gstime, eciToGeodetic
```

## Build Process

```
Development:
  next dev → webpack → hot module reload → localhost:3000

Production:
  next build → webpack → optimize → bundle
  next start → Node.js server → port 3000

Export (Static):
  next build (with output: 'export')
  → Static HTML/CSS/JS → deploy to CDN
```

## API Contract (Future)

### Request
```http
GET /api/satellite-positions
Accept: application/json
```

### Response
```json
[
  {
    "name": "string",
    "norad_id": "integer",
    "tle1": "string (69 chars)",
    "tle2": "string (69 chars)",
    "operator": "string (optional)",
    "launch_date": "string (optional)",
    "mission": "string (optional)",
    "status": "string (optional)"
  }
]
```

### Required Fields
- `norad_id` - Unique identifier
- `tle1` - TLE line 1
- `tle2` - TLE line 2

## Error Handling

### Propagation Errors
```javascript
if (!pv.position) continue; // Skip invalid positions
```

### Coordinate Conversion
- Expects lat/lon in radians (from eciToGeodetic)
- Handles altitude = 0 gracefully

### Render Errors
- Component wrapped in Next.js error boundary
- Console logs for debugging

## Security Considerations

1. **No sensitive data in frontend** - TLE data is public
2. **CORS validation** - Backend should verify origin
3. **Input validation** - Satellite selection from dropdown only
4. **No eval/unsafe operations** - Standard React patterns

---

**Architecture Status:** ✅ Implemented and Tested  
**Last Updated:** October 25, 2025  
**Version:** 1.0.0

