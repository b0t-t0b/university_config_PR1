import psutil
import re
import os


def get_vfs_name():
    """Возвращает тип файловой системы первого диска."""
    return psutil.disk_partitions()[0].fstype


def expand_environment_variables(text):
    """
    Раскрывает переменные окружения в тексте.
    Заменяет $VAR и ${VAR} на заданные значения.
    """
    def replace_var(match):
        var_name = match.group(1) or match.group(2)
        # Пытаемся получить переменную из окружения
        try:
            return os.environ[var_name]
        except KeyError:
            # Если переменной нет, оставляем оригинальную строку
            return match.group(0)

    pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)|\$\{([^}]*)\}'
    return re.sub(pattern, replace_var, text)


if __name__ == "__main__":
    vfs_name = get_vfs_name()
    success_symbol = "+"
    failure_symbol = "-"
    status_symbol = success_symbol
    success = True

    while True:
        if success:
            status_symbol = success_symbol
        else:
            status_symbol = failure_symbol

        inp = input(f"[ {vfs_name} ] {status_symbol} > ")

        # Раскрываем переменные окружения перед парсингом
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
                    args.append(var)
                except KeyError:
                    # Если переменной нет, оставляем оригинальную строку
                    print("Не удалось получить переменную окружения")
                    success_vars = False
            else:
                args.append(arg)

        # if len(args) == 1 and args[0] == "$":
        #     try:
        #         print(os.environ[args[1:]])
        #     except KeyError:
        #         # Если переменной нет, оставляем оригинальную строку
        #         print("Не удалось получить переменную окружения")

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