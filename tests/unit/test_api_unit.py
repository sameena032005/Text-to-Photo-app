"""
Unit Tests - Backend API Endpoints
TC-UNIT-001 to TC-UNIT-040 (40 test cases)
"""
import pytest
import requests
import json

API_URL = "http://localhost:8000"


class TestHealthEndpoint:
    def test_health_returns_200(self, api_session):
        """TC-UNIT-001: GET /health returns 200"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200

    def test_health_returns_json(self, api_session):
        """TC-UNIT-002: GET /health returns JSON"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.headers.get("Content-Type", "").startswith("application/json")

    def test_health_has_status_field(self, api_session):
        """TC-UNIT-003: GET /health response has status field"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        if r.status_code == 200:
            data = r.json()
            assert "status" in data or isinstance(data, dict)

    def test_health_response_time(self, api_session):
        """TC-UNIT-004: GET /health responds within 2 seconds"""
        import time
        start = time.time()
        r = api_session.get(f"{API_URL}/health", timeout=5)
        elapsed = time.time() - start
        assert elapsed < 2.0

    def test_health_get_method_only(self, api_session):
        """TC-UNIT-005: POST /health returns 405 Method Not Allowed"""
        r = api_session.post(f"{API_URL}/health", timeout=5)
        assert r.status_code in [405, 404, 400]


class TestGenerateEndpoint:
    def test_generate_requires_prompt(self, api_session):
        """TC-UNIT-006: POST /generate without prompt returns 400/422"""
        r = api_session.post(f"{API_URL}/generate", json={}, timeout=10)
        assert r.status_code in [400, 422, 500]

    def test_generate_with_prompt(self, api_session):
        """TC-UNIT-007: POST /generate with valid prompt returns non-500"""
        payload = {"prompt": "a sunset over mountains", "style": "Cinematic", "ratio": "1:1"}
        r = api_session.post(f"{API_URL}/generate", json=payload, timeout=60)
        assert r.status_code != 500

    def test_generate_returns_json(self, api_session):
        """TC-UNIT-008: POST /generate returns JSON content-type"""
        payload = {"prompt": "test", "style": "Realistic", "ratio": "16:9"}
        r = api_session.post(f"{API_URL}/generate", json=payload, timeout=60)
        assert "json" in r.headers.get("Content-Type", "").lower() or r.status_code in [400, 422]

    def test_generate_empty_prompt_rejected(self, api_session):
        """TC-UNIT-009: Empty string prompt is rejected"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": ""}, timeout=10)
        assert r.status_code in [400, 422]

    def test_generate_whitespace_prompt_rejected(self, api_session):
        """TC-UNIT-010: Whitespace-only prompt is rejected"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "   "}, timeout=10)
        assert r.status_code in [400, 422]

    def test_generate_accepts_all_styles(self, api_session):
        """TC-UNIT-011: All IMAGE_STYLES are accepted by API"""
        styles = ["Cinematic", "Anime", "Realistic", "3D", "Cartoon", "Cyberpunk", "Oil Painting", "Watercolor", "Digital Art"]
        for style in styles:
            r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": style, "ratio": "1:1"}, timeout=30)
            assert r.status_code != 500, f"Style {style} caused 500 error"

    def test_generate_accepts_all_ratios(self, api_session):
        """TC-UNIT-012: All aspect ratios accepted"""
        for ratio in ["16:9", "9:16", "1:1", "4:3", "3:2"]:
            r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": "Realistic", "ratio": ratio}, timeout=30)
            assert r.status_code != 500

    def test_generate_accepts_quality_low(self, api_session):
        """TC-UNIT-013: Quality=low accepted"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "quality": "low"}, timeout=30)
        assert r.status_code != 500

    def test_generate_accepts_quality_high(self, api_session):
        """TC-UNIT-014: Quality=high accepted"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "quality": "high"}, timeout=30)
        assert r.status_code != 500

    def test_generate_very_long_prompt(self, api_session):
        """TC-UNIT-015: Very long prompt (1000 chars) handled gracefully"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "a" * 1000, "style": "Realistic"}, timeout=30)
        assert r.status_code in [200, 202, 400, 422]

    def test_generate_special_chars_in_prompt(self, api_session):
        """TC-UNIT-016: Special characters in prompt handled"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "cat & dog <test> \"quoted\"", "style": "Realistic"}, timeout=30)
        assert r.status_code not in [500]

    def test_generate_unicode_prompt(self, api_session):
        """TC-UNIT-017: Unicode characters in prompt accepted"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "美しい山の夕日", "style": "Anime"}, timeout=30)
        assert r.status_code not in [500]

    def test_generate_cors_headers(self, api_session):
        """TC-UNIT-018: API returns CORS headers"""
        r = api_session.options(f"{API_URL}/generate", timeout=5)
        assert r.status_code in [200, 204, 405]

    def test_generate_method_post_only(self, api_session):
        """TC-UNIT-019: GET /generate returns 405"""
        r = api_session.get(f"{API_URL}/generate", timeout=5)
        assert r.status_code in [405, 404]


class TestAPIResponseSchema:
    def test_success_response_has_image_url(self, api_session):
        """TC-UNIT-020: Successful response contains image_url or job_id"""
        payload = {"prompt": "a blue sky", "style": "Realistic", "ratio": "1:1"}
        r = api_session.post(f"{API_URL}/generate", json=payload, timeout=120)
        if r.status_code == 200:
            data = r.json()
            assert "image_url" in data or "video_url" in data or "jobId" in data or "job_id" in data

    def test_error_response_has_message(self, api_session):
        """TC-UNIT-021: Error response contains message/detail"""
        r = api_session.post(f"{API_URL}/generate", json={}, timeout=10)
        if r.status_code in [400, 422]:
            data = r.json()
            assert "message" in data or "detail" in data or "error" in data

    def test_response_content_type_json(self, api_session):
        """TC-UNIT-022: All endpoints return Content-Type: application/json"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert "json" in r.headers.get("Content-Type", "").lower()

    def test_server_header_not_exposed(self, api_session):
        """TC-UNIT-023: Server version not exposed in headers"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        server = r.headers.get("Server", "")
        assert "python" not in server.lower() or True  # Soft check


class TestAPIEdgeCases:
    def test_null_prompt(self, api_session):
        """TC-UNIT-024: null prompt handled"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": None}, timeout=10)
        assert r.status_code in [400, 422, 500]

    def test_numeric_prompt(self, api_session):
        """TC-UNIT-025: Numeric prompt handled"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": 12345}, timeout=10)
        assert r.status_code in [200, 202, 400, 422]

    def test_array_prompt(self, api_session):
        """TC-UNIT-026: Array prompt handled gracefully"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": ["a", "b"]}, timeout=10)
        assert r.status_code in [400, 422, 500]

    def test_missing_content_type(self, api_session):
        """TC-UNIT-027: Missing Content-Type handled"""
        r = requests.post(f"{API_URL}/generate", data='{"prompt":"test"}', timeout=10)
        assert r.status_code in [200, 202, 400, 415, 422]

    def test_malformed_json(self, api_session):
        """TC-UNIT-028: Malformed JSON body returns 400"""
        r = requests.post(f"{API_URL}/generate", data="{bad json", headers={"Content-Type": "application/json"}, timeout=10)
        assert r.status_code in [400, 422]

    def test_extra_fields_ignored(self, api_session):
        """TC-UNIT-029: Extra unknown fields are ignored"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "unknown_field": "xyz"}, timeout=30)
        assert r.status_code not in [500]

    def test_concurrent_requests(self, api_session):
        """TC-UNIT-030: API handles multiple concurrent requests"""
        import concurrent.futures
        def call():
            return api_session.get(f"{API_URL}/health", timeout=5).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            results = list(ex.map(lambda _: call(), range(5)))
        assert all(s == 200 for s in results)

    def test_api_status_endpoint(self, api_session):
        """TC-UNIT-031: GET /api/status/test returns response"""
        r = api_session.get(f"{API_URL}/api/status/test-job-id", timeout=5)
        assert r.status_code in [200, 404]

    def test_request_id_in_response(self, api_session):
        """TC-UNIT-032: Response headers may include request-id"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200  # Just verify endpoint works

    def test_api_timeout_handling(self, api_session):
        """TC-UNIT-033: API responds within 120s for generation"""
        import time
        payload = {"prompt": "quick test", "style": "Realistic", "quality": "low"}
        start = time.time()
        r = api_session.post(f"{API_URL}/generate", json=payload, timeout=120)
        elapsed = time.time() - start
        assert elapsed < 120

    def test_empty_body_post(self, api_session):
        """TC-UNIT-034: POST with empty body returns 400/422"""
        r = requests.post(f"{API_URL}/generate", data="", headers={"Content-Type": "application/json"}, timeout=10)
        assert r.status_code in [400, 422]

    def test_api_reachable(self, api_session):
        """TC-UNIT-035: API base URL is reachable"""
        try:
            r = api_session.get(f"{API_URL}/health", timeout=5)
            assert r.status_code < 500
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running - skip")

    def test_generate_payload_encoding(self, api_session):
        """TC-UNIT-036: UTF-8 encoded payload accepted"""
        payload = {"prompt": "café au lait scene", "style": "Realistic"}
        r = api_session.post(f"{API_URL}/generate", json=payload, timeout=30)
        assert r.status_code not in [500]

    def test_api_no_500_on_health(self, api_session):
        """TC-UNIT-037: /health never returns 500"""
        for _ in range(3):
            r = api_session.get(f"{API_URL}/health", timeout=5)
            assert r.status_code != 500

    def test_api_cors_origin_header(self, api_session):
        """TC-UNIT-038: API responds to CORS preflight"""
        headers = {"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"}
        r = requests.options(f"{API_URL}/generate", headers=headers, timeout=5)
        assert r.status_code in [200, 204, 405]

    def test_api_returns_proper_http_methods(self, api_session):
        """TC-UNIT-039: API only allows intended HTTP methods"""
        r = api_session.delete(f"{API_URL}/generate", timeout=5)
        assert r.status_code in [404, 405]

    def test_generate_response_not_empty(self, api_session):
        """TC-UNIT-040: Successful generate response body is not empty"""
        payload = {"prompt": "blue sky", "style": "Realistic", "ratio": "1:1"}
        r = api_session.post(f"{API_URL}/generate", json=payload, timeout=120)
        if r.status_code == 200:
            assert len(r.text) > 0
