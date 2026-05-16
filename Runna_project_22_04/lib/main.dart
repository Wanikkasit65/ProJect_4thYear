import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(RunnaApp());
}

class RunnaApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Runna AI Coach',
      home: RunTestScreen(),
    );
  }
}

class RunTestScreen extends StatefulWidget {
  @override
  _RunTestScreenState createState() => _RunTestScreenState();
}

class _RunTestScreenState extends State<RunTestScreen> {
  String _result = '';
  bool _loading = false;

  final double lat = 18.7883;
  final double lng = 98.9853;
  final double distance = 5.0;
  final String pace = '5:45';
  final int steps = 5200;

  Future<void> testAI() async {
    setState(() {
      _loading = true;
      _result = 'Loading...';
    });

    try {
      final response = await http.post(
Uri.parse('http://localhost:8000/ai-summary'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'lat': lat,
          'lng': lng,
          'distance': distance,
          'pace': pace,
          'steps': steps,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _result = 'Location: ${data['locationName']}\nAI Coach: ${data['aiSummary']}';
        });
      } else {
        setState(() {
          _result = 'Error: ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _result = 'Network error: $e';
      });
    }

    setState(() {
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Runna AI Test')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
Text('Athlete Intelligence Test', style: Theme.of(context).textTheme.headlineSmall),
            SizedBox(height: 20),
            Text('lat: $lat, lng: $lng', style: TextStyle(fontSize: 16)),
            Text('Distance: $distance km, Pace: $pace, Steps: $steps', style: TextStyle(fontSize: 16)),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _loading ? null : testAI,
              child: _loading ? CircularProgressIndicator() : Text('Test AI Coach'),
            ),
            SizedBox(height: 20),
            Expanded(
              child: SingleChildScrollView(
                child: Container(
                  padding: EdgeInsets.all(16),
                  color: Colors.grey[100],
                  child: Text(_result, style: TextStyle(fontSize: 16)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

