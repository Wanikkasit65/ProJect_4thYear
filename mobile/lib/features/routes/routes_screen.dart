import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../../core/models.dart';
import '../auth/auth_controller.dart';

class RoutesScreen extends StatefulWidget {
  const RoutesScreen({super.key, required this.controller});

  final AuthController controller;

  @override
  State<RoutesScreen> createState() => _RoutesScreenState();
}

class _RoutesScreenState extends State<RoutesScreen> {
  final _mapController = MapController();
  final _manualRouteNameController = TextEditingController(text: 'Manual Campus Route');
  final _startController = TextEditingController(text: 'CMU Main Gate');
  final _distanceController = TextEditingController(text: '5');
  final _routeTypeController = TextEditingController(text: 'loop');
  final _environmentController = TextEditingController(text: 'park');

  BaseMapData? _baseMap;
  List<ManualRouteItem> _manualRoutes = const [];
  List<RoutePlanItem> _generatedRoutes = const [];
  List<RoutePoint> _drawnPoints = const [];
  RoutePlanItem? _selectedGeneratedRoute;
  String? _message;
  bool _isLoading = false;
  bool _drawMode = true;

  @override
  void initState() {
    super.initState();
    _loadMapStudio();
  }

  @override
  void dispose() {
    _manualRouteNameController.dispose();
    _startController.dispose();
    _distanceController.dispose();
    _routeTypeController.dispose();
    _environmentController.dispose();
    super.dispose();
  }

  Future<void> _loadMapStudio() async {
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      final baseMap = await widget.controller.getBaseMap();
      final manualRoutes = widget.controller.isAuthenticated ? await widget.controller.getManualRoutes() : const <ManualRouteItem>[];
      final generatedRoutes = widget.controller.isAuthenticated ? await widget.controller.getRoutes() : const <RoutePlanItem>[];
      if (!mounted) return;
      setState(() {
        _baseMap = baseMap;
        _manualRoutes = manualRoutes;
        _generatedRoutes = generatedRoutes;
        _selectedGeneratedRoute = generatedRoutes.isNotEmpty ? generatedRoutes.first : null;
      });
      _moveToCenter();
    } catch (error) {
      if (!mounted) return;
      setState(() {
        _message = '$error';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _moveToCenter() {
    final map = _baseMap;
    if (map == null || map.nodes.isEmpty) return;
    final first = map.nodes.first;
    _mapController.move(LatLng(first.lat, first.lng), 14);
  }

  void _handleMapTap(TapPosition _, LatLng point) {
    if (!_drawMode) return;
    setState(() {
      _drawnPoints = [..._drawnPoints, RoutePoint(lat: point.latitude, lng: point.longitude)];
    });
  }

  void _clearDrawnRoute() {
    setState(() {
      _drawnPoints = const [];
    });
  }

  Future<void> _saveManualRoute() async {
    if (_drawnPoints.length < 2) {
      setState(() {
        _message = 'Add at least two points before saving a manual route.';
      });
      return;
    }
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      await widget.controller.createManualRoute(
        name: _manualRouteNameController.text.trim(),
        points: _drawnPoints,
      );
      if (!mounted) return;
      setState(() {
        _drawnPoints = const [];
      });
      await _loadMapStudio();
    } catch (error) {
      if (!mounted) return;
      setState(() {
        _message = '$error';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _dropHazardMarker() async {
    if (_drawnPoints.isEmpty) {
      setState(() {
        _message = 'Tap the map to choose a position for a hazard marker first.';
      });
      return;
    }
    final point = _drawnPoints.last;
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      await widget.controller.createMarker(
        markerType: 'unsafe_crossing',
        severity: 3,
        lat: point.lat,
        lng: point.lng,
        note: 'Added from manual draw mode',
      );
      await _loadMapStudio();
    } catch (error) {
      if (!mounted) return;
      setState(() {
        _message = '$error';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _generateRoute() async {
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      final route = await widget.controller.generateRoute(
        startLabel: _startController.text.trim(),
        targetDistanceKm: double.tryParse(_distanceController.text.trim()) ?? 5,
        routeType: _routeTypeController.text.trim(),
        environment: _environmentController.text.trim(),
      );
      if (!mounted) return;
      setState(() {
        _selectedGeneratedRoute = route;
      });
      await _loadMapStudio();
    } catch (error) {
      if (!mounted) return;
      setState(() {
        _message = '$error';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final map = _baseMap;
    final drawnPolyline = _drawnPoints.map((point) => LatLng(point.lat, point.lng)).toList();
    final selectedGeneratedPolyline = _selectedGeneratedRoute?.points
            .map((point) => LatLng(point.lat, point.lng))
            .toList() ??
        const <LatLng>[];

    final edgePolylines = map?.edges
            .map(
              (edge) => Polyline(
                points: edge.points.map((point) => LatLng(point.lat, point.lng)).toList(),
                strokeWidth: edge.speedLimitKph >= 60 ? 4.5 : 3.0,
                color: edge.riskScore >= 0.8
                    ? const Color(0xFFD95D39)
                    : edge.riskScore >= 0.5
                        ? const Color(0xFFF4A261)
                        : const Color(0xFF6BAA75),
              ),
            )
            .toList() ??
        const <Polyline>[];

    final hazardMarkers = map?.markers
            .map(
              (marker) => Marker(
                point: LatLng(marker.lat, marker.lng),
                width: 36,
                height: 36,
                child: const _MapPin(
                  color: Color(0xFFD95D39),
                  icon: Icons.warning_amber_rounded,
                ),
              ),
            )
            .toList() ??
        const <Marker>[];

    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Text('Map Studio', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(24),
          ),
          child: Wrap(
            spacing: 12,
            runSpacing: 12,
            children: [
              ChoiceChip(
                label: const Text('Manual draw'),
                selected: _drawMode,
                onSelected: (_) => setState(() => _drawMode = true),
              ),
              ChoiceChip(
                label: const Text('Generated route'),
                selected: !_drawMode,
                onSelected: (_) => setState(() => _drawMode = false),
              ),
              FilledButton.tonal(
                onPressed: _isLoading ? null : _loadMapStudio,
                child: const Text('Refresh map'),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        Container(
          height: 420,
          clipBehavior: Clip.antiAlias,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(28),
            boxShadow: const [
              BoxShadow(
                color: Color(0x12000000),
                blurRadius: 24,
                offset: Offset(0, 10),
              ),
            ],
          ),
          child: FlutterMap(
            mapController: _mapController,
            options: MapOptions(
              initialCenter: LatLng(map?.nodes.first.lat ?? 18.8059, map?.nodes.first.lng ?? 98.9523),
              initialZoom: 14,
              onTap: _handleMapTap,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'runna_mobile',
              ),
              if (edgePolylines.isNotEmpty) PolylineLayer(polylines: edgePolylines),
              if (selectedGeneratedPolyline.isNotEmpty)
                PolylineLayer(
                  polylines: [
                    Polyline(
                      points: selectedGeneratedPolyline,
                      strokeWidth: 6,
                      color: const Color(0xFF23402B),
                    ),
                  ],
                ),
              if (drawnPolyline.isNotEmpty)
                PolylineLayer(
                  polylines: [
                    Polyline(
                      points: drawnPolyline,
                      strokeWidth: 5,
                      color: const Color(0xFF1F7A4C),
                    ),
                  ],
                ),
              MarkerLayer(
                markers: [
                  ...hazardMarkers,
                  ..._drawnPoints.map(
                    (point) => Marker(
                      point: LatLng(point.lat, point.lng),
                      width: 24,
                      height: 24,
                      child: const _MapPin(color: Color(0xFF1F7A4C), icon: Icons.circle),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        if (_message != null)
          Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Text(_message!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
          ),
        if (_drawMode)
          _ManualDrawPanel(
            nameController: _manualRouteNameController,
            pointCount: _drawnPoints.length,
            isLoading: _isLoading,
            onClear: _clearDrawnRoute,
            onSave: _saveManualRoute,
            onDropMarker: _dropHazardMarker,
          )
        else
          _GeneratedRoutePanel(
            startController: _startController,
            distanceController: _distanceController,
            routeTypeController: _routeTypeController,
            environmentController: _environmentController,
            generatedRoutes: _generatedRoutes,
            selectedRoute: _selectedGeneratedRoute,
            isLoading: _isLoading,
            onGenerate: _generateRoute,
            onSelectRoute: (route) => setState(() => _selectedGeneratedRoute = route),
          ),
        const SizedBox(height: 16),
        Text('Saved manual routes', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 12),
        if (_manualRoutes.isEmpty)
          const Text('No manual routes saved yet.')
        else
          ..._manualRoutes.map(
            (route) => Card(
              child: ListTile(
                title: Text(route.name),
                subtitle: Text('Distance: ${route.distanceKm.toStringAsFixed(2)} km • Points: ${route.points.length}'),
              ),
            ),
          ),
      ],
    );
  }
}

class _ManualDrawPanel extends StatelessWidget {
  const _ManualDrawPanel({
    required this.nameController,
    required this.pointCount,
    required this.isLoading,
    required this.onClear,
    required this.onSave,
    required this.onDropMarker,
  });

  final TextEditingController nameController;
  final int pointCount;
  final bool isLoading;
  final VoidCallback onClear;
  final VoidCallback onSave;
  final VoidCallback onDropMarker;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Manual draw route', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          Text('Tap on the map to add route points. Use this when auto-generation is not enough.'),
          const SizedBox(height: 16),
          TextField(
            controller: nameController,
            decoration: const InputDecoration(labelText: 'Manual route name'),
          ),
          const SizedBox(height: 12),
          Text('Current points: $pointCount'),
          const SizedBox(height: 12),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: [
              FilledButton(
                onPressed: isLoading ? null : onSave,
                child: const Text('Save manual route'),
              ),
              FilledButton.tonal(
                onPressed: isLoading ? null : onDropMarker,
                child: const Text('Drop hazard marker'),
              ),
              OutlinedButton(
                onPressed: isLoading ? null : onClear,
                child: const Text('Clear points'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _GeneratedRoutePanel extends StatelessWidget {
  const _GeneratedRoutePanel({
    required this.startController,
    required this.distanceController,
    required this.routeTypeController,
    required this.environmentController,
    required this.generatedRoutes,
    required this.selectedRoute,
    required this.isLoading,
    required this.onGenerate,
    required this.onSelectRoute,
  });

  final TextEditingController startController;
  final TextEditingController distanceController;
  final TextEditingController routeTypeController;
  final TextEditingController environmentController;
  final List<RoutePlanItem> generatedRoutes;
  final RoutePlanItem? selectedRoute;
  final bool isLoading;
  final VoidCallback onGenerate;
  final ValueChanged<RoutePlanItem> onSelectRoute;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Generated route', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          Text('Generate a safer route from the road graph and compare the result on the map.'),
          const SizedBox(height: 16),
          TextField(
            controller: startController,
            decoration: const InputDecoration(labelText: 'Start location label'),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: distanceController,
                  decoration: const InputDecoration(labelText: 'Distance (km)'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: TextField(
                  controller: routeTypeController,
                  decoration: const InputDecoration(labelText: 'Route type'),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          TextField(
            controller: environmentController,
            decoration: const InputDecoration(labelText: 'Environment'),
          ),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: isLoading ? null : onGenerate,
            child: const Text('Generate route'),
          ),
          const SizedBox(height: 16),
          if (selectedRoute != null)
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFFF4EFE8),
                borderRadius: BorderRadius.circular(18),
              ),
              child: Text(
                '${selectedRoute!.summary}\nSafety: ${selectedRoute!.safetyLevel} • ETA: ${selectedRoute!.estimatedMinutes} min',
              ),
            ),
          const SizedBox(height: 16),
          if (generatedRoutes.isEmpty)
            const Text('No generated routes yet.')
          else
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: generatedRoutes.map((route) {
                final selected = selectedRoute?.id == route.id;
                return ChoiceChip(
                  label: Text('${route.targetDistanceKm.toStringAsFixed(1)} km ${route.routeType}'),
                  selected: selected,
                  onSelected: (_) => onSelectRoute(route),
                );
              }).toList(),
            ),
        ],
      ),
    );
  }
}

class _MapPin extends StatelessWidget {
  const _MapPin({
    required this.color,
    required this.icon,
  });

  final Color color;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
        boxShadow: const [
          BoxShadow(
            color: Color(0x22000000),
            blurRadius: 10,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Icon(icon, color: Colors.white, size: 16),
    );
  }
}
