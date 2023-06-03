from selenium import webdriver
from selenium.webdriver.common.by import By
import time

website = "http://127.0.0.1:5005"
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
    driver.find_element(By.NAME, "name_registo").send_keys("Henrique")
    time.sleep(1)
    driver.find_element(By.NAME, "email_registo").send_keys("henrique.dias@ua.pt")
    time.sleep(1)
    driver.find_element(By.NAME, "password_registo").send_keys("henrique")
    time.sleep(1)
    driver.find_element(By.ID, "submit_registo").click()
    #ESTÁ A FUNCIONAR
    

def test_login():
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("joao@gmail.com")
    time.sleep(1)
    driver.find_element(By.NAME, "password").send_keys("1")
    time.sleep(1)
    driver.find_element(By.ID, "submit").click()
    #ESTÁ A FUNCIONAR


def main():
    start_webdriver()
    #test_registo()
    #voltar_home()
    test_login()

if __name__ == "__main__":
    main()