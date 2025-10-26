🛰️ Canadian Satellite Tracker
A full-stack web application for real-time tracking of Canadian satellites in orbit, featuring bilingual support, interactive mapping, orbital calculations, and backend integration with Space-Track for the latest satellite data.

🌟 Features
Real-time Satellite Tracking: Updates data from Space-Track every 30 seconds.

Interactive Map: Visualizes orbits and positions of 19 Canadian satellites with Leaflet.js.

Detailed Information: NORAD catalog info, launch dates, status, operators, mission descriptions (English & French).

Orbital Predictions: Calculates passes over major Canadian cities.

Responsive UI: Desktop and mobile friendly.

Bilingual Support: Toggle between English and French throughout the UI.

Dark Mode Theme: Space-inspired, modern UI.

🚀 Quick Start
Prerequisites

Node.js (v16+ recommended)
Python 3.x

Space-Track.org account (for backend credentials)

**Installation
Clone/Download the project:

    git clone https://github.com/YOUR_USERNAME/canadian-satellite-tracker.git
    cd canadian-satellite-tracker

**Install Node dependencies:

   npm install

**Configure Space-Track credentials:

Create a .env file in the project root:

    SPACETRACK_USERNAME=your_email@domain.com
    SPACETRACK_PASSWORD=your_password
    (Alternatively, enter these directly in SLTrack.ini for Python fetches.)

**Running the Application
1. Start the Backend Server
The backend provides /api/tle endpoint using your Space-Track credentials.

   node server.mjs

Listens by default on http://localhost:5000.

2. Start the Frontend (React/Vite)
   
   npm run dev

Opens at http://localhost:5173.

3. Navigate to the App

Open http://localhost:5173 in your browser.

Choose satellites to track, see orbital positions, filter & search, view satellite passes, toggle English/French.

⚡ Project Structure

canadian-satellite-tracker/
├── public/                # Static assets (favicons, images, etc.)
├── src/                   # React frontend source code
│   ├── components/        # UI components (Map.jsx, Sidebar.jsx, StatsBar.jsx, etc.)
│   ├── data/              # satellites.js (Canadian satellites, cities), translations.js
│   ├── styles/            # CSS stylesheets
│   ├── utils/             # tleUtils.js (propagation & fetching), dateUtils.js
├── server.mjs             # Node.js backend API proxy to Space-Track
├── SLTrack.py             # Python script, TLE fetcher for advanced usage
├── SLTrack.ini            # Python backend config
├── package.json           # NPM dependencies & scripts
├── vite.config.js         # Vite build configuration
├── README.md              # Project documentation (this file)

🛰️ Satellite Database
Canadian satellites are listed in src/data/satellites.js

Exports an array of 19 satellites with NORAD catalog IDs (noradId), metadata, descriptions, and operator info.

City database for pass predictions included in src/data/satellites.js.

🔁 Data Flow
Frontend: Requests TLE data from /api/tle?norad=... with all NORAD IDs.

Backend: Proxies TLE lookup from Space-Track, returns up-to-date orbital elements using credentials from .env.

Frontend: Propagates satellite orbits, maps real-time positions, and calculates passes.

UI: Provides filters for status, search, bilingual toggle, interactive detail panels, and pass predictions for major cities.

🛠️ Useful Scripts
Run App in Development


   npm run dev

**Build Production Bundle

   npm run build

Start Python Backend (optional, if using advanced features)

   python SLTrack.py

🧹 Repo Cleanup
Delete .DS_Store and other system files.

Remove unused demo data (local-tle.json) unless using fallback.

Ensure only a single node_modules/, up-to-date dependencies in package.json.

Add .gitignore to exclude system files and build artifacts.

🗒️ License
This project is licensed under the MIT License.

🤝 Credits
Built with React, Vite, Leaflet.js, satellite.js, and Space-Track.org.

Developed & maintained by [Aman Bhalla and Tanvi Talwar].


