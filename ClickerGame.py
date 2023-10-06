import tkinter as tk
import threading
import time
import pickle

# Глобальные переменные для хранения счета, количества улучшений и цен улучшений
score = 0
upgrades = 0
upgrade_price = 100
auto_clicks = 0
auto_click_price = 500
auto_click_rate = 5

# Функция, которая увеличивает счет при клике на кнопку
def click():
    global score
    score += 2 ** upgrades  # Увеличиваем количество очков за клик вдвое с учетом улучшений
    label.config(text=f"Score: {score}")

# Функция для покупки улучшения
def buy_upgrade():
    global score, upgrades, upgrade_price
    if score >= upgrade_price:
        score -= upgrade_price
        upgrades += 1
        label.config(text=f"Score: {score}")
        upgrade_price += 100  # Увеличиваем цену улучшения на 100 очков
        upgrade_label.config(text=f"Upgrades: {upgrades}")
        upgrade_button.config(text=f"Buy Upgrade ({upgrade_price} Score)")

# Функция для покупки улучшения "Автоклик"
def buy_auto_click():
    global score, auto_clicks, auto_click_price, auto_click_rate
    if score >= auto_click_price:
        score -= auto_click_price
        auto_clicks += 1
        label.config(text=f"Score: {score}")
        auto_click_price *= 2  # Увеличиваем цену улучшения "Автоклик" вдвое
        auto_click_rate = max(auto_click_rate / 2, 1)  # Увеличиваем скорость автоклика вдвое (минимум 1 клик в 1 секунду)
        auto_click_label.config(text=f"Auto Clicks: {auto_clicks}")
        auto_click_button.config(text=f"Buy Auto Click ({auto_click_price} Score)")

# Функция автоматического кликера
def auto_clicker():
    while True:
        global score
        score += auto_clicks * 2 ** upgrades  # Автоматический клик вдвое с учетом улучшений
        label.config(text=f"Score: {score}")
        time.sleep(auto_click_rate)  # Подождите указанное количество секунд перед следующим кликом

# Функция сохранения прогресса
def save_progress():
    global score, upgrades, upgrade_price, auto_clicks, auto_click_price, auto_click_rate
    progress_data = {
        "score": score,
        "upgrades": upgrades,
        "upgrade_price": upgrade_price,
        "auto_clicks": auto_clicks,
        "auto_click_price": auto_click_price,
        "auto_click_rate": auto_click_rate
    }
    with open("progress.pkl", "wb") as file:
        pickle.dump(progress_data, file)
    print("Прогресс сохранен.")

# Функция загрузки прогресса
def load_progress():
    global score, upgrades, upgrade_price, auto_clicks, auto_click_price, auto_click_rate
    try:
        with open("progress.pkl", "rb") as file:
            progress_data = pickle.load(file)
            score = progress_data["score"]
            upgrades = progress_data["upgrades"]
            upgrade_price = progress_data["upgrade_price"]
            auto_clicks = progress_data["auto_clicks"]
            auto_click_price = progress_data["auto_click_price"]
            auto_click_rate = progress_data["auto_click_rate"]
        label.config(text=f"Score: {score}")
        upgrade_label.config(text=f"Upgrades: {upgrades}")
        upgrade_button.config(text=f"Buy Upgrade ({upgrade_price} Score)")
        auto_click_label.config(text=f"Auto Clicks: {auto_clicks}")
        auto_click_button.config(text=f"Buy Auto Click ({auto_click_price} Score)")
        print("Прогресс загружен.")
    except FileNotFoundError:
        print("Файл прогресса не найден.")

# Создание графического интерфейса
root = tk.Tk()
root.title("ClickerGame")

# Создание метки для отображения счета
label = tk.Label(root, text="Score: 0", font=("Helvetica", 24))
label.pack(pady=20)

# Создание кнопки для кликов
button = tk.Button(root, text="Click", command=click, font=("Helvetica", 18))
button.pack()

# Создание кнопки для покупки улучшения
upgrade_button = tk.Button(root, text=f"Buy Upgrade ({upgrade_price} Score)", command=buy_upgrade, font=("Helvetica", 18))
upgrade_button.pack()

# Метка для отображения количества улучшений
upgrade_label = tk.Label(root, text="Upgrades: 0", font=("Helvetica", 16))
upgrade_label.pack()

# Создание кнопки для покупки улучшения "Автоклик"
auto_click_button = tk.Button(root, text=f"Buy Auto Click ({auto_click_price} Score)", command=buy_auto_click, font=("Helvetica", 18))
auto_click_button.pack()

# Метка для отображения количества улучшений "Автоклик"
auto_click_label = tk.Label(root, text="Auto Clicks: 0", font=("Helvetica", 16))
auto_click_label.pack()

# Создание кнопки для сохранения прогресса
save_button = tk.Button(root, text="Save Progress", command=save_progress, font=("Helvetica", 18))
save_button.pack()

# Создание кнопки для загрузки прогресса
load_button = tk.Button(root, text="Load Progress", command=load_progress, font=("Helvetica", 18))
load_button.pack()

# Запуск потока автоматического кликера
auto_click_thread = threading.Thread(target=auto_clicker)
auto_click_thread.daemon = True
auto_click_thread.start()

# Запуск главного цикла приложения
root.mainloop()
