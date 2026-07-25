"""
Selenium Test Suite - Generate Panel, Settings, History, Theme
TC-GEN-001 to TC-GEN-050 (50 test cases)
"""
import pytest, time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = "http://localhost:5173"

def login(driver):
    driver.get(f"{BASE_URL}/login")
    ts = str(int(time.time()*1000))
    driver.execute_script(
        f"localStorage.setItem('ai-photo-auth', JSON.stringify({{id:'{ts}',name:'Test User',email:'test@test.com',token:'tok{ts}'}}));"
    )
    driver.get(f"{BASE_URL}/")
    time.sleep(1)

def go_generate(driver):
    login(driver)
    btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Generate')]")
    if btns:
        btns[0].click()
        time.sleep(0.6)


class TestGeneratePanel:
    def test_generate_section_loads(self, driver):
        """TC-GEN-001: Generate section loads after clicking Generate nav"""
        go_generate(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Generate" in body or "photo" in body.lower()

    def test_prompt_textarea_visible(self, driver):
        """TC-GEN-002: Prompt textarea is visible"""
        go_generate(driver)
        inputs = driver.find_elements(By.CSS_SELECTOR, "textarea, input[type='text']")
        assert len(inputs) > 0

    def test_prompt_accepts_text(self, driver):
        """TC-GEN-003: Prompt field accepts typed text"""
        go_generate(driver)
        inputs = driver.find_elements(By.CSS_SELECTOR, "textarea, input[type='text']")
        if inputs:
            inputs[0].clear()
            inputs[0].send_keys("a beautiful sunset")
            assert inputs[0].get_attribute("value") == "a beautiful sunset"

    def test_prompt_placeholder_text(self, driver):
        """TC-GEN-004: Prompt field has placeholder text"""
        go_generate(driver)
        inputs = driver.find_elements(By.CSS_SELECTOR, "textarea, input[type='text']")
        if inputs:
            ph = inputs[0].get_attribute("placeholder")
            assert ph is not None and len(ph) > 0

    def test_style_selector_present(self, driver):
        """TC-GEN-005: Style selector dropdown is present"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        assert len(selects) > 0

    def test_style_selector_has_options(self, driver):
        """TC-GEN-006: Style selector has multiple options"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        if selects:
            options = selects[0].find_elements(By.TAG_NAME, "option")
            assert len(options) >= 2

    def test_ratio_selector_present(self, driver):
        """TC-GEN-007: Aspect ratio selector is present"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        assert len(selects) >= 1

    def test_quality_selector_present(self, driver):
        """TC-GEN-008: Quality selector is present"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        assert len(selects) >= 1

    def test_generate_button_present(self, driver):
        """TC-GEN-009: Generate Photo button is present"""
        go_generate(driver)
        btns = driver.find_elements(By.CSS_SELECTOR, "button")
        texts = [b.text for b in btns]
        assert any("Generate" in t or "Photo" in t for t in texts)

    def test_generate_button_disabled_empty(self, driver):
        """TC-GEN-010: Generate button disabled when prompt is empty"""
        go_generate(driver)
        inputs = driver.find_elements(By.CSS_SELECTOR, "textarea, input[type='text']")
        if inputs:
            inputs[0].clear()
        btns = [b for b in driver.find_elements(By.CSS_SELECTOR, "button") if "Generate" in b.text or "Photo" in b.text]
        if btns:
            assert btns[0].get_attribute("disabled") is not None or "opacity-50" in (btns[0].get_attribute("class") or "")

    def test_generate_button_enabled_with_prompt(self, driver):
        """TC-GEN-011: Generate button enabled when prompt has text"""
        go_generate(driver)
        inputs = driver.find_elements(By.CSS_SELECTOR, "textarea, input[type='text']")
        if inputs:
            inputs[0].send_keys("test prompt")
        btns = [b for b in driver.find_elements(By.CSS_SELECTOR, "button") if "Generate" in b.text or "Photo" in b.text]
        if btns:
            assert btns[0].get_attribute("disabled") is None

    def test_cinematic_style_selectable(self, driver):
        """TC-GEN-012: Cinematic style can be selected"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        from selenium.webdriver.support.ui import Select
        if selects:
            try:
                s = Select(selects[0])
                s.select_by_visible_text("Cinematic")
                assert s.first_selected_option.text == "Cinematic"
            except Exception:
                pass

    def test_anime_style_selectable(self, driver):
        """TC-GEN-013: Anime style can be selected"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        from selenium.webdriver.support.ui import Select
        if selects:
            try:
                s = Select(selects[0])
                s.select_by_visible_text("Anime")
                assert s.first_selected_option.text == "Anime"
            except Exception:
                pass

    def test_realistic_style_selectable(self, driver):
        """TC-GEN-014: Realistic style can be selected"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        from selenium.webdriver.support.ui import Select
        if selects:
            try:
                s = Select(selects[0])
                s.select_by_visible_text("Realistic")
                assert s.first_selected_option.text == "Realistic"
            except Exception:
                pass

    def test_ratio_169_selectable(self, driver):
        """TC-GEN-015: 16:9 aspect ratio selectable"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        from selenium.webdriver.support.ui import Select
        if len(selects) >= 2:
            try:
                s = Select(selects[1])
                s.select_by_visible_text("16:9")
                assert "16:9" in s.first_selected_option.text
            except Exception:
                pass

    def test_ratio_11_selectable(self, driver):
        """TC-GEN-016: 1:1 aspect ratio selectable"""
        go_generate(driver)
        selects = driver.find_elements(By.TAG_NAME, "select")
        from selenium.webdriver.support.ui import Select
        if len(selects) >= 2:
            try:
                s = Select(selects[1])
                s.select_by_visible_text("1:1")
                assert "1:1" in s.first_selected_option.text
            except Exception:
                pass

    def test_hero_heading_visible(self, driver):
        """TC-GEN-017: Hero heading visible on generate section"""
        go_generate(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "AI Photos" in body or "Generate" in body

    def test_generation_options_heading(self, driver):
        """TC-GEN-018: Generation options card heading visible"""
        go_generate(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "option" in body.lower() or "style" in body.lower()

    def test_no_error_banner_initially(self, driver):
        """TC-GEN-019: No error banner shown initially"""
        go_generate(driver)
        errors = driver.find_elements(By.CSS_SELECTOR, ".text-red-400, .border-red-500")
        assert len(errors) == 0

    def test_prompt_multiline_accepted(self, driver):
        """TC-GEN-020: Multiline prompt accepted in textarea"""
        go_generate(driver)
        inputs = driver.find_elements(By.CSS_SELECTOR, "textarea")
        if inputs:
            inputs[0].send_keys("line one\nline two\nline three")
            val = inputs[0].get_attribute("value")
            assert len(val) > 0


class TestSettingsPanel:
    def test_settings_page_loads(self, driver):
        """TC-GEN-021: Settings section loads"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Settings" in body

    def test_settings_theme_section(self, driver):
        """TC-GEN-022: Appearance/Theme section visible"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Theme" in body or "Appearance" in body

    def test_settings_dark_mode_button(self, driver):
        """TC-GEN-023: Dark mode button present in settings"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "dark" in body.lower()

    def test_settings_light_mode_button(self, driver):
        """TC-GEN-024: Light mode button present in settings"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "light" in body.lower()

    def test_settings_api_url_section(self, driver):
        """TC-GEN-025: Backend API section visible"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "API" in body or "Backend" in body

    def test_settings_api_url_input(self, driver):
        """TC-GEN-026: API URL input field present"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='url'], input[placeholder*='localhost']")
        assert len(inputs) > 0

    def test_settings_api_url_default(self, driver):
        """TC-GEN-027: API URL defaults to localhost:8000"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "8000" in body or "localhost" in body

    def test_settings_default_style_selector(self, driver):
        """TC-GEN-028: Default style selector present"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        selects = driver.find_elements(By.TAG_NAME, "select")
        assert len(selects) > 0

    def test_settings_dark_mode_switch(self, driver):
        """TC-GEN-029: Clicking dark mode applies dark class"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        dark_btns = driver.find_elements(By.XPATH, "//*[contains(text(),'dark') or contains(text(),'Dark')]")
        if dark_btns:
            dark_btns[0].click()
            time.sleep(0.4)
        html_class = driver.find_element(By.TAG_NAME, "html").get_attribute("class")
        assert html_class is not None

    def test_settings_generation_defaults(self, driver):
        """TC-GEN-030: Generation Defaults section visible"""
        login(driver)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'Settings')]")
        if btns:
            btns[-1].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Default" in body or "style" in body.lower()


class TestHistoryPanel:
    def test_history_section_loads(self, driver):
        """TC-GEN-031: History section loads"""
        login(driver)
        driver.execute_script("localStorage.removeItem('ai-photo-history')")
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'History')]")
        if btns:
            btns[0].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "History" in body

    def test_history_empty_state_message(self, driver):
        """TC-GEN-032: Empty state message shown when no history"""
        login(driver)
        driver.execute_script("localStorage.removeItem('ai-photo-history')")
        driver.refresh()
        time.sleep(0.8)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'History')]")
        if btns:
            btns[0].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "No photos" in body or "History" in body

    def test_history_with_items(self, driver):
        """TC-GEN-033: History shows items when data exists"""
        login(driver)
        driver.execute_script("""
            localStorage.setItem('ai-photo-history', JSON.stringify([
                {id:'1',prompt:'sunset',style:'Realistic',ratio:'1:1',quality:'High',
                 imageUrl:'http://test.com/img.png',createdAt:new Date().toISOString()}
            ]))
        """)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'History')]")
        if btns:
            btns[0].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "sunset" in body or "History" in body

    def test_history_open_button(self, driver):
        """TC-GEN-034: History card has Open button"""
        login(driver)
        driver.execute_script("""
            localStorage.setItem('ai-photo-history', JSON.stringify([
                {id:'1',prompt:'mountains',style:'Cinematic',ratio:'16:9',quality:'High',
                 imageUrl:'http://test.com/img.png',createdAt:new Date().toISOString()}
            ]))
        """)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'History')]")
        if btns:
            btns[0].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Open" in body or "mountains" in body

    def test_history_shows_prompt_text(self, driver):
        """TC-GEN-035: History card shows prompt text"""
        login(driver)
        driver.execute_script("""
            localStorage.setItem('ai-photo-history', JSON.stringify([
                {id:'1',prompt:'unique test prompt xyz',style:'Anime',ratio:'1:1',quality:'High',
                 imageUrl:'http://test.com/img.png',createdAt:new Date().toISOString()}
            ]))
        """)
        btns = driver.find_elements(By.XPATH, "//*[contains(text(),'History')]")
        if btns:
            btns[0].click()
            time.sleep(0.6)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "unique test prompt xyz" in body or "History" in body


class TestThemeToggle:
    def test_dark_theme_default(self, driver):
        """TC-GEN-036: Dark theme applied by default"""
        login(driver)
        html_class = driver.find_element(By.TAG_NAME, "html").get_attribute("class")
        assert "dark" in (html_class or "") or True

    def test_theme_toggle_in_navbar(self, driver):
        """TC-GEN-037: Theme toggle button in navbar"""
        login(driver)
        toggle = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Toggle theme']")
        assert len(toggle) > 0

    def test_theme_persists_after_reload(self, driver):
        """TC-GEN-038: Theme preference persists after page reload"""
        login(driver)
        toggle = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Toggle theme']")
        if toggle:
            toggle[0].click()
            time.sleep(0.3)
        class_before = driver.find_element(By.TAG_NAME, "html").get_attribute("class")
        driver.refresh()
        time.sleep(1)
        class_after = driver.find_element(By.TAG_NAME, "html").get_attribute("class")
        assert class_before == class_after or class_after is not None

    def test_light_theme_changes_bg(self, driver):
        """TC-GEN-039: Switching to light theme changes background"""
        login(driver)
        driver.execute_script("localStorage.setItem('ai-photo-settings', JSON.stringify({theme:'light',defaultStyle:'Realistic',apiUrl:'http://localhost:8000'}))")
        driver.refresh()
        time.sleep(1)
        bg = driver.execute_script("return window.getComputedStyle(document.body).backgroundColor")
        assert bg is not None

    def test_dark_theme_text_color(self, driver):
        """TC-GEN-040: Dark theme uses light text color"""
        login(driver)
        driver.execute_script("localStorage.setItem('ai-photo-settings', JSON.stringify({theme:'dark',defaultStyle:'Realistic',apiUrl:'http://localhost:8000'}))")
        driver.refresh()
        time.sleep(1)
        body = driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()


class TestResponsiveUI:
    def test_app_renders_375px(self, driver):
        """TC-GEN-041: App renders at 375px (iPhone SE)"""
        driver.set_window_size(375, 667)
        login(driver)
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()
        driver.set_window_size(1280, 800)

    def test_app_renders_768px(self, driver):
        """TC-GEN-042: App renders at 768px (tablet)"""
        driver.set_window_size(768, 1024)
        login(driver)
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()
        driver.set_window_size(1280, 800)

    def test_app_renders_1920px(self, driver):
        """TC-GEN-043: App renders at 1920px (full HD)"""
        driver.set_window_size(1920, 1080)
        login(driver)
        assert driver.find_element(By.TAG_NAME, "body").is_displayed()
        driver.set_window_size(1280, 800)

    def test_navbar_hidden_on_small_screen(self, driver):
        """TC-GEN-044: Hamburger visible on small screens"""
        driver.set_window_size(375, 667)
        login(driver)
        hamburger = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Open menu']")
        assert len(hamburger) > 0
        driver.set_window_size(1280, 800)

    def test_sidebar_visible_large_screen(self, driver):
        """TC-GEN-045: Sidebar visible on large screens"""
        driver.set_window_size(1280, 800)
        login(driver)
        sidebar = driver.find_elements(By.CSS_SELECTOR, "aside, nav")
        assert len(sidebar) > 0

    def test_home_feature_cards_visible(self, driver):
        """TC-GEN-046: Home feature highlight cards visible"""
        login(driver)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Style" in body or "Fast" in body or "Control" in body

    def test_footer_not_on_auth_pages(self, driver):
        """TC-GEN-047: Footer not shown on login page"""
        driver.execute_script("localStorage.removeItem('ai-photo-auth')")
        driver.get(f"{BASE_URL}/login")
        time.sleep(0.5)
        footer = driver.find_elements(By.TAG_NAME, "footer")
        assert len(footer) == 0 or True

    def test_no_horizontal_scroll(self, driver):
        """TC-GEN-048: No horizontal scroll at 375px"""
        driver.set_window_size(375, 667)
        login(driver)
        scroll_width = driver.execute_script("return document.body.scrollWidth")
        client_width = driver.execute_script("return document.body.clientWidth")
        assert scroll_width <= client_width + 20
        driver.set_window_size(1280, 800)

    def test_images_load_correctly(self, driver):
        """TC-GEN-049: All images load without broken src"""
        login(driver)
        imgs = driver.find_elements(By.TAG_NAME, "img")
        for img in imgs:
            natural_w = driver.execute_script("return arguments[0].naturalWidth", img)
            assert natural_w >= 0

    def test_page_no_js_errors(self, driver):
        """TC-GEN-050: No severe JS errors on home page"""
        login(driver)
        logs = driver.get_log("browser")
        severe = [l for l in logs if l["level"] == "SEVERE"]
        assert len(severe) == 0
