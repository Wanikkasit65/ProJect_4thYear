import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:runna_mobile/core/models.dart';
import 'package:runna_mobile/features/auth/auth_controller.dart';
import 'package:runna_mobile/features/auth/auth_screen.dart';

void main() {
  testWidgets('Runna app renders', (tester) async {
    await tester.pumpWidget(_testApp());

    expect(find.text('Runna'), findsOneWidget);
    expect(find.text('Login'), findsOneWidget);
    expect(find.text('Register'), findsOneWidget);
  });
}

class _FakeAuthController extends AuthController {
  @override
  Future<HealthResponse> getHealth() async => const HealthResponse(status: 'ok');
}

Widget _testApp() {
  return MaterialApp(
    home: AuthScreen(controller: _FakeAuthController()),
  );
}
