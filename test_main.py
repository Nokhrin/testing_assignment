import config # константы
import pytest

# драйвер Firefox для Selenium
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# firefox_driver = Firefox(service=FirefoxService(GeckoDriverManager().install()))

# драйвер Chrome для Selenium
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# chrome_driver = Chrome(service=ChromeService(ChromeDriverManager().install()))


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# для управления временем ожидания загрузки страниц
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# для работы со списками типа select
from selenium.webdriver.support.select import Select

# для управления курсором
from selenium.webdriver import ActionChains

import time
import random
from datetime import datetime

from config import URL


# логирование
import logging
logging.basicConfig(
    level=logging.INFO,
    filename=config.LOG_PATH,
    filemode='w',
    format=config.LOG_FORMAT,
)


class InvestingTest():
    def test_page(self, selected_driver):
        try:
            # создать экземпляр объекта веб-драйвера
            if selected_driver == 'firefox_driver':
                driver = Firefox(service=FirefoxService(GeckoDriverManager().install()))
            elif selected_driver == 'chrome_driver':
                driver = Chrome(service=ChromeService(ChromeDriverManager().install()))

            # управление курсором
            action_chains = ActionChains(driver)


            # 1. Зайти на сайт https://ru.investing.com
            driver.get(config.URL)
            driver.maximize_window()
            print('браузер стартовал')
            logging.info('браузер стартовал')

            # 2. Перейти в меню "Котировки" -> "Акции" -> "Россия".
            print(f'поиск элемента:\n{config.XPATH_markets}')
            logging.info(f'поиск элемента: {config.XPATH_markets}')

            markets_button = driver.find_element(By.XPATH, config.XPATH_markets)
            action_chains.move_to_element(markets_button).perform()

            logging.info(f'наведение на элемент: {config.XPATH_markets}')
            #===================


            print(f'поиск элемента:\n{config.XPATH_markets_equities}')
            logging.info(f'поиск элемента: {config.XPATH_markets_equities}')

            equities_button = driver.find_element(By.XPATH, config.XPATH_markets_equities)
            action_chains.move_to_element(equities_button).perform()
            #===================


            print(f'поиск элемента:\n{config.XPATH_markets_equities_russia}')
            logging.info(f'поиск элемента: {config.XPATH_markets_equities_russia}')

            russia_button = driver.find_element(By.XPATH, config.XPATH_markets_equities_russia)

            logging.info(f'нажатие на элемент: {config.XPATH_markets}')
            russia_button.click()


            # 3. В выпадающем меню с типами акций выбрать "Россия - все акции"

            print(f'поиск элемента:\n{config.XPATH_stocks_filter_dropdown}')
            logging.info(f'поиск элемента: {config.XPATH_stocks_filter_dropdown}')

            stocks_filter_dropdown = driver.find_element(By.XPATH, config.XPATH_stocks_filter_dropdown)

            # выбрать пункт списка
            selected_element = Select(stocks_filter_dropdown)
            selected_element.select_by_index(0) # выбрать первый в списке
            # selected_element.select_by_visible_text("Россия - все акции") # выбрать по отображаемому тексту

            selected_element_text = driver.find_element(By.XPATH, config.XPATH_stocksFilter_all).text

            print(f'первый пункт в списке:\n{selected_element_text}')
            logging.info(f'первый пункт в списке: {selected_element_text}')


            # 4. Выбрать случайную акцию в таблице со списком акций
            # (сформировать список элементов таблицы, выбрать случайный элемент
            # данные находятся в tbody таблицы cross_rate_markets_stocks_1

            time.sleep(5) # ждать загрузки таблицы

            # просмотреть названия акций
            # строкой считаем каждый <tr>
            rows = driver.find_elements(By.XPATH, config.XPATH_table_row)

            print(f'всего строк найдено: {len(rows)}')
            logging.info(f'всего строк найдено: {len(rows)}')


            # выбор случайной строки = случайной акции
            random_stock_row = random.randint(0, (len(rows) - 1))
            print(f'выбрали строку: {random_stock_row}')
            logging.info(f'выбрали строку: {random_stock_row}')




            # ячейка
            # selected_stock_cell_XPATH = f'/html/body/div[4]/section/div[8]/div/table/tbody/tr[{random_stock_row}]/td[2]'
            # selected_stock_cell = driver.find_element(By.XPATH, selected_stock_cell_XPATH)
            # action_chains.move_to_element(selected_stock_cell).perform()

            # гиперссылка в ячейке
            selected_stock_link_XPATH = f'/html/body/div[4]/section/div[8]/div/table/tbody/tr[{random_stock_row}]/td[2]/a'
            selected_stock_link = driver.find_element(By.XPATH, selected_stock_link_XPATH)

            print(f'переход на выбранную строку: {selected_stock_link_XPATH}')
            logging.info(f'переход на выбранную строку: {selected_stock_link_XPATH}')


            # 5. Навести курсор мыши на название выбранной акции

            driver.execute_script("return arguments[0].scrollIntoView();", selected_stock_link)
            logging.info(f'наведение курсора на выбранную строку: {selected_stock_link_XPATH}')

            action_chains.pause(50)
            action_chains.move_to_element(selected_stock_link).perform()



            # 6. Сохранить название акции, отображающееся в всплывающей подсказке
            selected_stock_title = selected_stock_link.get_attribute('title')

            logging.info(f'наименование во всплывающей подсказке: {selected_stock_title}')


            # 7. Нажать на выбранную акцию для перехода в детальное описание
            selected_stock_link.click()
            logging.info(f'переход на страницу детального описания')

            # ожидать загрузки страницы
            stock_detailed_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, config.XPATH_stock_name))
            )

            # 8. Проверить совпадение названия акций на странице детального описания с сохраненным названием.
            # получить название акции со страницы детального описания
            print(f'поиск наименования: {config.XPATH_stock_name}')
            logging.info(f'поиск наименования: {config.XPATH_stock_name}')

            stock_detailed_name = driver.find_element(By.XPATH, config.XPATH_stock_name)

            print(f'детальное наименование: {stock_detailed_name.text}')
            logging.info(f'детальное наименование: {stock_detailed_name.text}')

            # подготовка наименования для сравнения
            split_position = stock_detailed_name.text.rfind('(')
            stock_name = stock_detailed_name.text[:split_position].strip()

            logging.info(f'детальное наименование подготовленное: {stock_name}')

            # сравнение наименований
            if selected_stock_title.lower() == stock_name.lower():
                print(f'названия совпадают')
                logging.info(f'названия совпадают')
            else:
                print(f'названия различаются')
                logging.info(f'названия различаются')


            # снимок финальной страницы

            url_to_screenshot = driver.current_url

            # создать уникальное имя для снимка
            time_stamp = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            print(time_stamp)
            split_position = url_to_screenshot.rfind('/')
            screenshot_filename = f'{url_to_screenshot[split_position:]}_{time_stamp}.png'
            print(screenshot_filename)
            screenshot_fullname = f'{config.SCREENSHOTS_PATH}{screenshot_filename}'
            print(screenshot_fullname)

            logging.info(f'сохранить снимок страницы {url_to_screenshot} в файл {screenshot_fullname}')

            driver.save_screenshot(screenshot_fullname)

        finally:
            # завершить работу веб-драйвера
            logging.info(f'завершить выполнение')
            driver.quit()


if __name__ == '__main__':
    inv_test = InvestingTest()
    # inv_test.test_page('firefox_driver')
    inv_test.test_page('chrome_driver')
