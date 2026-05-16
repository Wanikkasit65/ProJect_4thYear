# Runna Mobile

Flutter app for the Runna project.

## Current status

This first implementation pass includes:

- real Flutter project scaffolding
- backend health check integration
- registration screen
- login screen
- profile fetch after login
- base map rendering
- manual route drawing
- generated route preview
- hazard marker placement

## Run locally

```powershell
flutter pub get
flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:8000/api
```

## Notes

- Android tooling is not installed yet, so Android builds are not verified in this session.
- The app now targets GIS routing flows rather than social/chat features.
