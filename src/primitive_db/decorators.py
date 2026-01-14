#!/usr/bin/env python3
"""Decorators for the primitive database."""
import time
import functools
from typing import Callable, Any, Dict


def handle_db_errors(func: Callable) -> Callable:
    """Декоратор для обработки ошибок базы данных."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"Ошибка: Файл не найден - {e}")
            return None
        except KeyError as e:
            print(f"Ошибка: Ключ не найден - {e}")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка в {func.__name__}: {e}")
            return None
    
    return wrapper


def confirm_action(action_name: str) -> Callable:
    """Декоратор для подтверждения действий."""
    
    def decorator(func: Callable) -> Callable:
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower()
            if answer == 'y' or answer == 'yes' or answer == 'да':
                return func(*args, **kwargs)
            else:
                print('Операция отменена.')
                return None
        
        return wrapper
    
    return decorator


def log_time(func: Callable) -> Callable:
    """Декоратор для логирования времени выполнения."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        
        # Просто выводим время как в примере задания
        print(f'Функция {func.__name__} выполнилась за {end_time - start_time:.3f} секунд')
        
        return result
    
    return wrapper

def create_cacher() -> Callable:
    """Создаёт кэширующую функцию с замыканием."""
    
    cache: Dict[str, Any] = {}
    
    def cache_result(key: str, value_func: Callable) -> Any:
        """Кэширует результат функции."""
        if key in cache:
            return cache[key]
        
        result = value_func()
        cache[key] = result
        return result
    
    # Добавляем метод для очистки кэша
    cache_result.clear = lambda: cache.clear()
    
    return cache_result


# Глобальный кэш для запросов
query_cacher = create_cacher()
