import 'package:flutter/material.dart';

import '../../core/models.dart';
import '../auth/auth_controller.dart';

class RunsScreen extends StatefulWidget {
  const RunsScreen({super.key, required this.controller});

  final AuthController controller;

  @override
  State<RunsScreen> createState() => _RunsScreenState();
}

class _RunsScreenState extends State<RunsScreen> {
  List<RunItem> _runs = const [];
  RunItem? _activeRun;
  String? _message;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadRuns();
  }

  Future<void> _loadRuns() async {
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      final runs = await widget.controller.getRuns();
      if (!mounted) return;
      setState(() {
        _runs = runs;
        _activeRun = runs.where((run) => run.status == 'active').cast<RunItem?>().firstWhere(
              (run) => run != null,
              orElse: () => null,
            );
      });
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

  Future<void> _startRun() async {
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      final run = await widget.controller.startRun(notes: 'Started from prototype UI');
      if (!mounted) return;
      setState(() {
        _activeRun = run;
      });
      await _loadRuns();
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

  Future<void> _finishRun() async {
    final activeRun = _activeRun;
    if (activeRun == null) return;
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      await widget.controller.finishRun(
        runId: activeRun.id,
        distanceKm: 5.0,
        durationSeconds: 1800,
      );
      await _loadRuns();
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
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Text('Runs', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(_activeRun == null ? 'No active run' : 'Active run #${_activeRun!.id}'),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: FilledButton(
                      onPressed: _isLoading || _activeRun != null ? null : _startRun,
                      child: const Text('Start run'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: FilledButton.tonal(
                      onPressed: _isLoading || _activeRun == null ? null : _finishRun,
                      child: const Text('Finish run'),
                    ),
                  ),
                ],
              ),
              if (_message != null) ...[
                const SizedBox(height: 12),
                Text(_message!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
              ],
            ],
          ),
        ),
        const SizedBox(height: 20),
        FilledButton.tonal(
          onPressed: _isLoading ? null : _loadRuns,
          child: const Text('Refresh runs'),
        ),
        const SizedBox(height: 16),
        if (_runs.isEmpty)
          const Text('No runs yet.')
        else
          ..._runs.map(
            (run) => Card(
              child: ListTile(
                title: Text('Run #${run.id}'),
                subtitle: Text(
                  'Status: ${run.status}\nDistance: ${run.distanceKm.toStringAsFixed(2)} km\nDuration: ${run.durationSeconds}s',
                ),
                isThreeLine: true,
              ),
            ),
          ),
      ],
    );
  }
}
