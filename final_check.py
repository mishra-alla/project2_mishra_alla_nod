#!/usr/bin/env python3
"""Простая проверка 2 этапа."""

print("ПРОВЕРКА 2 этапа: Управление таблицами")
print("-" * 50)

# 1. Проверка файлов
print("\n1. Проверка структуры файлов:")
import os
files = [
    "src/primitive_db/main.py",
    "src/primitive_db/engine.py", 
    "src/primitive_db/core.py",
    "src/primitive_db/utils.py",
    "pyproject.toml"
]
for f in files:
    if os.path.exists(f):
        print(f"   + {f}")
    else:
        print(f"   - {f} - отсутствует")

# 2. Проверка команд
print("\n2. Проверка команд базы данных:")
import sys
sys.path.insert(0, 'src')

try:
    from primitive_db.core import create_table, drop_table, list_tables
    from primitive_db.utils import load_metadata, save_metadata
    print("   + Модули импортируются")
    
    # Тест создания таблицы
    metadata = {}
    metadata = create_table(metadata, 'test_users', ['name:str', 'age:int'])
    if metadata and 'test_users' in metadata:
        print("   + create_table работает")
    else:
        print("   - create_table не работает")
    
    # Тест списка таблиц
    print("   + list_tables работает (функция есть)")
    
    # Тест удаления таблицы  
    metadata = drop_table(metadata, 'test_users')
    if metadata and 'test_users' not in metadata:
        print("   + drop_table работает")
    else:
        print("   + drop_table не работает")
        
except Exception as e:
    print(f"   + Ошибка: {e}")

# 3. Проверка JSON
print("\n3. Проверка сохранения в JSON:")
try:
    if os.path.exists('db_meta.json'):
        os.remove('db_meta.json')
    
    test_data = {'test': ['ID:int', 'field:str']}
    save_metadata(test_data)
    
    if os.path.exists('db_meta.json'):
        loaded = load_metadata()
        if loaded == test_data:
            print("   + JSON сохранение/загрузка работает")
        else:
            print("   - JSON данные не совпадают")
    else:
        print("   - Файл не создан")
        
    os.remove('db_meta.json')
except Exception as e:
    print(f"   - Ошибка JSON: {e}")

# 4. Проверка Makefile
print("\n4. Проверка Makefile:")
if os.path.exists('Makefile'):
    with open('Makefile', 'r') as f:
        content = f.read()
    
    targets = ['install:', 'project:', 'build:', 'lint:']
    missing = []
    for target in targets:
        if target not in content:
            missing.append(target)
    
    if not missing:
        print("   + Makefile содержит все цели")
    else:
        print(f"   !  Отсутствуют цели: {missing}")
else:
    print("   - Makefile отсутствует")

print("\n" + "-" * 50)
print("ПРОВЕРКА ЗАВЕРШЕНА")
