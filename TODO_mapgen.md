# Freehand Drawing → Route Gen TODO

## Progress
- [x] planMapgen.md created
- [ ] Backend snapping enhancement
- [ ] Route gen from snapped points
- [ ] Mobile tap-to-route
- [ ] Validation UI

## Step 1: Enhanced Snapping (Current)
```
read backend/app/services/map_service.py create_manual_route()
enhance point-to-edge projection
test with POST /api/v1/map/manual-routes
```

## Step 2: Snapped Route Generation
```
add route_service.snap_points_to_route(snapped_points)
Dijkstra between consecutive snapped nodes
save final_route_json
```

## Step 3: Mobile Tap-to-Route
```
routes_screen.dart: track GPS, tap → API call
runna_api.dart: /routes/tap-to-route
```

## Commands
```bash
cd backend
uvicorn app.main:app --reload --port 8001
# Test: curl -X POST http://localhost:8001/api/v1/map/manual-routes -d '{"name":"test", "points":[{"lat":18.8059,"lng":98.9523},{"lat":18.8088,"lng":98.9595}]}' -H "Content-Type: application/json"
```

**Status**: Ready for Step 1 - map_service.py

