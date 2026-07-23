"""
Shared pytest fixtures for all test suites.
"""
import os
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker

BASE_URL = os.getenv("APP_URL", "http://localhost:5173")
API_URL  = os.getenv("API_URL",  "http://localhost:8000")
fake     = Faker()


@pytest.fixture(scope="session")
def chrome_options():
    opts = ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    opts.add_argument("--disable-web-security")
    opts.add_argument("--allow-running-insecure-content")
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return opts


@pytest.fixture(scope="function")
def driver(chrome_options):
    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=chrome_options)
    drv.implicitly_wait(10)
    drv.set_page_load_timeout(30)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def driver_session(chrome_options):
    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=chrome_options)
    drv.implicitly_wait(10)
    drv.set_page_load_timeout(30)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def api_session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    yield s


@pytest.fixture
def test_user():
    return {"name": fake.name(), "email": fake.email(), "password": "Test@12345"}


@pytest.fixture
def valid_credentials():
    return {"email": "test@example.com", "password": "Test@12345"}


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression tests")
    config.addinivalue_line("markers", "security: Security/vulnerability tests")
    config.addinivalue_line("markers", "load: Load/performance tests")
    config.addinivalue_line("markers", "mobile: Appium/mobile tests")
