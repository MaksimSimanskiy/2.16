#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os
import jsonschema


def get_shop():
    """
    Данная функция добавляет пары
    ключ-значение в словарь
    для каждого товара
    """
    name = input("Название магазина ")
    product = input("Товар ")
    price = int(input("Цена "))
    return{
        'name': name,
        'product': product,
        'price': price,
    }


def display_shops(shops):
    """
    Отображает данные о товаре в виде таблицы и
    Сортирует данные, по названию маганзина
    """
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 8,
        '-' * 20
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
            "No",
            "Название.",
            "Товар",
            "Цена"
        )
    )
    print(line)
    for idx, shop in enumerate(shops, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(

                idx,
                shop.get('name', ''),
                shop.get('product', ''),
                shop.get('price', 0)

            )
        )
        print(line)


def select_shops(shops):
    """
    По заданому магазину находит товары, находящиеся в нем,
    если магазина нет - показывает соответсвующее сообщение
    """
    sname = input("Название магазина ")
    cout = 0
    for shop in shops:
        if (shop.get('name') == sname):
            cout = 1
            print(
                ' | {:<5} | {:<5} '.format(
                    shop.get('product', ''),
                    shop.get('price', 0),
                )
            )
        elif cout == 0:
            print("Такого магазина нет")


def save_shops(file_name, shops):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(shops, fout, ensure_ascii=False, indent=4)


def load_shops(file_name):
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "product": {
                        "type": "string"
                    },
                    "price": {
                        "type": "number"
                    }
                },
                "required": [
                    "name",
                    "product",
                    "price"
                ]
            }
        ]
    }
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadfile):
                print("Валидация прошла успешно")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации", list(validator.iter_errors(loadfile)))
            exit()
    return loadfile


def main():
    """
    главная функция программы
    """
    shops = []
    while True:
        command = input(">>> ").lower()
        if command == 'exit':
            break
        elif command == 'add':
            shop = get_shop()
            shops.append(shop)
            if len(shops) > 1:
                shops.sort(key=lambda item: item.get('product', ''))
        elif command == 'list':
            display_shops(shops)
        elif command.startswith('select '):
            selected = select_shops(shops)
            display_shops(selected)
        elif command.startswith('save'):
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_shops(file_name, shops)
        elif command.startswith('load'):
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            shops = load_shops(file_name)
        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить магазин;")
            print("select - показать товары из заданного магазина;")
            print("list - вывести список магазинов;")
            print("save - сохранить список магазинов;")
            print("load - загрузить список магазинов;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
