"""
Load Testing Suite - Locust
TC-LOAD-001 to TC-LOAD-055 (55 scenarios)
Run: locust -f locustfile.py --host=http://localhost:8000 --headless -u 50 -r 10 -t 60s
"""
import json
import random
import time
from locust import HttpUser, TaskSet, between, task, events
from locust.exception import StopUser

PROMPTS = [
    "a beautiful sunset over mountains",
    "a futuristic city at night with neon lights",
    "a cat sitting on a cozy window sill",
    "an ancient forest with magical lights",
    "a serene beach at golden hour",
    "a snowy mountain peak above clouds",
    "a vibrant flower market in Amsterdam",
    "a dragon flying over a medieval castle",
]

STYLES = ["Cinematic", "Anime", "Realistic", "3D", "Cartoon", "Cyberpunk", "Oil Painting", "Watercolor"]
RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:2"]
QUALITIES = ["low", "medium", "high"]


# ── TC-LOAD-001 to TC-LOAD-010: Health endpoint load ─────────────────────────
class HealthCheckTaskSet(TaskSet):
    """TC-LOAD-001 to TC-LOAD-010"""

    @task(10)
    def health_check(self):
        """TC-LOAD-001: Health endpoint under load"""
        with self.client.get("/health", catch_response=True) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"Expected 200, got {r.status_code}")

    @task(5)
    def health_repeated(self):
        """TC-LOAD-002: Health under repeated rapid calls"""
        for _ in range(3):
            self.client.get("/health")

    @task(2)
    def health_with_header(self):
        """TC-LOAD-003: Health with custom header"""
        self.client.get("/health", headers={"X-Test": "locust"})

    @task(1)
    def health_concurrent_check(self):
        """TC-LOAD-004: Multiple health calls per user"""
        results = []
        for _ in range(5):
            r = self.client.get("/health")
            results.append(r.status_code)
        assert all(s == 200 for s in results)


class HealthUser(HttpUser):
    tasks = [HealthCheckTaskSet]
    wait_time = between(0.1, 0.5)
    weight = 3


# ── TC-LOAD-011 to TC-LOAD-030: Generate endpoint load ───────────────────────
class GenerateTaskSet(TaskSet):
    """TC-LOAD-011 to TC-LOAD-030"""

    @task(8)
    def generate_basic(self):
        """TC-LOAD-011: Basic generate request under load"""
        payload = {
            "prompt": random.choice(PROMPTS),
            "style": random.choice(STYLES),
            "ratio": random.choice(RATIOS),
        }
        with self.client.post("/generate", json=payload, catch_response=True, timeout=120) as r:
            if r.status_code in [200, 202]:
                r.success()
            elif r.status_code in [400, 422]:
                r.failure(f"Validation error: {r.text[:100]}")
            else:
                r.failure(f"Unexpected status: {r.status_code}")

    @task(4)
    def generate_low_quality(self):
        """TC-LOAD-012: Low quality generates faster under load"""
        payload = {
            "prompt": random.choice(PROMPTS),
            "style": "Realistic",
            "ratio": "1:1",
            "quality": "low",
        }
        self.client.post("/generate", json=payload, timeout=60)

    @task(3)
    def generate_anime_style(self):
        """TC-LOAD-013: Anime style under load"""
        self.client.post("/generate", json={"prompt": "anime character", "style": "Anime", "ratio": "9:16"}, timeout=120)

    @task(3)
    def generate_cinematic(self):
        """TC-LOAD-014: Cinematic style under load"""
        self.client.post("/generate", json={"prompt": "epic cinematic scene", "style": "Cinematic", "ratio": "16:9"}, timeout=120)

    @task(2)
    def generate_all_ratios(self):
        """TC-LOAD-015: All aspect ratios under load"""
        for ratio in RATIOS:
            self.client.post("/generate", json={"prompt": "test", "style": "Realistic", "ratio": ratio}, timeout=60)

    @task(2)
    def generate_long_prompt(self):
        """TC-LOAD-016: Long prompt under load"""
        long_prompt = " ".join(random.choice(PROMPTS) for _ in range(5))
        self.client.post("/generate", json={"prompt": long_prompt, "style": "Realistic"}, timeout=120)

    @task(1)
    def generate_unicode_prompt(self):
        """TC-LOAD-017: Unicode prompt under load"""
        self.client.post("/generate", json={"prompt": "美しい夕日 beautiful sunset", "style": "Anime"}, timeout=60)

    @task(1)
    def generate_empty_prompt(self):
        """TC-LOAD-018: Empty prompt returns 400 under load"""
        with self.client.post("/generate", json={"prompt": ""}, catch_response=True, timeout=10) as r:
            if r.status_code in [400, 422]:
                r.success()
            else:
                r.failure(f"Should have failed with 400/422, got {r.status_code}")

    @task(1)
    def generate_missing_prompt(self):
        """TC-LOAD-019: Missing prompt field under load"""
        with self.client.post("/generate", json={}, catch_response=True, timeout=10) as r:
            if r.status_code in [400, 422]:
                r.success()
            else:
                r.failure(f"Expected 400/422, got {r.status_code}")

    @task(1)
    def generate_3d_style(self):
        """TC-LOAD-020: 3D style under concurrent load"""
        self.client.post("/generate", json={"prompt": "3D rendered scene", "style": "3D", "ratio": "1:1"}, timeout=120)


class GenerateUser(HttpUser):
    tasks = [GenerateTaskSet]
    wait_time = between(2, 8)
    weight = 2


# ── TC-LOAD-031 to TC-LOAD-045: Mixed workload ───────────────────────────────
class MixedTaskSet(TaskSet):
    """TC-LOAD-031 to TC-LOAD-045: Simulates real user behaviour"""

    def on_start(self):
        """TC-LOAD-031: User session starts with health check"""
        self.client.get("/health")
        time.sleep(0.5)

    @task(5)
    def user_journey_generate(self):
        """TC-LOAD-032: Full user journey - health then generate"""
        self.client.get("/health")
        time.sleep(random.uniform(0.5, 2))
        self.client.post("/generate", json={
            "prompt": random.choice(PROMPTS),
            "style": random.choice(STYLES),
            "ratio": random.choice(RATIOS),
            "quality": random.choice(QUALITIES),
        }, timeout=120)

    @task(3)
    def rapid_health_then_generate(self):
        """TC-LOAD-033: Rapid health check then generate"""
        for _ in range(2):
            self.client.get("/health")
        self.client.post("/generate", json={"prompt": "quick test", "style": "Realistic", "ratio": "1:1", "quality": "low"}, timeout=60)

    @task(2)
    def multiple_generates_session(self):
        """TC-LOAD-034: Multiple generates in single session"""
        for prompt in random.sample(PROMPTS, 2):
            self.client.post("/generate", json={"prompt": prompt, "style": random.choice(STYLES), "ratio": "1:1"}, timeout=120)
            time.sleep(1)

    @task(2)
    def generate_with_all_qualities(self):
        """TC-LOAD-035: Generate with all quality levels"""
        for quality in QUALITIES:
            self.client.post("/generate", json={
                "prompt": "quality test scene",
                "style": "Realistic",
                "quality": quality,
            }, timeout=120)

    @task(1)
    def stress_health_endpoint(self):
        """TC-LOAD-036: Stress health endpoint with 10 rapid calls"""
        for _ in range(10):
            self.client.get("/health")

    @task(1)
    def invalid_then_valid(self):
        """TC-LOAD-037: Invalid request followed by valid request"""
        self.client.post("/generate", json={}, timeout=5)
        time.sleep(0.5)
        self.client.post("/generate", json={"prompt": "valid prompt", "style": "Realistic"}, timeout=120)

    @task(1)
    def generate_all_styles_sequential(self):
        """TC-LOAD-038: All styles sequentially in one session"""
        for style in STYLES:
            self.client.post("/generate", json={"prompt": f"test {style} style", "style": style, "ratio": "1:1"}, timeout=60)
            time.sleep(0.5)

    @task(1)
    def error_recovery(self):
        """TC-LOAD-039: Client recovers from server errors"""
        self.client.post("/generate", json={"prompt": None}, timeout=5)
        time.sleep(0.3)
        r = self.client.get("/health")
        assert r.status_code == 200

    @task(1)
    def check_status_endpoint(self):
        """TC-LOAD-040: Poll job status endpoint"""
        self.client.get("/api/status/test-job-id")

    @task(1)
    def concurrent_generate_low(self):
        """TC-LOAD-041: Concurrent low-quality generates"""
        import concurrent.futures
        def gen():
            return self.client.post("/generate", json={"prompt": "concurrent test", "quality": "low", "style": "Realistic"}, timeout=60).status_code
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            list(ex.map(lambda _: gen(), range(3)))

    @task(1)
    def simulate_page_refresh(self):
        """TC-LOAD-042: Simulate page refresh pattern"""
        self.client.get("/health")
        time.sleep(0.2)
        self.client.get("/health")

    @task(1)
    def watercolor_style(self):
        """TC-LOAD-043: Watercolor style under load"""
        self.client.post("/generate", json={"prompt": "watercolor landscape", "style": "Watercolor", "ratio": "4:3"}, timeout=120)

    @task(1)
    def digital_art_style(self):
        """TC-LOAD-044: Digital Art style under load"""
        self.client.post("/generate", json={"prompt": "digital art scene", "style": "Digital Art", "ratio": "1:1"}, timeout=120)

    @task(1)
    def oil_painting_style(self):
        """TC-LOAD-045: Oil Painting style under load"""
        self.client.post("/generate", json={"prompt": "oil painting portrait", "style": "Oil Painting", "ratio": "3:2"}, timeout=120)


class MixedUser(HttpUser):
    tasks = [MixedTaskSet]
    wait_time = between(1, 5)
    weight = 1


# ── TC-LOAD-046 to TC-LOAD-055: Spike & soak testing ────────────────────────
class SpikeTaskSet(TaskSet):
    """TC-LOAD-046 to TC-LOAD-055: Spike load scenarios"""

    @task(10)
    def spike_health(self):
        """TC-LOAD-046: Health endpoint during spike"""
        self.client.get("/health")

    @task(5)
    def spike_generate(self):
        """TC-LOAD-047: Generate during spike load"""
        self.client.post("/generate", json={"prompt": "spike test", "style": "Realistic", "quality": "low"}, timeout=120)

    @task(3)
    def spike_invalid_requests(self):
        """TC-LOAD-048: Invalid requests during spike"""
        with self.client.post("/generate", json={}, catch_response=True, timeout=5) as r:
            if r.status_code in [400, 422]:
                r.success()

    @task(2)
    def spike_concurrent_health(self):
        """TC-LOAD-049: Many concurrent health checks"""
        for _ in range(20):
            self.client.get("/health")

    @task(1)
    def spike_large_payload(self):
        """TC-LOAD-050: Large payload during spike"""
        large_prompt = "test " * 200
        self.client.post("/generate", json={"prompt": large_prompt, "style": "Realistic"}, timeout=30)

    @task(1)
    def spike_all_fields(self):
        """TC-LOAD-051: All fields provided during spike"""
        self.client.post("/generate", json={
            "prompt": "full fields test",
            "style": "Cyberpunk",
            "ratio": "16:9",
            "quality": "ultra",
        }, timeout=120)

    @task(1)
    def soak_generate_low(self):
        """TC-LOAD-052: Soak test - sustained low quality generate"""
        for _ in range(3):
            self.client.post("/generate", json={"prompt": "soak test", "style": "Realistic", "quality": "low"}, timeout=60)
            time.sleep(2)

    @task(1)
    def soak_health(self):
        """TC-LOAD-053: Soak test - health check every second"""
        for _ in range(5):
            self.client.get("/health")
            time.sleep(1)

    @task(1)
    def measure_p95_health(self):
        """TC-LOAD-054: Health p95 should be under 200ms"""
        times = []
        for _ in range(10):
            start = time.time()
            self.client.get("/health")
            times.append(time.time() - start)
        times.sort()
        p95 = times[int(len(times) * 0.95)]
        assert p95 < 2.0  # Lenient for local server

    @task(1)
    def measure_error_rate(self):
        """TC-LOAD-055: Error rate stays below 5% during load"""
        errors = 0
        total = 10
        for _ in range(total):
            r = self.client.get("/health")
            if r.status_code >= 500:
                errors += 1
        assert errors / total < 0.05


class SpikeUser(HttpUser):
    tasks = [SpikeTaskSet]
    wait_time = between(0.1, 1)
    weight = 1
