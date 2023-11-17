import subprocess
import time

def run_adb_command(command):
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

# 执行adb命令
package_name = "com.github.kr328.clash"
activity_name = "com.github.kr328.clash.MainActivity"
command = f'adb shell su -c "am start -n {package_name}/{activity_name}"'
run_adb_command(command)
time.sleep(0.5)
command_start=f'adb shell su -c "input tap 690 690"'
run_adb_command(command_start)