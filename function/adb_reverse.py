import subprocess

def run_adb_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0 or result.stdout.strip() == "8080":
            print("操作成功！")
            if result.stdout.strip() == "8080":
                print("返回值为8080")
            else:
                print("无返回值")
        else:
            print("操作失败！")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败：{e}")

# 执行adb命令
command = 'adb reverse tcp:8080 tcp:8080'
run_adb_command(command)