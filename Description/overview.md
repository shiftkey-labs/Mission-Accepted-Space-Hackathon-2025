# SatelLocator

### Team: Space++
### Members: Jeet Jani (jeetjani270@gmail.com), Alamedin Sabit (asabitt29@gmail.com)

---

## 🚀 Project Overview

**SatelLocator** is an interactive web platform that visualizes live satellite orbits and positions in real-time.  
It provides an intuitive 3D view of the Earth where users can track multiple satellites simultaneously, adjust simulation speed up to **4096×**, and toggle between visual layers like atmosphere, clouds, and bloom effects.

The system utilizes **Two-Line Element (TLE)** datasets to compute and propagate satellite positions in the **Earth-Centered Inertial (ECI)** frame, ensuring realistic, drift-free orbit alignment.  
The project was developed during the **Mission Accepted: Space Hackathon 2025** to showcase real-time satellite visualization and time control capabilities using open satellite data.

---

## 🧩 Key Features

- **Real-time satellite tracking** using TLE propagation in ECI coordinates.  
- **Accurate orbit visualization** with dynamically redrawn paths synchronized to simulation time.  
- **Adaptive time control** — smooth slider from **1× to 4096×** (log2 scale) with Play/Pause.  
- **Visually polished globe** with day/night terminator, dynamic lighting, atmosphere glow, and cloud layers.  
- **Adaptive markers** that automatically scale with zoom distance for readability.
- **Backend communication via Socket.IO** for live satellite position updates.  

## 🧠 Technical Architecture

### Frontend (Visualization)
- **Framework:** Next.js + React  
- **3D Engine:** Three.js + Three-stdlib (Line2, OrbitControls)  
- **Postprocessing:** Bloom + SMAA for cinematic glow  
- **Shaders:** Custom day/night blend with real solar illumination  
- **Language:** JavaScript (ES6)  

### Backend (Data & API)
- **Server:** Flask (Python)
- **Data Source:** Static TLE catalog (extendable to dynamic updates)  
- **Communication:** Socket.IO for streaming positions  
- **Coordinate System:** ECI propagation using SGP4 model  

---

## 🪐 System Flow

1. **Backend**
   - Loads TLE data and computes position vectors over time.
   - Emits updated positions via Socket.IO to connected clients.
2. **Frontend**
   - Subscribes to backend updates and merges metadata with live position feed.
   - Renders globe, orbits, and markers using WebGL.
   - Applies time-scaling and visual postprocessing in real time.

---

## 📊 Datasets & Sources

- **TLE Data Source:**  
  - [CelesTrak](https://celestrak.org/NORAD/elements/) — public satellite orbital elements.  
- **Earth Textures:**  
  - NASA Blue Marble dataset  
- **Libraries:**  
  - `three`, `three-stdlib`, `postprocessing`, `socket.io-client`, `next`, `react`.

---

## 🎨 Design Choices

- **ECI Coordinates** — consistent inertial frame for both orbits and markers (fixes drift).  
- **Logarithmic Speed Scale** — intuitive human perception of time acceleration.  
- **Strict Render Order** — resolves transparency and depth-fighting issues.  
- **Adaptive Marker Sizing** — ensures visibility across zoom scales.   
- **Performance-Aware Orbit Sampling** — ~150 vertices per orbit for precision vs efficiency balance.

---

## 🔬 Results

- Smooth visualization of up to **dozens of satellites simultaneously**.  
- Stable performance and consistent orbit-marker alignment across all speeds.  
- No transparency or z-fighting artifacts after depth ordering fix.  
- Fully portable between localhost and hosted deployments (Render/Vercel).  

---

## 🧭 Future Work

- Implement **local city lookup and pass prediction** (on-demand visibility).  
- Space Weather Integration to track solar flares, radiation, storms, metoers/ satellite collision detection.
- Enable **live TLE updates** from upstream feeds (CelesTrak API).  
- Add **screenshot/export** feature for orbit configurations.  
- Introduce **historical path playback** and **decay visualization** for decommissioned satellites.

## 🧑‍💻 Team Roles

| Member | Role | Focus Area |
|:--|:--|:--|
| Jeet | Backend Developer | Path Rendering, TLE propagation, Socket.IO API |
| Alamedin | Frontend Developer | WebGL, Three.js visualization |


## 🔗 Project Links

| Resource | Link |
|-----------|------|
| **Live Deployment** | [https://satellocator-frontend.vercel.app/](#) |
| **Frontend Repository** | [https://github.com/CodeBreaker2712/SatelLocator_Frontend](#) |
| **Backend Repository** | [https://github.com/CodeBreaker2712/SatelLocator](#) |

## ⚙️ Setup & Run

### Backend (Flask)
```bash
cd Codebase/backend
pip install -r requirements.txt
python app.py
```

### Frontend (Next.js)
```bash
cd Codebase/frontend
cp .env.example .env.local
# Example:
# NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
npm install
npm run dev
```

Then open **[http://localhost:3000](http://localhost:3000)** to launch **SatelLocator**.



## 🏁 Hackathon Context

Built during **Mission Accepted: Space Hackathon 2025**,  
supported by **ShiftKey Labs**, **MDA Space**, and the **Canadian Space Agency**.


## 📬 Acknowledgements

- **ShiftKey Labs mentors** for technical guidance.  
- **MDA Space & CSA** for access to public satellite datasets.  
- **Open-source contributors** of **Three.js**, **Socket.IO**, and **CelesTrak**.

---

*Prepared for final submission by **Team Space++**, Oct 26, 2025.*