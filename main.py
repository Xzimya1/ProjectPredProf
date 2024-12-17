import sqlite3

# Создаем подключение к базе данных
connection = sqlite3.connect('combined_database.db')

# Создаем курсор
cursor = connection.cursor()

# Создаем таблицу для пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ФИО TEXT NOT NULL,
    Password TEXT NOT NULL,
    Login TEXT NOT NULL,
    Взятые TEXT NOT NULL
)
''')

# Создаем таблицу для заказов
cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    supplier_name TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(ID)
)
''')

# Создаем таблицу для продуктов
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    condition TEXT NOT NULL,
    batch_id TEXT NOT NULL
);
''')

def sklad_dobav(quantity, product_namee, usssr_id, condition, batch_id):
    for i in range(quantity):
        cursor.execute("INSERT INTO products(product_name, user_id, condition, batch_id) VALUES (?, ?, ?, ?)",
                       (product_namee, usssr_id, condition, batch_id))
    connection.commit()
    print("Партия добавлена")

# Функция для добавления пользователя
def insert_user(fio, password, login, items):
    cursor.execute("INSERT INTO Users(ФИО, Password, Login, Взятые) VALUES (?, ?, ?, ?)",
                   (fio, password, login, items))
    connection.commit()
    print('Пользователь добавлен.')

# Функция для проверки пользователя
def check_user(username, password):
    cursor.execute("SELECT * FROM Users WHERE Login=? AND Password=?", (username, password))
    user = cursor.fetchone()
    return user is not None

# Функция для получения уникальных значений из столбца
def get_unique(column_name):
    cursor.execute(f"SELECT DISTINCT {column_name} FROM Users;")
    unique_values = cursor.fetchall()
    return [value[0] for value in unique_values]

# Функция для добавления заказа
def add_order(order_id, product_name, quantity, supplier_name, user_id):
    cursor.execute("INSERT INTO Orders (order_id, product_name, quantity, supplier_name, user_id) VALUES (?, ?, ?, ?, ?)",
                   (order_id, product_name, quantity, supplier_name, user_id))
    connection.commit()

# Функция для получения всех заказов
def get_all_orders():
    cursor.execute("SELECT * FROM Orders")
    return cursor.fetchall()

# Генерация следующего order_id
def generate_order_id():
    cursor.execute("SELECT COUNT(*) FROM Orders")
    count = cursor.fetchone()[0]
    return f'ORD{count + 1}'

# Ввод данных пользователя
fio = input("Введите ФИО: ")
password = input("Введите пароль: ")
login = input("Введите логин: ")
items = "-"
insert_user(fio, password, login, items)

# Ввод данных для создания заявки на покупку инвентаря
product_name = input("Введите название товара: ")
quantity = int(input("Введите количество: "))
supplier_name = input("Введите имя поставщика: ")
user_id = 1  # Предположим фиксированный ID пользователя

# Получение usssr_id и batch_id из базы данных
usssr_id_query = "SELECT ID FROM Users WHERE Login=?"
cursor.execute(usssr_id_query, (login,))
usssr_result = cursor.fetchone()
usssr_id = usssr_result[0] if usssr_result else None

batch_query = "SELECT MAX(batch_id) FROM products"
cursor.execute(batch_query)
batch_result = cursor.fetchone()
batch_id = batch_result[0] + 1 if batch_result[0] is not None else 1  # Генерация нового batch_id

if usssr_id is not None:
    sklad_dobav(quantity, product_name, usssr_id, "Новый", str(batch_id))
else:
    print("Пользователь не найден.")

cursor.close()
connection.close()
