# Canadian Satellite Viz

A real-time visualization platform for tracking Canadian satellites in orbit, monitoring their positions, orbital paths, and analyzing potential conjunction events (collision risks).

## Features

- **3D Interactive Globe**: Powered by Globe.gl and Three.js, displaying satellite positions, orbital paths, and conjunction alerts
- **Real-time Tracking**: Live satellite position updates using SGP4/SDP4 orbit propagation
- **Conjunction Analysis**: Monitor potential collision events with risk assessment and probability calculations
- **Comprehensive Dashboard**:
  - Searchable satellite list with detailed information
  - Conjunction events table with time-to-closest-approach
  - Analytics charts showing risk distribution and timelines
- **Time Controls**: Simulate satellite movements forward and backward in time
- **Space-themed UI**: Modern dark mode design optimized for space operations

## Canadian Satellites Tracked

The application monitors ~30 active Canadian satellites including:

- **SAPPHIRE** (NORAD 39089) - Space Surveillance
- **RADARSAT-2** (NORAD 32382) - Earth Observation
- **RADARSAT Constellation** (RCM-1, RCM-2, RCM-3) - Earth Observation
- **SCISAT-1** (NORAD 27843) - Atmospheric Research
- **CASSIOPE** (NORAD 40895) - Communications & Science
- **M3MSAT** (NORAD 43616) - Maritime Surveillance
- And more...

## Tech Stack

- **Frontend**: Next.js 15+ with React 18 and TypeScript
- **3D Visualization**: Globe.gl (Three.js based)
- **Orbit Propagation**: Satellite.js (SGP4/SDP4 implementation)
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Styling**: Tailwind CSS with custom space theme
- **Data Sources**:
  - Space-Track.org for TLE data (optional)
  - Celestrak SOCRATES for conjunction data (optional)
  - Built-in fallback data for offline operation

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Clone the repository:
   \`\`\`bash
   git clone <repository-url>
   cd Canadian Satellite Visualization
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. (Optional) Configure Space-Track.org credentials:

   - Copy `.env.example` to `.env.local`
   - Sign up at https://www.space-track.org/auth/createAccount
   - Add your credentials to `.env.local`

4. Run the development server:
   \`\`\`bash
   npm run dev
   \`\`\`

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

### Navigation

- **Search**: Use the search bar to find satellites by name or NORAD ID
- **Select Satellite**: Click on a satellite in the list or on the globe to view details
- **Time Controls**: Use the play/pause button and time slider to simulate satellite movements
- **Dashboard Tabs**: Switch between Satellites, Conjunctions, and Analytics views

### Understanding Conjunction Alerts

- **High Risk** (Red): Probability > 0.0001 or minimum range < 1 km
- **Medium Risk** (Yellow): Probability > 0.00001 or minimum range < 5 km
- **Low Risk** (Gray): Lower probability events

### API Endpoints

The application provides several API endpoints:

- `GET /api/satellites` - List all Canadian satellites
- `GET /api/tle/[noradId]` - Get TLE data for a specific satellite
- `POST /api/tle/batch` - Get TLE data for multiple satellites
- `GET /api/conjunctions?noradId=[id]` - Get conjunction events

## Data Sources

### Primary Sources (Optional)

1. **Space-Track.org**: Official TLE data from US Space Command

   - Requires free account registration
   - Provides most accurate orbital elements

2. **Celestrak SOCRATES**: Satellite Orbital Conjunction Reports Assessing Threatening Encounters in Space
   - Public conjunction data
   - Updated regularly

### Fallback Data

The application includes built-in fallback data for all Canadian satellites, ensuring it works without external API access. This makes it perfect for demos, development, and offline scenarios.

## Project Structure

\`\`\`
Canadian Satellite Visualization/
├── app/
│ ├── api/ # Next.js API routes
│ ├── layout.tsx # Root layout
│ ├── page.tsx # Main page
│ └── globals.css # Global styles
├── components/
│ ├── Globe.tsx # 3D globe visualization
│ ├── GlobeViewer.tsx # Globe wrapper component
│ ├── SatelliteViewer.tsx # Main viewer component
│ ├── Dashboard.tsx # Dashboard container
│ ├── SatelliteList.tsx # Satellite list component
│ ├── ConjunctionTable.tsx # Conjunction events table
│ ├── RiskChart.tsx # Analytics charts
│ ├── SatelliteDetails.tsx # Satellite info panel
│ ├── Header.tsx # App header
│ ├── TimeControls.tsx # Time simulation controls
│ └── ui/ # UI components
├── lib/
│ ├── types.ts # TypeScript type definitions
│ ├── canadianSatellites.ts # Satellite data
│ ├── satelliteUtils.ts # Orbit propagation utilities
│ ├── dataService.ts # API data service
│ └── utils.ts # Utility functions
└── public/ # Static assets
\`\`\`

## Development

### Adding New Satellites

Edit `lib/canadianSatellites.ts` and add new satellite entries with TLE data:

\`\`\`typescript
{
noradId: 12345,
name: "NEW SATELLITE",
line1: "1 12345U ...",
line2: "2 12345 ...",
launchDate: "2024-01-01",
status: "active",
operator: "Operator Name",
purpose: "Mission Purpose"
}
\`\`\`

### Customizing the Theme

Edit `app/globals.css` to modify the color palette and design tokens.

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import the project in Vercel
3. Add environment variables (if using Space-Track.org)
4. Deploy

### Other Platforms

The application can be deployed to any platform supporting Next.js:

\`\`\`bash
npm run build
npm start
\`\`\`

## Performance Considerations

- TLE data is cached for 1 hour to reduce API calls
- Orbit paths are generated on-demand for selected satellites
- Globe rendering is optimized with WebGL
- Satellite positions update every second during simulation

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

WebGL support is required for 3D visualization.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

MIT License - feel free to use this project for educational and commercial purposes.

## Acknowledgments

- **Canadian Space Agency** for satellite data
- **Space-Track.org** for TLE data
- **Celestrak** for conjunction analysis data
- **Globe.gl** for the amazing 3D visualization library
- **Satellite.js** for orbit propagation algorithms

## Support

For issues and questions, please open a GitHub issue or contact the maintainers.

---

Built with ❤️ for the Canadian space community
