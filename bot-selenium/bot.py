from selenium import webdriver
from selenium.webdriver.common.by import By
import time

website = "http://127.0.0.1:5005/"
driver = None

def start_webdriver():
    global driver
    driver = webdriver.Firefox()

    driver.get(website)
    driver.maximize_window()
    time.sleep(1)

def voltar_home():
    driver.find_element(By.CLASS_NAME, "logo").click()
    time.sleep(1)

def test_registo():
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(1)
    driver.find_element(By.NAME, "name").send_keys("")

def test_login():
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(1)

def main():
    start_webdriver()
    test_registo()
    voltar_home()
    #test_login()

if __name__ == "__main__":
    main()