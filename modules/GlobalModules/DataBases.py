"""Работа с базами данных"""

import asyncio
from typing import Any
import sqlite3 as sq

class DB:
    """
        Класс для работы с базой данных
        Одна таблица == одна база данных
    """
    
    def __init__(self, path: str, table_name: str, columns: dict):
        self.path = path
        self.table_name = table_name
        self.columns = columns

        self.create_db()
    
    def create_db(self) -> None:
        """Создает базу данных"""
        
        def get_column_crete_info(column: dict) -> str:
            """Строка с созданием колонки"""
            
            column_str = (
                f'''{column['name']} {column['type']}'''
                f'''{' not null' if column.get('not_null') else ''}'''
                f'''{' primary key' if column.get('primary_key') else ''}'''
                f'''{f' default {column.get("default")}' if column.get('default') else ''}'''
            )
            
            return column_str
        
        columns_str = ',\n\t'.join([get_column_crete_info(column) for column in self.columns])
        
        query = (
            f'''create table if not exists {self.table_name}(\n\t'''
            f'{columns_str}'
            '\n)'
        )
        
        asyncio.run(self.run_query(query))
    
    
    def create_table(self) -> None:
        """Создает таблицу"""
        
        pass
    
    
    def add_values(self, columns: list, values: list):
        """Добавляет записи в таблицу"""
        
        pass
    
    
    def update_values(self, new_values: dict, condition: str) -> None:
        """Обновляет данные в таблице"""
        
        pass
    
    
    def get_values(self, columns_name: list, condition: str) -> list:
        """Достает записи из таблицы"""
        
        pass
    
    
    def drop_values(self, condition: str) -> None:
        """Удаляет записи"""
        
        pass
    
    
    async def run_query(self, query: str) -> Any:
        """Запрос в базу данных"""
        
        with sq.connect(self.path) as connect:
            return connect.cursor().execute(query).fetchall()
        

if __name__ == '__main__':
    import json
    with open('/home/hubble_dj/hubble_assistant_bot/databases/global_db/schemes.json', 'r') as f:
        db_info = json.load(f)
        
    for table in db_info:
        DB(
            path=f'''/home/hubble_dj/hubble_assistant_bot/databases/global_db/{table['name']}.db''',
            table_name=table['name'],
            columns=table['columns']
        )