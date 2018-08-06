from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import platform
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class Driver:
  
  def __init__(self, remote = False, remoteURL = None):
      # Опции для успешной скачки файлов
      chrome_options = Options()
      chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd() +  os.path.join(r"\archives"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
      })
      chrome_options.add_argument("--window-size=1920x1080")

      executable = "chromedriver.exe" if platform.system() == 'Windows' else "chromedriver"
      chromeDriver = os.path.join(os.getcwd(), os.path.join("chromeDrivers", executable))
      
      self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromeDriver)
      self.wait = WebDriverWait(self.driver, 15)
  
  def pasteText(self, xpath, text, timeout = None, clearField = False):        
    pyperclip.copy(text)
    def f(wait): 
      wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
      self.driver.find_element_by_xpath(xpath).send_keys(Keys.CONTROL, 'v')
    return self.elementActionWrapper(f, timeout = timeout)

  def simpleClick(self, xpath, timeout = None):
    def f(wait): 
      wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
      self.driver.find_element_by_xpath(xpath).click()
    return self.elementActionWrapper(f, timeout = timeout)
  
  def confirmVisibility(self, xpath, timeout = None):
    return self.elementActionWrapper(lambda wait: 
      wait.until(EC.visibility_of_element_located((By.XPATH, xpath))), timeout = timeout)

  def confirmInvisibility(self, xpath, timeout = None):
    return self.elementActionWrapper(lambda wait: 
      wait.until_not(EC.presence_of_element_located((By.XPATH, xpath))), timeout = timeout)

  def waitTime(self, t):
    time.sleep(t)
  
  def elementActionWrapper(self, f, timeout = None):
    wait = self.checkForCustomWait(timeout)
    try: f(wait)
    except Exception as e: self.handleError(e)

  def handleError(self, e):
    self.driver.save_screenshot('Error.png')
    raise e
  
  def checkForCustomWait(self, timeout):
    wait = self.wait if not timeout else WebDriverWait(self.driver, timeout)
    return wait
      
    