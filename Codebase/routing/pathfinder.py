import routing_util
import geopandas as gpd
import heapq

tif_path = "./N_19781026_extent_v4.0.tif"

start_lat = 62.2
start_lon = -91.6
end_lat = 52.77
end_lon = -79.6

def find_nearest_open(navmap, row, col, radius=10):
    h, w = navmap.shape
    for r in range(-radius, radius + 1):
        for c in range(-radius, radius + 1):
            rr, cc = row + r, col + c
            if 0 <= rr < h and 0 <= cc < w and navmap[rr, cc] == 1:
                return (rr, cc)
    return None

# --- 8-connected A* pathfinding ---
def astar_pathfinding(navmap, start, goal):
    h, w = navmap.shape
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    def heuristic(a, b):
        # Manhattan distance is fine here; diagonal cost handled separately
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1),
                 (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            # reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for dr, dc in neighbors:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)
            if 0 <= nr < h and 0 <= nc < w and navmap[nr, nc] == 1:
                cost = 1.0 if abs(dr) + abs(dc) == 1 else 1.4
                tentative_g = g_score[current] + cost
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
    return []  # No path found

navmap, rgb_img, src = routing_util.preprocess_color_tiff_to_binary(
    tif_path,
    water_blue_ratio=1.2,
    blue_min=80,
    ice_brightness=220
)

start_pixel = routing_util.get_pixel_value_from_latlon(tif_path, start_lat, start_lon)
goal_pixel  = routing_util.get_pixel_value_from_latlon(tif_path, end_lat, end_lon)

start = find_nearest_open(navmap, *start_pixel)
goal = find_nearest_open(navmap, *goal_pixel)
if not start or not goal:
    raise ValueError("Could not find valid start/goal near given points.")

print(f"Start: {start}, Goal: {goal}")

path = astar_pathfinding(navmap, start_pixel, goal_pixel)

# routing_util.export_navmap(navmap)

if not path:
    print("⚠️ No path found!")
else:
    print(f"Path length: {len(path)} points")
    
    # export as GeoJSON in raster CRS:
    # line = routing_util.pixel_path_to_linestring(path, tif_path)
    # gdf = gpd.GeoDataFrame(geometry=[line], crs=src.crs)
    # gdf_wgs = gdf.to_crs("EPSG:4326")
    # gdf_wgs.to_file("pixel_route_wgs84.geojson", driver="GeoJSON")
    routing_util.export_route_geojson(path, tif_path)


# export as GeoJSON in raster CRS:
# line = routing_util.pixel_path_to_linestring(path, src)
# gdf = gpd.GeoDataFrame(geometry=[line], crs=src.crs)
# gdf_wgs = gdf.to_crs("EPSG:4326")
# gdf_wgs.to_file("pixel_route_wgs84.geojson", driver="GeoJSON")

# import numpy as np
# import matplotlib.pyplot as plt
# import heapq
# import geojson_utils

# # Generate fake "ice concentration" grid
# np.random.seed(42)
# ice = np.random.rand(10, 10)

# # Start and end coordinates (grid indices)
# start = (0, 0)
# end = (9, 9)

# # Simple A* pathfinding
# def astar(grid, start, end):
#     h, w = grid.shape
#     open_set = [(0 + np.linalg.norm(np.array(start)-np.array(end)), 0, start, [])]
#     visited = set()

#     while open_set:
#         est_total, cost, node, path = heapq.heappop(open_set)
#         if node in visited:
#             continue
#         visited.add(node)
#         path = path + [node]
#         if node == end:
#             return path
#         for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
#             x, y = node[0]+dx, node[1]+dy
#             if 0 <= x < h and 0 <= y < w:
#                 new_cost = cost + grid[x,y]
#                 est_total = new_cost + np.linalg.norm(np.array((x,y))-np.array(end))
#                 heapq.heappush(open_set, (est_total, new_cost, (x,y), path))
#     return []

# path = astar(ice, start, end)

# geojsonOutput = geojson_utils.route_to_geojson(path)
# print(geojsonOutput)

# # Plot result
# plt.imshow(ice, cmap='Blues')
# y, x = zip(*path)
# plt.plot(x, y, color='red')
# plt.title("Simulated Optimal Route Through Ice Field")
# plt.show()