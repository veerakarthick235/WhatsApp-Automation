from datetime import datetime

def save_log(log_file, text):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now()} - {text}\n")