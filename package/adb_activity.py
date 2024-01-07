import subprocess

def run_adb_command_activity(command):
    try:
        adb_command = f"adb shell {command}"
        output = subprocess.check_output(adb_command, shell=True)
        with open('adb_output.txt', 'w') as f:
            f.write(output.decode('utf-8'))
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败：{e}")

# 执行adb命令
def activity():
    print("All:\n")
    command = 'su -c "dumpsys window"'
    run_adb_command_activity(command)
    print("\nOn Windows:\n")
    command = 'su -c "dumpsys window | grep Current"'
