import os
import requests
import winreg
import datetime


def check_internet_connection(ip_address: str = "google.com") -> str:
    response = os.popen(f"ping {ip_address}").read()

    if "Ping" in response:
        return "Данный компьютер подключен к интернету"

    return "Данный компьютер не подключен к интернету"


def check_for_firewall() -> str:
    path = winreg.HKEY_LOCAL_MACHINE
    standard_profile = winreg.OpenKeyEx(
        path,
        r"SYSTEM\\ControlSet001\Services\SharedAccess\\Parameters\\FirewallPolicy\StandardProfile",
    )
    is_firewall_enabled = winreg.QueryValueEx(standard_profile, "EnableFirewall")[0]

    if standard_profile:
        winreg.CloseKey(standard_profile)

    if is_firewall_enabled == 1:
        return "Фаервол Windows Defender установлен"

    return "Фаервол Windows Defender установлен"


def firewall_activity(ip_address: str = "https://www.google.com/") -> str:
    try:
        requests.get(ip_address)
        return "Межсетевой экран функционирует неверно, либо не функционирует вовсе"
    except:
        return "Межсетевой экран функционирует корректно"


def check_for_antivirus(antivirus_name: str) -> str:
    path = winreg.HKEY_LOCAL_MACHINE

    if ("windows" or "defender") in antivirus_name.lower():
        microsoft_apps = winreg.OpenKeyEx(path, r"SOFTWARE\\Microsoft")
        for i in range(winreg.QueryInfoKey(microsoft_apps)[0]):
            if winreg.EnumKey(microsoft_apps, i) == "Windows Defender":
                return "Windows Defender установлен в системе"

        if microsoft_apps:
            winreg.CloseKey(microsoft_apps)

    list_of_apps = winreg.OpenKeyEx(
        path, r"SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Uninstall"
    )
    arr_of_subkeys = []

    for i in range(winreg.QueryInfoKey(list_of_apps)[0]):
        app_key = winreg.OpenKeyEx(list_of_apps, winreg.EnumKey(list_of_apps, i))
        arr_of_subkeys.append(app_key)

    for x in arr_of_subkeys:
        if winreg.QueryInfoKey(x)[1] > 0:
            for y in range(winreg.QueryInfoKey(x)[1]):
                if winreg.EnumValue(x, y)[1] == f"{antivirus_name}":
                    return f"Антивирус {antivirus_name} установлен в системе"

    return f"Антивирус {antivirus_name} не найден"


def antivirus_activity() -> str:
    path = winreg.HKEY_LOCAL_MACHINE
    windows_defender = winreg.OpenKeyEx(path, r"SOFTWARE\\Microsoft\Windows Defender")
    if winreg.QueryValueEx(windows_defender, "DisableAntiVirus")[0] == 0:
        return "Антивирус Windows Defender работает"

    return "Антивирус Windows Defender не работает"


def show_results(results: set) -> str:
    i = 1
    results_string = ""

    if len(results) == 0:
        print("Результаты отсутствуют")
        return results_string

    for result in results:
        results_string += f"{i} - {result}\n"
        i += 1

    return results_string


def write_results(results_str: str) -> None:
    if len(results_str) == 0:
        return

    current_time = datetime.datetime.now().strftime("Результаты от %d.%m.%y, %H:%M:%S")

    results_file = open("./results.txt", "a", encoding="utf-8")
    results_file.write(f"{current_time}:\n{results_str}\n")
    results_file.close()

    print(
        "Результаты были записаны в текстовый файл results.txt, расположенном в папке проекта"
    )


if __name__ == "__main__":
    program_is_working = True
    results = set()

    print(
        """1. Проверка наличия подключения к интернету
2. Проверка наличия установленного межсетевого экрана
3. Проверка работоспособности межсетевого экрана
4. Проверка наличия установленного антивируса
5. Проверка работоспособности антивирусного ПО
6. Вывести результаты
7. Сохранить результаты в файл
8. Выйти из программы"""
    )

    while program_is_working:
        user_input = str(input("Введите команду: "))

        match user_input:
            case "1":
                results.add(check_internet_connection())
                print(check_internet_connection())
            case "2":
                results.add(check_for_firewall())
                print(check_for_firewall())
            case "3":
                results.add(firewall_activity())
                print(firewall_activity())
            case "4":
                arg = str(input("Введите наименование Вашего антивируса: "))
                if not arg.strip():
                    print("Не был введено наименование антивируса")
                    continue
                results.add(check_for_antivirus(arg))
                print(check_for_antivirus(arg))
            case "5":
                results.add(antivirus_activity())
                print(antivirus_activity())
            case "6":
                print(show_results(results))
            case "7":
                write_results(show_results(results))
            case "8":
                print("Был произведен выход из программы")
                program_is_working = False
            case _:
                print("Введено неверное значение")
