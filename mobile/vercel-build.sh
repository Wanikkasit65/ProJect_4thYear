#!/bin/bash
set -e

echo "Cloning Flutter SDK..."
git clone https://github.com/flutter/flutter.git -b stable --depth 1
export PATH="$PATH:`pwd`/flutter/bin"

echo "Running flutter doctor..."
flutter doctor

echo "Getting dependencies..."
flutter pub get

echo "Building web..."
flutter build web --release --dart-define=API_BASE_URL=https://runna-backend.onrender.com/api