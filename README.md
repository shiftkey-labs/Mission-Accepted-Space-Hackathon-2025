# ProjectShores – Protecting Canadian Shorelines with Satellite Data  

## Overview  
Canada has the largest coastline in the world, and its shorelines are increasingly threatened by climate change. Rising ocean temperatures and increased trade routes pose risks to both ecosystems and communities.  

Our project focuses on **two key factors**:  
1. **Shipping routes** → increased vessel traffic near Canadian coastlines.  
2. **Leatherback turtle migration** → endangered species at risk from habitat changes and vessel collisions.  

By combining satellite Earth Observation data with data feeds, and applying **machine learning with a K-Nearest Neighbors (KNN) prediction model**, a prototype was built that visualizes and predicts risk zones where **climate change, human activity, and biodiversity overlap**.  

---

## Data Sources  
- **Satellite AIS (Automatic Identification System)** → Ship positions and routes.  
- **Tagging datasets (DFO/WWF)** → Leatherback turtle migration corridors.
  
## Approach  
1. **Data Integration**  
   - Mapped turtle migration corridors and shipping routes on a single geospatial layer.  
   - Highlighted overlap “red zones” where risks to coastlines and wildlife are highest.  

2. **Prediction with KNN Model**  
   - Trained a **K-Nearest Neighbors (KNN) regression model** on turtle migration and vessel route data.  
   - Model predicts likely turtle positions and overlap zones based on historical sightings, distance, and time.  
   - Filters out unrealistic predictions by constraining distances and checking against land boundaries.  

3. **Protection Outcomes**  
   - Identify safer shipping corridors away from sensitive habitats.  
   - Inform conservation policy for marine ecosystems.  
   - Support shoreline protection by reducing human-caused pressure.  
