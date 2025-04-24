import timeit

import pandas as pd
from BTrees.OOBTree import OOBTree

# Завантаження CSV
df = pd.read_csv("generated_items_data.csv")

# Створення структур
tree_by_price = OOBTree()  # ключ = Price, значення = список товарів з цією ціною
dict_by_id = {}  # ключ = ID, значення = товар


# Додавання елементів
def add_item_to_tree_by_price(tree, item):
    price = item['Price']
    record = {'ID': item['ID'], 'Name': item['Name'], 'Category': item['Category'], 'Price': price}
    if price in tree:
        tree[price].append(record)
    else:
        tree[price] = [record]


def add_item_to_dict(dct, item):
    dct[item['ID']] = {'Name': item['Name'], 'Category': item['Category'], 'Price': item['Price']}


for _, row in df.iterrows():
    item = row.to_dict()
    add_item_to_tree_by_price(tree_by_price, item)
    add_item_to_dict(dict_by_id, item)


# Функції діапазонного запиту
def range_query_tree(tree, min_price, max_price):
    results = []
    for price, items in tree.items(min_price, max_price):
        results.extend(items)
    return results


def range_query_dict(dct, min_price, max_price):
    return [item for item in dct.values() if min_price <= item['Price'] <= max_price]


# Timeit-обгортки
def make_tree_query():
    return lambda: range_query_tree(tree_by_price, 100.0, 300.0)


def make_dict_query():
    return lambda: range_query_dict(dict_by_id, 100.0, 300.0)


if __name__ == '__main__':
    # Вимірювання часу
    tree_total_time = timeit.timeit(make_tree_query(), number=100)
    dict_total_time = timeit.timeit(make_dict_query(), number=100)

    # Вивід
    print(f"Total range_query time for OOBTree: {tree_total_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_total_time:.6f} seconds")
