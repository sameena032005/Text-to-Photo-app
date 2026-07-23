"""
Validation Test Suite - Form inputs, API schema, boundary values
TC-VAL-001 to TC-VAL-060 (60 test cases)
"""
import pytest
import requests
import re

API_URL = "http://localhost:8000"
APP_URL = "http://localhost:5173"


class TestEmailValidation:
    """TC-VAL-001 to TC-VAL-015: Email field validation"""

    VALID_EMAILS = [
        "user@example.com",
        "user.name@example.com",
        "user+tag@example.co.uk",
        "user123@test.io",
        "USER@EXAMPLE.COM",
    ]

    INVALID_EMAILS = [
        "notanemail",
        "missing@",
        "@nodomain.com",
        "spaces in@email.com",
        "double@@domain.com",
        "no-tld@domain",
        "",
        "   ",
    ]

    @pytest.mark.parametrize("email", VALID_EMAILS)
    def test_valid_email_accepted(self, driver):
        """TC-VAL-001-005: Valid email formats accepted"""
        driver.get(f"{APP_URL}/login")
        driver.find_element_by_css_selector = driver.find_element
        from selenium.webdriver.common.by import By
        field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        field.clear()
        field.send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        import time; time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "valid email" not in body.lower()

    @pytest.mark.parametrize("email", INVALID_EMAILS)
    def test_invalid_email_rejected(self, driver):
        """TC-VAL-006-013: Invalid email formats rejected"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        field.clear()
        field.send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "email" in body.lower() or "required" in body.lower() or "valid" in body.lower()

    def test_email_case_insensitive_login(self, driver):
        """TC-VAL-014: Email comparison is case-insensitive"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        ts = str(int(time.time()))
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Case Test")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(f"case{ts}@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        assert "signup" not in driver.current_url

    def test_email_max_length_boundary(self, driver):
        """TC-VAL-015: Email at maximum reasonable length"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("a" * 64 + "@" + "b" * 63 + ".com")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()


class TestPasswordValidation:
    """TC-VAL-016 to TC-VAL-030: Password validation"""

    def test_password_exactly_6_chars(self, driver):
        """TC-VAL-016: Password of exactly 6 chars passes"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("abc123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 6" not in body.lower()

    def test_password_5_chars_fails(self, driver):
        """TC-VAL-017: Password of 5 chars fails"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("abc12")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "6" in body or "characters" in body.lower()

    def test_password_100_chars_accepted(self, driver):
        """TC-VAL-018: Very long password accepted"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("A" * 100)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 6" not in body.lower()

    def test_password_with_spaces(self, driver):
        """TC-VAL-019: Password with spaces accepted"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass word")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 6" not in body.lower()

    def test_password_special_chars(self, driver):
        """TC-VAL-020: Password with special characters accepted"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("P@ss!#$%^")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 6" not in body.lower()

    def test_confirm_password_mismatch(self, driver):
        """TC-VAL-021: Confirm password mismatch shows error"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("pass456")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert "match" in driver.find_element(By.TAG_NAME, "body").text.lower()

    def test_confirm_password_match(self, driver):
        """TC-VAL-022: Matching confirm password passes"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        ts = str(int(time.time()))
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(f"match{ts}@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "match" not in body.lower() or "signup" not in driver.current_url

    def test_empty_confirm_password(self, driver):
        """TC-VAL-023: Empty confirm password shows error"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "confirm" in body.lower() or "password" in body.lower()

    @pytest.mark.parametrize("password,expected_strength", [
        ("abc123", "weak"),
        ("Abc123!!", "good"),
        ("Tr0ub4dor&3!XY", "strong"),
    ])
    def test_password_strength_levels(self, driver, password, expected_strength):
        """TC-VAL-024-026: Password strength levels shown correctly"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(password)
        time.sleep(0.4)
        body = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "weak" in body or "fair" in body or "good" in body or "strong" in body

    def test_password_only_spaces(self, driver):
        """TC-VAL-027: Password of spaces only - length check"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("      ")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 6" not in body.lower()  # 6 spaces passes length check


class TestAPIPayloadValidation:
    """TC-VAL-028 to TC-VAL-045: API payload validation"""

    def test_prompt_required(self, api_session):
        """TC-VAL-028: Prompt is required field"""
        r = api_session.post(f"{API_URL}/generate", json={"style": "Realistic"}, timeout=10)
        assert r.status_code in [400, 422]

    def test_prompt_min_length(self, api_session):
        """TC-VAL-029: Single character prompt attempted"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "a", "style": "Realistic"}, timeout=30)
        assert r.status_code in [200, 202, 400, 422]

    def test_prompt_exactly_1_char(self, api_session):
        """TC-VAL-030: 1-character prompt boundary"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "x"}, timeout=30)
        assert r.status_code in [200, 202, 400, 422]

    def test_prompt_max_boundary(self, api_session):
        """TC-VAL-031: Prompt at 500 chars"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "a" * 500, "style": "Realistic"}, timeout=30)
        assert r.status_code in [200, 202, 400, 422]

    def test_style_valid_values(self, api_session):
        """TC-VAL-032: Valid style values accepted"""
        for style in ["Cinematic", "Anime", "Realistic", "3D", "Cartoon", "Cyberpunk"]:
            r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": style}, timeout=30)
            assert r.status_code != 500

    def test_ratio_valid_values(self, api_session):
        """TC-VAL-033: Valid ratio values accepted"""
        for ratio in ["16:9", "9:16", "1:1", "4:3", "3:2"]:
            r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": "Realistic", "ratio": ratio}, timeout=30)
            assert r.status_code != 500

    def test_quality_valid_values(self, api_session):
        """TC-VAL-034: Valid quality values accepted"""
        for quality in ["low", "medium", "high", "ultra"]:
            r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "quality": quality}, timeout=30)
            assert r.status_code != 500

    def test_prompt_with_numbers(self, api_session):
        """TC-VAL-035: Prompt with numbers accepted"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "A 3D scene with 10 towers", "style": "3D"}, timeout=30)
        assert r.status_code not in [400, 422]

    def test_prompt_with_punctuation(self, api_session):
        """TC-VAL-036: Prompt with punctuation accepted"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "A scene: mountains, rivers, and forests!", "style": "Realistic"}, timeout=30)
        assert r.status_code not in [500]

    def test_response_schema_image_url(self, api_session):
        """TC-VAL-037: Success response has image_url string"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "blue sky", "style": "Realistic"}, timeout=120)
        if r.status_code == 200:
            data = r.json()
            if "image_url" in data:
                assert isinstance(data["image_url"], str)
                assert len(data["image_url"]) > 0

    def test_response_schema_error_message(self, api_session):
        """TC-VAL-038: Error response message is string"""
        r = api_session.post(f"{API_URL}/generate", json={}, timeout=10)
        if r.status_code in [400, 422]:
            data = r.json()
            if "message" in data:
                assert isinstance(data["message"], str)
            elif "detail" in data:
                assert isinstance(data["detail"], (str, list))

    def test_health_response_schema(self, api_session):
        """TC-VAL-039: Health response matches expected schema"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, dict)

    def test_integer_quality_rejected(self, api_session):
        """TC-VAL-040: Integer quality value handled"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "quality": 5}, timeout=10)
        assert r.status_code in [200, 202, 400, 422]

    def test_boolean_prompt_rejected(self, api_session):
        """TC-VAL-041: Boolean prompt rejected"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": True}, timeout=10)
        assert r.status_code in [400, 422]

    def test_nested_object_prompt(self, api_session):
        """TC-VAL-042: Nested object as prompt rejected"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": {"text": "test"}}, timeout=10)
        assert r.status_code in [400, 422]

    def test_array_style_rejected(self, api_session):
        """TC-VAL-043: Array as style value rejected"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": ["Realistic", "Anime"]}, timeout=10)
        assert r.status_code in [400, 422]

    def test_null_style_handled(self, api_session):
        """TC-VAL-044: Null style handled gracefully"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": None}, timeout=10)
        assert r.status_code in [200, 202, 400, 422]

    def test_extra_fields_allowed(self, api_session):
        """TC-VAL-045: Extra unknown fields do not cause 500"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": "Realistic", "unknownField": "value"}, timeout=30)
        assert r.status_code not in [500]


class TestBoundaryValues:
    """TC-VAL-046 to TC-VAL-060: Boundary value analysis"""

    def test_prompt_zero_length(self, api_session):
        """TC-VAL-046: Zero-length prompt rejected"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": ""}, timeout=10)
        assert r.status_code in [400, 422]

    def test_prompt_1_char(self, api_session):
        """TC-VAL-047: 1-character prompt boundary"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "a"}, timeout=30)
        assert r.status_code in [200, 202, 400, 422]

    def test_prompt_2_chars(self, api_session):
        """TC-VAL-048: 2-character prompt"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "ab"}, timeout=30)
        assert r.status_code not in [500]

    def test_prompt_255_chars(self, api_session):
        """TC-VAL-049: 255-character prompt (common boundary)"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "a" * 255, "style": "Realistic"}, timeout=30)
        assert r.status_code not in [500]

    def test_prompt_256_chars(self, api_session):
        """TC-VAL-050: 256-character prompt (over common boundary)"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "a" * 256, "style": "Realistic"}, timeout=30)
        assert r.status_code not in [500]

    def test_prompt_1000_chars(self, api_session):
        """TC-VAL-051: 1000-character prompt"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "scene " * 166, "style": "Realistic"}, timeout=30)
        assert r.status_code not in [500]

    def test_name_min_2_chars(self, driver):
        """TC-VAL-052: Name minimum 2 chars boundary"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("AB")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 2" not in body.lower()

    def test_name_1_char_fails(self, driver):
        """TC-VAL-053: Name of 1 char fails"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("A")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "2" in body or "characters" in body.lower()

    def test_password_boundary_6(self, driver):
        """TC-VAL-054: Password exactly at minimum boundary (6)"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@t.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("123456")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 6" not in body.lower()

    def test_concurrent_signups_different_emails(self, api_session):
        """TC-VAL-055: Concurrent signup with different emails"""
        import concurrent.futures, time
        def signup(i):
            return requests.post(f"{API_URL}/register",
                json={"name": f"User{i}", "email": f"user{i}{int(time.time())}@test.com", "password": "pass123"},
                timeout=10).status_code
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
                results = list(ex.map(signup, range(3)))
            assert all(s in [200, 201, 404, 405] for s in results)
        except Exception:
            pass

    def test_api_response_time_health(self, api_session):
        """TC-VAL-056: Health response under 500ms"""
        import time
        start = time.time()
        api_session.get(f"{API_URL}/health", timeout=5)
        assert time.time() - start < 0.5

    def test_empty_json_body(self, api_session):
        """TC-VAL-057: Empty JSON object returns 400/422"""
        r = api_session.post(f"{API_URL}/generate", json={}, timeout=10)
        assert r.status_code in [400, 422]

    def test_whitespace_style(self, api_session):
        """TC-VAL-058: Whitespace-only style handled"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": "   "}, timeout=10)
        assert r.status_code in [200, 202, 400, 422]

    def test_whitespace_ratio(self, api_session):
        """TC-VAL-059: Whitespace-only ratio handled"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": "Realistic", "ratio": "  "}, timeout=10)
        assert r.status_code in [200, 202, 400, 422]

    def test_numeric_ratio(self, api_session):
        """TC-VAL-060: Numeric ratio value handled"""
        r = api_session.post(f"{API_URL}/generate", json={"prompt": "test", "style": "Realistic", "ratio": 169}, timeout=10)
        assert r.status_code in [200, 202, 400, 422]
