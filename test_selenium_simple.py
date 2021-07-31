import pytest
from selenium import webdriver


@pytest.fixture(autouse=True)
def testing():

    pytest.driver = webdriver.Chrome('D:/chromedriver/chrome_d')
    pytest.driver.implicitly_wait(10)

    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    wait_for_the_login_page = pytest.driver.find_element_by_id("email")

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('kirill_srpti@mail.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('kirill99')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    wait_for_the_main_page_petfriends = pytest.driver.find_element_by_link_text('PetFriends')
    wait_for_a_pets_photo = pytest.driver.find_elements_by_css_selector(".card_deck .card-img-top")
    wait_for_a_pets_name = pytest.driver.find_elements_by_css_selector(".card-deck .card-title")
    wait_for_a_pets_age = pytest.driver.find_elements_by_css_selector(".card-deck .card-text")

    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
