import psutil
import re


def get_vfs_name():
    """Возвращает тип файловой системы первого диска."""
    return psutil.disk_partitions()[0].fstype


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

    def replace_var(match):
        var_name = match.group(1) or match.group(2)
        return env_vars.get(var_name, match.group(0))

    pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)|\$\{([^}]*)\}'
    return re.sub(pattern, replace_var, text)


if __name__ == "__main__":
    vfs_name = get_vfs_name()
    # после ошибки в приглашении к вводу будет -
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

        cmd, *args = parts
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