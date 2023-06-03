from selenium import webdriver
from selenium.webdriver.common.by import By
import time

website = "http://127.0.0.1:5005"
driver = None
wait = 1

def start_webdriver():
    global driver
    driver = webdriver.Firefox()

    driver.get(website)
    driver.maximize_window()
    time.sleep(wait)


def voltar_home():
    driver.find_element(By.CLASS_NAME, "logo").click()
    time.sleep(wait)


def test_registo():
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    driver.find_element(By.ID, "name_registo").send_keys("Henrique")
    time.sleep(wait)
    driver.find_element(By.ID, "email_registo").send_keys("henrique.dias@ua.pt")
    time.sleep(wait)
    driver.find_element(By.ID, "password_registo").send_keys("henrique")
    time.sleep(wait)
    driver.find_element(By.ID, "submit_registo").click()
    #ESTÁ A FUNCIONAR
    time.sleep(wait)


def test_login(email, password):
    voltar_home()
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    driver.find_element(By.NAME, "email").send_keys(email)
    time.sleep(wait)
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(wait)
    driver.find_element(By.ID, "submit").click()
    #ESTÁ A FUNCIONAR
    time.sleep(wait)


def test_adicionar_animal():
    voltar_home()
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    driver.find_element(By.ID, "meus_animais").click()
    time.sleep(wait)
    driver.find_element(By.ID, "add_animal").click()
    time.sleep(wait)
    driver.find_element(By.NAME, "name").send_keys("Chico")
    time.sleep(wait)
    driver.find_element(By.NAME, "idade").send_keys("3")
    time.sleep(wait)
    driver.find_element(By.NAME, "genero").send_keys("Masculino")
    time.sleep(wait)
    driver.find_element(By.NAME, "raca").send_keys("Husky")
    time.sleep(wait)
    driver.find_element(By.NAME, "peso").send_keys("20")
    time.sleep(wait)
    driver.find_element(By.NAME, "imagem").send_keys("/home/henrique/Documents/ProjetoAS/bot-selenium/husky.jpeg")
    time.sleep(wait)
    element = driver.find_element(By.ID,'submit')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(wait)
    # ESTÁ A FUNCIONAR


def test_aderir_plano():
    driver.find_element(By.ID, "planos").click()
    time.sleep(wait)
    element = driver.find_element(By.ID,'aderir_standard')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(wait)
    driver.find_element(By.ID, "pagar").click()
    time.sleep(wait)
    # ESTÁ A FUNCIONAR


def test_ficha_animal():
    voltar_home()
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    driver.find_element(By.ID, "meus_animais").click()
    time.sleep(wait)
    element = driver.find_element(By.ID,'ver_mais')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(wait)
    #ESTÁ A FUNCIONAR
    

def test_agendar_consulta():
    voltar_home()
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    driver.find_element(By.ID, "consultas").click()
    time.sleep(wait)
    element = driver.find_element(By.ID,'agendar_consulta')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(wait)
    driver.find_element(By.ID, "animal_sel").click()
    time.sleep(wait)
    element = driver.find_element(By.ID,'local-clinica')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(wait)
    driver.find_element(By.ID, "data").send_keys("06/06/2023")
    time.sleep(wait)
    driver.find_element(By.ID, "hora").send_keys("14:00")
    time.sleep(wait)
    driver.find_element(By.ID, "descricao").send_keys("Checkup Mensal")
    time.sleep(wait)
    driver.find_element(By.ID, "agendar_submit").click()
    time.sleep(wait)
    #ESTÁ A FUNCIONAR


def test_ver_consultas():
    voltar_home()
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    #ESTÁ A FUNCIONAR


def test_contactar_veterinario():
    logout()
    test_login("marco@gmail.com", "1")
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    driver.find_element(By.ID, "contactar_veterinario").click()
    time.sleep(wait)
    #ESTÁ A FUNCIONAR


def test_ver_info_cliente():
    # logout()
    test_login("carlos@nutrivet.pt", "1")
    driver.find_element(By.ID, "email_cliente").send_keys("joao@gmail.com")
    time.sleep(wait)
    driver.find_element(By.ID, "pesquisar").click()
    time.sleep(wait)
    #ESTÁ A FUNCIONAR


def test_ver_consultas_veterinario():
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    driver.find_element(By.ID, "consultas").click()
    time.sleep(wait)
    #ESTÁ A FUNCIONAR


def logout():
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    time.sleep(wait)
    driver.find_element(By.ID, "logout").click()
    time.sleep(wait)


def main():
    email = "joao@gmail.com"
    password = "1"

    start_webdriver()
    # test_registo()
    # print("login")
    # test_login(email, password)
    # print("add animal")
    # test_adicionar_animal()
    # print("aderir plano")
    # test_aderir_plano()
    # print("ver ficha")
    # test_ficha_animal()
    # print("agendar consulta")
    # test_agendar_consulta()
    # print("ver histórico consultas")
    # test_ver_consultas()
    # print("contactar veterinário")
    # test_contactar_veterinario()
    print("Consultar ficha de cliente")
    test_ver_info_cliente()
    print("Ver Consultas do Veterinário")
    test_ver_consultas_veterinario()

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