# Freehand Drawing → Snapped Route Generation Plan

## Goal
User freehand draw → snap to roads → generate real runnable route → safety scoring → tap-to-route (current → target)

## Current State
- ✅ Mobile: Flutter tap-draw (`_drawnPoints`)
- ✅ Model: `path_json`, `snapped_path_json`, `validation_json`
- ⚠️ Backend: Crude snapping (edge midpoint)
- ❌ No full route gen between snapped points
- ❌ No \"current pos → tap\" route

## Phase 1: Enhanced Snapping Logic
**MapService.create_manual_route()**
```
1. Raw points → segments
2. Each segment → nearest edge line projection
3. Snap if <30m, else warn
4. Collect snapped nodes/edges
```

**Geometry projection**:
```python
def point_to_line_projection(point, line_start, line_end):
  # Vector math to project point onto line segment
  # Return closest point on edge geometry
```

## Phase 2: Route Generation from Snapped Points
**New**: `snap_and_route()` → snapped nodes → Dijkstra path

**Cost**: `length_m * (1 + risk_score * factor)`
**Avoid**: `is_forbidden`

**Final**:
```
manual_route.final_route_json = graph_route(path)
manual_route.final_score = avg_risk
```

## Phase 3: Mobile \"Tap to Route\"
**routes_screen.dart**:
```
1. Track user GPS current_pos
2. Tap → target_pos
3. Call new API /routes/from-points (current_pos, target_pos)
4. Show generated path + score
```

## Phase 4: Validation & Feedback
```
validation_json: {
  snapped_ratio: 0.85,
  risky_ratio: 0.15,
  avg_risk: 0.42,
  warnings: [\"3 risky segments\"]
}
```

## Files to Edit
```
Backend:
- services/map_service.py (enhanced snapping)
- services/route_service.py (snapped route gen)
- api/routes/map.py (new endpoints)

Mobile:
- lib/features/routes/routes_screen.dart (tap-to-route)
- core/runna_api.dart (new API calls)
```

## Testing Steps
1. Backend: POST manual-route → check snapped_path_json
2. Mobile: Draw → save → see validation
3. Tap-to-route: GPS → tap → safe path shown

## Dependencies
```
pip install scipy (geometry projection)
No external APIs needed - uses seeded graph
```

**Next**: Create TODO.md, start with map_service.py snapping enhancement.

**Approve to proceed?**

