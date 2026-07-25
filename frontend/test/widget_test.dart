import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/main.dart';

void main() {
  testWidgets('App builds without error', (WidgetTester tester) async {
    await tester.pumpWidget(const AiPhotoApp());
    expect(find.byType(AiPhotoApp), findsOneWidget);
  });
}
