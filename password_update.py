import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge import service
# from selenium.webdriver.support.ui import WebDriverWait
from shared_lists import device_list

pass_2021 = "COPradio2021!"
pass_2022 = "COPradio2022!"

edgeOption = webdriver.EdgeOptions()
edgeOption.use_chromium = True
# edgeOption.add_argument("start-maximized")
edgeOption.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
s = service.Service(r'C:\Users\pboynto\edge\msedgedriver.exe')
driver = webdriver.Edge(service=s, options=edgeOption)


def login():
    for i in device_list.devices:
        try:
            url = i
            driver.get(url)
        #    wait = WebDriverWait(driver, 5)
            x = driver.find_element(By.ID, value="password")
            x.send_keys(pass_2021)
            driver.find_element(by=By.NAME, value="login_submit").click()
            time.sleep(1)
            old_pass_prompt = driver.find_element(By.ID, value="currentPassword")
            old_pass_prompt.send_keys(pass_2021)
            new_pass_prompt = driver.find_element(By.ID, value="newPassword")
            new_pass_prompt.send_keys(pass_2022)
            confirm_pass_prompt = driver.find_element(By.ID, value="confirmNewPassword")
            confirm_pass_prompt.send_keys(pass_2022)
            driver.find_element(by=By.NAME, value="pswd_update_submit").click()
        except Exception as e:
            print(f'{i} has failed due to {e}')
            continue


def main():
    login()
    driver.quit()


if __name__ == '__main__':
    main()
