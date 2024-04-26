import sqlite3 as sql
import json

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = sql.connect(db_name)
        self.cursor = self.conn.cursor()
        self.get = DBGet(self.conn, self.cursor)
        self.update = DBUpdate(self.conn, self.cursor)
        self.delete = DBDelete(self.conn, self.cursor)

    def _get_create_column_command(self, column: dict[str, str | int | bool]) -> str:
        column_name = column["name"]
        column_type = column["type"]
        nullable = column["nullable"]
        unique = column["unique"]
        default = column["default"]
        
        default = default if default not in (None, False) else None
        if default is not None and isinstance(default, str):
            default = f"DEFAULT '{default}'"
        else:
            default = f"DEFAULT {default}"
        
        return f"\"{column_name}\" {column_type} {'NOT NULL' if not nullable else ''} {default if default is not None else ''} {'UNIQUE' if unique else ''}"

    def create_column(self, table_name: str, column_name: str, column_type: str, nullable: bool = False, unique: bool = False, default: str | int | bool = None):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = self.cursor.fetchall()
        if column_name not in [i[1] for i in columns]:
            default = default if default not in (None, False) else None

            self.cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {self._get_create_column_command({"name": column_name, "type": column_type, "nullable": nullable, "unique": unique, "default": default})}')
            self.conn.commit()
    
    def check_colums(self, table_name: str, columns: list[dict[str, str | int | bool]]):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        table_columns = self.cursor.fetchall()
        for column in columns:
            if column["name"] not in [i[1] for i in table_columns] and "primary_key" not in column:
                self.create_column(table_name, column["name"], column["type"], column["nullable"], False, column["default"])

    def create_table(self, table_name: str, table_columns: list[dict[str, str | int | bool]]):
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        if table_name not in [i[0] for i in tables]:
            command = f"CREATE TABLE IF NOT EXISTS {table_name}("
            primary_col = None
            for column in table_columns:
                if "primary_key" in column:
                    primary_col = column
                    break
            
            command += self._get_create_column_command({"name": primary_col["name"], "type": primary_col["type"], "nullable": primary_col["nullable"], "unique": primary_col["unique"], "default": primary_col["default"]})
            command += f", PRIMARY KEY({primary_col['name']}))"
            self.cursor.execute(command)
            self.conn.commit()

            table_columns.remove(primary_col)
            
        self.check_colums(table_name, table_columns)


class DBGet:
    def __init__(self, conn, cursor):
        self.conn: sql.Connection = conn
        self.cursor: sql.Cursor = cursor
    
    def all_columns(self, table_name: str):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        data = {}
        for i in self.cursor.fetchall():
            data[i[1]] = {"name": i[1], "type": i[2], "nullable": not bool(i[3]), "default": i[4], "primary_key": bool(i[5])}
        return data
    
    def all_columns_names(self, table_name: str):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return [i[1] for i in self.cursor.fetchall()]

    def user_infos(self, id: int, only_elements: bool = False):
        self.cursor.execute(f"SELECT * FROM users WHERE discord_id = {id}")
        _data = self.cursor.fetchone()

        if _data:
            if only_elements:
                return _data
            
            data = {}
            columns = self.all_columns_names("users")
            for i in range(len(columns)):
                data[columns[i]] = _data[i]
            return data
        return None
    
    def nb_connexions(self, id: int):
        self.cursor.execute(f"SELECT connexions FROM users WHERE discord_id = {id}")
        return self.cursor.fetchone()[0]
    
    def leaderboard(self, limit: int = 10):
        if limit == -1:
            self.cursor.execute(f"SELECT * FROM users ORDER BY connexions DESC")
        else:
            self.cursor.execute(f"SELECT * FROM users ORDER BY connexions DESC LIMIT {limit}")
        return self.cursor.fetchall()


class DBUpdate:
    def __init__(self, conn, cursor):
        self.conn: sql.Connection = conn
        self.cursor: sql.Cursor = cursor
    
    def user_infos(self, id: int, data: dict[str, str | int | bool]):
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{i}'" if isinstance(i, str) else str(i) for i in data.values()])
        
        self.cursor.execute(f"UPDATE users SET {columns} = {values} WHERE discord_id = {id}")
        self.conn.commit()
    
    def add_user(self, id: int, connexions: int):
        self.cursor.execute(f"INSERT INTO users (discord_id, connexions) VALUES ({id}, {connexions})")
        self.conn.commit()
    
    def user(self, id: int, data: dict[str, str | int | bool]):
        for key in data:
            self.cursor.execute(f"UPDATE users SET {key} = {data[key]} WHERE discord_id = {id}")
        self.conn.commit()


class DBDelete:
    def __init__(self, conn, cursor):
        self.conn: sql.Connection = conn
        self.cursor: sql.Cursor = cursor
    
    def user(self, id: int):
        self.cursor.execute(f"DELETE FROM users WHERE discord_id = {id}")
        self.conn.commit()
    
    def all(self):
        self.cursor.execute(f"DELETE FROM users")
        self.conn.commit()
    
    def table(self, table_name: str):
        self.cursor.execute(f"DELETE FROM {table_name}")
        self.conn.commit()
    
    def all_tables(self):
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for table in tables:
            self.cursor.execute(f"DELETE FROM {table[0]}")
        self.conn.commit()