import argparse
import os
import psutil


def get_vfs_name():
    """Возвращает тип файловой системы первого диска."""
    partitions = psutil.disk_partitions()
    return partitions[0].fstype if partitions else "UNKNOWN"


def expand_environment_variables(text):
    """
    Раскрывает переменные окружения в тексте.
    Заменяет $VAR и ${VAR} на заданные значения.
    """
    env_vars = {
        "HOME": "/home/user",
        "USER": "testuser",
        "PWD": "/home/user/vfs",
        "VFS_ROOT": "/vfs/storage"
    }

    import re
    def replace_var(match):
        var_name = match.group(1) or match.group(2)
        return env_vars.get(var_name, match.group(0))

    pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)|\$\{([^}]*)\}'
    return re.sub(pattern, replace_var, text)


def run_script(script_path):
    """Выполняет команды из скрипта с отображением ввода и вывода."""
    try:
        with open(script_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):  # Пропускаем пустые строки и комментарии
                    continue

                print(f"[script] > {line}")  # Показываем ввод
                expanded_line = expand_environment_variables(line)
                parts = expanded_line.split()
                cmd, *args = parts

                # Обрабатываем команды
                if cmd == "ls":
                    print(cmd, args)
                elif cmd == "cd":
                    print(cmd, args)
                elif cmd == "exit":
                    return
                else:
                    print("command not found")
    except Exception as e:
        print(f"Ошибка выполнения скрипта: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Эмулятор командной оболочки")
    parser.add_argument("--vfs", type=str, help="Путь к физическому расположению VFS")
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту")

    args = parser.parse_args()

    # Отладочный вывод параметров
    print(f"[DEBUG] VFS путь: {args.vfs}")
    print(f"[DEBUG] Скрипт: {args.script}")

    # Если указан скрипт - выполняем его
    if args.script:
        if os.path.exists(args.script):
            run_script(args.script)
        else:
            print(f"Ошибка: скрипт {args.script} не найден")

    # Запускаем интерактивный режим
    vfs_name = get_vfs_name()
    success_symbol = "✓"
    failure_symbol = "✗"
    status_symbol = success_symbol
    success = True

    while True:
        if success:
            status_symbol = success_symbol
        else:
            status_symbol = failure_symbol

        inp = input(f"[ {vfs_name} ] {status_symbol} > ")

        expanded_inp = expand_environment_variables(inp)
        parts = expanded_inp.split()

        if not parts:
            continue

        cmd, *raw_args = parts
        args = []
        success_vars = True
        for arg in raw_args:
            if arg[0] == "$":
                try:
                    var = os.environ[arg[1:]]
                    #args.append(var)
                except KeyError:
                    # Если переменной нет, оставляем оригинальную строку
                    print("Не удалось получить переменную окружения")
                    success_vars = False
            else:
                args.append(arg)
        # cmd, *args = parts
        if success_vars:
            match cmd:
                case "ls":
                    print(cmd, args)
                    success = True

                case "cd":
                    print(cmd, args)
                    success = True

                case "exit":
                    exit(0)

                case _:
                    print("command not found")
                    success = False