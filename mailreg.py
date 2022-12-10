from selenium import webdriver
from selenium.common import NoSuchElementException
from time import sleep
from random import randint as rnd
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from PIL import Image


class MailRegistrator:
    # Functionality of closing browser
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # Functionality of searching for XPATH
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # Functionality of name generator. You can add your names.
    def name_generator(self):
        return ['Иван', 'Владимир', 'Олег', 'Александр', 'Николай', 'Алексей'][rnd(0, 5)]

    # Functionality of surname generator. You can add your surnames.
    def surname_generator(self):
        return ['Бабич', 'Иванов', 'Оганесян', 'Еременко', 'Милютин', 'Никитченко'][rnd(0, 5)]

    # Functionality of username generator.
    def username_generator(self):
        uname = ['f', 'w', 'a', '9', '0', '7']
        uname = f'mymail{uname[rnd(0, 5)]}{uname[rnd(0, 5)]}{uname[rnd(0, 5)]}{uname[rnd(0, 5)]}{uname[rnd(0, 5)]}{uname[rnd(0, 5)]}'
        return uname

    # Function gender generator
    def gender(self):
        try:
            self.browser.find_element(By.XPATH, "//*[@class='border-0-2-148']").click()
        except Exception as ex:
            print(ex)
            self.close_browser()
            self.registration()

    # Functionality of birthday generator.
    def birthday(self):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, "//*[@data-test-id='birth-date__day']").click()
            select = browser.find_elements(By.XPATH, "//*[contains(text(), '31')]")
            select[4].click()
            browser.find_element(By.XPATH, "//*[@data-test-id='birth-date__month']").click()
            browser.find_element(By.XPATH, "//*[contains(text(),'Апрель')]").click()
            browser.find_element(By.XPATH, "//*[@data-test-id='birth-date__year']").click()
            browser.find_element(By.XPATH, "//*[contains(text(),'1990')]").click()
        except Exception as ex:
            print(ex)
            self.close_browser()
            self.registration()

    # Function of clicking to the verification button.
    def first_click(self):
        try:
            btns = self.browser.find_elements(By.XPATH, "//button")
            btns[5].click()
        except Exception as ex:
            print(ex)
            self.close_browser()
            self.registration()

    # Captcha hacking.
    def captcha(self):
        try:
            browser = self.browser
            browser.save_screenshot('1.jpeg')
            img = Image.open('1.jpeg')
            img2 = img.crop((1500, 412, 1800, 530))
            img2.save('2.png')
            solver = TwoCaptcha('YOUR API KEY')
            result = solver.normal('2.png')
            captcha = result['code']
            cap = browser.find_element(By.XPATH, "//input[@data-test-id='captcha']")
            cap.send_keys(captcha)
            cap.submit()
            sleep(10)
        except Exception as ex:
            print(ex)
            self.close_browser()
            self.registration()

    # Logging
    def logging(self, my_username, mypassword):
        with open('Log.txt', 'a+') as f:
            f.write(f'{my_username}@mail.ru:{mypassword}\n')
            f.close()

    # Main function of mail.ru registration.
    def registration(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            #Add chromedriver path
            self.browser = webdriver.Chrome(r'YOUR PATH',
                                            options=options)
            self.browser.maximize_window()
            browser = self.browser
            browser.get('https://account.mail.ru/signup?from=main&rf=auth.mail.ru')
            name = browser.find_element(By.XPATH, f"//input[@id='fname']")
            name.send_keys(self.name_generator())
            sleep(2)
            surname = browser.find_element(By.XPATH, "//input[@id='lname']")
            surname.send_keys(self.surname_generator())
            self.birthday()
            sleep(2)
            self.gender()
            username = browser.find_element(By.XPATH, "//input[@name='username']")
            my_username = self.username_generator()
            username.send_keys(my_username)
            select = browser.find_element(By.LINK_TEXT, 'Сгенерировать надёжный пароль')
            select.click()
            password = browser.find_element(By.XPATH, "//input[@name='password']")
            my_password = password.get_attribute('value')
            sleep(2)
            self.first_click()
            sleep(5)
            self.captcha()
            self.logging(my_username, my_password)
            self.close_browser()
            self.registration()

        except NoSuchElementException as ex:
            print(ex)
            self.close_browser()
            self.registration()


if __name__ == '__main__':
    MyBot = MailRegistrator()
    MyBot.registration()
