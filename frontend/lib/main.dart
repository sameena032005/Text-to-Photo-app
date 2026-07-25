import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:share_plus/share_plus.dart';
import 'package:webview_flutter/webview_flutter.dart';

import 'src/platform_urls.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const AiPhotoApp());
}

class AiPhotoApp extends StatelessWidget {
  const AiPhotoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Photo Generator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF7C3AED),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const WebAppShell(),
    );
  }
}

class WebAppShell extends StatefulWidget {
  const WebAppShell({super.key});

  @override
  State<WebAppShell> createState() => _WebAppShellState();
}

class _WebAppShellState extends State<WebAppShell> {
  late final WebViewController _controller;
  bool _loading = true;
  String _error = '';
  bool _actionInProgress = false;

  @override
  void initState() {
    super.initState();

    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0xFF0A0A0F))
      ..setNavigationDelegate(NavigationDelegate(
        onPageStarted: (_) => setState(() {
          _loading = true;
          _error = '';
        }),
        onPageFinished: (_) => setState(() => _loading = false),
        onWebResourceError: (err) => setState(() {
          _loading = false;
          _error = err.description;
        }),
      ))

      // ── JS Channel: Download image ─────────────────────────────────────────
      ..addJavaScriptChannel(
        'FlutterDownload',
        onMessageReceived: (msg) => _handleDownload(msg.message),
      )

      // ── JS Channel: Share image ────────────────────────────────────────────
      ..addJavaScriptChannel(
        'FlutterShare',
        onMessageReceived: (msg) => _handleShare(msg.message),
      )

      // ── JS Channel: Toast / snackbar messages from React ──────────────────
      ..addJavaScriptChannel(
        'FlutterToast',
        onMessageReceived: (msg) => _showSnackbar(msg.message),
      )

      ..loadRequest(Uri.parse(AppUrls.appUrl));
  }

  // ── Download handler ───────────────────────────────────────────────────────
  Future<void> _handleDownload(String imageUrl) async {
    if (_actionInProgress) return;
    setState(() => _actionInProgress = true);

    try {
      _showSnackbar('Starting download...');

      // Request permission
      PermissionStatus status = await Permission.storage.request();
      if (!status.isGranted) {
        // Android 13+ uses media permissions
        status = await Permission.photos.request();
      }

      if (!status.isGranted) {
        _showSnackbar('Storage permission denied. Please allow in Settings.');
        return;
      }

      // Get downloads directory
      Directory? saveDir;
      if (Platform.isAndroid) {
        // Save to Pictures/AIPhotoGenerator on Android
        saveDir = Directory('/storage/emulated/0/Pictures/AIPhotoGenerator');
        if (!await saveDir.exists()) {
          await saveDir.create(recursive: true);
        }
      } else {
        saveDir = await getApplicationDocumentsDirectory();
      }

      final fileName = 'ai_photo_${DateTime.now().millisecondsSinceEpoch}.png';
      final filePath = '${saveDir.path}/$fileName';

      // Download using Dio
      await Dio().download(imageUrl, filePath,
        onReceiveProgress: (received, total) {
          // Progress is silent — snackbar shown on completion
        },
      );

      _showSnackbar('✅ Saved to Pictures/AIPhotoGenerator/$fileName');
    } catch (e) {
      _showSnackbar('Download failed: ${e.toString()}');
    } finally {
      setState(() => _actionInProgress = false);
    }
  }

  // ── Share handler ──────────────────────────────────────────────────────────
  Future<void> _handleShare(String imageUrl) async {
    if (_actionInProgress) return;
    setState(() => _actionInProgress = true);

    try {
      _showSnackbar('Preparing to share...');

      // Download image to temp directory first
      final tempDir = await getTemporaryDirectory();
      final fileName = 'ai_photo_share_${DateTime.now().millisecondsSinceEpoch}.png';
      final filePath = '${tempDir.path}/$fileName';

      await Dio().download(imageUrl, filePath);

      final xFile = XFile(filePath, mimeType: 'image/png');

      // Open native share sheet — shows ALL share options (WhatsApp, Gmail,
      // Instagram, Telegram, Bluetooth, Copy, Save to Drive, etc.)
      await Share.shareXFiles(
        [xFile],
        text: 'Check out this AI generated photo! 🎨',
        subject: 'AI Photo Generator',
      );
    } catch (e) {
      _showSnackbar('Share failed: ${e.toString()}');
    } finally {
      setState(() => _actionInProgress = false);
    }
  }

  // ── Snackbar helper ────────────────────────────────────────────────────────
  void _showSnackbar(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: const Color(0xFF1E1B4B),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        duration: const Duration(seconds: 3),
      ),
    );
  }

  void _reload() => _controller.loadRequest(Uri.parse(AppUrls.appUrl));

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0F),
      appBar: AppBar(
        title: const Text('AI Photo Generator'),
        backgroundColor: const Color(0xFF12121A),
        actions: [
          if (_actionInProgress)
            const Padding(
              padding: EdgeInsets.only(right: 16),
              child: Center(
                child: SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: Color(0xFF8B5CF6),
                  ),
                ),
              ),
            ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _reload,
            tooltip: 'Reload',
          ),
        ],
      ),
      body: Stack(
        children: [
          WebViewWidget(controller: _controller),
          if (_loading)
            const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(color: Color(0xFF8B5CF6)),
                  SizedBox(height: 16),
                  Text('Loading AI Photo Studio...',
                      style: TextStyle(color: Colors.white70)),
                  SizedBox(height: 8),
                  Text('Ensure React UI (port 5173) is running',
                      style: TextStyle(color: Colors.white38, fontSize: 12)),
                ],
              ),
            ),
          if (_error.isNotEmpty && !_loading)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.cloud_off,
                        color: Colors.redAccent, size: 48),
                    const SizedBox(height: 16),
                    Text('Cannot reach UI at ${AppUrls.uiBase}',
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: Colors.white)),
                    const SizedBox(height: 8),
                    Text(_error,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                            color: Colors.white54, fontSize: 12)),
                    const SizedBox(height: 16),
                    const Text('Run START_ALL.bat or start-frontend.bat first.',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                            color: Colors.white38, fontSize: 12)),
                    const SizedBox(height: 24),
                    FilledButton.icon(
                      onPressed: _reload,
                      icon: const Icon(Icons.refresh),
                      label: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
