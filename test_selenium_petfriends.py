import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math

url = ('http://petfriends1.herokuapp.com/login')
wd = webdriver.Chrome("D:/chromedriver/chrome_d")


@pytest.fixture(autouse=True)
def testing():
    wd.get(url)
    wait_for_the_login_page = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID, "email")))

    yield

    wd.quit()


def test_show_my_pets():
    # Заходим на сайт PetFriends.
    wd.find_element_by_id('email').send_keys('kirill_srpti@mail.ru')
    wd.find_element_by_id('pass').send_keys('kirill99')
    wd.find_element_by_css_selector('button[type="submit"]').click()
    wait_for_the_main_page_petfriends = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                                                    "card-deck")))
    assert wd.find_element_by_tag_name('h1').text == "PetFriends"

    # Переходим в раздел "мои питомцы".
    wd.find_element_by_xpath('//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
    wait_for_the_page_of_my_pets = WebDriverWait(wd, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                              ".\\.col-sm-8.right.fill")
                                                                                             ))
    assert wd.find_element_by_tag_name('th').text == 'Фото'

    """(1)Проверяем чтобы кол-во питомцев соответствовало сатистике """
    # Находим локатор статистики пользователя.
    number_of_pets = wd.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text
    # Разделяем полученные слова.
    number_of_pets = number_of_pets.split()
    # Находим число питомцев.
    print(number_of_pets[2])
    # Находим всех питомцев на странице пользователя, сравниваем кол-во питомцев в таблице и число в статистике.
    pets = wd.find_elements_by_css_selector('.table.table-hover>tbody>tr')
    assert str(len(pets)) == number_of_pets[2]
    print('(1)Кол-во питомцев соответствует статистике')

    """(2)Проверяем кол-во питомцев с фото"""
    # Находим локатор для фото питомцев пользователя.
    images_pets = wd.find_elements_by_css_selector('.table>tbody>tr>th>img')
    # Делаем удобный список.
    list_images_pets = [img.get_attribute('src') for img in images_pets]
    # Пишем цикл, в кот. отбираем пустые строки и записываем их в счетчик.
    li = 0
    for i in list_images_pets:
        if i == '':
            li += 1
    # Сравниваем кол-во фото питомцев в списке(деленным пополам) с кол-вом пустых строк и делаем вывод.
    if math.ceil(len(list_images_pets)/2) > li:  # math.ceil - округление в большую сторону.
        print('(2)Питомцев с фото больше половины.')

    elif len(list_images_pets) / 2 == li:
        print('(2)Питомцев с фото и без фото одинаковое кол-во.')

    else:
        print(f'(2)Питомцев без фото более половины, а именно: {li}шт')

    """(3)Смотрим ,чтобы у всех питомцев были имена, возраст и порода"""
    # Находим по отдельности имя, породу и возраст питомцев. Записываем полученные данные в переменные.
    all_pets_name = wd.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    all_pets_animal_type = wd.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    all_pets_age = wd.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    try:
        li_name = [i.text for i in all_pets_name]
        for i in range(len(li_name)):
            assert li_name[i] != ''

        li_animal_type = [i.text for i in all_pets_animal_type]
        for i in range(len(li_animal_type)):
            assert li_animal_type[i] != ''

        li_age = [i.text for i in all_pets_age]
        for i in range(len(li_age)):
            assert li_age[i] != ''

        assert str(len(li_name)) == str(len(li_animal_type)) == str(len(li_age)) == number_of_pets[2]
        print('(3)У всех питомцев есть имена, возраст и порода')
    except Exception:
        print('(3)ОШИБКА! Не у всех питомцев присутствуют все данные.')

    """(4)Проверяем, есть ли повторяющиеся имена питомцев"""
    # Находим локатор имени питомца.
    pets_name = wd.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    # Переводим все полученные данные в текст и далее в список.
    list_name = [i.text for i in pets_name]

    try:
        # Сверяем кол-во питомцев в статистике пользователя и кол-во имен.
        assert number_of_pets[2] == str(len(set(list_name)))
        print('(4)Нет одинаковых имен')

    except Exception:
        # Если получаем ошибку, значит есть повторяющиеся слова(выводим эти слова).
        repeat_a_word = lambda array: sorted(list(set([x for x in array if array.count(x) > 1])))
        print(f"(4)Присутствуют одинаковые имена:{repeat_a_word(list_name)}")

