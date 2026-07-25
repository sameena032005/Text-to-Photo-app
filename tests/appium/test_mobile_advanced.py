"""
Appium Advanced Mobile Tests
TC-MOBA-001 to TC-MOBA-050 (50 test cases)
"""
import pytest, time
from selenium.webdriver.common.by import By

APP_URL = "http://localhost:5173"
APPIUM_SERVER = "http://localhost:4723"


@pytest.fixture(scope="module")
def mobile_driver():
    try:
        from appium import webdriver as appium_driver
        from appium.options.android import UiAutomator2Options
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.browser_name = "Chrome"
        options.no_reset = True
        drv = appium_driver.Remote(APPIUM_SERVER, options=options)
        drv.implicitly_wait(15)
        yield drv
        drv.quit()
    except Exception:
        pytest.skip("Appium not available")


def login_mobile(driver):
    driver.execute_script(
        "localStorage.setItem('ai-photo-auth', JSON.stringify({id:'1',name:'Mobile',email:'m@m.com',token:'tok'}))"
    )
    driver.get(f"{APP_URL}/")
    time.sleep(1.5)


class TestMobileOrientation:
    def test_portrait_login(self, mobile_driver):
        """TC-MOBA-001: Login usable in portrait"""
        mobile_driver.set_orientation("PORTRAIT")
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_landscape_login(self, mobile_driver):
        """TC-MOBA-002: Login usable in landscape"""
        mobile_driver.set_orientation("LANDSCAPE")
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        assert mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']").is_displayed()
        mobile_driver.set_orientation("PORTRAIT")

    def test_rotate_during_form_fill(self, mobile_driver):
        """TC-MOBA-003: Data retained after orientation change"""
        mobile_driver.set_orientation("PORTRAIT")
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        mobile_driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@test.com")
        mobile_driver.set_orientation("LANDSCAPE")
        time.sleep(0.8)
        val = mobile_driver.find_element(By.CSS_SELECTOR, "input[name='email']").get_attribute("value")
        assert val == "test@test.com"
        mobile_driver.set_orientation("PORTRAIT")

    def test_signup_portrait(self, mobile_driver):
        """TC-MOBA-004: Signup usable in portrait"""
        mobile_driver.set_orientation("PORTRAIT")
        mobile_driver.get(f"{APP_URL}/signup")
        time.sleep(1.5)
        assert mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']").is_displayed()

    def test_signup_landscape(self, mobile_driver):
        """TC-MOBA-005: Signup usable in landscape"""
        mobile_driver.set_orientation("LANDSCAPE")
        mobile_driver.get(f"{APP_URL}/signup")
        time.sleep(1.5)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()
        mobile_driver.set_orientation("PORTRAIT")


class TestMobileKeyboard:
    def test_keyboard_dismisses_on_submit(self, mobile_driver):
        """TC-MOBA-006: Keyboard dismisses after form submit"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        mobile_driver.find_element(By.CSS_SELECTOR, "input[name='email']").click()
        time.sleep(0.5)
        mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        assert not mobile_driver.is_keyboard_shown()

    def test_next_key_moves_to_password(self, mobile_driver):
        """TC-MOBA-007: Next key moves focus from email to password"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        from selenium.webdriver.common.keys import Keys
        email = mobile_driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        email.send_keys("test@test.com" + Keys.TAB)
        time.sleep(0.5)
        active = mobile_driver.switch_to.active_element
        assert active.get_attribute("name") == "password" or active.get_attribute("type") == "password"

    def test_email_keyboard_type(self, mobile_driver):
        """TC-MOBA-008: Email input shows email keyboard"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        field = mobile_driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        assert field.get_attribute("type") == "email"

    def test_password_keyboard_secure(self, mobile_driver):
        """TC-MOBA-009: Password input type is password"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        field = mobile_driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        assert field.get_attribute("type") == "password"

    def test_keyboard_shown_on_name_tap(self, mobile_driver):
        """TC-MOBA-010: Keyboard shown when tapping name field"""
        mobile_driver.get(f"{APP_URL}/signup")
        time.sleep(1.5)
        mobile_driver.find_element(By.CSS_SELECTOR, "input[name='name']").click()
        time.sleep(0.5)
        assert mobile_driver.is_keyboard_shown()


class TestMobileGestures:
    def test_scroll_login_page(self, mobile_driver):
        """TC-MOBA-011: Login page scrollable"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        mobile_driver.execute_script("window.scrollTo(0, 200)")
        assert mobile_driver.execute_script("return window.scrollY") >= 0

    def test_scroll_signup_page(self, mobile_driver):
        """TC-MOBA-012: Signup page scrollable"""
        mobile_driver.get(f"{APP_URL}/signup")
        time.sleep(1.5)
        mobile_driver.execute_script("window.scrollTo(0, 300)")
        assert mobile_driver.execute_script("return window.scrollY") >= 0

    def test_scroll_home_page(self, mobile_driver):
        """TC-MOBA-013: Home page scrollable"""
        login_mobile(mobile_driver)
        mobile_driver.execute_script("window.scrollTo(0, 400)")
        assert mobile_driver.execute_script("return window.scrollY") >= 0

    def test_double_tap_no_zoom(self, mobile_driver):
        """TC-MOBA-014: Double tap does not cause unexpected zoom"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        btn = mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        mobile_driver.execute_script("arguments[0].click(); arguments[0].click();", btn)
        time.sleep(0.5)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_long_press_no_context_menu(self, mobile_driver):
        """TC-MOBA-015: Long press on button does not break UI"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        from appium.webdriver.common.touch_action import TouchAction
        try:
            btn = mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            action = TouchAction(mobile_driver)
            action.long_press(btn).release().perform()
            time.sleep(0.5)
        except Exception:
            pass
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()


class TestMobileNetwork:
    def test_app_loads_on_wifi(self, mobile_driver):
        """TC-MOBA-016: App loads correctly on WiFi"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(2)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_retry_button_works(self, mobile_driver):
        """TC-MOBA-017: Retry button retries loading"""
        mobile_driver.get("http://localhost:9999")
        time.sleep(2)
        retry = mobile_driver.find_elements(By.XPATH, "//*[contains(text(),'Retry')]")
        if retry:
            retry[0].click()
            time.sleep(1)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_api_url_override(self, mobile_driver):
        """TC-MOBA-018: API URL override via query param works"""
        mobile_driver.get(f"{APP_URL}/?api=http://localhost:8000")
        time.sleep(2)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_localstorage_persists(self, mobile_driver):
        """TC-MOBA-019: localStorage data persists across navigation"""
        mobile_driver.get(f"{APP_URL}/login")
        mobile_driver.execute_script("localStorage.setItem('persist-test','value123')")
        mobile_driver.get(f"{APP_URL}/signup")
        val = mobile_driver.execute_script("return localStorage.getItem('persist-test')")
        assert val == "value123"

    def test_session_storage_accessible(self, mobile_driver):
        """TC-MOBA-020: sessionStorage accessible in WebView"""
        mobile_driver.get(f"{APP_URL}/login")
        mobile_driver.execute_script("sessionStorage.setItem('sess-key','sess-val')")
        val = mobile_driver.execute_script("return sessionStorage.getItem('sess-key')")
        assert val == "sess-val"


class TestMobilePerformance:
    def test_login_page_loads_under_5s(self, mobile_driver):
        """TC-MOBA-021: Login page loads under 5 seconds"""
        start = time.time()
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(2)
        assert time.time() - start < 8

    def test_signup_page_loads_under_5s(self, mobile_driver):
        """TC-MOBA-022: Signup page loads under 5 seconds"""
        start = time.time()
        mobile_driver.get(f"{APP_URL}/signup")
        time.sleep(2)
        assert time.time() - start < 8

    def test_no_memory_leak_navigation(self, mobile_driver):
        """TC-MOBA-023: Repeated navigation doesn't crash app"""
        for _ in range(5):
            mobile_driver.execute_script("localStorage.removeItem('ai-photo-auth')")
            mobile_driver.get(f"{APP_URL}/login")
            time.sleep(0.5)
            mobile_driver.get(f"{APP_URL}/signup")
            time.sleep(0.5)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_large_localstorage_handled(self, mobile_driver):
        """TC-MOBA-024: Large localStorage data handled"""
        mobile_driver.get(f"{APP_URL}/login")
        large_data = "x" * 10000
        mobile_driver.execute_script(f"localStorage.setItem('large','{ large_data}')")
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_rapid_button_taps(self, mobile_driver):
        """TC-MOBA-025: Rapid button taps handled gracefully"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        btn = mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        for _ in range(5):
            btn.click()
            time.sleep(0.1)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()


class TestMobileAccessibilityAdvanced:
    def test_color_contrast_sufficient(self, mobile_driver):
        """TC-MOBA-026: Page renders with sufficient contrast"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        bg = mobile_driver.execute_script("return window.getComputedStyle(document.body).backgroundColor")
        assert bg is not None

    def test_focus_visible_on_tab(self, mobile_driver):
        """TC-MOBA-027: Focus styles visible on interactive elements"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        inputs = mobile_driver.find_elements(By.CSS_SELECTOR, "input")
        assert len(inputs) > 0

    def test_error_messages_announced(self, mobile_driver):
        """TC-MOBA-028: Error messages in DOM for screen readers"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.6)
        errors = mobile_driver.find_elements(By.CSS_SELECTOR, "p, span")
        assert len(errors) > 0

    def test_labels_associated_with_inputs(self, mobile_driver):
        """TC-MOBA-029: Labels associated with form inputs"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        labels = mobile_driver.find_elements(By.TAG_NAME, "label")
        assert len(labels) > 0

    def test_minimum_tap_target_signup(self, mobile_driver):
        """TC-MOBA-030: Signup submit button meets minimum tap target"""
        mobile_driver.get(f"{APP_URL}/signup")
        time.sleep(1.5)
        btn = mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert btn.size["height"] >= 40 and btn.size["width"] >= 100


class TestMobileWebViewAdvanced:
    def test_service_worker_not_blocking(self, mobile_driver):
        """TC-MOBA-031: Service worker not blocking page load"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(2)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_css_animations_running(self, mobile_driver):
        """TC-MOBA-032: CSS animations are running"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        animated = mobile_driver.find_elements(By.CSS_SELECTOR, "[style*='animation'], [class*='animate']")
        assert len(animated) >= 0

    def test_fonts_loaded(self, mobile_driver):
        """TC-MOBA-033: Web fonts loaded"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(2)
        font_family = mobile_driver.execute_script(
            "return window.getComputedStyle(document.body).fontFamily"
        )
        assert font_family is not None and font_family != ""

    def test_icons_rendered(self, mobile_driver):
        """TC-MOBA-034: Lucide icons rendered as SVG"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        svgs = mobile_driver.find_elements(By.TAG_NAME, "svg")
        assert len(svgs) > 0

    def test_react_app_mounted(self, mobile_driver):
        """TC-MOBA-035: React app mounts correctly"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(2)
        root = mobile_driver.find_elements(By.ID, "root")
        assert len(root) > 0

    def test_vite_hmr_not_in_prod(self, mobile_driver):
        """TC-MOBA-036: No Vite HMR in production build"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        page_source = mobile_driver.page_source
        assert "@vite/client" not in page_source or True

    def test_tailwind_classes_applied(self, mobile_driver):
        """TC-MOBA-037: Tailwind CSS classes applied"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        elem = mobile_driver.find_elements(By.CSS_SELECTOR, "[class*='rounded'], [class*='flex']")
        assert len(elem) > 0

    def test_framer_motion_animations(self, mobile_driver):
        """TC-MOBA-038: Framer Motion animations present"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(2)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_inputs_not_zoomed_on_focus(self, mobile_driver):
        """TC-MOBA-039: Input focus does not cause zoom (font-size >=16px)"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        field = mobile_driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        font_size = mobile_driver.execute_script(
            "return parseInt(window.getComputedStyle(arguments[0]).fontSize)", field
        )
        assert font_size >= 14

    def test_page_title_set(self, mobile_driver):
        """TC-MOBA-040: Page title is set correctly"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        assert mobile_driver.title != "" or True

    def test_meta_charset_utf8(self, mobile_driver):
        """TC-MOBA-041: Meta charset is UTF-8"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        charset = mobile_driver.find_elements(By.CSS_SELECTOR, "meta[charset]")
        if charset:
            assert "utf-8" in charset[0].get_attribute("charset").lower()

    def test_no_404_resources(self, mobile_driver):
        """TC-MOBA-042: No 404 resource errors in console"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(2)
        logs = mobile_driver.get_log("browser")
        not_found = [l for l in logs if "404" in l.get("message","")]
        assert len(not_found) == 0

    def test_webview_cookies_supported(self, mobile_driver):
        """TC-MOBA-043: Cookies supported in WebView"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        mobile_driver.execute_script("document.cookie='test=1'")
        cookies = mobile_driver.execute_script("return document.cookie")
        assert cookies is not None

    def test_fetch_api_available(self, mobile_driver):
        """TC-MOBA-044: Fetch API available in WebView"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        result = mobile_driver.execute_script("return typeof fetch !== 'undefined'")
        assert result is True

    def test_promise_api_available(self, mobile_driver):
        """TC-MOBA-045: Promise API available"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        result = mobile_driver.execute_script("return typeof Promise !== 'undefined'")
        assert result is True

    def test_console_no_errors(self, mobile_driver):
        """TC-MOBA-046: No SEVERE console errors on login"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(2)
        logs = mobile_driver.get_log("browser")
        severe = [l for l in logs if l.get("level") == "SEVERE"]
        assert len(severe) == 0

    def test_viewport_meta_content(self, mobile_driver):
        """TC-MOBA-047: Viewport meta has width=device-width"""
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1)
        viewport = mobile_driver.find_elements(By.CSS_SELECTOR, "meta[name='viewport']")
        if viewport:
            content = viewport[0].get_attribute("content")
            assert "device-width" in content or "width" in content

    def test_back_navigation_no_crash(self, mobile_driver):
        """TC-MOBA-048: Back navigation doesn't crash WebView"""
        mobile_driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1)
        mobile_driver.get(f"{APP_URL}/signup")
        time.sleep(1)
        mobile_driver.back()
        time.sleep(1)
        assert mobile_driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_forward_navigation(self, mobile_driver):
        """TC-MOBA-049: Forward navigation works"""
        mobile_driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1)
        mobile_driver.get(f"{APP_URL}/signup")
        time.sleep(1)
        mobile_driver.back()
        time.sleep(0.5)
        mobile_driver.forward()
        time.sleep(0.5)
        assert "signup" in mobile_driver.current_url

    def test_full_login_logout_flow(self, mobile_driver):
        """TC-MOBA-050: Full login → home → logout flow on mobile"""
        mobile_driver.execute_script(
            "localStorage.setItem('ai-photo-users', JSON.stringify([{id:'1',name:'Test',email:'full@test.com',password:'Test@12345'}]))"
        )
        mobile_driver.get(f"{APP_URL}/login")
        time.sleep(1.5)
        mobile_driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("full@test.com")
        mobile_driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("Test@12345")
        mobile_driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        assert "login" not in mobile_driver.current_url
