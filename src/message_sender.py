import time
import urllib.parse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def clean_phone(phone):

    phone = str(phone)

    phone = (
        phone.replace("+", "")
        .replace(" ", "")
        .replace(",", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    return phone


def send_whatsapp_message(driver, phone, message, wait_time):

    phone = clean_phone(phone)

    encoded_message = urllib.parse.quote(message)

    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"

    driver.get(url)

    time.sleep(wait_time)

    try:

        message_box = driver.find_element(
            By.XPATH,
            '//div[@contenteditable="true"][@data-tab="10"]'
        )

        time.sleep(2)

        message_box.send_keys(Keys.ENTER)

        print(f"Message sent to {phone}")

        return True

    except Exception as e:

        print("Error:", e)

        return False