import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('n_user@ya.ru')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('123')
   # ожидаем активность кнопки для входа в аккаунт
   element = WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
   # Нажимаем на кнопку входа в аккаунт
   element.click()
   # ожидаем загрузку заголовка на главной странице пользователя (явное ожидание)
   wait = WebDriverWait(pytest.driver, 10).until(EC.title_is("PetFriends: My Pets"))
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

   #переходим на страницу с питомцами пользователя
   pytest.driver.find_element_by_css_selector('.nav-link[href="/my_pets"]').click()
   #ожидаем загрузку таблицы с питомцами (явное ожидание)
   wait = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))
   # ожидаем активность кнопки "Добавить питомца"
   add_pet = WebDriverWait(pytest.driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, '//button[@data-target="#addPetsModal"]')))
   pets = pytest.driver.find_elements_by_css_selector('#all_my_pets tbody tr')
   #count_pets = pytest.driver.find_element_by_class_name('.col-sm-4 left')
   #print("Text: "+count_pets.text)
   assert len(pets) == 2

   #неявные ожидания всех элементов (фото, имя питомца, его возраст)
   pytest.driver.implicitly_wait(10)
   # проверяем, что внутри каждого из них есть фото, имя питомца, возраст и вид
   # получаем фото питомцев
   images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//img')
   names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tr/td[1]')
   species = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tr/td[2]')
   age = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tr/td[3]')
   assert len(images) == len(pets)
   assert len(names) == len(pets)
   for i in range(len(pets)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert species[i].text != ''
      assert age[i].text != ''
      print(age[i].text)