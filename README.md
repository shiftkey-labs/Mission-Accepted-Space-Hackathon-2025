# ProjectShores – Protecting Canadian Shorelines with Satellite Data  

## Overview  
Canada has the largest coastline in the world, and its shorelines are increasingly threatened by climate change. Rising ocean temperatures and increased trade routes pose risks to both ecosystems and communities.  

Our project focuses on **two key factors**:  
1. **Shipping routes** → increased vessel traffic near Canadian coastlines.  
2. **Leatherback turtle migration** → endangered species at risk from habitat changes and fishing vessels.  

By combining satellite Earth Observation data with data feeds, and applying **machine learning with a K-Nearest Neighbors (KNN) prediction model**, a prototype was built that visualizes and predicts risk zones where **climate change, human activity, and biodiversity overlap**.  

---

## Data Sources  
- **Satellite AIS (Automatic Identification System)** → Ship positions and routes.  https://globalfishingwatch.org/
- **Tagging datasets (DFO/WWF)** → Leatherback turtle migration corridors.  https://open.canada.ca/data/dataset/7d187ff6-19f9-4f57-9de3-bd38ab760643
  
## Approach  
1. **Data Integration**  
   - Mapped turtle migration corridors and shipping routes on a single geospatial layer.  
   - Highlighted overlap “red zones” where risks to coastlines and wildlife are highest.  

2. **Prediction with KNN Model**  
   - Trained a **K-Nearest Neighbors (KNN) regression model** on turtle migration. 
   - Model predicts likely turtle positions based on historical sightings, distance, and time.  
   - Filters out unrealistic predictions by constraining distances and checking against land boundaries.  

3. **Protection Outcomes**  
   - Identify safer shipping corridors away from sensitive habitats.  
   - Inform conservation policy for marine ecosystems.  
   - Support shoreline protection by reducing human-caused pressure.  

**Team Members**
- Rehab Shakir - [LinkedIn](www.linkedin.com/in/rehabshakir)
- [Email](rehabshakir2@gmail.com)
- Tanishka Ghosh - [LinkedIn](https://www.linkedin.com/in/tanishka-ghosh)
- [Email](tn620502@dal.ca)
- Link to repo:
(https://github.com/Tanishka-G/geospatial-app-vite)
