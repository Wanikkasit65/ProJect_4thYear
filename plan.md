# Runna GIS Routing Plan

## Goal

Build Runna as a GIS-based running route planning system focused on:

- safe route generation
- base map data management
- manual route drawing
- run tracking and navigation
- collaborative hazard markers
- admin-managed map updates

This version removes:

- social feed
- private chat
- accident detection
- emergency alert workflow

The system should help users generate or draw safer running routes by combining map geometry, road constraints, warnings, and route scoring.

## Product direction

Runna is no longer a social running app.

Runna becomes a location intelligence system for runners:

- users plan routes on top of GIS data
- the system evaluates road safety using constraints and risk scoring
- users can manually draw routes when auto-generation is not good enough
- users can contribute hazard markers for others
- admins manage map layers, risk rules, and warning data

## Core concept

The system should think in GIS structures first:

- `Point`
  - intersections
  - warning markers
  - landmarks
  - user pins

- `LineString`
  - road segments
  - user-drawn routes
  - generated route geometry
  - navigation path

- `Polygon`
  - parks
  - campuses
  - lakes
  - high-risk zones
  - preferred running zones
  - blocked or restricted areas

GeoJSON should be used as the interchange format for these geometries.

## New scope

### User features

- search and view base map
- view GIS layers
- generate route from structured input
- optionally generate route from coordinates
- manually draw route on map
- save route
- start run and track progress
- receive navigation guidance along planned route
- detect off-route deviation
- create collaborative hazard markers
- view hazard markers from others

### Admin features

- upload and update GIS layers
- approve or reject collaborative hazard markers
- mark road segments as preferred, discouraged, or forbidden
- configure road risk rules
- import map-related external data
- rebuild routing graph when base map changes

### Removed features

- post feed
- one-to-one chat
- accident detection
- emergency contacts
- emergency notifications

## Definition of success

The project is successful when:

- the app can display a base map with relevant GIS layers
- users can generate a route from location and constraints
- users can manually draw a route when needed
- the system can score routes using road risk logic
- routes avoid high-risk roads where possible
- users can start a run and follow a route on the map
- users can place collaborative warning markers
- admins can review markers and update map constraints
- all of this works as a coherent end-to-end workflow

## Main system idea

The backend should model the city or target area as a routing graph:

- `nodes`
  - usually intersections or connection points

- `edges`
  - road segments between nodes

Every edge should carry route-relevant properties such as:

- road class
- road width if available
- speed limit if available
- one-way or two-way
- footpath presence
- sidewalk presence
- bike lane presence if relevant
- lighting quality if available
- park proximity
- collaborative warning density
- admin restriction level
- computed risk score

Route generation should then operate on graph edges, not only on freehand coordinates.

## Safety model

### Rule

Main roads and big roads may still be runnable, but should usually be avoided because high speed limits and traffic exposure increase danger.

That means:

- do not blindly ban them
- give them higher traversal cost
- allow them only when route alternatives are poor
- let admin override a segment as forbidden when necessary

### Statistical / probability approach

Each road segment should have a risk score or probability-like measure.

Suggested concept:

- `P(risk | segment attributes)`

Initial inputs:

- road class
- speed limit
- lane count
- proximity to intersections
- lack of sidewalk
- lack of shoulder
- traffic incident density
- collaborative hazard density
- admin restriction tags

Initial implementation should be rule-based, for example:

- low speed local road = low penalty
- medium road with some warnings = medium penalty
- arterial / big road / high speed = high penalty

Later, this can evolve into:

- logistic scoring
- ranking model
- learned segment preference model

But the first production version should use transparent rule-based scoring.

## Base map and GIS strategy

### Data sources

Primary base map sources:

- OpenStreetMap / Overpass
- Nominatim for search and reverse geocoding
- optional routing providers such as openrouteservice

Optional premium sources later:

- TomTom traffic incidents
- TomTom safety-related traffic info
- Mapbox directions if needed

### Storage strategy

Use:

- PostgreSQL
- PostGIS

Main data groups:

- raw GIS layers
- road graph tables
- route plans
- route geometries
- manual drawn routes
- hazard markers
- admin restrictions
- feedback and labels

### Suggested GIS entities

- `map_nodes`
- `map_edges`
- `map_polygons`
- `hazard_markers`
- `restricted_segments`
- `preferred_segments`
- `route_plans`
- `route_feedback`
- `gis_layer_versions`

## Route generation modes

### Mode 1: generated route

User provides:

- start point or start location
- target distance
- route type
- environment preference
- risk tolerance

System returns:

- route geometry
- estimated distance
- estimated time
- route score
- safety explanation

### Mode 2: manual draw route

User draws a route directly on the map.

System then:

- snaps the line to valid road segments if possible
- checks whether it crosses risky or forbidden segments
- gives route quality feedback
- saves it as a planned route

This mode is required because early auto-generation may not always match user intent.

## Navigation and tracking

When the user starts a run:

- load the chosen route
- show current location
- show planned path
- track GPS progress
- compare live position to planned route
- warn on off-route deviation
- show basic navigation progress

The early version does not need voice navigation.
Visual path guidance is enough.

## Collaborative markers

This replaces social features.

Users should be able to place markers such as:

- dark area
- unsafe crossing
- stray dogs
- construction
- flooded path
- heavy traffic
- blocked walkway
- poor surface

Each marker should include:

- point geometry
- type
- severity
- timestamp
- created_by
- status
- optional note
- optional expiry

Markers should affect route scoring after approval or through confidence rules.

## Admin tools

Admin must be able to:

- upload GIS data
- refresh or replace map layers
- classify roads
- mark roads as discouraged or forbidden
- approve collaborative markers
- merge duplicate markers
- expire stale warnings
- inspect route generation output
- adjust routing weights

Admin should also have map-focused monitoring, not social moderation.

## AI strategy

### What AI should not do first

- do not start with an LLM-based route engine
- do not start by training a model without reliable labels

### What AI can do later

- learn safer segment ranking
- learn route preference from accepted vs rejected routes
- classify marker confidence
- predict route quality by area and time

### What to build first

- deterministic GIS pipeline
- rule-based risk scoring
- structured route generation
- manual drawing tools
- label collection for future training

## Implementation phases

## Phase 0: Scope reset

### Objective

Remove old product assumptions and align the entire project with the new GIS-first scope.

### Tasks

1. Remove old scope from docs:
- delete social assumptions
- delete accident/emergency assumptions
- rewrite architecture notes

2. Freeze new MVP:
- base map
- GIS storage
- route generation
- manual drawing
- run tracking
- collaborative markers
- admin GIS tools

3. Freeze non-MVP:
- advanced AI ranking
- live traffic prediction
- full external incident integrations
- large-scale map editing workflows

### Exit criteria

- project documentation matches the new direction

## Phase 1: GIS-first architecture foundation

### Objective

Prepare the backend and database for geospatial work.

### Tasks

1. Keep:
- FastAPI
- PostgreSQL
- PostGIS
- Flutter

2. Add GIS-oriented modules:
- geometry utils
- map import service
- route scoring service
- route graph builder

3. Confirm geospatial standards:
- GeoJSON for API exchange
- PostGIS geometry/geography in storage

4. Define map pipeline:
- source import
- graph extraction
- scoring
- serving

### Exit criteria

- architecture supports map-native workflows cleanly

## Phase 2: Database redesign for GIS

### Objective

Change the schema so GIS data becomes a first-class part of the system.

### Main tables

- `users`
- `roles`
- `map_nodes`
- `map_edges`
- `map_polygons`
- `route_plans`
- `route_segments`
- `manual_routes`
- `hazard_markers`
- `admin_segment_rules`
- `route_feedback`
- `gis_layer_imports`

### Tasks

1. Add PostGIS columns where needed
2. Add geometry indexes
3. Store route geometry as GeoJSON or PostGIS geometry
4. Track source and version of imported map data

### Exit criteria

- schema supports points, lines, polygons, graph edges, and user overlays

## Phase 3: Base map ingestion

### Objective

Load a usable base map into the system.

### Tasks

1. Select target area:
- city
- district
- campus

2. Import OSM data

3. Extract road network

4. Normalize road classes

5. Build intersection nodes and edge segments

6. Import polygon features:
- parks
- campuses
- lakes
- restricted zones

7. Store layer version metadata

### Exit criteria

- base map can be queried and rendered in the app

## Phase 4: Routing graph and edge scoring

### Objective

Turn the imported roads into a scored graph for route planning.

### Tasks

1. Build graph nodes from intersections
2. Build graph edges from road segments
3. Add edge attributes:
- class
- estimated speed
- penalty
- warning count
- segment length

4. Create risk scoring formula
5. Penalize high-speed and major roads
6. Support admin overrides

### Exit criteria

- each traversable segment has a usable route cost

## Phase 5: Generated route engine

### Objective

Generate running routes from structured constraints.

### Inputs

- start coordinate
- target distance
- route type
- environment preference
- risk tolerance

### Tasks

1. Implement graph-based search
2. Support loop routes
3. Support out-and-back routes
4. Prefer safer edges
5. Avoid forbidden segments
6. Return geometry and explanation

### Outputs

- route geometry
- distance
- ETA
- safety score
- route summary
- reason codes

### Exit criteria

- system can generate repeatable route output from constraints

## Phase 6: Manual draw route

### Objective

Let users draw their own route directly on the map.

### Tasks

1. Add draw mode in Flutter
2. Capture line geometry from user touches
3. Snap to known road segments when possible
4. Validate against forbidden or risky zones
5. Save manual route
6. Show warnings about poor segments

### Exit criteria

- user can manually create and save a route on the map

## Phase 7: Route preview and map UX

### Objective

Make the route visually understandable.

### Tasks

1. Show base map tiles
2. Show route line
3. Show start and end markers
4. Show road risk highlights
5. Show hazard markers
6. Show polygons such as parks or restricted areas

### Exit criteria

- user can understand why a route was generated and where risk lies

## Phase 8: Run tracking and navigation

### Objective

Let the user follow a planned route during a run.

### Tasks

1. Start run from selected route
2. Track current GPS
3. Render live location on map
4. Compare current position with route geometry
5. Detect off-route movement
6. Show progress and remaining distance

### Exit criteria

- user can start and follow a route on the map

## Phase 9: Collaborative hazard markers

### Objective

Allow users to contribute route-relevant warning data.

### Tasks

1. Add marker creation
2. Add marker categories
3. Add severity levels
4. Add expiry rules
5. Add review status
6. Feed approved markers into segment scoring

### Exit criteria

- user markers can influence route safety logic

## Phase 10: Admin GIS dashboard

### Objective

Give admins control over map layers and segment safety.

### Tasks

1. View GIS layers
2. Inspect segment scores
3. Approve markers
4. Override segment status
5. Upload new layer versions
6. Rebuild scoring and graph

### Exit criteria

- admin can maintain map quality and route safety rules

## Phase 11: External map and incident integrations

### Objective

Add supporting data sources where useful.

### Candidate integrations

- Overpass API for feature extraction
- Nominatim for geocoding
- openrouteservice for fallback routing
- TomTom incidents for road event overlays

### Tasks

1. Add integration abstraction layer
2. Cache external responses
3. Normalize external incidents into local marker format
4. Merge external data with admin and user signals

### Exit criteria

- external data can enrich route scoring without breaking local control

## Phase 12: AI training readiness

### Objective

Collect the right data so AI can improve routing later.

### Data to collect

- chosen route
- rejected route
- manual redraw actions
- off-route frequency
- marker density
- admin override labels
- route completion feedback

### Goal

Use these later to train:

- segment ranking
- route preference prediction
- marker confidence models

### Exit criteria

- system is ready for future AI without depending on it now

## MVP recommendation

The MVP should include only:

- GIS base map
- route generation from structured input
- manual draw route
- route preview on map
- run tracking
- collaborative markers
- basic admin review tools

Do not delay MVP for:

- advanced AI
- premium traffic APIs
- complex prediction models

## Important design rules

- always treat GIS data as the core product asset
- route planning must use road segments and constraints, not only direct coordinate lines
- high-speed roads should be penalized statistically, not always banned
- manual route drawing must exist as fallback
- collaborative markers must affect route scoring
- admin must be able to override the map
- AI should be layered on top of a strong deterministic system

## Final recommendation

The best rewrite path is:

1. remove old social/emergency scope completely
2. rebuild the schema around GIS objects and road graphs
3. make base map and manual draw work first
4. add safe route generation on top of scored road edges
5. add collaborative hazard markers
6. add admin GIS control
7. collect data for future AI training

This gives the project a stronger identity and a much better chance of producing a useful, researchable, and demoable system.
