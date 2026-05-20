import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from csv_reader import load_contacts
from message_sender import send_whatsapp_message
from utils import save_log

import config


# =========================
# LOAD CONTACTS
# =========================

contacts = load_contacts(config.CSV_FILE)


# =========================
# LOAD MESSAGE TEMPLATE
# =========================

with open(config.MESSAGE_TEMPLATE, "r", encoding="utf-8") as file:
    template = file.read()


# =========================
# LOAD SENT NUMBERS
# =========================

sent_numbers = set()

try:

    with open(config.LOG_FILE, "r", encoding="utf-8") as file:

        for line in file:

            if "Message sent to" in line:

                try:
                    phone = (
                        line.split("(")[-1]
                        .replace(")", "")
                        .strip()
                    )

                    sent_numbers.add(phone)

                except:
                    pass

except FileNotFoundError:

    pass


# =========================
# SETUP CHROME
# =========================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)


# =========================
# OPEN WHATSAPP WEB
# =========================

driver.get("https://web.whatsapp.com")


# =========================
# WAIT FOR QR SCAN
# =========================

input("Scan QR Code then press ENTER...")


print("\nStarting WhatsApp Automation...\n")


# =========================
# START AUTOMATION
# =========================

for index, row in contacts.iterrows():

    try:

        # =========================
        # GET CONTACT DETAILS
        # =========================

        name = str(row['name']).strip()
        phone = str(row['phone']).strip()


        # =========================
        # SKIP EMPTY NUMBERS
        # =========================

        if phone.lower() == "nan" or phone == "":

            print(f"Skipping {name} because number is missing")

            continue


        # =========================
        # SKIP ALREADY SENT
        # =========================

        if phone in sent_numbers:

            print(f"Already sent to {name}")

            continue


        # =========================
        # CREATE MESSAGE
        # =========================

        personalized_message = template.format(name=name)


        print(f"Sending to {name} ({phone})")


        # =========================
        # SEND MESSAGE
        # =========================

        success = send_whatsapp_message(
            driver,
            phone,
            personalized_message,
            config.WAIT_TIME
        )


        # =========================
        # SUCCESS
        # =========================

        if success:

            print(f"SUCCESS -> {name}")

            save_log(
                config.LOG_FILE,
                f"Message sent to {name} ({phone})"
            )

            sent_numbers.add(phone)


        # =========================
        # FAILED
        # =========================

        else:

            print(f"FAILED -> {name}")

            save_log(
                config.LOG_FILE,
                f"Failed for {name} ({phone})"
            )


        # =========================
        # DELAY
        # =========================

        time.sleep(config.DELAY_BETWEEN_MESSAGES)


    # =========================
    # ERROR HANDLING
    # =========================

    except Exception as e:

        print(f"ERROR for {name}: {e}")

        save_log(
            config.LOG_FILE,
            f"Error for {name}: {e}"
        )

        continue


# =========================
# FINISHED
# =========================

print("\nAutomation Completed Successfully")


# =========================
# CLOSE BROWSER
# =========================

driver.quit()