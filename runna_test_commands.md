# Runna Test Commands

## Backend API Test
```bash
cd g:/test_project/backend

# Start server
uvicorn app.main:app --reload --port 8001

# Terminal 2 - Test endpoints
# 1. Load map (seeded or OSM)
curl http://localhost:8001/api/v1/map/base

# 2. Create manual route (draw points)
curl -X POST http://localhost:8001/api/v1/map/manual-routes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Draw",
    "points": [
      {"lat":18.8059, "lng":98.9523},
      {"lat":18.8088, "lng":98.9595},
      {"lat":18.8018, "lng":98.9630}
    ]
  }'

# 3. List routes
curl http://localhost:8001/api/v1/map/manual-routes

# 4. Generate route
curl -X POST http://localhost:8001/api/v1/routes/generate \
  -H "Content-Type: application/json" \
  -d '{
    "start_label": "CMU",
    "target_distance_km": 5.0,
    "route_type": "loop",
    "environment": "campus"
  }'

# Admin
curl -X POST http://localhost:8001/api/v1/admin/edge/1/override \
  -H "Content-Type: application/json" \
  -d '{"risk_score": 0.9, "is_forbidden": true}'
```

## Frontend Test
```bash
cd g:/test_project/mobile
flutter clean
flutter pub get
flutter run -d chrome --web-port 8080
# Draw on map, save, check validation
```

## OSM Import Test
```bash
# In backend terminal
curl -X POST "http://localhost:8001/api/v1/map/import?min_lat=18.79&min_lng=98.94&max_lat=18.82&max_lng=98.97"
curl http://localhost:8001/api/v1/map/base | jq '.edges | length'
```

## Expected Results
- Manual route: `snapped_path_json` ≠ null, `validation_json` shows risks
- Generated route: `path_json` uses real edges, `safety_level` reflects risk
- Map: 50+ edges after OSM import

## Debug
```
# Backend logs
tail -f backend/app.log

# DB check
psql -d runna -c "SELECT count(*) FROM map_edges;"
```

