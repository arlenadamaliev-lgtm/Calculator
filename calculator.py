import os


def get_number(prompt, memory=None):
    """Запрашивает число, повторяет при ошибке ввода.
    Если memory не None и пользователь ввёл 'mem' или 'm' — вернуть memory."""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in ("mem", "m"):
            if memory is not None:
                return memory
            else:
                print("Память пуста. Пожалуйста, введите число.")
                continue
        try:
            return float(user_input)
        except ValueError:
            print("Ошибка: введите число или 'mem' (если память не пуста)")


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Ошибка: деление на ноль"


def save_to_history(operation_str):
    """Сохраняет строку операции в файл history.txt"""
    if not os.path.exists("Calculator/history.txt"):
        mode = "w"
    else:
        mode = "a"
    with open("Calculator/history.txt", mode, encoding="utf-8") as f:
        f.write(f"{operation_str}\n")


def show_history():
    """Показывает последние 100 операций из history.txt"""
    if not os.path.exists("Calculator/history.txt"):
        print("\n✨ It's empty for now. Let's create some history! ✨")
        return

    with open("Calculator/history.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("\n📭 No operations yet. Time to calculate something! 📭")
        return

    # Берём последние 100 (или сколько есть)
    last_lines = lines[-100:]

    print("\n" + "=" * 40)
    print("📜 LAST OPERATIONS (max 100) 📜")
    print("=" * 40)
    for i, line in enumerate(last_lines, 1):
        print(f"{i:3}. {line}")
    print("=" * 40)


def main():
    memory = None
    # Словарь операций: ключ -> (символ, функция)
    operations = {
        "1": ("+", lambda a, b: a + b),
        "2": ("-", lambda a, b: a - b),
        "3": ("*", lambda a, b: a * b),
        "4": ("/", divide),
    }

    while True:
        print("\n--- Калькулятор ---")
        print("1. Сложение (+)")
        print("2. Вычитание (-)")
        print("3. Умножение (*)")
        print("4. Деление (/)")
        print("5. Выход")
        print("Или введите 'calc_history' для просмотра истории")

        choice = input("Выберите операцию (1-5) или команду: ").strip()

        # Команда просмотра истории (независимо от регистра)
        if choice.lower() == "calc_history":
            show_history()
            continue

        if choice == "5":
            print("До свидания!")
            break

        if choice not in operations:
            print(
                "🛠Ошибка: неверный выбор. Введите число от 1 до 5 или 'calc_history'."
            )
            continue

        a = get_number("Введите первое число: ", memory)
        b = get_number("Введите второе число: ", memory)

        symbol, func = operations[choice]
        result = func(a, b)

        operation_str = f"{a} {symbol} {b} = {result}"
        save_to_history(operation_str)
        print(operation_str)

        if isinstance(result, (int, float)) and not isinstance(result, str):
            memory = result
            print(f"💾 Память сохранена: {memory}")
        else:
            # Деление на ноль — очищаем память
            memory = None
            print("🧹 Память очищена (ошибка вычисления)")


if __name__ == "__main__":
    main()
