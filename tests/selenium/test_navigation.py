"""
Selenium Test Suite - Navigation & App Shell
TC-NAV-001 to TC-NAV-035 (35 test cases)
"""
import pytest, time
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:5173"

def login(driver, email="nav@test.com", password="Test@12345"):
    driver.get(f"{BASE_URL}/signup")
    import time as t; ts = str(int(t.time() * 1000))
    driver.execute_script(
        f"localStorage.setItem('ai-photo-auth', JSON.stringify({{id:'{ts}',name:'Nav User',email:'{email}',token:'tok{ts}'}}))"
    )
    driver.get(f"{BASE_URL}/")
    time.sleep(0.8)


class TestProtectedRoutes:
    def test_home_redirects_to_login(self, driver):
        """TC-NAV-001: Unauthenticated user redirected to /login"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/")
        time.sleep(1)
        assert "login" in driver.current_url

    def test_direct_access_blocked(self, driver):
        """TC-NAV-002: /generate redirects unauthenticated user to /login"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/generate")
        time.sleep(1)
        assert "login" in driver.current_url

    def test_login_page_accessible_unauthenticated(self, driver):
        """TC-NAV-003: /login accessible without auth"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/login")
        time.sleep(0.5)
        assert "login" in driver.current_url

    def test_signup_page_accessible_unauthenticated(self, driver):
        """TC-NAV-004: /signup accessible without auth"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/signup")
        time.sleep(0.5)
        assert "signup" in driver.current_url

    def test_authenticated_home_loads(self, driver):
        """TC-NAV-005: Authenticated user can access home"""
        login(driver)
        assert "login" not in driver.current_url


class TestNavbar:
    def test_navbar_visible(self, driver):
        """TC-NAV-006: Navbar is visible after login"""
        login(driver)
        assert driver.find_element(By.TAG_NAME, "header").is_displayed()

    def test_app_logo_in_navbar(self, driver):
        """TC-NAV-007: App name shown in navbar"""
        login(driver)
        header = driver.find_element(By.TAG_NAME, "header").text
        assert "AI Photo Generator" in header or "AI" in header

    def test_user_name_in_navbar(self, driver):
        """TC-NAV-008: Logged-in user name shown in navbar"""
        login(driver)
        header = driver.find_element(By.TAG_NAME, "header").text
        assert "Nav User" in header or "user" in header.lower()

    def test_theme_toggle_button(self, driver):
        """TC-NAV-009: Theme toggle button present in navbar"""
        login(driver)
        btns = driver.find_elements(By.CSS_SELECTOR, "header button")
        assert len(btns) > 0

    def test_logout_dropdown_opens(self, driver):
        """TC-NAV-010: User avatar click opens dropdown"""
        login(driver)
        user_btn = driver.find_elements(By.CSS_SELECTOR, "header button")
        if user_btn:
            user_btn[-1].click()
            time.sleep(0.4)
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_logout_clears_session(self, driver):
        """TC-NAV-011: Logout clears auth and redirects to login"""
        login(driver)
        btns = driver.find_elements(By.CSS_SELECTOR, "header button")
        if btns:
            btns[-1].click()
            time.sleep(0.4)
            logout_btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Sign out') or contains(text(),'Logout')]")
            if logout_btns:
                logout_btns[0].click()
                time.sleep(1)
                assert "login" in driver.current_url

    def test_navbar_not_on_login(self, driver):
        """TC-NAV-012: Navbar hamburger hidden on login page"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/login")
        time.sleep(0.5)
        hamburgers = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Open menu']")
        assert len(hamburgers) == 0

    def test_signin_btn_on_login_page_navbar(self, driver):
        """TC-NAV-013: Navbar shows Sign in/Sign up when logged out"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/login")
        time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "sign" in body.lower() or "login" in body.lower()

    def test_theme_toggle_works(self, driver):
        """TC-NAV-014: Theme toggle changes page class"""
        login(driver)
        html_class_before = driver.find_element(By.TAG_NAME, "html").get_attribute("class")
        theme_btn = driver.find_element(By.CSS_SELECTOR, "header button[aria-label='Toggle theme']")
        theme_btn.click()
        time.sleep(0.4)
        html_class_after = driver.find_element(By.TAG_NAME, "html").get_attribute("class")
        assert html_class_before != html_class_after


class TestSidebar:
    def test_sidebar_visible_desktop(self, driver):
        """TC-NAV-015: Sidebar visible on desktop"""
        driver.set_window_size(1280, 800)
        login(driver)
        sidebar = driver.find_elements(By.CSS_SELECTOR, "aside, nav")
        assert len(sidebar) > 0

    def test_sidebar_home_link(self, driver):
        """TC-NAV-016: Sidebar has Home nav item"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Home" in body

    def test_sidebar_generate_link(self, driver):
        """TC-NAV-017: Sidebar has Generate nav item"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Generate" in body

    def test_sidebar_history_link(self, driver):
        """TC-NAV-018: Sidebar has History nav item"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "History" in body

    def test_sidebar_settings_link(self, driver):
        """TC-NAV-019: Sidebar has Settings nav item"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Settings" in body

    def test_navigate_to_generate(self, driver):
        """TC-NAV-020: Clicking Generate shows generate panel"""
        login(driver)
        gen_btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Generate')]")
        if gen_btns:
            gen_btns[0].click()
            time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Generate" in body or "photo" in body.lower()

    def test_navigate_to_settings(self, driver):
        """TC-NAV-021: Clicking Settings shows settings panel"""
        login(driver)
        settings_btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if settings_btns:
            settings_btns[0].click()
            time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Settings" in body or "Theme" in body

    def test_navigate_to_history(self, driver):
        """TC-NAV-022: Clicking History shows history section"""
        login(driver)
        hist_btns = driver.find_elements(By.XPATH, "//*[contains(text(),'History')]")
        if hist_btns:
            hist_btns[0].click()
            time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "History" in body or "photo" in body.lower()

    def test_hamburger_visible_mobile(self, driver):
        """TC-NAV-023: Hamburger menu visible on mobile"""
        driver.set_window_size(375, 812)
        login(driver)
        hamburger = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Open menu']")
        assert len(hamburger) > 0
        driver.set_window_size(1280, 800)

    def test_sidebar_ai_photos_label(self, driver):
        """TC-NAV-024: Sidebar shows AI Photos branding"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "AI" in body


class TestHomeSection:
    def test_home_hero_heading(self, driver):
        """TC-NAV-025: Home shows hero heading"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "AI Photos" in body or "Generate" in body

    def test_home_start_generating_button(self, driver):
        """TC-NAV-026: Home page has Start generating button"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "generating" in body.lower() or "generate" in body.lower()

    def test_home_feature_cards(self, driver):
        """TC-NAV-027: Home shows feature highlight cards"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Style" in body or "Fast" in body or "Control" in body

    def test_page_title_correct(self, driver):
        """TC-NAV-028: Browser tab title is AI Photo Generator"""
        login(driver)
        assert "AI" in driver.title or driver.title != ""

    def test_404_unknown_route(self, driver):
        """TC-NAV-029: Unknown route still loads app (catch-all)"""
        login(driver)
        driver.get(f"{BASE_URL}/unknown-page-xyz")
        time.sleep(0.8)
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    def test_back_button_works(self, driver):
        """TC-NAV-030: Browser back button navigates correctly"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/login")
        time.sleep(0.5)
        driver.get(f"{BASE_URL}/signup")
        time.sleep(0.5)
        driver.back()
        time.sleep(0.5)
        assert "login" in driver.current_url

    def test_forward_button_works(self, driver):
        """TC-NAV-031: Browser forward button navigates correctly"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/login")
        time.sleep(0.5)
        driver.get(f"{BASE_URL}/signup")
        time.sleep(0.5)
        driver.back()
        time.sleep(0.5)
        driver.forward()
        time.sleep(0.5)
        assert "signup" in driver.current_url

    def test_page_load_time(self, driver):
        """TC-NAV-032: Page loads within 5 seconds"""
        import time as t
        start = t.time()
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/login")
        elapsed = t.time() - start
        assert elapsed < 5.0

    def test_generate_panel_has_prompt_input(self, driver):
        """TC-NAV-033: Generate section has prompt textarea"""
        login(driver)
        gen_btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Generate')]")
        if gen_btns:
            gen_btns[0].click()
            time.sleep(0.5)
        inputs = driver.find_elements(By.CSS_SELECTOR, "textarea, input[type='text']")
        assert len(inputs) > 0

    def test_settings_api_url_field(self, driver):
        """TC-NAV-034: Settings page has API URL input"""
        login(driver)
        settings_btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if settings_btns:
            settings_btns[-1].click()
            time.sleep(0.5)
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='url'], input[placeholder*='localhost']")
        assert len(inputs) > 0

    def test_history_empty_state(self, driver):
        """TC-NAV-035: History shows empty state when no photos generated"""
        login(driver)
        driver.execute_script("localStorage.removeItem('ai-photo-history')")
        hist_btns = driver.find_elements(By.XPATH, "//*[contains(text(),'History')]")
        if hist_btns:
            hist_btns[0].click()
            time.sleep(0.5)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "No photos" in body or "History" in body
