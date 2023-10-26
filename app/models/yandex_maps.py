from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import os
from time import sleep
import uuid
import logging
import traceback
import random
import shutil
from .errors import (
    DriverNotInitialized,
    TextAreaNotFound,
)


logger = logging.getLogger(__name__)


class YandexMaps:
    def __init__(self, page_url: str, headless=False) -> None:
        self.page_url = page_url
        self.headless = headless
        self.driver = None
        self.tmp_path = f"{os.getcwd()}/tmp/chrome_{str(uuid.uuid4())}"

        self.init_driver()

    def close(self) -> None:
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
        
            for _ in range(10):
                try:
                    if os.path.exists(self.tmp_path) and os.path.isdir(self.tmp_path):
                        shutil.rmtree(self.tmp_path)
                    break
                except:
                    sleep(0.3)

    def init_driver(self):
        logger.info(f"Try init on Yandex Maps on {self.page_url}")
        self.driver = None

        filename = f'blank_{str(uuid.uuid4())}.html'
        try:
            if not os.path.exists(self.tmp_path):
                os.makedirs(self.tmp_path)

            # make temp blank page with link to target page
            with open(f'{self.tmp_path}/{filename}', 'w') as f:
                f.write(
                    f'<a href="{self.page_url}" target="_blank">link</a>')

            # init driver
            options = uc.ChromeOptions()
            options.arguments.extend(
                ["--no-sandbox", "--disable-setuid-sandbox", "--incognito", "--start-fullscreen"])
            # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            try:
                # try to init dockered cromium driver first
                self.driver = uc.Chrome(
                    headless=self.headless,
                    use_subprocess=False,
                    user_multi_procs=True,
                    user_data_dir=self.tmp_path,
                    options=options,
                    driver_executable_path='/usr/lib/chromium/chromedriver',
                )
            except:
                self.driver = uc.Chrome(
                    headless=self.headless,
                    use_subprocess=False,
                    user_multi_procs=True,
                    user_data_dir=self.tmp_path,
                    options=options,
                )

            # open the link
            self.driver.get(f'file://{self.tmp_path}/{filename}')
            links = self.driver.find_elements(By.XPATH, "//a[@href]")
            logger.info('run driver and waiting 10 sec')
            sleep(random.uniform(10, 13))
            links[0].click()
            logger.info('click blank page link and waiting 10 sec')
            sleep(random.uniform(10, 12))
            self.driver.switch_to.window(self.driver.window_handles[1])
            sleep(random.uniform(10, 13))
            logger.info('waiting 10 sec and try to login')

            
            logger.info('Swith to discord tab')

            # waiting while page is loaded
            for _ in range(3):
                for _ in range(40):
                    text_area = self.driver.find_elements(
                        By.XPATH, '//input[@type="text"]')
                    if len(text_area) > 0:
                        break
                    sleep(0.5)
                else:
                    print('try to refresh page')
                    self.driver.refresh()
                    print('refreshed, sleep 20 dec')
                    sleep(20)
                
                print('try to find input after resresh')
                text_area = self.driver.find_elements(
                    By.XPATH, '//input[@type="text"]')
                if len(text_area) > 0:
                    print('input is found!')
                    break
                else:
                    print('fail. Try again.')
            else:
                raise RuntimeError("Can't find input!")
            
        except Exception as e:
            error_message = f"INIT Exception occurred: {type(e).__name__}, {e.args}\n"
            error_message += traceback.format_exc()
            logger.error(error_message)
            self.close()
            self.driver = None
            sleep(5)
            # self.init_driver()
    
    def refresh_page(self):
        if not self.driver:
            raise DriverNotInitialized

        logger.info('Try to refresh the page.')
        self.driver.refresh()
        logger.info('page refreshed. Waiting for textarea element.')
        sleep(3)

        for _ in range(40):
            text_area = self.driver.find_elements(
                By.XPATH, '//input[@type="text"]')
            if len(text_area) > 0:
                logger.info('input fund! Try to run the func again')
                return
            sleep(0.5)

    def send_prompt(self, text: str) -> dict:
        """The function send prompt
        Args:
            text (str): prompt text
        """
        if self.driver is None:
            raise DriverNotInitialized
        
        logger.info(f'Try to send prompt: {text}')

        # find input
        for _ in range(60):
            text_area = self.driver.find_elements(By.XPATH, '//input[@type="text"]')
            if text_area:
                text_area = text_area[-1]
                break
            sleep(0.2)
        else:
            raise TextAreaNotFound
        
        # send prompt

        wait = WebDriverWait(self.driver, 2)
        text_area = wait.until(EC.visibility_of(text_area))

        text_area.clear()
        text_area.send_keys(f' {text}')
        sleep(random.uniform(0.3, 0.6))
        text_area.send_keys(Keys.ENTER)

        sleep(3)
        current_url = self.driver.current_url

        parsed_url = urlparse(current_url)
        query_parameters = parse_qs(parsed_url.query)

        latitude = query_parameters.get('ll', [])[0].split(',')[1]
        longitude = query_parameters.get('ll', [])[0].split(',')[0]

        return dict(latitude=latitude, longitude=longitude)