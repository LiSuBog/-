def parse_recipes(file_path):
    """Парсит файл с рецептами и возвращает словарь рецептов."""
    cook_book = {}
    with open(file_path, encoding='utf-8') as f:
        while True:
            dish_name = f.readline().strip()
            if not dish_name:
                break
            print(f"Считываем блюдо: {dish_name}")  # Отладочный вывод
            ingredient_count = int(f.readline().strip())
            ingredients = []
            for _ in range(ingredient_count):
                ingredient_line = f.readline().strip()
                ingredient_name, quantity, measure = ingredient_line.split(' | ')
                ingredients.append({
                    'ingredient_name': ingredient_name,
                    'quantity': int(quantity),
                    'measure': measure
                })
            cook_book[dish_name] = ingredients
    return cook_book

def get_shop_list_by_dishes(dishes, person_count, cook_book):
    """Создает список покупок на основе выбранных блюд и количества персон."""
    shopping_list = {}
    for dish in dishes:
        print(f"Проверяем наличие блюда: '{dish}'")  # Отладочный вывод
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                name = ingredient['ingredient_name']
                quantity = ingredient['quantity'] * person_count
                measure = ingredient['measure']
                if name in shopping_list:
                    shopping_list[name]['quantity'] += quantity
                else:
                    shopping_list[name] = {'measure': measure, 'quantity': quantity}
        else:
            print(f"Блюдо '{dish}' не найдено в рецептах.")
    return shopping_list

def merge_files(file_list, output_file):
    """Объединяет содержимое файлов в один с указанием количества строк."""
    file_data = []

    for file_name in file_list:
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                file_data.append((file_name, len(lines), lines))
        except FileNotFoundError:
            print(f"Warning: File '{file_name}' not found and will be skipped.")
            continue

    # Сортируем файлы по количеству строк
    file_data.sort(key=lambda x: x[1])

    with open(output_file, 'w', encoding='utf-8') as output:
        for file_name, line_count, lines in file_data:
            output.write(f"{file_name}\n{line_count}\n")
            output.writelines(lines)

# Пример использования
if __name__ == "__main__":
    # Чтение кулинарной книги
    cook_book_path = 'Recipes.txt'  # Путь к файлу с рецептами
    cook_book = parse_recipes(cook_book_path)

    print("Кулинарная книга:", cook_book)  # Это должно показать всю кулинарную книгу

    # Выведите все названия блюд
    print("Список блюд в кулинарной книге:")
    for dish in cook_book.keys():
        print(dish)

    # Получение списка покупок для заданных блюд и количества персон
    dishes_to_prepare = ['Фахитос', 'Запеченный картофель']
    person_count = 2
    shop_list = get_shop_list_by_dishes(dishes_to_prepare, person_count, cook_book)

    print("Список покупок:")
    for ingredient, info in shop_list.items():
        print(f"{ingredient}: {info['quantity']} {info['measure']}")

    # Список файлов для объединения
    files_to_merge = ['1.txt', '2.txt', '3.txt']

    # Путь к выходному файлу
    output_file_path = 'merged.txt'

    merge_files(files_to_merge, output_file_path)
    print(f"Файлы объединены в {output_file_path}")