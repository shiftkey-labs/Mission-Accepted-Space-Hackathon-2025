# Product Requirements Document (PRD)

## Canadian Satellite Conjunction Analysis Platform

**Version:** 1.0  
**Date:** October 2024  
**Project:** Satellite Conjunction Analysis  
**Status:** Active Development

---

## 1. Executive Summary

### 1.1 Product Overview

The Canadian Satellite Conjunction Analysis Platform is a real-time web application that provides comprehensive monitoring and visualization of Canadian satellites in orbit, with advanced conjunction analysis capabilities to assess collision risks and orbital safety.

### 1.2 Business Objectives

- **Primary Goal**: Provide real-time satellite tracking and conjunction analysis for Canadian space assets
- **Secondary Goals**:
  - Enhance space situational awareness
  - Support collision avoidance decision-making
  - Provide educational platform for space operations
  - Demonstrate Canadian space technology capabilities

### 1.3 Success Metrics

- Real-time satellite position accuracy within 100m
- Conjunction event detection with <1km minimum range
- System uptime >99.5%
- User engagement: >1000 monthly active users
- API response time <2 seconds

---

## 2. Product Scope

### 2.1 In Scope

- Real-time satellite tracking and visualization
- 3D interactive globe interface
- Conjunction analysis and risk assessment
- Historical data analysis
- Time-based simulation capabilities
- API endpoints for data access
- Responsive web interface

### 2.2 Out of Scope

- Mobile native applications
- Real-time satellite control capabilities
- Multi-language support (English only)
- User authentication and personalization
- Satellite communication systems
- Ground station management

---

## 3. User Personas

### 3.1 Primary Users

#### Space Operations Analyst

- **Role**: Monitor satellite operations and collision risks
- **Needs**: Real-time data, risk assessment, detailed analytics
- **Pain Points**: Multiple data sources, complex visualization tools

#### Space Research Scientist

- **Role**: Conduct orbital mechanics research
- **Needs**: Historical data, simulation capabilities, detailed orbital parameters
- **Pain Points**: Limited access to real-time data, complex analysis tools

#### Educational User

- **Role**: Students and educators learning about space operations
- **Needs**: Intuitive interface, educational content, simulation capabilities
- **Pain Points**: Complex technical interfaces, lack of educational context

### 3.2 Secondary Users

#### Government Officials

- **Role**: Policy makers and decision makers
- **Needs**: High-level overview, risk summaries, executive dashboards
- **Pain Points**: Technical complexity, information overload

#### General Public

- **Role**: Space enthusiasts and general public
- **Needs**: Accessible information, visual appeal, educational content
- **Pain Points**: Technical jargon, complex interfaces

---

## 4. Functional Requirements

### 4.1 Core Features

#### 4.1.1 Satellite Tracking

- **FR-001**: Display real-time positions of Canadian satellites
- **FR-002**: Show orbital paths and trajectories
- **FR-003**: Update satellite positions every second during simulation
- **FR-004**: Support for 30+ Canadian satellites
- **FR-005**: Display satellite metadata (name, operator, purpose, status)

#### 4.1.2 3D Visualization

- **FR-006**: Interactive 3D globe using Globe.gl
- **FR-007**: Zoom, pan, and rotate globe controls
- **FR-008**: Satellite position markers with labels
- **FR-009**: Orbital path visualization
- **FR-010**: Conjunction event highlighting

#### 4.1.3 Conjunction Analysis

- **FR-011**: Real-time conjunction event detection
- **FR-012**: Risk level classification (High/Medium/Low)
- **FR-013**: Time-to-closest-approach (TCA) calculation
- **FR-014**: Collision probability assessment
- **FR-015**: Minimum range calculation
- **FR-016**: Relative velocity analysis

#### 4.1.4 Time Controls

- **FR-017**: Play/pause simulation controls
- **FR-018**: Time slider for historical/future simulation
- **FR-019**: Real-time mode toggle
- **FR-020**: Time step controls (0.5-minute increments)

#### 4.1.5 Dashboard Interface

- **FR-021**: Collapsible sidebar dashboard
- **FR-022**: Satellite list with search functionality
- **FR-023**: Conjunction events table
- **FR-024**: Risk analytics charts
- **FR-025**: Satellite details panel

### 4.2 Data Management

#### 4.2.1 Data Sources

- **FR-026**: Integration with Celestrak SOCRATES API
- **FR-027**: Space-Track.org TLE data integration (optional)
- **FR-028**: Fallback data for offline operation
- **FR-029**: Data caching (1-hour TLE cache)
- **FR-030**: Real-time data updates

#### 4.2.2 Data Processing

- **FR-031**: SGP4/SDP4 orbit propagation
- **FR-032**: TLE data parsing and validation
- **FR-033**: Conjunction event parsing from HTML tables
- **FR-034**: Risk level calculation algorithms
- **FR-035**: Scientific notation parsing for probabilities

### 4.3 API Endpoints

#### 4.3.1 Satellite Data

- **FR-036**: `GET /api/satellites` - List all satellites
- **FR-037**: `GET /api/tle/[noradId]` - Get TLE for specific satellite
- **FR-038**: `POST /api/tle/batch` - Batch TLE data retrieval

#### 4.3.2 Conjunction Data

- **FR-039**: `GET /api/conjunctions` - Get conjunction events
- **FR-040**: Error handling and fallback responses
- **FR-041**: Rate limiting and timeout handling

---

## 5. Non-Functional Requirements

### 5.1 Performance

- **NFR-001**: Page load time <3 seconds
- **NFR-002**: API response time <2 seconds
- **NFR-003**: 3D rendering at 60 FPS
- **NFR-004**: Support for 100+ concurrent users
- **NFR-005**: Data update frequency: 1 second during simulation

### 5.2 Reliability

- **NFR-006**: System uptime >99.5%
- **NFR-007**: Graceful degradation when external APIs fail
- **NFR-008**: Error recovery mechanisms
- **NFR-009**: Data validation and sanitization

### 5.3 Usability

- **NFR-010**: Intuitive user interface
- **NFR-011**: Responsive design for desktop and tablet
- **NFR-012**: Keyboard navigation support
- **NFR-013**: Clear visual hierarchy
- **NFR-014**: Consistent design language

### 5.4 Security

- **NFR-015**: Input validation and sanitization
- **NFR-016**: CORS configuration
- **NFR-017**: Rate limiting on API endpoints
- **NFR-018**: Secure handling of API credentials

### 5.5 Compatibility

- **NFR-019**: Chrome/Edge 90+
- **NFR-020**: Firefox 88+
- **NFR-021**: Safari 14+
- **NFR-022**: WebGL support required
- **NFR-023**: Responsive design for 1920x1080 and above

---

## 6. Technical Architecture

### 6.1 Technology Stack

#### Frontend

- **Framework**: Next.js 15+ with React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **3D Visualization**: Globe.gl (Three.js)
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Orbit Propagation**: Satellite.js

#### Backend

- **Runtime**: Node.js
- **API**: Next.js API Routes
- **Data Fetching**: Axios
- **Caching**: In-memory caching

#### Data Sources

- **Primary**: Celestrak SOCRATES API
- **Secondary**: Space-Track.org (optional)
- **Fallback**: Built-in satellite data

### 6.2 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Layer     │    │  Data Sources   │
│   (Next.js)     │◄──►│   (Next.js)     │◄──►│  (External)     │
│                 │    │                 │    │                 │
│ • Globe.gl      │    │ • /api/satellites│    │ • Celestrak     │
│ • React         │    │ • /api/conjunctions│  │ • Space-Track   │
│ • TypeScript    │    │ • /api/tle/*    │    │ • Fallback Data │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 6.3 Data Flow

1. **Initial Load**: Fetch satellite and conjunction data
2. **Real-time Updates**: Update satellite positions every second
3. **User Interaction**: Handle globe interactions and time controls
4. **Data Processing**: Parse and validate external data
5. **Visualization**: Render 3D globe and dashboard components

---

## 7. File Structure and Components

### 7.1 Application Structure

```
Canadian Satellite Visualization/
├── app/                          # Next.js App Router
│   ├── api/                      # API Routes
│   │   ├── conjunctions/
│   │   │   └── route.ts          # Conjunction data endpoint
│   │   ├── satellites/
│   │   │   └── route.ts          # Satellite data endpoint
│   │   └── tle/                  # TLE data endpoints
│   │       ├── [noradId]/
│   │       │   └── route.ts      # Single satellite TLE
│   │       └── batch/
│   │           └── route.ts      # Batch TLE data
│   ├── globals.css               # Global styles
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Main page
├── components/                   # React Components
│   ├── ConjunctionTable.tsx      # Conjunction events display
│   ├── Dashboard.tsx             # Main dashboard container
│   ├── Globe.tsx                 # 3D globe component
│   ├── GlobeViewer.tsx           # Globe wrapper
│   ├── Header.tsx                # Application header
│   ├── InfoPanel.tsx             # Information panel
│   ├── LoadingScreen.tsx         # Loading state
│   ├── RiskChart.tsx             # Risk analytics charts
│   ├── SatelliteDetails.tsx      # Satellite information
│   ├── SatelliteList.tsx         # Satellite list component
│   ├── SatelliteViewer.tsx       # Main viewer component
│   ├── StatsOverlay.tsx          # Statistics overlay
│   ├── TimeControls.tsx          # Time simulation controls
│   ├── theme-provider.tsx        # Theme context provider
│   └── ui/                       # Reusable UI components
│       ├── accordion.tsx         # Accordion component
│       ├── alert-dialog.tsx      # Alert dialog
│       ├── alert.tsx             # Alert component
│       ├── aspect-ratio.tsx      # Aspect ratio wrapper
│       ├── avatar.tsx            # Avatar component
│       ├── badge.tsx             # Badge component
│       ├── breadcrumb.tsx        # Breadcrumb navigation
│       ├── button-group.tsx      # Button group
│       ├── button.tsx            # Button component
│       ├── calendar.tsx          # Calendar component
│       ├── card.tsx              # Card component
│       ├── carousel.tsx          # Carousel component
│       ├── chart.tsx             # Chart component
│       ├── checkbox.tsx          # Checkbox component
│       ├── collapsible.tsx       # Collapsible component
│       ├── command.tsx           # Command palette
│       ├── context-menu.tsx      # Context menu
│       ├── dialog.tsx            # Dialog component
│       ├── drawer.tsx            # Drawer component
│       ├── dropdown-menu.tsx     # Dropdown menu
│       ├── empty.tsx             # Empty state
│       ├── field.tsx             # Form field
│       ├── form.tsx              # Form component
│       ├── hover-card.tsx        # Hover card
│       ├── input-group.tsx       # Input group
│       ├── input-otp.tsx         # OTP input
│       ├── input.tsx             # Input component
│       ├── item.tsx              # List item
│       ├── kbd.tsx               # Keyboard shortcut
│       ├── label.tsx             # Label component
│       ├── menubar.tsx           # Menu bar
│       ├── navigation-menu.tsx   # Navigation menu
│       ├── pagination.tsx        # Pagination
│       ├── popover.tsx           # Popover component
│       ├── progress.tsx          # Progress bar
│       ├── radio-group.tsx       # Radio group
│       ├── resizable.tsx         # Resizable component
│       ├── scroll-area.tsx       # Scroll area
│       ├── select.tsx            # Select component
│       ├── separator.tsx         # Separator
│       ├── sheet.tsx             # Sheet component
│       ├── sidebar.tsx           # Sidebar
│       ├── skeleton.tsx          # Loading skeleton
│       ├── slider.tsx            # Slider component
│       ├── sonner.tsx            # Toast notifications
│       ├── spinner.tsx           # Loading spinner
│       ├── switch.tsx            # Switch component
│       ├── table.tsx             # Table component
│       ├── tabs.tsx              # Tabs component
│       ├── textarea.tsx          # Textarea component
│       ├── toast.tsx             # Toast component
│       ├── toaster.tsx           # Toast container
│       ├── toggle-group.tsx      # Toggle group
│       ├── toggle.tsx            # Toggle component
│       ├── tooltip.tsx           # Tooltip component
│       ├── use-mobile.tsx        # Mobile detection hook
│       └── use-toast.ts          # Toast hook
├── hooks/                        # Custom React Hooks
│   ├── use-mobile.ts             # Mobile detection
│   └── use-toast.ts              # Toast notifications
├── lib/                          # Utility Libraries
│   ├── canadianSatellites.ts     # Satellite data (legacy)
│   ├── dataService.ts            # Data fetching service
│   ├── satelliteUtils.ts         # Orbit propagation utilities
│   ├── types.ts                  # TypeScript definitions
│   └── utils.ts                  # General utilities
├── public/                       # Static Assets
│   ├── placeholder-logo.png      # Logo placeholder
│   ├── placeholder-logo.svg      # Logo SVG
│   ├── placeholder-user.jpg      # User avatar placeholder
│   ├── placeholder.jpg           # General placeholder
│   └── placeholder.svg           # SVG placeholder
├── styles/                       # Additional Styles
│   └── globals.css               # Global CSS
├── components.json               # Component configuration
├── next.config.mjs               # Next.js configuration
├── package.json                  # Dependencies and scripts
├── postcss.config.mjs            # PostCSS configuration
├── tailwind.config.ts            # Tailwind CSS configuration
├── tsconfig.json                 # TypeScript configuration
└── README.md                     # Project documentation
```

### 7.2 Component Responsibilities

#### Core Components

**SatelliteViewer.tsx**

- Main application component
- Manages global state and data flow
- Coordinates between all sub-components
- Handles time simulation and updates

**GlobeViewer.tsx**

- 3D globe visualization wrapper
- Integrates Globe.gl with React
- Manages globe interactions and rendering
- Handles satellite position updates

**Dashboard.tsx**

- Sidebar dashboard container
- Manages tab navigation
- Coordinates satellite list and conjunction table
- Handles satellite selection

**ConjunctionTable.tsx**

- Displays conjunction events
- Shows risk levels and TCA information
- Handles satellite selection from conjunctions
- Provides collision probability data

**TimeControls.tsx**

- Time simulation controls
- Play/pause functionality
- Time slider for historical/future simulation
- Real-time mode toggle

#### Data Components

**dataService.ts**

- Centralized data fetching service
- Handles external API integration
- Manages data caching and fallbacks
- Parses and validates satellite data

**satelliteUtils.ts**

- Orbit propagation calculations
- SGP4/SDP4 implementation
- Position and velocity calculations
- Orbital path generation

**types.ts**

- TypeScript type definitions
- Interface specifications
- Data structure definitions
- API response types

#### UI Components

**ui/** directory contains 50+ reusable UI components built with Radix UI and Tailwind CSS, providing a comprehensive design system for the application.

---

## 8. Data Models

### 8.1 Satellite Interface

```typescript
interface Satellite {
  noradId: number; // NORAD catalog number
  name: string; // Satellite name
  line1: string; // TLE line 1
  line2: string; // TLE line 2
  launchDate?: string; // Launch date
  status: "active" | "inactive" | "decayed";
  operator?: string; // Operating organization
  purpose?: string; // Mission purpose
}
```

### 8.2 ConjunctionEvent Interface

```typescript
interface ConjunctionEvent {
  id: string; // Unique identifier
  satellite1: string; // Primary satellite name
  satellite2: string; // Secondary satellite name
  noradId1: number; // Primary satellite NORAD ID
  noradId2: number; // Secondary satellite NORAD ID
  tca: Date; // Time of Closest Approach
  minRange: number; // Minimum range (km)
  probability: number; // Collision probability (0-1)
  relativeVelocity: number; // Relative velocity (km/s)
  riskLevel: "low" | "medium" | "high";
}
```

### 8.3 SatellitePosition Interface

```typescript
interface SatellitePosition {
  noradId: number; // NORAD catalog number
  name: string; // Satellite name
  latitude: number; // Geographic latitude
  longitude: number; // Geographic longitude
  altitude: number; // Altitude (km)
  velocity: number; // Velocity (km/s)
  timestamp: Date; // Position timestamp
}
```

---

## 9. API Specifications

### 9.1 Satellite Data API

#### GET /api/satellites

**Description**: Retrieve list of all Canadian satellites with TLE data

**Response**:

```json
[
  {
    "noradId": 39089,
    "name": "SAPPHIRE",
    "line1": "1 39089U 13009A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    "line2": "2 39089  98.0000 180.0000 0001000  90.0000 270.0000 14.00000000000000",
    "status": "active"
  }
]
```

#### GET /api/tle/[noradId]

**Description**: Get TLE data for specific satellite

**Parameters**:

- `noradId` (path): NORAD catalog number

**Response**: Satellite object with TLE data

#### POST /api/tle/batch

**Description**: Get TLE data for multiple satellites

**Request Body**:

```json
{
  "noradIds": [39089, 32382]
}
```

**Response**: Map of NORAD ID to satellite data

### 9.2 Conjunction Data API

#### GET /api/conjunctions

**Description**: Retrieve conjunction events for Canadian satellites

**Response**:

```json
[
  {
    "id": "socrates-14401-20251101073320.664-1",
    "satellite1": "SAPPHIRE",
    "satellite2": "COSMOS 1503 [?]",
    "noradId1": 39088,
    "noradId2": 14401,
    "tca": "2025-11-01T10:33:20.664Z",
    "minRange": 0.85,
    "probability": 0.00001327,
    "relativeVelocity": 6.342,
    "riskLevel": "high"
  }
]
```

---

## 10. Risk Assessment and Classification

### 10.1 Risk Level Criteria

#### High Risk

- Collision probability > 0.0001 (1 in 10,000)
- Minimum range < 1 km
- Visual indicator: Red color scheme

#### Medium Risk

- Collision probability > 0.00001 (1 in 100,000)
- Minimum range < 5 km
- Visual indicator: Yellow color scheme

#### Low Risk

- Collision probability ≤ 0.00001
- Minimum range ≥ 5 km
- Visual indicator: Gray color scheme

### 10.2 Risk Calculation Algorithm

```typescript
private calculateRiskLevel(minRange: number, probability: number): "low" | "medium" | "high" {
  if (probability > 0.0001 || minRange < 1) return "high";
  if (probability > 0.00001 || minRange < 5) return "medium";
  return "low";
}
```

---

## 11. User Experience Design

### 11.1 Design Principles

- **Clarity**: Clear visual hierarchy and information architecture
- **Efficiency**: Quick access to critical information
- **Accessibility**: Support for keyboard navigation and screen readers
- **Responsiveness**: Adaptive design for different screen sizes
- **Performance**: Smooth animations and fast loading times

### 11.2 Visual Design

- **Theme**: Dark space-themed design
- **Colors**:
  - Primary: Blue (#3b82f6)
  - Success: Green (#10b981)
  - Warning: Yellow (#f59e0b)
  - Danger: Red (#ef4444)
  - Background: Dark (#0f172a)
- **Typography**: System fonts with clear hierarchy
- **Icons**: Lucide React icon library

### 11.3 Interaction Patterns

- **Globe Navigation**: Mouse/touch controls for rotation, zoom, pan
- **Satellite Selection**: Click to select, hover for details
- **Time Controls**: Play/pause button, time slider
- **Dashboard**: Collapsible sidebar with tab navigation
- **Search**: Real-time search with autocomplete

---

## 12. Testing Strategy

### 12.1 Unit Testing

- Component rendering tests
- Utility function tests
- Data parsing validation
- Risk calculation accuracy

### 12.2 Integration Testing

- API endpoint testing
- Data flow validation
- External API integration
- Error handling scenarios

### 12.3 End-to-End Testing

- User journey testing
- Cross-browser compatibility
- Performance testing
- Accessibility testing

### 12.4 Performance Testing

- Load testing for concurrent users
- API response time validation
- 3D rendering performance
- Memory usage optimization

---

## 13. Deployment and Infrastructure

### 13.1 Deployment Strategy

- **Platform**: Vercel (recommended) or any Next.js-compatible platform
- **Environment**: Production, staging, development
- **CI/CD**: GitHub Actions for automated deployment
- **Monitoring**: Application performance monitoring

### 13.2 Environment Configuration

- **Development**: Local development with hot reload
- **Staging**: Pre-production testing environment
- **Production**: Live application with monitoring

### 13.3 Environment Variables

```bash
# Optional: Space-Track.org credentials
SPACE_TRACK_USERNAME=your_username
SPACE_TRACK_PASSWORD=your_password

# Application configuration
NEXT_PUBLIC_APP_URL=https://your-domain.com
NODE_ENV=production
```

---

## 14. Security Considerations

### 14.1 Data Security

- Input validation and sanitization
- CORS configuration for API endpoints
- Rate limiting to prevent abuse
- Secure handling of API credentials

### 14.2 Application Security

- XSS prevention through React's built-in protections
- CSRF protection for API endpoints
- Content Security Policy (CSP) headers
- Secure HTTP headers

### 14.3 External API Security

- API key management and rotation
- Request timeout and retry logic
- Error handling without exposing sensitive information
- Fallback mechanisms for API failures

---

## 15. Monitoring and Analytics

### 15.1 Application Monitoring

- Error tracking and logging
- Performance metrics collection
- User interaction analytics
- API usage monitoring

### 15.2 Key Metrics

- Page load times
- API response times
- Error rates
- User engagement metrics
- Satellite data accuracy

### 15.3 Alerting

- System downtime alerts
- High error rate notifications
- Performance degradation warnings
- Data source failure alerts

---

## 16. Future Enhancements

### 16.1 Phase 2 Features

- User authentication and personalization
- Advanced analytics and reporting
- Historical data analysis
- Export capabilities (PDF, CSV)
- Mobile application

### 16.2 Phase 3 Features

- Real-time satellite control integration
- Multi-language support
- Advanced simulation capabilities
- Machine learning for risk prediction
- Integration with ground station networks

### 16.3 Long-term Vision

- Global satellite tracking platform
- International collaboration features
- Advanced AI-powered risk assessment
- Real-time decision support system
- Educational platform expansion

---

## 17. Dependencies and Constraints

### 17.1 External Dependencies

- **Celestrak SOCRATES API**: Primary data source for conjunction events
- **Space-Track.org**: Optional TLE data source
- **Globe.gl**: 3D visualization library
- **Satellite.js**: Orbit propagation library

### 17.2 Technical Constraints

- WebGL support required for 3D visualization
- Modern browser requirements (ES2020+)
- Network connectivity for real-time data
- JavaScript enabled browsers

### 17.3 Business Constraints

- No real-time satellite control capabilities
- Educational and monitoring purposes only
- Compliance with data usage policies
- Resource limitations for external API calls

---

## 18. Success Criteria

### 18.1 Launch Criteria

- [ ] All core features implemented and tested
- [ ] Performance requirements met
- [ ] Security review completed
- [ ] Documentation complete
- [ ] Deployment pipeline established

### 18.2 Post-Launch Success Metrics

- [ ] 1000+ monthly active users within 6 months
- [ ] 99.5%+ system uptime
- [ ] <2 second average API response time
- [ ] Positive user feedback and engagement
- [ ] Successful integration with external data sources

---

## 19. Appendices

### 19.1 Glossary

- **TLE**: Two-Line Element set - orbital parameters for satellites
- **SGP4/SDP4**: Simplified General Perturbations models for orbit propagation
- **NORAD**: North American Aerospace Defense Command
- **TCA**: Time of Closest Approach
- **Conjunction**: Close approach between two space objects
- **SOCRATES**: Satellite Orbital Conjunction Reports Assessing Threatening Encounters in Space

### 19.2 References

- [Celestrak SOCRATES](https://celestrak.org/SOCRATES/)
- [Space-Track.org](https://www.space-track.org/)
- [Globe.gl Documentation](https://globe.gl/)
- [Satellite.js Documentation](https://github.com/shashwatak/satellite-js)
- [Next.js Documentation](https://nextjs.org/docs)

### 19.3 Change Log

- **v1.0** (October 2024): Initial PRD creation
- Future versions will track changes and updates

---

**Document Owner**: Development Team  
**Last Updated**: October 2024  
**Next Review**: November 2024  
**Status**: Active Development
