from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Setup Chrome options
options = Options()
options.add_argument("--headless")

# Set path to chromedriver as a service
webdriver_service = Service(ChromeDriverManager().install())
