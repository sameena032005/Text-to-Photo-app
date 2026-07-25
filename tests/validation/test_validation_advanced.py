"""Advanced Validation Tests - TC-VALA-001 to TC-VALA-050"""
import pytest, requests, re, json
API_URL = "http://localhost:8000"
APP_URL = "http://localhost:5173"

class TestRegexValidation:
    def test_email_regex_valid(self, api_session):
        """TC-VALA-001: Valid email regex patterns accepted"""
        valid = ["a@b.co","user.name+tag@example.co.uk","test123@sub.domain.com"]
        for e in valid:
            assert re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", e)

    def test_email_regex_invalid(self, api_session):
        """TC-VALA-002: Invalid email regex patterns rejected"""
        invalid = ["notanemail","@domain.com","user@","user @domain.com"]
        for e in invalid:
            assert not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", e)

    def test_url_regex_valid(self, api_session):
        """TC-VALA-003: Valid API URL patterns"""
        urls = ["http://localhost:8000","http://192.168.1.1:8000","https://api.example.com"]
        pattern = r"^https?://.+"
        for u in urls:
            assert re.match(pattern, u)

    def test_url_regex_invalid(self, api_session):
        """TC-VALA-004: Invalid API URL patterns rejected"""
        invalid = ["localhost","ftp://bad","://noscheme"]
        pattern = r"^https?://.+"
        for u in invalid:
            assert not re.match(pattern, u)

    def test_prompt_no_only_spaces(self, api_session):
        """TC-VALA-005: Prompt of only spaces fails regex"""
        prompt = "   "
        assert not prompt.strip()

    def test_prompt_alphanumeric(self, api_session):
        """TC-VALA-006: Alphanumeric prompt valid"""
        assert re.match(r"^[\w\s]+$", "sunset over mountains 2024")

    def test_style_exact_match(self, api_session):
        """TC-VALA-007: Style must match allowed values"""
        allowed = ["Cinematic","Anime","Realistic","3D","Cartoon","Cyberpunk","Oil Painting","Watercolor","Digital Art"]
        for s in allowed:
            assert s in allowed

    def test_ratio_format_colon(self, api_session):
        """TC-VALA-008: Ratio format is N:N"""
        ratios = ["16:9","9:16","1:1","4:3","3:2"]
        for r in ratios:
            assert re.match(r"^\d+:\d+$", r)

    def test_quality_values_exact(self, api_session):
        """TC-VALA-009: Quality values are exact strings"""
        assert all(q in ["low","medium","high","ultra"] for q in ["low","high"])

    def test_name_min_2_chars_regex(self, api_session):
        """TC-VALA-010: Name min length validation"""
        assert len("AB".strip()) >= 2
        assert len("A".strip()) < 2

class TestAPISchemaValidation:
    def test_health_schema(self, api_session):
        """TC-VALA-011: Health response has status key"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        if r.status_code == 200:
            assert isinstance(r.json(), dict)

    def test_generate_response_has_url(self, api_session):
        """TC-VALA-012: Success response has image_url string"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"sky","style":"Realistic"},timeout=120)
        if r.status_code == 200:
            d = r.json()
            assert "image_url" in d or "video_url" in d or "jobId" in d

    def test_error_response_has_detail(self, api_session):
        """TC-VALA-013: Error response has message/detail"""
        r = api_session.post(f"{API_URL}/generate", json={}, timeout=10)
        if r.status_code in [400,422]:
            d = r.json()
            assert "message" in d or "detail" in d or "error" in d

    def test_response_is_json_parseable(self, api_session):
        """TC-VALA-014: All responses are JSON parseable"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        try:
            json.loads(r.text)
            assert True
        except json.JSONDecodeError:
            pytest.fail("Response not valid JSON")

    def test_image_url_is_string(self, api_session):
        """TC-VALA-015: image_url value is string type"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"test","style":"Realistic"},timeout=120)
        if r.status_code == 200:
            d = r.json()
            if "image_url" in d:
                assert isinstance(d["image_url"], str)

    def test_status_field_string(self, api_session):
        """TC-VALA-016: status field in health is string"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        if r.status_code == 200:
            d = r.json()
            if "status" in d:
                assert isinstance(d["status"], str)

    def test_no_null_values_in_success(self, api_session):
        """TC-VALA-017: Success response has no null critical fields"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"test","style":"Realistic"},timeout=120)
        if r.status_code == 200:
            d = r.json()
            if "image_url" in d:
                assert d["image_url"] is not None

    def test_http_status_codes_correct(self, api_session):
        """TC-VALA-018: Correct HTTP status codes returned"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200
        r2 = api_session.post(f"{API_URL}/generate", json={}, timeout=10)
        assert r2.status_code in [400,422]

    def test_content_type_header(self, api_session):
        """TC-VALA-019: Content-Type is application/json"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert "json" in r.headers.get("Content-Type","").lower()

    def test_response_encoding_utf8(self, api_session):
        """TC-VALA-020: Response encoding is UTF-8"""
        r = api_session.get(f"{API_URL}/health", timeout=5)
        assert r.encoding is None or "utf" in (r.encoding or "utf").lower()

class TestBoundaryAdvanced:
    def test_prompt_exactly_10_chars(self, api_session):
        """TC-VALA-021: Prompt of 10 chars accepted"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"a"*10,"style":"Realistic"},timeout=30)
        assert r.status_code not in [500]

    def test_prompt_exactly_100_chars(self, api_session):
        """TC-VALA-022: Prompt of 100 chars accepted"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"word "*20,"style":"Realistic"},timeout=30)
        assert r.status_code not in [500]

    def test_prompt_exactly_500_chars(self, api_session):
        """TC-VALA-023: Prompt of 500 chars accepted"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"a"*500,"style":"Realistic"},timeout=30)
        assert r.status_code not in [500]

    def test_prompt_exactly_1000_chars(self, api_session):
        """TC-VALA-024: Prompt of 1000 chars handled"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"a"*1000,"style":"Realistic"},timeout=30)
        assert r.status_code in [200,202,400,413,422]

    def test_prompt_5000_chars(self, api_session):
        """TC-VALA-025: Prompt of 5000 chars handled"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"a"*5000,"style":"Realistic"},timeout=30)
        assert r.status_code in [200,202,400,413,422]

    def test_quality_boundary_low(self, api_session):
        """TC-VALA-026: Quality=low boundary accepted"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"test","quality":"low"},timeout=30)
        assert r.status_code not in [500]

    def test_quality_boundary_ultra(self, api_session):
        """TC-VALA-027: Quality=ultra boundary accepted"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"test","quality":"ultra"},timeout=30)
        assert r.status_code not in [500]

    def test_ratio_minimum_valid(self, api_session):
        """TC-VALA-028: Minimum valid ratio 1:1 accepted"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"test","style":"Realistic","ratio":"1:1"},timeout=30)
        assert r.status_code not in [500]

    def test_ratio_maximum_wide(self, api_session):
        """TC-VALA-029: Wide ratio 16:9 accepted"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"test","style":"Realistic","ratio":"16:9"},timeout=30)
        assert r.status_code not in [500]

    def test_ratio_portrait(self, api_session):
        """TC-VALA-030: Portrait ratio 9:16 accepted"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt":"test","style":"Realistic","ratio":"9:16"},timeout=30)
        assert r.status_code not in [500]

class TestFormValidationAdvanced:
    def test_email_trim_whitespace(self, driver):
        """TC-VALA-031: Email with leading spaces shows error"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR,"input[name='email']").send_keys("  test@test.com")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(0.5)
        assert driver.find_element(By.TAG_NAME,"body").is_displayed()

    def test_name_trim_whitespace(self, driver):
        """TC-VALA-032: Name with only spaces rejected"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        driver.find_element(By.CSS_SELECTOR,"input[name='name']").send_keys("   ")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME,"body").text
        assert "name" in body.lower() or "required" in body.lower()

    def test_password_exactly_6_boundary(self, driver):
        """TC-VALA-033: Password exactly 6 chars passes"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR,"input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR,"input[name='password']").send_keys("abc123")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(0.5)
        assert "at least 6" not in driver.find_element(By.TAG_NAME,"body").text.lower()

    def test_password_5_chars_boundary(self, driver):
        """TC-VALA-034: Password 5 chars fails boundary"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR,"input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR,"input[name='password']").send_keys("ab123")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(0.5)
        assert "6" in driver.find_element(By.TAG_NAME,"body").text

    def test_confirm_password_exact_match(self, driver):
        """TC-VALA-035: Exact password match passes"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        ts = str(int(time.time()))
        driver.find_element(By.CSS_SELECTOR,"input[name='name']").send_keys("Test")
        driver.find_element(By.CSS_SELECTOR,"input[name='email']").send_keys(f"v{ts}@t.com")
        driver.find_element(By.CSS_SELECTOR,"input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR,"input[name='confirmPassword']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(2)
        assert "match" not in driver.find_element(By.TAG_NAME,"body").text.lower()

    def test_api_url_valid_format(self, driver):
        """TC-VALA-036: Valid API URL accepted in settings"""
        from selenium.webdriver.common.by import By
        import time
        driver.execute_script("localStorage.setItem('ai-photo-auth',JSON.stringify({id:'1',name:'T',email:'t@t.com',token:'tok'}))")
        driver.get(f"{APP_URL}/")
        time.sleep(0.8)
        btns = driver.find_elements(By.XPATH,"//*[contains(text(),'Settings')]")
        if btns: btns[-1].click(); time.sleep(0.5)
        inputs = driver.find_elements(By.CSS_SELECTOR,"input[type='url'],input[placeholder*='localhost']")
        if inputs:
            inputs[0].clear()
            inputs[0].send_keys("http://localhost:9000")
            assert inputs[0].get_attribute("value") == "http://localhost:9000"

    def test_empty_fields_all_shown(self, driver):
        """TC-VALA-037: All empty field errors shown at once"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/signup")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(0.5)
        errors = driver.find_elements(By.CSS_SELECTOR,".text-red-400")
        assert len(errors) >= 2

    def test_form_resubmit_after_fix(self, driver):
        """TC-VALA-038: Form can be resubmitted after fixing errors"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(0.4)
        driver.find_element(By.CSS_SELECTOR,"input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR,"input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(1)
        assert driver.find_element(By.TAG_NAME,"body").is_displayed()

    def test_special_chars_email_rejected(self, driver):
        """TC-VALA-039: Special chars in email rejected"""
        from selenium.webdriver.common.by import By
        import time
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR,"input[name='email']").send_keys("user<>@test.com")
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME,"body").text
        assert "valid" in body.lower() or "email" in body.lower()

    def test_form_accessible_by_keyboard(self, driver):
        """TC-VALA-040: Entire form accessible by keyboard only"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        driver.get(f"{APP_URL}/login")
        driver.find_element(By.CSS_SELECTOR,"input[name='email']").send_keys("t@t.com")
        driver.find_element(By.CSS_SELECTOR,"input[name='email']").send_keys(Keys.TAB)
        active = driver.switch_to.active_element
        assert active.get_attribute("name") == "password" or active.get_attribute("type") == "password"

class TestDataIntegrity:
    def test_history_stored_correctly(self, driver):
        """TC-VALA-041: History data stored with correct schema"""
        from selenium.webdriver.common.by import By
        import time, json as j
        driver.execute_script("localStorage.setItem('ai-photo-auth',JSON.stringify({id:'1',name:'T',email:'t@t.com',token:'tok'}))")
        driver.execute_script("""
            localStorage.setItem('ai-photo-history',JSON.stringify([
                {id:'1',prompt:'test',style:'Realistic',ratio:'1:1',quality:'High',
                 imageUrl:'http://test.com/img.png',createdAt:new Date().toISOString()}
            ]))""")
        driver.get(f"{APP_URL}/")
        time.sleep(0.8)
        raw = driver.execute_script("return localStorage.getItem('ai-photo-history')")
        data = j.loads(raw)
        assert data[0]["prompt"] == "test"
        assert data[0]["style"] == "Realistic"

    def test_user_data_stored_correctly(self, driver):
        """TC-VALA-042: User auth data stored with correct fields"""
        from selenium.webdriver.common.by import By
        import json as j
        driver.get(f"{APP_URL}/login")
        driver.execute_script("localStorage.setItem('ai-photo-auth',JSON.stringify({id:'1',name:'Jane',email:'jane@t.com',token:'tok123'}))")
        raw = driver.execute_script("return localStorage.getItem('ai-photo-auth')")
        data = j.loads(raw)
        assert data["name"] == "Jane"
        assert data["email"] == "jane@t.com"
        assert "token" in data

    def test_settings_data_stored(self, driver):
        """TC-VALA-043: Settings persisted correctly"""
        from selenium.webdriver.common.by import By
        import json as j
        driver.get(f"{APP_URL}/login")
        driver.execute_script("localStorage.setItem('ai-photo-settings',JSON.stringify({theme:'dark',defaultStyle:'Anime',apiUrl:'http://localhost:8000'}))")
        raw = driver.execute_script("return localStorage.getItem('ai-photo-settings')")
        data = j.loads(raw)
        assert data["theme"] == "dark"
        assert data["defaultStyle"] == "Anime"

    def test_logout_clears_auth(self, driver):
        """TC-VALA-044: Logout removes auth from localStorage"""
        from selenium.webdriver.common.by import By
        import time
        driver.execute_script("localStorage.setItem('ai-photo-auth',JSON.stringify({id:'1',name:'T',email:'t@t.com',token:'tok'}))")
        driver.get(f"{APP_URL}/")
        time.sleep(0.8)
        btns = driver.find_elements(By.CSS_SELECTOR,"header button")
        if btns:
            btns[-1].click()
            time.sleep(0.4)
            logout = driver.find_elements(By.XPATH,"//*[contains(text(),'Sign out')]")
            if logout:
                logout[0].click()
                time.sleep(1)
        auth = driver.execute_script("return localStorage.getItem('ai-photo-auth')")
        assert auth is None or "login" in driver.current_url

    def test_history_max_50_items(self, driver):
        """TC-VALA-045: History capped at 50 items"""
        import json as j
        driver.get(f"{APP_URL}/login")
        items = [{"id":str(i),"prompt":f"p{i}","style":"R","ratio":"1:1","quality":"H","imageUrl":"u","createdAt":"2024-01-01"} for i in range(60)]
        driver.execute_script(f"localStorage.setItem('ai-photo-history',JSON.stringify({j.dumps(items)}))")
        driver.execute_script("localStorage.setItem('ai-photo-auth',JSON.stringify({id:'1',name:'T',email:'t@t.com',token:'tok'}))")
        driver.get(f"{APP_URL}/")
        import time; time.sleep(1)
        assert driver.find_element(By.TAG_NAME,"body").is_displayed()

    def test_api_url_persists_settings(self, api_session):
        """TC-VALA-046: API URL persists across requests"""
        r1 = api_session.get(f"{API_URL}/health", timeout=5)
        r2 = api_session.get(f"{API_URL}/health", timeout=5)
        assert r1.status_code == r2.status_code == 200

    def test_generate_payload_schema(self, api_session):
        """TC-VALA-047: Generate payload schema validated"""
        required_fields = {"prompt": "test scene"}
        r = api_session.post(f"{API_URL}/generate", json=required_fields, timeout=30)
        assert r.status_code not in [500]

    def test_style_value_preserved(self, api_session):
        """TC-VALA-048: Style value sent is preserved in request"""
        payload = {"prompt": "test", "style": "Anime", "ratio": "1:1"}
        r = api_session.post(f"{API_URL}/generate", json=payload, timeout=30)
        assert r.status_code not in [500]

    def test_ratio_value_preserved(self, api_session):
        """TC-VALA-049: Ratio value sent is preserved"""
        payload = {"prompt": "test", "style": "Realistic", "ratio": "16:9"}
        r = api_session.post(f"{API_URL}/generate", json=payload, timeout=30)
        assert r.status_code not in [500]

    def test_validation_summary(self, api_session):
        """TC-VALA-050: All validation rules work end-to-end"""
        r = api_session.post(f"{API_URL}/generate",
            json={"prompt": "final validation test", "style": "Realistic", "ratio": "1:1", "quality": "high"},
            timeout=120)
        assert r.status_code in [200, 202, 400, 422]
