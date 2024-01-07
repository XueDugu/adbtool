import subprocess
import time

def run_adb_command_unlock(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print("操作成功！")
        else:
            print("操作失败！")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

def unlock():
# 亮屏
    close_command = f'adb shell su -c "input keyevent 82"'
    run_adb_command_unlock(close_command)
    # 显示解锁界面
    run_adb_command_unlock(close_command)
    time.sleep(0.2)
    # 输入密码
    command_0=f'adb shell su -c "input tap 780 2380"'
    run_adb_command_unlock(command_0)
    run_adb_command_unlock(command_0)
    run_adb_command_unlock(command_0)
    run_adb_command_unlock(command_0)
    time.sleep(0.1)
    # 解锁进入
    command_go=f'adb shell su -c "input tap 1140 2390"'
    run_adb_command_unlock(command_go)
    # 保持亮屏1分钟
    command_light=f'adb shell su -c "settings put system screen_off_timeout 60000"'
    run_adb_command_unlock(command_light)