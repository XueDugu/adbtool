# import subprocess

# def run_adb_test(command):
#     try:
#         process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         # 等待进程完成
#         process.wait()
#         result=process.stdout.readline()
#         if result:
#             result = result[:-1]
#             print("操作成功！")
#             command = 'adb forward tcp:27042 tcp:27042'
#             run_adb_command(command)
#             command = 'adb shell su -c "{0}"'.format(result)
#             result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
#         else:
#             print("没找到frida-server不在指定位置,操作失败!")
#     except subprocess.CalledProcessError as e:
#         print(f"命令执行失败：{e}")

# def run_adb_command(command):
#     try:
#         result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
#         if result.returncode == 0:
#             print("操作成功！")
#         else:
#             print("操作失败！")
#             print(result.stderr)
#     except subprocess.CalledProcessError as e:
#         print(f"命令执行失败：{e}")
#     except Exception as e:
#         print(f"发生未知错误：{e}")

# # 执行adb命令
# command = 'adb shell su -c "find /data/local|grep frida-server"'
# run_adb_test(command)

import subprocess

def run_adb_test(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.wait()
        result = process.stdout.readline().strip()
        if result:
            print("操作成功！")
            command_forward = 'adb forward tcp:27042 tcp:27042'
            run_adb_command(command_forward)

            command_execute = f'adb shell su -c "{result}"'
            run_adb_command(command_execute)
        else:
            print("没找到frida-server不在指定位置,操作失败!")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败：{e}")

def run_adb_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print("操作成功！")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
        else:
            print("操作失败！")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

# 执行adb命令
command = 'adb shell su -c "find /data/local | grep frida-server"'
run_adb_test(command)
