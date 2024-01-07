import subprocess

def run_adb_command(command):
    try:
        adb_command = f"adb shell {command}"
        process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        if process.returncode == 0:
            # 输出在adb shell中进行了grep，直接打印输出
            print(f"命令执行成功！输出: {output}")
        else:
            print(f"命令执行失败，错误信息：{error}")
    except Exception as e:
        print(f"发生异常：{e}")

# 在这里使用双引号包裹整个getevent命令
command = 'su -c "getevent | grep -e \'0035\' -e \'0036\'"'
run_adb_command(command)
