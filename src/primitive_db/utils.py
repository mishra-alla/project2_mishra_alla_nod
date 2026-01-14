#!/usr/bin/env python3
"""Utility functions for the primitive database"""

import json
import os
from .constants import META_FILE, DATA_DIR
from .decorators import handle_db_errors


@handle_db_errors
def load_metadata(filepath=META_FILE):
    """загрузка данных из json"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


@handle_db_errors
def save_metadata(data, filepath=META_FILE):
    """сохранение данных в json"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@handle_db_errors
def load_table_data(table_name, data_dir=DATA_DIR):
    """загрузка данных таблицы из json"""
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, f"{table_name}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


@handle_db_errors
def save_table_data(table_name, data, data_dir=DATA_DIR):
    """сохранение данных таблицы в json"""
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
