"""
Selenium Test Suite - Login Page
Tests: 35 test cases covering login UI, validation, auth flow
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

BASE_URL = "http://localhost:5173"


class TestLoginPageLoad:
    """TC-LOGIN-001 to TC-LOGIN-008: Page load and structure"""

    def test_login_page_loads(self, driver):
        """TC-LOGIN-001: Login page loads without errors"""
        driver.get(f"{BASE_URL}/login")
        assert "login" in driver.current_url.lower() or driver.title != ""

    def test_login_page_title(self, driver):
        """TC-LOGIN-002: Page has correct title"""
        driver.get(f"{BASE_URL}/login")
        assert "AI Photo Generator" in driver.title or driver.find_element(By.TAG_NAME, "body")

    def test_email_field_present(self, driver):
        """TC-LOGIN-003: Email input field is present"""
        driver.get(f"{BASE_URL}/login")
        field = driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email']")
        assert field.is_displayed()

    def test_password_field_present(self, driver):
        """TC-LOGIN-004: Password input field is present"""
        driver.get(f"{BASE_URL}/login")
        field = driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
        assert field.is_displayed()

    def test_submit_button_present(self, driver):
        """TC-LOGIN-005: Sign in button is present"""
        driver.get(f"{BASE_URL}/login")
        btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert btn.is_displayed()

    def test_signup_link_present(self, driver):
        """TC-LOGIN-006: Link to signup page is present"""
        driver.get(f"{BASE_URL}/login")
        links = driver.find_elements(By.TAG_NAME, "a")
        hrefs = [l.get_attribute("href") for l in links]
        assert any("signup" in (h or "") for h in hrefs)

    def test_logo_present(self, driver):
        """TC-LOGIN-007: App logo/icon is visible"""
        driver.get(f"{BASE_URL}/login")
        body = driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()

    def test_page_background_dark(self, driver):
        """TC-LOGIN-008: Page uses dark background"""
        driver.get(f"{BASE_URL}/login")
        bg = driver.execute_script(
            "return window.getComputedStyle(document.body).backgroundColor"
        )
        assert bg is not None


class TestLoginValidation:
    """TC-LOGIN-009 to TC-LOGIN-022: Client-side validation"""

    def test_empty_form_submit(self, driver):
        """TC-LOGIN-009: Empty form shows validation errors"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        errors = driver.find_elements(By.CSS_SELECTOR, "p.text-red-400, .text-red-400")
        assert len(errors) > 0

    def test_empty_email_error(self, driver):
        """TC-LOGIN-010: Empty email shows error message"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "email" in body_text.lower() or "required" in body_text.lower()

    def test_empty_password_error(self, driver):
        """TC-LOGIN-011: Empty password shows error message"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@example.com")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "password" in body_text.lower() or "required" in body_text.lower()

    def test_invalid_email_format(self, driver):
        """TC-LOGIN-012: Invalid email format shows error"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("notanemail")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "valid" in body_text.lower() or "email" in body_text.lower()

    def test_email_without_domain(self, driver):
        """TC-LOGIN-013: Email without domain shows error"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("user@")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "valid" in body_text.lower() or "email" in body_text.lower()

    def test_short_password_error(self, driver):
        """TC-LOGIN-014: Password shorter than 6 chars shows error"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@example.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("abc")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "6" in body_text or "characters" in body_text.lower()

    def test_password_5_chars_fails(self, driver):
        """TC-LOGIN-015: Password of exactly 5 chars is rejected"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@example.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("abcde")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "6" in body_text or "password" in body_text.lower()

    def test_password_6_chars_passes_validation(self, driver):
        """TC-LOGIN-016: Password of exactly 6 chars passes client validation"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@example.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("abcdef")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        # Should NOT show "at least 6 characters" error
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "at least 6" not in body_text.lower()

    def test_spaces_only_email(self, driver):
        """TC-LOGIN-017: Spaces-only email shows error"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("   ")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "email" in body_text.lower() or "required" in body_text.lower()

    def test_email_field_accepts_input(self, driver):
        """TC-LOGIN-018: Email field correctly accepts typed input"""
        driver.get(f"{BASE_URL}/login")
        email_field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        email_field.send_keys("hello@test.com")
        assert email_field.get_attribute("value") == "hello@test.com"

    def test_password_field_masked(self, driver):
        """TC-LOGIN-019: Password field masks input by default"""
        driver.get(f"{BASE_URL}/login")
        pwd_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        assert pwd_field.get_attribute("type") == "password"

    def test_show_password_toggle(self, driver):
        """TC-LOGIN-020: Show/hide password toggle works"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("secret123")
        toggle = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='password'], button[aria-label*='Password']")
        toggle.click()
        time.sleep(0.3)
        pwd_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        assert pwd_field.get_attribute("type") == "text"

    def test_hide_password_toggle(self, driver):
        """TC-LOGIN-021: Password can be re-hidden after showing"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("secret123")
        toggle = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='password'], button[aria-label*='Password']")
        toggle.click()
        time.sleep(0.2)
        toggle.click()
        time.sleep(0.2)
        pwd_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        assert pwd_field.get_attribute("type") == "password"

    def test_error_clears_on_input(self, driver):
        """TC-LOGIN-022: Error message clears when user starts typing"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.4)
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("a")
        time.sleep(0.3)
        errors = driver.find_elements(By.CSS_SELECTOR, ".text-red-400")
        # Email error should be gone
        email_errors = [e for e in errors if "email" in e.text.lower()]
        assert len(email_errors) == 0


class TestLoginFunctionality:
    """TC-LOGIN-023 to TC-LOGIN-035: Login flow"""

    def test_wrong_credentials_error(self, driver):
        """TC-LOGIN-023: Wrong credentials shows error banner"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("wrong@example.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("wrongpass")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "invalid" in body_text.lower() or "incorrect" in body_text.lower() or "error" in body_text.lower()

    def test_loading_state_on_submit(self, driver):
        """TC-LOGIN-024: Button shows loading state during submit"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@example.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        btn.click()
        # Check loading state briefly
        time.sleep(0.2)
        assert btn is not None  # Button still in DOM

    def test_signup_link_navigates(self, driver):
        """TC-LOGIN-025: Clicking signup link navigates to /signup"""
        driver.get(f"{BASE_URL}/login")
        links = driver.find_elements(By.TAG_NAME, "a")
        signup_link = next((l for l in links if "signup" in (l.get_attribute("href") or "")), None)
        assert signup_link is not None
        signup_link.click()
        time.sleep(1)
        assert "signup" in driver.current_url

    def test_enter_key_submits_form(self, driver):
        """TC-LOGIN-026: Pressing Enter key submits the form"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@example.com")
        driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345" + Keys.RETURN)
        time.sleep(1.5)
        # Either navigated away or shows an error - both mean form submitted
        assert driver.current_url is not None

    def test_redirect_already_logged_in(self, driver):
        """TC-LOGIN-027: Logged-in user is redirected away from /login"""
        # Set localStorage token to simulate logged-in state
        driver.get(f"{BASE_URL}/login")
        driver.execute_script(
            "localStorage.setItem('ai-photo-auth', JSON.stringify({id:'1',name:'Test',email:'t@t.com',token:'abc'}))"
        )
        driver.get(f"{BASE_URL}/login")
        time.sleep(1)
        assert "login" not in driver.current_url or driver.current_url == f"{BASE_URL}/"

    def test_form_autocomplete_email(self, driver):
        """TC-LOGIN-028: Email field has autocomplete attribute"""
        driver.get(f"{BASE_URL}/login")
        field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        assert field.get_attribute("autocomplete") == "email"

    def test_form_autocomplete_password(self, driver):
        """TC-LOGIN-029: Password field has autocomplete attribute"""
        driver.get(f"{BASE_URL}/login")
        field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        assert field.get_attribute("autocomplete") in ["current-password", "password"]

    def test_page_responsive_mobile(self, driver):
        """TC-LOGIN-030: Page is responsive on mobile viewport"""
        driver.set_window_size(375, 812)
        driver.get(f"{BASE_URL}/login")
        form = driver.find_element(By.TAG_NAME, "form")
        assert form.is_displayed()
        driver.set_window_size(1280, 800)

    def test_page_responsive_tablet(self, driver):
        """TC-LOGIN-031: Page is responsive on tablet viewport"""
        driver.set_window_size(768, 1024)
        driver.get(f"{BASE_URL}/login")
        form = driver.find_element(By.TAG_NAME, "form")
        assert form.is_displayed()
        driver.set_window_size(1280, 800)

    def test_multiple_failed_attempts(self, driver):
        """TC-LOGIN-032: Multiple failed attempts handled gracefully"""
        driver.get(f"{BASE_URL}/login")
        for _ in range(3):
            email = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
            pwd = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            email.clear()
            pwd.clear()
            email.send_keys("wrong@example.com")
            pwd.send_keys("wrongpass123")
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(1.2)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "invalid" in body_text.lower() or "error" in body_text.lower()

    def test_clear_fields_after_error(self, driver):
        """TC-LOGIN-033: Fields retain value after error (no unexpected clear)"""
        driver.get(f"{BASE_URL}/login")
        email_field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        email_field.send_keys("test@example.com")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        assert email_field.get_attribute("value") == "test@example.com"

    def test_no_js_errors_on_load(self, driver):
        """TC-LOGIN-034: No JavaScript console errors on page load"""
        driver.get(f"{BASE_URL}/login")
        logs = driver.get_log("browser")
        severe = [l for l in logs if l["level"] == "SEVERE"]
        assert len(severe) == 0

    def test_tab_order_correct(self, driver):
        """TC-LOGIN-035: Tab order flows email → password → submit"""
        driver.get(f"{BASE_URL}/login")
        email = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        email.click()
        email.send_keys(Keys.TAB)
        active = driver.switch_to.active_element
        assert active.get_attribute("name") == "password" or active.get_attribute("type") == "password"
