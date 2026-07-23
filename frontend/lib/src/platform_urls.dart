import 'package:flutter/foundation.dart';

class AppUrls {
  static String get host {
    if (kIsWeb) return '127.0.0.1';
    if (defaultTargetPlatform == TargetPlatform.android) {
      return 'localhost'; // adb reverse maps localhost→host machine
    }
    return '127.0.0.1';
  }

  static String get uiBase => 'http://$host:5173';
  static String get apiBase => 'http://$host:8000';

  static String get appUrl =>
      '$uiBase/?api=${Uri.encodeComponent(apiBase)}';
}
