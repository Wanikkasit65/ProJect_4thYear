import 'package:flutter/material.dart';

import 'features/auth/auth_controller.dart';
import 'features/auth/auth_screen.dart';
import 'features/routes/routes_screen.dart';
import 'features/runs/runs_screen.dart';

void main() {
  runApp(const RunnaApp());
}

class RunnaApp extends StatefulWidget {
  const RunnaApp({super.key});

  @override
  State<RunnaApp> createState() => _RunnaAppState();
}

class _RunnaAppState extends State<RunnaApp> {
  late final AuthController _controller;
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    _controller = AuthController()..addListener(_handleControllerUpdate);
  }

  @override
  void dispose() {
    _controller.removeListener(_handleControllerUpdate);
    _controller.dispose();
    super.dispose();
  }

  void _handleControllerUpdate() {
    if (mounted) {
      setState(() {});
    }
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: const Color(0xFF23402B),
      brightness: Brightness.light,
    );

    final pages = [
      AuthScreen(controller: _controller),
      RoutesScreen(controller: _controller),
      RunsScreen(controller: _controller),
    ];

    return MaterialApp(
      title: 'Runna',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: colorScheme,
        scaffoldBackgroundColor: const Color(0xFFF4EFE8),
        useMaterial3: true,
      ),
      home: Scaffold(
        body: SafeArea(child: pages[_currentIndex]),
        bottomNavigationBar: NavigationBar(
          selectedIndex: _currentIndex,
          onDestinationSelected: (index) => setState(() => _currentIndex = index),
          destinations: const [
            NavigationDestination(icon: Icon(Icons.person_outline), label: 'Account'),
            NavigationDestination(icon: Icon(Icons.map_outlined), label: 'Map Studio'),
            NavigationDestination(icon: Icon(Icons.directions_run_outlined), label: 'Runs'),
          ],
        ),
      ),
    );
  }
}
