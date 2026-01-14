#!/usr/bin/env python3
"""Utility functions for the primitive database."""

import json
from .decorators import handle_db_errors


@handle_db_errors
def load_metadata(filepath="db_meta.json"):
    """загрузка данных из json"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


@handle_db_errors
def save_metadata(data, filepath="db_meta.json"):
    """сохранение данных в json"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
