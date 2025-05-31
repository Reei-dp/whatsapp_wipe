import ctypes
import sys
import os
import shutil
import subprocess
import winreg
import uuid


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()


def stop_whatsapp():
    try:
        subprocess.call(["taskkill", "/f", "/im", "WhatsApp.exe"])
    except Exception as e:
        print(e)


def delete_whatsapp_data():
    possible_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\WhatsApp"),
        os.path.expandvars(r"%APPDATA%\WhatsApp"),
        r"C:\Program Files\WindowsApps",
        r"C:\Program Files\WhatsApp",
        r"C:\Program Files (x86)\WhatsApp"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                shutil.rmtree(path, ignore_errors=True)
                print(f"Удалена папка: {path}")
            except Exception as e:
                print(f"Ошибка при удалении {path}: {e}")


def change_machine_guid():
    key_path = r"SOFTWARE\Microsoft\Cryptography"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        new_guid = str(uuid.uuid4())
        winreg.SetValueEx(reg_key, "MachineGuid", 0, winreg.REG_SZ, new_guid)
        winreg.CloseKey(reg_key)
        print(f"Новый MachineGuid: {new_guid}")
    except PermissionError:
        print("Недостаточно прав для изменения MachineGuid (требуются права администратора)")


def delete_whatsapp_desktop_folders():
    base_path = r"C:\Program Files\WindowsApps"

    if not os.path.exists(base_path):
        print(f"Путь не найден: {base_path}")
        return

    try:
        for folder in os.listdir(base_path):
            if "WhatsAppDesktop" in folder:
                full_path = os.path.join(base_path, folder)
                try:
                    shutil.rmtree(full_path, ignore_errors=True)
                    print(f"Удалена папка: {full_path}")
                except Exception as e:
                    print(f"Ошибка при удалении {full_path}: {e}")
    except PermissionError:
        print("Недостаточно прав для чтения содержимого WindowsApps (требуются права администратора)")


if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    stop_whatsapp()
    delete_whatsapp_desktop_folders()
    delete_whatsapp_data()
    change_machine_guid()
