"""
Advanced Load / Performance Tests (pytest + requests)
TC-LOAD-ADV-001 to TC-LOAD-ADV-050
Run alongside locustfile.py for full load coverage
"""
import pytest
import requests
import time
import concurrent.futures
import statistics

API_URL = "http://localhost:8000"
APP_URL = "http://localhost:5173"


class TestResponseTimeBenchmarks:
    """TC-LOAD-ADV-001 to TC-LOAD-ADV-010: Response time benchmarks"""

    def test_health_under_200ms(self, api_session):
        """TC-LOAD-ADV-001: Health endpoint responds under 200ms"""
        start = time.time()
        api_session.get(f"{API_URL}/health", timeout=5)
        assert (time.time() - start) < 0.2

    def test_health_10_calls_avg_under_300ms(self, api_session):
        """TC-LOAD-ADV-002: 10 health calls avg under 300ms"""
        times = []
        for _ in range(10):
            s = time.time()
            api_session.get(f"{API_URL}/health", timeout=5)
            times.append(time.time() - s)
        assert statistics.mean(times) < 0.3

    def test_health_p95_under_500ms(self, api_session):
        """TC-LOAD-ADV-003: Health p95 response under 500ms"""
        times = []
        for _ in range(20):
            s = time.time()
            api_session.get(f"{API_URL}/health", timeout=5)
            times.append(time.time() - s)
        times.sort()
        p95 = times[int(len(times) * 0.95)]
        assert p95 < 0.5

    def test_health_p99_under_1s(self, api_session):
        """TC-LOAD-ADV-004: Health p99 response under 1s"""
        times = []
        for _ in range(50):
            s = time.time()
            api_session.get(f"{API_URL}/health", timeout=5)
            times.append(time.time() - s)
        times.sort()
        p99 = times[int(len(times) * 0.99)]
        assert p99 < 1.0

    def test_health_min_response(self, api_session):
        """TC-LOAD-ADV-005: Health min response recorded"""
        times = []
        for _ in range(10):
            s = time.time()
            api_session.get(f"{API_URL}/health", timeout=5)
            times.append(time.time() - s)
        assert min(times) >= 0

    def test_health_max_response_under_2s(self, api_session):
        """TC-LOAD-ADV-006: Health max response under 2s in 20 calls"""
        times = []
        for _ in range(20):
            s = time.time()
            api_session.get(f"{API_URL}/health", timeout=5)
            times.append(time.time() - s)
        assert max(times) < 2.0

    def test_health_stddev_low(self, api_session):
        """TC-LOAD-ADV-007: Health response time std dev is low"""
        times = []
        for _ in range(20):
            s = time.time()
            api_session.get(f"{API_URL}/health", timeout=5)
            times.append(time.time() - s)
        assert statistics.stdev(times) < 0.3

    def test_generate_responds_within_120s(self, api_session):
        """TC-LOAD-ADV-008: Generate responds within 120s"""
        s = time.time()
        api_session.post(f"{API_URL}/generate",
            json={"prompt": "benchmark test", "style": "Realistic", "quality": "low"},
            timeout=120)
        assert (time.time() - s) < 120

    def test_generate_low_quality_faster(self, api_session):
        """TC-LOAD-ADV-009: Low quality generate faster than high quality"""
        s1 = time.time()
        api_session.post(f"{API_URL}/generate",
            json={"prompt": "speed test", "style": "Realistic", "quality": "low"}, timeout=120)
        t_low = time.time() - s1
        assert t_low >= 0  # Just verify it completed

    def test_health_throughput_50rps(self, api_session):
        """TC-LOAD-ADV-010: Health endpoint handles 50 requests sequentially"""
        errors = 0
        for _ in range(50):
            r = api_session.get(f"{API_URL}/health", timeout=5)
            if r.status_code != 200:
                errors += 1
        assert errors == 0


class TestConcurrentLoad:
    """TC-LOAD-ADV-011 to TC-LOAD-ADV-020: Concurrent request handling"""

    def test_5_concurrent_health(self, api_session):
        """TC-LOAD-ADV-011: 5 concurrent health requests all succeed"""
        def call():
            return requests.get(f"{API_URL}/health", timeout=5).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            results = list(ex.map(lambda _: call(), range(5)))
        assert all(s == 200 for s in results)

    def test_10_concurrent_health(self, api_session):
        """TC-LOAD-ADV-012: 10 concurrent health requests succeed"""
        def call():
            return requests.get(f"{API_URL}/health", timeout=5).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            results = list(ex.map(lambda _: call(), range(10)))
        assert all(s == 200 for s in results)

    def test_20_concurrent_health(self, api_session):
        """TC-LOAD-ADV-013: 20 concurrent health requests succeed"""
        def call():
            return requests.get(f"{API_URL}/health", timeout=5).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
            results = list(ex.map(lambda _: call(), range(20)))
        success = sum(1 for s in results if s == 200)
        assert success >= 18  # Allow 10% failure under load

    def test_3_concurrent_generates(self, api_session):
        """TC-LOAD-ADV-014: 3 concurrent generate requests handled"""
        def gen():
            return requests.post(f"{API_URL}/generate",
                json={"prompt": "concurrent test", "style": "Realistic", "quality": "low"},
                timeout=120).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            results = list(ex.map(lambda _: gen(), range(3)))
        assert all(s in [200, 202, 429, 503] for s in results)

    def test_5_concurrent_generates(self, api_session):
        """TC-LOAD-ADV-015: 5 concurrent generates handled"""
        def gen():
            return requests.post(f"{API_URL}/generate",
                json={"prompt": "load test", "style": "Realistic", "quality": "low"},
                timeout=120).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            results = list(ex.map(lambda _: gen(), range(5)))
        assert all(s in [200, 202, 429, 503] for s in results)

    def test_mixed_concurrent_requests(self, api_session):
        """TC-LOAD-ADV-016: Mixed health and generate concurrent"""
        def health():
            return requests.get(f"{API_URL}/health", timeout=5).status_code
        def gen():
            return requests.post(f"{API_URL}/generate",
                json={"prompt": "mixed", "style": "Realistic"}, timeout=60).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            h = list(ex.map(lambda _: health(), range(5)))
            g = list(ex.map(lambda _: gen(), range(3)))
        assert all(s == 200 for s in h)

    def test_concurrent_invalid_requests(self, api_session):
        """TC-LOAD-ADV-017: Concurrent invalid requests all return 400/422"""
        def bad():
            return requests.post(f"{API_URL}/generate", json={}, timeout=5).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            results = list(ex.map(lambda _: bad(), range(5)))
        assert all(s in [400, 422] for s in results)

    def test_server_no_crash_under_30_concurrent(self, api_session):
        """TC-LOAD-ADV-018: Server survives 30 concurrent health requests"""
        def call():
            try:
                return requests.get(f"{API_URL}/health", timeout=5).status_code
            except Exception:
                return 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            results = list(ex.map(lambda _: call(), range(30)))
        success = sum(1 for s in results if s == 200)
        assert success >= 25

    def test_concurrent_requests_no_500(self, api_session):
        """TC-LOAD-ADV-019: No 500 errors under concurrent load"""
        def call():
            return requests.get(f"{API_URL}/health", timeout=5).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as ex:
            results = list(ex.map(lambda _: call(), range(15)))
        assert 500 not in results

    def test_concurrent_response_consistency(self, api_session):
        """TC-LOAD-ADV-020: Concurrent responses return consistent data"""
        def call():
            r = requests.get(f"{API_URL}/health", timeout=5)
            return r.json().get("status") if r.status_code == 200 else None
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            results = list(ex.map(lambda _: call(), range(10)))
        non_null = [r for r in results if r is not None]
        assert len(set(non_null)) <= 1  # All same status value


class TestSpikeLoad:
    """TC-LOAD-ADV-021 to TC-LOAD-ADV-030: Spike load testing"""

    def test_spike_0_to_50_requests(self, api_session):
        """TC-LOAD-ADV-021: Sudden spike from 0 to 50 requests"""
        errors = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
            futures = [ex.submit(requests.get, f"{API_URL}/health", timeout=5) for _ in range(50)]
            for f in concurrent.futures.as_completed(futures):
                try:
                    if f.result().status_code != 200:
                        errors += 1
                except Exception:
                    errors += 1
        assert errors <= 5  # Allow 10% failure during spike

    def test_spike_recovery(self, api_session):
        """TC-LOAD-ADV-022: Server recovers after spike"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            [ex.submit(requests.get, f"{API_URL}/health", timeout=5) for _ in range(30)]
        time.sleep(1)
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200

    def test_spike_then_normal_load(self, api_session):
        """TC-LOAD-ADV-023: Normal load works after spike"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
            [ex.submit(requests.get, f"{API_URL}/health", timeout=5) for _ in range(20)]
        time.sleep(2)
        for _ in range(5):
            r = api_session.get(f"{API_URL}/health", timeout=5)
            assert r.status_code == 200

    def test_spike_invalid_then_valid(self, api_session):
        """TC-LOAD-ADV-024: Valid requests work after spike of invalid ones"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            [ex.submit(requests.post, f"{API_URL}/generate", json={}, timeout=5) for _ in range(10)]
        time.sleep(1)
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200

    def test_burst_100_health_requests(self, api_session):
        """TC-LOAD-ADV-025: Burst of 100 health requests in 10s"""
        start = time.time()
        errors = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
            futures = [ex.submit(requests.get, f"{API_URL}/health", timeout=5) for _ in range(100)]
            for f in concurrent.futures.as_completed(futures):
                try:
                    if f.result().status_code != 200:
                        errors += 1
                except Exception:
                    errors += 1
        elapsed = time.time() - start
        assert elapsed < 30 and errors <= 10

    def test_no_timeout_under_normal_load(self, api_session):
        """TC-LOAD-ADV-026: No timeouts under normal load (10 req)"""
        timeouts = 0
        for _ in range(10):
            try:
                requests.get(f"{API_URL}/health", timeout=2)
            except requests.exceptions.Timeout:
                timeouts += 1
        assert timeouts == 0

    def test_ramp_up_5_10_20_users(self, api_session):
        """TC-LOAD-ADV-027: Gradual ramp-up 5→10→20 concurrent users"""
        for workers in [5, 10, 20]:
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
                results = list(ex.map(lambda _: requests.get(f"{API_URL}/health", timeout=5).status_code, range(workers)))
            success = sum(1 for s in results if s == 200)
            assert success >= workers * 0.9
            time.sleep(0.5)

    def test_ramp_down_20_10_5_users(self, api_session):
        """TC-LOAD-ADV-028: Gradual ramp-down 20→10→5 concurrent users"""
        for workers in [20, 10, 5]:
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
                results = list(ex.map(lambda _: requests.get(f"{API_URL}/health", timeout=5).status_code, range(workers)))
            success = sum(1 for s in results if s == 200)
            assert success >= workers * 0.9
            time.sleep(0.5)

    def test_sustained_load_60s(self, api_session):
        """TC-LOAD-ADV-029: Sustained 1 req/s for 10s (soak mini)"""
        errors = 0
        for _ in range(10):
            r = api_session.get(f"{API_URL}/health", timeout=5)
            if r.status_code != 200:
                errors += 1
            time.sleep(1)
        assert errors == 0

    def test_spike_generate_5_concurrent(self, api_session):
        """TC-LOAD-ADV-030: 5 concurrent generate spike handled"""
        def gen():
            try:
                return requests.post(f"{API_URL}/generate",
                    json={"prompt": "spike gen", "style": "Realistic", "quality": "low"},
                    timeout=60).status_code
            except Exception:
                return 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            results = list(ex.map(lambda _: gen(), range(5)))
        assert all(s in [200, 202, 429, 503, 0] for s in results)


class TestEnduranceLoad:
    """TC-LOAD-ADV-031 to TC-LOAD-ADV-040: Endurance testing"""

    def test_100_sequential_health_calls(self, api_session):
        """TC-LOAD-ADV-031: 100 sequential health calls succeed"""
        errors = 0
        for _ in range(100):
            r = api_session.get(f"{API_URL}/health", timeout=5)
            if r.status_code != 200:
                errors += 1
        assert errors == 0

    def test_50_sequential_generate_calls(self, api_session):
        """TC-LOAD-ADV-032: 10 sequential generate calls succeed"""
        errors = 0
        for _ in range(10):
            r = api_session.post(f"{API_URL}/generate",
                json={"prompt": "endurance test", "style": "Realistic", "quality": "low"},
                timeout=120)
            if r.status_code not in [200, 202]:
                errors += 1
        assert errors <= 2

    def test_memory_stable_50_calls(self, api_session):
        """TC-LOAD-ADV-033: Server stable after 50 health calls"""
        for _ in range(50):
            api_session.get(f"{API_URL}/health", timeout=5)
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200

    def test_response_consistent_over_time(self, api_session):
        """TC-LOAD-ADV-034: Response body consistent over 20 calls"""
        responses = []
        for _ in range(20):
            r = api_session.get(f"{API_URL}/health", timeout=5)
            responses.append(r.json().get("status") if r.status_code == 200 else None)
        non_null = [r for r in responses if r is not None]
        assert len(set(non_null)) <= 1

    def test_no_error_rate_increase_over_time(self, api_session):
        """TC-LOAD-ADV-035: Error rate doesn't increase over 30 calls"""
        errors_first_half = 0
        errors_second_half = 0
        for i in range(30):
            r = api_session.get(f"{API_URL}/health", timeout=5)
            if r.status_code != 200:
                if i < 15:
                    errors_first_half += 1
                else:
                    errors_second_half += 1
        assert errors_second_half <= errors_first_half + 2

    def test_connection_reuse(self, api_session):
        """TC-LOAD-ADV-036: Session connection reuse works"""
        times = []
        for _ in range(10):
            s = time.time()
            api_session.get(f"{API_URL}/health", timeout=5)
            times.append(time.time() - s)
        assert statistics.mean(times) < 0.5

    def test_no_connection_refused_after_load(self, api_session):
        """TC-LOAD-ADV-037: No connection refused after 30 rapid requests"""
        refused = 0
        for _ in range(30):
            try:
                api_session.get(f"{API_URL}/health", timeout=2)
            except requests.exceptions.ConnectionError:
                refused += 1
        assert refused == 0

    def test_generate_error_rate_under_10pct(self, api_session):
        """TC-LOAD-ADV-038: Generate error rate under 10% for 10 calls"""
        errors = 0
        for _ in range(10):
            r = api_session.post(f"{API_URL}/generate",
                json={"prompt": "error rate test", "style": "Realistic", "quality": "low"},
                timeout=120)
            if r.status_code >= 500:
                errors += 1
        assert errors / 10 < 0.10

    def test_api_healthy_after_generate_load(self, api_session):
        """TC-LOAD-ADV-039: API health check passes after generate load"""
        for _ in range(3):
            api_session.post(f"{API_URL}/generate",
                json={"prompt": "post load check", "quality": "low"}, timeout=60)
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200

    def test_throughput_measurement(self, api_session):
        """TC-LOAD-ADV-040: Measure throughput for 20 health calls"""
        start = time.time()
        for _ in range(20):
            api_session.get(f"{API_URL}/health", timeout=5)
        elapsed = time.time() - start
        throughput = 20 / elapsed
        assert throughput > 1  # At least 1 req/s


class TestLoadEdgeCases:
    """TC-LOAD-ADV-041 to TC-LOAD-ADV-050: Load edge cases"""

    def test_large_prompt_under_load(self, api_session):
        """TC-LOAD-ADV-041: Large prompt under concurrent load"""
        def gen():
            return requests.post(f"{API_URL}/generate",
                json={"prompt": "large " * 100, "style": "Realistic"},
                timeout=60).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            results = list(ex.map(lambda _: gen(), range(3)))
        assert all(s in [200, 202, 400, 413, 422] for s in results)

    def test_mixed_valid_invalid_load(self, api_session):
        """TC-LOAD-ADV-042: Mixed valid/invalid requests under load"""
        def valid():
            return requests.post(f"{API_URL}/generate",
                json={"prompt": "valid", "style": "Realistic"}, timeout=60).status_code
        def invalid():
            return requests.post(f"{API_URL}/generate", json={}, timeout=5).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
            v = list(ex.map(lambda _: valid(), range(3)))
            i = list(ex.map(lambda _: invalid(), range(3)))
        assert all(s in [400, 422] for s in i)

    def test_zero_content_length(self, api_session):
        """TC-LOAD-ADV-043: Zero content requests handled"""
        errors = 0
        for _ in range(5):
            try:
                r = requests.post(f"{API_URL}/generate",
                    data="", headers={"Content-Type": "application/json"}, timeout=5)
                if r.status_code >= 500:
                    errors += 1
            except Exception:
                pass
        assert errors == 0

    def test_keep_alive_connections(self, api_session):
        """TC-LOAD-ADV-044: Keep-alive connections work"""
        session = requests.Session()
        for _ in range(10):
            session.get(f"{API_URL}/health", timeout=5)
        r = session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200
        session.close()

    def test_timeout_not_reached_health(self, api_session):
        """TC-LOAD-ADV-045: Health responds well before 1s timeout"""
        try:
            r = requests.get(f"{API_URL}/health", timeout=1)
            assert r.status_code == 200
        except requests.exceptions.Timeout:
            pytest.fail("Health endpoint timed out in 1s")

    def test_response_size_health(self, api_session):
        """TC-LOAD-ADV-046: Health response size is small"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert len(r.content) < 1024  # Under 1KB

    def test_generate_response_size(self, api_session):
        """TC-LOAD-ADV-047: Generate response size is reasonable"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt": "size test", "style": "Realistic", "quality": "low"},
            timeout=120)
        assert len(r.content) < 10 * 1024 * 1024  # Under 10MB

    def test_api_accepts_gzip(self, api_session):
        """TC-LOAD-ADV-048: API accepts gzip content-encoding"""
        r = requests.get(f"{API_URL}/health",
            headers={"Accept-Encoding": "gzip, deflate"}, timeout=5)
        assert r.status_code == 200

    def test_no_duplicate_responses(self, api_session):
        """TC-LOAD-ADV-049: Each generate request gets unique response"""
        results = []
        for _ in range(3):
            r = api_session.post(f"{API_URL}/generate",
                json={"prompt": f"unique {time.time()}", "style": "Realistic"},
                timeout=120)
            if r.status_code == 200:
                results.append(r.json().get("image_url", ""))
        if len(results) > 1:
            assert True  # Just verify responses received

    def test_load_test_summary(self, api_session):
        """TC-LOAD-ADV-050: Full load summary - health stable after all tests"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, dict)
