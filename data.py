import subprocess
import json
from datetime import datetime, timedelta

TIME_DELTA = 15 # in minutes
BLACKLIST_FILE_NAME = "blacklist.txt"
INFO_FILE_NAME = "application_info.json"
SETTINGS_FILE_NAME = "settings.json"


def get_active_apps() -> list[str]:
    # gets currently running processes with windows
    windows = []
    cmd = 'powershell "Get-Process | Where-Object {$_.mainWindowTitle} | Format-Table Id, Name, mainWindowtitle -AutoSize"'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
        if line.rstrip():
            windows.append(line.decode().rstrip().split()[1])

    return windows


def filter_apps(processes) -> list[str]:
    # filters processes based on blacklist file
    filtered_processes = []
    with open(BLACKLIST_FILE_NAME, "r") as file:
        blacklist = file.read()
        for process in processes:
            if not process in blacklist:
                filtered_processes.append(process)

    return filtered_processes


def get_apps_info(apps) -> list[dict]:
    # if app record exists - adds info to output data
    apps_info = []
    with open("application_info.json", "r") as file:
        info = json.load(file)
        for app in apps:
            if app in info.keys():
                apps_info.append(info[app])
    return apps_info


def get_apps_info() -> dict[dict]:
    try:
        with open(INFO_FILE_NAME, "r+") as file:
            records = json.load(file)
            return records
    except FileNotFoundError:
        f = open(INFO_FILE_NAME, "x")
        f.close()
        return {}
    except json.decoder.JSONDecodeError:
        return {}


def update_apps_info(current_apps: list[str], records: dict[dict]) -> dict[dict]:
    for app in current_apps:
        if app in records:
            record = records[app]
            record['Total time'] = str_to_timedelta(record['Total time']) + timedelta(minutes=TIME_DELTA)
            record['Background time'] = str_to_timedelta(record['Background time']) + timedelta(0)
            record['Active window time'] = str_to_timedelta(record['Active window time']) + timedelta(0)
            record['Last run'] = datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
            records[app] = record
        else:
            record = {}
            record['Custom name'] = app
            record['Total time'] = timedelta(0)
            record['Background time'] = timedelta(0)
            record['Active window time'] = timedelta(0)
            record['Last run'] = datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
            records[app] = record


def save_apps_info(records: dict[dict]):
    with open(INFO_FILE_NAME, "w") as file:
        file.write(json.dumps(records, default=str))


def change_custom_name(app: str, new_name: str):
    with open(INFO_FILE_NAME, "rw") as file:
        records = json.load(file)
        records[app]['Custom name'] = new_name

        file.write(json.dumps(records))


def str_to_timedelta(string: str) -> timedelta:
    if "day" in string:
        days = int(string.split(',')[0])
        hours = int(string.split(',')[1].split(':')[0])
        minutes = int(string.split(',')[1].split(':')[1])
        return timedelta(days=days, hours=hours, minutes=minutes)
    else:
        hours = int(string.split(':')[0])
        minutes = int(string.split(':')[1])
        return timedelta(hours=hours, minutes=minutes)


if __name__ == "__main__":
    active_apps = get_active_apps()
    print(active_apps)

    filtered_apps = filter_apps(active_apps)
    print(filtered_apps)

    records = get_apps_info()
    print(records)

    update_apps_info(filtered_apps, records)
    print(records)

    save_apps_info(records)