import sqlite3


class BotDB:

    def __init__(self, bd_file: str) -> None:
        """Инциализация соединения"""
        self.conn = sqlite3.connect(bd_file)
        self.cursor = self.conn.cursor()

    def start_db(self) -> None:
        """Создание системных бд"""
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS chat_stat  (
                id INTEGER PRIMARY KEY,
                object_id INTEGER NOT NULL UNIQUE,
                news_sub INTEGER NOT NULL DEFAULT (0),
                new_hedgehog TEXT
            )
        ''')

        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS user_stat  (
                id INTEGER,
                object_id INTEGER NOT NULL UNIQUE,
                vip INTEGER NOT NULL DEFAULT (0)
            )
        ''')

        self.cursor.execute(f"UPDATE chat_stat SET news_sub = ? WHERE news_sub = ?", (0, 1,))

        return self.conn.commit()

    def create_table(self, table: str) -> None:
        """Создание таблицы"""
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY NOT NULL,
                object_id INTEGER UNIQUE NOT NULL,
                hedgehog TEXT,
                hedgehog_name TEXT NOT NULL DEFAULT [Мой ёжик],
                hunger INTEGER NOT NULL DEFAULT (24),
                is_starving INTEGER NOT NULL DEFAULT (0),
                remove_hedgehog INTEGER NOT NULL DEFAULT (0),
                can_eat INTEGER NOT NULL DEFAULT (1)
            )
        ''')
        return self.conn.commit()

    def object_exists(self, object_id: int, table: str) -> bool:
        """Проверка наличия в бд"""
        result = self.cursor.execute(f"SELECT id FROM '{table}' WHERE object_id = ?", (object_id,))
        return bool(len(result.fetchall()))

    def get_info(self, object_id: int, table: str, column: str):
        """Получение данных из бд"""
        result = self.cursor.execute(f"SELECT {column} FROM '{table}' WHERE object_id = ?", (object_id,))
        return result.fetchone()[0]

    def add_object(self, object_id: int, table: str) -> None:
        """Добавление object в бд"""
        self.cursor.execute(f"INSERT INTO '{table}' ('object_id') VALUES (?)", (object_id,))
        return self.conn.commit()

    def update_info(self, object_id: int, table: str, column: str, info):
        """Обновление данных в бд"""
        self.cursor.execute(f"UPDATE {table} SET {column} = ? WHERE object_id = ?", (info, object_id,))
        return self.conn.commit()

    def close(self) -> None:
        """Закрытие соединения"""
        self.conn.close()
