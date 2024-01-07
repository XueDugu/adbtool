import subprocess

def run_adb_command_back(command):
    try:
        adb_command = f"adb shell {command}"
        subprocess.check_output(adb_command, shell=True)
        # with open('adb_output.txt', 'a') as f:
        #     f.write(output.decode('utf-8') + "\n")
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败：{e}")
        
def back():
    command='su -c "input keyevent 4"'
    run_adb_command_back(command)