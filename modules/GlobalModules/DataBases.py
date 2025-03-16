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
        self.create_db_and_table()
    
    def create_db_and_table(self) -> None:
        """Создает базу данных и таблицу"""
        
        def get_column_crete_info(column: dict) -> str:
            """Строка с созданием колонки"""
            
            return (
                f'''{column['name']} {column['type']}'''
                f'''{' not null' if column.get('not_null') else ''}'''
                f'''{' primary key' if column.get('primary_key') else ''}'''
                f'''{f' default {column.get("default")}' if column.get('default') else ''}'''
            )
        
        columns_str = ',\n\t'.join([get_column_crete_info(column) for column in self.columns])
        
        query = (
            f'''create table if not exists {self.table_name}(\n\t'''
            f'{columns_str}'
            '\n)'
        )
        asyncio.run(self.run_query(query))
    
    def add_values(self, data: tuple[dict[str, str|int|float]]) -> None:
        """Добавляет записи в таблицу"""
        
        first_row_keys = list(data[0].keys())
        
        for row in data:
            row_keys = frozenset(row.keys())
            if len(frozenset(first_row_keys) ^ row_keys) > 0:
                raise ValueError((
                    'Разное количество параметров в строках. '
                    f'''Первая строка: {', '.join(first_row_keys)}. '''
                    f'''Другая: {', '.join(row_keys)}'''
                ))
            
        query = f'''insert into {self.table_name} values({', '.join([f':{column}' for column in first_row_keys])})'''
        
        asyncio.run(self.run_query(
            query=query,
            data=data
        ))
    
    def update_values(self, new_values: dict, condition: str) -> None:
        """Обновляет данные в таблице"""
        
        set_clause = ', '.join([f'''{column} = ?''' for column in new_values.keys()])
        query = f'''update {self.table_name} set {set_clause} where {condition}'''
        values = tuple(new_values.values())
        
        asyncio.run(self.run_query(
            query=query,
            values=values
        ))
    
    def get_values(self, columns_name: list, condition: str) -> list:
        """Достает записи из таблицы"""
        
        query = f'''select {', '.join(columns_name)} from {self.table_name} where {condition}'''
        return asyncio.run(self.run_query(query=query))
    
    def drop_values(self, condition: str) -> None:
        """Удаляет записи"""
        
        query=f'''delete from {self.table_name} where {condition}'''
        
        asyncio.run(self.run_query(query=query))
    
    def get_table_info(self) -> list:
        """
            Получение информации о таблице
            
            column_id       - Идентификатор колонки
            name            - Имя колонки
            type            - Тип данных колонки
            is_not_null     - Может ли колонка содержать NULL (0 или 1)
            default_value   - Значение по умолчанию
            is_primary_key  - Является ли колонка частью первичного ключа (0 или 1)
        """
        
        table_info = []
        column_names = [
            'column_id', 'name', 'type', 'is_not_null',
            'default_value', 'is_primary_key'
        ]
        query = f'''pragma table_info({self.table_name})'''
        
        for column in asyncio.run(self.run_query(query=query)):
            column_dict = dict(zip(column_names, column))
            table_info.append(column_dict)
        return table_info
    
    async def run_query(self, query: str, data: tuple[dict[str, str|int|float]]=None, values: tuple[int|str|float]=None) -> Any:
        """Запрос в базу данных"""
        
        with sq.connect(self.path) as connect:
            if data:
                return connect.cursor().executemany(query, data).fetchall()
            elif values:
                return connect.cursor().execute(query, values).fetchall()
            else:
                return connect.cursor().execute(query).fetchall()


if __name__ == '__main__':
    import json
    with open('/home/hubble_dj/hubble_assistant_bot/databases/global_db/schemes.json', 'r') as f:
        db_info = json.load(f)
        
    for table in db_info:
        db = DB(
            path=f'''/home/hubble_dj/hubble_assistant_bot/databases/global_db/{table['name']}.db''',
            table_name=table['name'],
            columns=table['columns']
        )
        
        if db.table_name == 'text':
            db.add_values(
                data=(
                    {
                        'name': 'лол',
                        'text': 'Рандомный текст',
                        'group_in': '[]',
                        'group_not_in': '[]'
                    },
                )
            )

            db.drop_values(condition='name=1')
            
            db.update_values(
                new_values={'group_in': '1'},
                condition='name="test"'
            )
            
            print(db.get_values(columns_name=['group_in'], condition='name="валера"'))
            print(db.get_table_info())
        