# Quick Start Guide

## 🚀 Get Running in 30 Seconds

```bash
# 1. Navigate to the project
cd satellocator-frontend

# 2. Install dependencies (if not already done)
npm install

# 3. Start the dev server
npm run dev
```

Open **http://localhost:3000** in your browser.

## 🎯 What You'll See

1. **Left sidebar**: Dropdown to select satellites
2. **Right panel**: Interactive 3D Earth globe
3. **Select a satellite**: A magenta orbit path appears showing 100 predicted positions

## 🎮 Controls

- **Left click + drag**: Rotate camera around Earth
- **Scroll wheel**: Zoom in/out
- **Right click + drag**: Pan camera

## 📊 Current Data

The app currently uses local data from:
```
public/data/Satellite-TLE-Data.json
```

Two satellites are included:
- **SAPPHIRE** (NORAD ID: 39088)
- **RADARSAT-2** (NORAD ID: 32382)

## ✅ Testing the Orbit Path

1. Open http://localhost:3000
2. Select "SAPPHIRE" from the dropdown
3. You should see:
   - Satellite info in the sidebar (NORAD ID, operator, launch date)
   - A **magenta orbit line** around Earth (100 points)
4. Switch to "RADARSAT-2"
   - Previous orbit disappears
   - New orbit appears for RADARSAT-2

## 🔧 Adding More Satellites

Edit `public/data/Satellite-TLE-Data.json`:

```json
[
  {
    "name": "YOUR_SATELLITE",
    "norad_id": 12345,
    "tle1": "1 12345U ...",
    "tle2": "2 12345 ...",
    "operator": "Your Org",
    "launch_date": "Jan 1, 2024",
    "mission": "Description",
    "status": "Active"
  }
]
```

Get TLE data from: https://celestrak.org/

## 🐛 Troubleshooting

### Port 3000 already in use
```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
npm run dev -- -p 3001
```

### Blank screen / Three.js errors
- Check browser console (F12)
- Ensure `satellite.js` and `three` are installed
- Try `rm -rf node_modules && npm install`

### Orbit not showing
- Open browser console
- Check if TLE data is valid
- Verify satellite selection triggered

## 📁 Project Structure

```
satellocator-frontend/
├── app/
│   ├── page.js          ← Main UI (satellite selector)
│   └── layout.js        ← Root layout
├── components/
│   └── GlobeScene.jsx   ← Three.js scene + orbit rendering
├── lib/
│   ├── orbit.js         ← TLE propagation logic
│   └── store.js         ← Global orbit mesh store
└── public/
    └── data/
        └── Satellite-TLE-Data.json ← Satellite data
```

## 🎨 Customization

### Change orbit color
`components/GlobeScene.jsx`, line ~150:
```javascript
const mat = new THREE.LineBasicMaterial({ color: 0xff00ff }); // ← Change this
```

Color options:
- `0xff0000` - Red
- `0x00ff00` - Green
- `0x0000ff` - Blue
- `0xffff00` - Yellow
- `0x00ffff` - Cyan

### Change number of orbit points
`components/GlobeScene.jsx`, line ~141:
```javascript
const pts = getOrbitPositions(tle1, tle2, 100); // ← Change 100
```

### Change Earth appearance
`components/GlobeScene.jsx`, line ~98:
```javascript
const earthMat = new THREE.MeshPhongMaterial({ 
  color: 0x003355,      // ← Base color
  emissive: 0x001020    // ← Glow color
});
```

## 🔗 Backend Integration (Later)

When Flask backend is ready, update `app/page.js`:

```javascript
// Line 11: Replace local fetch
fetch('/data/Satellite-TLE-Data.json')

// With API fetch
fetch('http://localhost:5000/api/satellite-positions')
```

See `BACKEND-INTEGRATION.md` for full backend setup guide.

## 📚 Learn More

- **satellite.js**: https://github.com/shashwatak/satellite-js
- **Three.js**: https://threejs.org/
- **Next.js**: https://nextjs.org/docs

## 🎉 You're Ready!

The frontend is fully functional. When your backend teammate finishes the Flask API, just update the fetch URL and you're done!

