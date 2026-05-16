import 'package:flutter/material.dart';

import '../../core/models.dart';
import '../../core/runna_api.dart';
import 'auth_controller.dart';

class AuthScreen extends StatefulWidget {
  const AuthScreen({super.key, required this.controller});

  final AuthController controller;

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  final _loginFormKey = GlobalKey<FormState>();
  final _registerFormKey = GlobalKey<FormState>();
  final _loginIdentifierController = TextEditingController();
  final _loginPasswordController = TextEditingController();
  final _registerFirstNameController = TextEditingController();
  final _registerLastNameController = TextEditingController();
  final _registerUsernameController = TextEditingController();
  final _registerEmailController = TextEditingController();
  final _registerPasswordController = TextEditingController();

  HealthResponse? _health;
  UserProfile? _user;
  String? _message;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadHealth();
  }

  @override
  void dispose() {
    _loginIdentifierController.dispose();
    _loginPasswordController.dispose();
    _registerFirstNameController.dispose();
    _registerLastNameController.dispose();
    _registerUsernameController.dispose();
    _registerEmailController.dispose();
    _registerPasswordController.dispose();
    super.dispose();
  }

  Future<void> _loadHealth() async {
    try {
      final health = await widget.controller.getHealth();
      if (!mounted) return;
      setState(() {
        _health = health;
        _message = null;
      });
    } catch (error) {
      if (!mounted) return;
      setState(() {
        _message = 'Health check failed: $error';
      });
    }
  }

  Future<void> _handleLogin() async {
    if (!_loginFormKey.currentState!.validate()) return;
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      final user = await widget.controller.login(
        usernameOrEmail: _loginIdentifierController.text.trim(),
        password: _loginPasswordController.text,
      );
      if (!mounted) return;
      setState(() {
        _user = user;
      });
    } on RunnaApiException catch (error) {
      if (!mounted) return;
      setState(() {
        _message = error.message;
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _handleRegister() async {
    if (!_registerFormKey.currentState!.validate()) return;
    setState(() {
      _isLoading = true;
      _message = null;
    });
    try {
      final user = await widget.controller.register(
        firstName: _registerFirstNameController.text.trim(),
        lastName: _registerLastNameController.text.trim(),
        username: _registerUsernameController.text.trim(),
        email: _registerEmailController.text.trim(),
        password: _registerPasswordController.text,
      );
      if (!mounted) return;
      setState(() {
        _user = user;
        _message = 'Registration successful. You can log in now.';
      });
    } on RunnaApiException catch (error) {
      if (!mounted) return;
      setState(() {
        _message = error.message;
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
    final colorScheme = Theme.of(context).colorScheme;
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        backgroundColor: const Color(0xFFF4EFE8),
        appBar: AppBar(
          title: const Text('Runna'),
          backgroundColor: const Color(0xFF23402B),
          foregroundColor: Colors.white,
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Login'),
              Tab(text: 'Register'),
            ],
          ),
        ),
        body: SafeArea(
          child: ListView(
            padding: const EdgeInsets.all(20),
            children: [
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(18),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Backend status',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 8),
                    Text(_health?.status ?? 'Checking...'),
                    if (_user != null) ...[
                      const SizedBox(height: 16),
                      Text(
                        'Active member: ${_user!.firstName} ${_user!.lastName}',
                        style: TextStyle(
                          color: colorScheme.primary,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      Text('@${_user!.username}'),
                    ],
                    if (_message != null) ...[
                      const SizedBox(height: 12),
                      Text(
                        _message!,
                        style: TextStyle(color: colorScheme.error),
                      ),
                    ],
                  ],
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(
                height: 520,
                child: TabBarView(
                  children: [
                    _AuthCard(
                      title: 'Welcome back',
                      subtitle: 'Sign in to the first Runna build.',
                      child: Form(
                        key: _loginFormKey,
                        child: Column(
                          children: [
                            _FormField(
                              controller: _loginIdentifierController,
                              label: 'Username or email',
                            ),
                            const SizedBox(height: 12),
                            _FormField(
                              controller: _loginPasswordController,
                              label: 'Password',
                              obscureText: true,
                            ),
                            const SizedBox(height: 20),
                            _PrimaryButton(
                              label: _isLoading ? 'Signing in...' : 'Sign in',
                              onPressed: _isLoading ? null : _handleLogin,
                            ),
                          ],
                        ),
                      ),
                    ),
                    _AuthCard(
                      title: 'Create account',
                      subtitle: 'Set up the first member profile for Runna.',
                      child: Form(
                        key: _registerFormKey,
                        child: Column(
                          children: [
                            _FormField(
                              controller: _registerFirstNameController,
                              label: 'First name',
                            ),
                            const SizedBox(height: 12),
                            _FormField(
                              controller: _registerLastNameController,
                              label: 'Last name',
                            ),
                            const SizedBox(height: 12),
                            _FormField(
                              controller: _registerUsernameController,
                              label: 'Username',
                            ),
                            const SizedBox(height: 12),
                            _FormField(
                              controller: _registerEmailController,
                              label: 'Email',
                            ),
                            const SizedBox(height: 12),
                            _FormField(
                              controller: _registerPasswordController,
                              label: 'Password',
                              obscureText: true,
                            ),
                            const SizedBox(height: 20),
                            _PrimaryButton(
                              label: _isLoading ? 'Creating...' : 'Create account',
                              onPressed: _isLoading ? null : _handleRegister,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _AuthCard extends StatelessWidget {
  const _AuthCard({
    required this.title,
    required this.subtitle,
    required this.child,
  });

  final String title;
  final String subtitle;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
      ),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 8),
            Text(subtitle),
            const SizedBox(height: 20),
            child,
          ],
        ),
      ),
    );
  }
}

class _FormField extends StatelessWidget {
  const _FormField({
    required this.controller,
    required this.label,
    this.obscureText = false,
  });

  final TextEditingController controller;
  final String label;
  final bool obscureText;

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      obscureText: obscureText,
      validator: (value) {
        if (value == null || value.trim().isEmpty) {
          return '$label is required';
        }
        return null;
      },
      decoration: InputDecoration(
        labelText: label,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(16)),
      ),
    );
  }
}

class _PrimaryButton extends StatelessWidget {
  const _PrimaryButton({
    required this.label,
    required this.onPressed,
  });

  final String label;
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: FilledButton(
        onPressed: onPressed,
        style: FilledButton.styleFrom(
          backgroundColor: const Color(0xFF23402B),
          padding: const EdgeInsets.symmetric(vertical: 16),
        ),
        child: Text(label),
      ),
    );
  }
}
