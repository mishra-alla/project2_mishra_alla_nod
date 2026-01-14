#!/usr/bin/env python3
"""Engine module for the primitive database."""
import prompt


def welcome():
    """Display welcome message and handle commands."""
    print("Первая попытка запустить проект!")
    print("***")

    while True:
        command = prompt.string(
            "<command> exit - выйти из программы\n"
            "<command> help - справочная информация\n"
            "Введите команду: "
        )

        if command == "exit":
            print("Выход из программы.")
            break
        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print(f"Неизвестная команда: {command}")

    return True
