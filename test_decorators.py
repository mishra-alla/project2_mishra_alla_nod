#!/usr/bin/env python3
"""Тестирование декораторов."""

import sys
import os
sys.path.insert(0, 'src')

from primitive_db.engine import run

# Очищаем старые данные
if os.path.exists('db_meta.json'):
    os.remove('db_meta.json')
if os.path.exists('data'):
    import shutil
    shutil.rmtree('data')

# Тестовые команды для проверки декораторов
commands = [
    "create_table users name:str age:int is_active:bool",
    "insert into users values (\"Тест1\", 25, true)",
    "insert into users values (\"Тест2\", 30, false)",
    "insert into users values (\"Тест3\", 28, true)",
    
    # Проверяем кэширование - первый вызов
    "select from users",
    # Второй вызов (должен быть быстрее из-за кэша)
    "select from users",
    
    # Проверяем select с условием
    "select from users where age > 26",
    
    # Проверяем обновление
    "update users set age = 31 where name = \"Тест2\"",
    
    # Проверяем удаление (будет запрос подтверждения)
    "delete from users where name = \"Тест1\"",
    
    # Проверяем info
    "info users",
    
    # Проверяем list_tables
    "list_tables",
    
    # Проверяем удаление таблицы (будет запрос подтверждения)
    "drop_table users",
    
    # Проверяем list_tables после удаления
    "list_tables",
    
    "exit"
]

# Мок для input с автоматическим подтверждением
input_index = 0
def mock_input(prompt):
    global input_index
    
    # Автоматически подтверждаем все действия для теста
    if "Вы уверены" in prompt:
        print(f"{prompt}y")
        return "y"
    
    if input_index < len(commands):
        cmd = commands[input_index]
        print(f"{prompt}{cmd}")
        input_index += 1
        return cmd
    
    return "exit"

import builtins
original_input = builtins.input
builtins.input = mock_input

print("=== ТЕСТ ДЕКОРАТОРОВ ===")
print("1. Проверяем кэширование запросов")
print("2. Проверяем подтверждение действий")
print("3. Проверяем логирование времени")
print("=" * 60)

run()
builtins.input = original_input

print("=" * 60)
print("=== ТЕСТ ЗАВЕРШЕН ===")

# Проверяем что файлы создались и удалились
print("\nПроверка файлов:")
if os.path.exists('db_meta.json'):
    print("db_meta.json создан")
else:
    print("db_meta.json не создан - таблица удалена")

if os.path.exists('data/users.json'):
    print("data/users.json создан")
else:
    print("data/users.json не создан - таблица удалена")
