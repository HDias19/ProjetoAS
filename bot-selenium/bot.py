from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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
    driver.find_element(By.ID, "name_registo").send_keys("Henrique")
    time.sleep(1)
    driver.find_element(By.ID, "email_registo").send_keys("henrique.dias@ua.pt")
    time.sleep(1)
    driver.find_element(By.ID, "password_registo").send_keys("henrique")
    time.sleep(1)
    driver.find_element(By.ID, "submit_registo").click()
    #ESTÁ A FUNCIONAR
    voltar_home()
    time.sleep(1)


def test_login(email, password):
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys(email)
    time.sleep(1)
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(1)
    driver.find_element(By.ID, "submit").click()
    #ESTÁ A FUNCIONAR
    time.sleep(1)


def test_adicionar_animal(email, password, nome_animal):
    test_login(email, password)
    driver.find_element(By.ID, "meus_animais").click()
    time.sleep(1)
    driver.find_element(By.ID, "add_animal").click()
    time.sleep(1)
    driver.find_element(By.NAME, "name").send_keys(nome_animal)
    time.sleep(1)
    driver.find_element(By.NAME, "idade").send_keys("3")
    time.sleep(1)
    driver.find_element(By.NAME, "genero").send_keys("Masculino")
    time.sleep(1)
    driver.find_element(By.NAME, "raca").send_keys("Husky")
    time.sleep(1)
    driver.find_element(By.NAME, "peso").send_keys("20")
    time.sleep(1)
    driver.find_element(By.NAME, "imagem").send_keys("/home/henrique/Documents/ProjetoAS/bot-selenium/husky.jpeg")
    time.sleep(1)
    element = driver.find_element(By.ID,'submit')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)
    # ESTÁ A FUNCIONAR


def test_aderir_plano(email, password):
    test_adicionar_animal(email, password, "Chico")
    driver.find_element(By.ID, "planos").click()
    time.sleep(1)
    element = driver.find_element(By.ID,'aderir_standard')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)
    driver.find_element(By.ID, "pagar").click()
    time.sleep(1)
    # ESTÁ A FUNCIONAR


def test_ficha_animal(email, password):
    driver
    


def logout():
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(1)
    driver.find_element(By.ID, "logout").click()
    time.sleep(1)


def main():
    email = "joao@gmail.com"
    password = "1"

    start_webdriver()
    #test_registo()
    #test_login(email, password)
    #test_adicionar_animal(email, password, "Chuchu")
    #test_aderir_plano(email, password)
    #test_ficha_animal(email, password)
    
    time.sleep(15)
    driver.quit()

if __name__ == "__main__":
    main()

# JSON format for joao@gmail.com.json
# {
#     "animais": [],
#     "planos": [],
#     "consultas": []
# }