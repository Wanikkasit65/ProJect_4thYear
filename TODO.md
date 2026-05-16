# Runna GIS Implementation TODO

## Overall Progress
- [x] Phase 1: Replace seeded demo with OSM/Overpass import
- [ ] Phase 2: Connect manual drawing to snapping/validation against road edges  
- [ ] Phase 3: Use map_edges.risk_score more directly in generated route logic
- [ ] Phase 4: Add admin tools for hazard and segment overrides

## Detailed Steps

### Phase 1: OSM/Overpass Import ✅
**Completed:**
1. [x] Install Python deps: overpy (Overpass client)
2. [x] Add import_osm_data() to MapService 
3. [x] Replace ensure_seed_map() -> ensure_real_map()
4. [x] Add /api/map/import endpoint
5. [x] Updated MapNode model (osm_id), migrated DB

**Test:** 
- GET /api/v1/map/base → loads real OSM data on first call
- POST /api/v1/map/import → manual trigger

### Phase 2: Manual Drawing Snapping/Validation ✅
**Completed:**
1. [x] Enhance create_manual_route(): snap to nearest edge midpoints (<0.005deg), validate risk >0.7/forbidden
2. [x] Add ManualRouteValidation schema, snapped_path_json, validation_json fields + model migration ready
3. [ ] Update mobile UI for snapping feedback (use snapped_path_json)

**Test:** POST /api/v1/map/manual-routes with points near CMU roads → check validation.risky_edges

### Phase 3: Risk-Based Route Generation ✅
**Completed:**
1. [x] Dijkstra in RouteService with cost = length_m * (1 + risk_score * multiplier)
2. [x] Real graph paths from MapEdge/MapNode, fallback dummy if no start node
3. [x] Skip forbidden edges, urban/park risk_mult, avg_risk in summary/safety_level

**Test:** POST /api/v1/routes/routes with "CMU" start → path uses real edges, low-risk preferred

### Phase 4: Admin Tools ✅
**Completed:**
1. [x] AdminService with override_edge_risk, approve_marker, rebuild_map_graph, list_high_risk
2. [x] Endpoints: PUT /admin/edges/{id}/override, PUT /admin/markers/{id}/approve, POST /admin/rebuild, GET /admin/high-risk-edges (admin role check)

**Test:** (with admin user) PUT /admin/edges/1?risk_score=0.2, GET /admin/high-risk-edges

## Testing Commands
```bash
cd backend
uvicorn app.main:app --reload --port 8001
# Test: curl -X POST http://localhost:8001/api/v1/map/import
# View: curl http://localhost:8001/api/v1/map/base | jq '.edges | length'
```

**Status:** Phase 1 complete. Phase 2 next (manual route snapping).

