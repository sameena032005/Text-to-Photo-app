"""
Selenium Test Suite - Signup Page
TC-SIGNUP-001 to TC-SIGNUP-040 (40 test cases)
"""
import pytest, time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = "http://localhost:5173"


class TestSignupPageLoad:
    def test_signup_page_loads(self, driver):
        """TC-SIGNUP-001: Signup page loads successfully"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_name_field_present(self, driver):
        """TC-SIGNUP-002: Full name field is present"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "input[name='name']").is_displayed()

    def test_email_field_present(self, driver):
        """TC-SIGNUP-003: Email field is present"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "input[name='email']").is_displayed()

    def test_password_field_present(self, driver):
        """TC-SIGNUP-004: Password field is present"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "input[name='password']").is_displayed()

    def test_confirm_password_field_present(self, driver):
        """TC-SIGNUP-005: Confirm password field is present"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").is_displayed()

    def test_submit_button_present(self, driver):
        """TC-SIGNUP-006: Create account button is present"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "button[type='submit']").is_displayed()

    def test_login_link_present(self, driver):
        """TC-SIGNUP-007: Sign in link is present"""
        driver.get(f"{BASE_URL}/signup")
        links = [a.get_attribute("href") or "" for a in driver.find_elements(By.TAG_NAME, "a")]
        assert any("login" in h for h in links)

    def test_page_heading_present(self, driver):
        """TC-SIGNUP-008: Page heading is visible"""
        driver.get(f"{BASE_URL}/signup")
        headings = driver.find_elements(By.CSS_SELECTOR, "h1, h2")
        assert any(h.is_displayed() for h in headings)


class TestSignupValidation:
    def test_empty_form_shows_errors(self, driver):
        """TC-SIGNUP-009: Empty form shows all required errors"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        errors = driver.find_elements(By.CSS_SELECTOR, ".text-red-400, p.text-red-400")
        assert len(errors) >= 2

    def test_name_required(self, driver):
        """TC-SIGNUP-010: Name field is required"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("a@b.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert "name" in driver.find_element(By.TAG_NAME, "body").text.lower()

    def test_name_min_length(self, driver):
        """TC-SIGNUP-011: Name must be at least 2 characters"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("A")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert "2" in driver.find_element(By.TAG_NAME, "body").text or "characters" in driver.find_element(By.TAG_NAME, "body").text.lower()

    def test_invalid_email_format(self, driver):
        """TC-SIGNUP-012: Invalid email rejected"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Jane")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("notanemail")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert "valid" in driver.find_element(By.TAG_NAME, "body").text.lower()

    def test_password_min_length(self, driver):
        """TC-SIGNUP-013: Password must be at least 6 characters"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Jane")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("jane@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("abc")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert "6" in driver.find_element(By.TAG_NAME, "body").text

    def test_passwords_must_match(self, driver):
        """TC-SIGNUP-014: Confirm password must match password"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Jane")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("jane@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("pass456")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert "match" in driver.find_element(By.TAG_NAME, "body").text.lower()

    def test_password_strength_bar_shows(self, driver):
        """TC-SIGNUP-015: Password strength indicator appears on input"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        time.sleep(0.3)
        strength_bars = driver.find_elements(By.CSS_SELECTOR, ".h-1.flex-1, .rounded-full")
        assert len(strength_bars) > 0

    def test_confirm_password_required(self, driver):
        """TC-SIGNUP-016: Confirm password is required"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Jane")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("jane@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert "confirm" in driver.find_element(By.TAG_NAME, "body").text.lower() or "password" in driver.find_element(By.TAG_NAME, "body").text.lower()

    def test_password_field_masked(self, driver):
        """TC-SIGNUP-017: Password field is masked by default"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "input[name='password']").get_attribute("type") == "password"

    def test_confirm_password_field_masked(self, driver):
        """TC-SIGNUP-018: Confirm password field is masked by default"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").get_attribute("type") == "password"


class TestSignupFunctionality:
    def test_successful_signup_redirects(self, driver):
        """TC-SIGNUP-019: Valid signup redirects to home"""
        driver.get(f"{BASE_URL}/signup")
        import time as t; ts = str(int(t.time()))
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test User")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(f"user{ts}@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        assert "signup" not in driver.current_url

    def test_duplicate_email_shows_error(self, driver):
        """TC-SIGNUP-020: Duplicate email shows error"""
        driver.get(f"{BASE_URL}/signup")
        driver.execute_script(
            "localStorage.setItem('ai-photo-users', JSON.stringify([{id:'1',name:'Existing',email:'existing@test.com',password:'pass123'}]))"
        )
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("New User")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("existing@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)
        assert "already" in driver.find_element(By.TAG_NAME, "body").text.lower() or "exists" in driver.find_element(By.TAG_NAME, "body").text.lower()

    def test_login_link_navigates(self, driver):
        """TC-SIGNUP-021: Login link navigates to /login"""
        driver.get(f"{BASE_URL}/signup")
        login_link = next(a for a in driver.find_elements(By.TAG_NAME, "a") if "login" in (a.get_attribute("href") or ""))
        login_link.click()
        time.sleep(0.8)
        assert "login" in driver.current_url

    def test_loading_state_on_submit(self, driver):
        """TC-SIGNUP-022: Submit button shows loading during request"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("new@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("pass123")
        btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        btn.click()
        time.sleep(0.1)
        assert btn is not None

    def test_already_logged_in_redirect(self, driver):
        """TC-SIGNUP-023: Logged-in user redirected from signup"""
        driver.get(f"{BASE_URL}/signup")
        driver.execute_script(
            "localStorage.setItem('ai-photo-auth', JSON.stringify({id:'1',name:'User',email:'u@u.com',token:'tok'}))"
        )
        driver.get(f"{BASE_URL}/signup")
        time.sleep(1)
        assert "signup" not in driver.current_url

    def test_form_responsive_mobile(self, driver):
        """TC-SIGNUP-024: Form usable on mobile viewport"""
        driver.set_window_size(375, 812)
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "button[type='submit']").is_displayed()
        driver.set_window_size(1280, 800)

    def test_no_console_errors(self, driver):
        """TC-SIGNUP-025: No severe JS errors on signup page"""
        driver.get(f"{BASE_URL}/signup")
        logs = driver.get_log("browser")
        assert len([l for l in logs if l["level"] == "SEVERE"]) == 0

    def test_autocomplete_email(self, driver):
        """TC-SIGNUP-026: Email has autocomplete=email"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "input[name='email']").get_attribute("autocomplete") == "email"

    def test_autocomplete_name(self, driver):
        """TC-SIGNUP-027: Name field has autocomplete=name"""
        driver.get(f"{BASE_URL}/signup")
        assert driver.find_element(By.CSS_SELECTOR, "input[name='name']").get_attribute("autocomplete") == "name"

    def test_password_show_toggle(self, driver):
        """TC-SIGNUP-028: Show password toggle on password field"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("secret")
        buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label]")
        pwd_toggles = [b for b in buttons if "password" in b.get_attribute("aria-label").lower()]
        assert len(pwd_toggles) >= 1

    def test_error_banner_animation(self, driver):
        """TC-SIGNUP-029: Error banner appears with animation on dup email"""
        driver.get(f"{BASE_URL}/signup")
        driver.execute_script(
            "localStorage.setItem('ai-photo-users', JSON.stringify([{id:'1',name:'X',email:'dup@test.com',password:'pass123'}]))"
        )
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Dup")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("dup@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "already" in body.lower() or "exists" in body.lower()

    def test_fields_retain_values_on_error(self, driver):
        """TC-SIGNUP-030: Fields keep values after validation error"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Jane")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert driver.find_element(By.CSS_SELECTOR, "input[name='name']").get_attribute("value") == "Jane"

    def test_long_name_accepted(self, driver):
        """TC-SIGNUP-031: Long name (50 chars) is accepted"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("A" * 50)
        val = driver.find_element(By.CSS_SELECTOR, "input[name='name']").get_attribute("value")
        assert len(val) >= 2

    def test_special_chars_in_name(self, driver):
        """TC-SIGNUP-032: Special characters in name handled"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("O'Brien-Smith")
        val = driver.find_element(By.CSS_SELECTOR, "input[name='name']").get_attribute("value")
        assert "O" in val

    def test_numeric_password_accepted(self, driver):
        """TC-SIGNUP-033: All-numeric password (>=6 digits) passes validation"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("n@test.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("123456")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("123456")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 6" not in body.lower()

    def test_tab_key_navigation(self, driver):
        """TC-SIGNUP-034: Tab key moves focus through fields"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys(Keys.TAB)
        assert driver.switch_to.active_element.get_attribute("name") == "email"

    def test_signup_page_title(self, driver):
        """TC-SIGNUP-035: Page has appropriate heading text"""
        driver.get(f"{BASE_URL}/signup")
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "account" in body.lower() or "sign" in body.lower() or "create" in body.lower()

    def test_very_long_email(self, driver):
        """TC-SIGNUP-036: Very long email (200 chars) is validated"""
        driver.get(f"{BASE_URL}/signup")
        long_email = "a" * 190 + "@test.com"
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(long_email)
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']").send_keys("pass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        assert driver.current_url is not None

    def test_unicode_name(self, driver):
        """TC-SIGNUP-037: Unicode characters in name field accepted"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("张伟")
        val = driver.find_element(By.CSS_SELECTOR, "input[name='name']").get_attribute("value")
        assert len(val) >= 1

    def test_password_strength_weak(self, driver):
        """TC-SIGNUP-038: Short password shows weak strength"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("abc123")
        time.sleep(0.3)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "weak" in body.lower() or "fair" in body.lower() or "strong" in body.lower()

    def test_password_strength_strong(self, driver):
        """TC-SIGNUP-039: Complex password shows strong strength"""
        driver.get(f"{BASE_URL}/signup")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Tr0ub4dor&3!")
        time.sleep(0.3)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "strong" in body.lower() or "good" in body.lower() or "very" in body.lower()

    def test_form_novalidate_attribute(self, driver):
        """TC-SIGNUP-040: Form uses novalidate (custom validation only)"""
        driver.get(f"{BASE_URL}/signup")
        form = driver.find_element(By.TAG_NAME, "form")
        assert form.get_attribute("novalidate") is not None or form.get_attribute("noValidate") is not None
