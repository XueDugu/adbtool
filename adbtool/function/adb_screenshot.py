import subprocess
import re
import time

def run_adb_command(command):
    try:
        adb_command = f"adb shell {command}"
        subprocess.check_output(adb_command, shell=True)
        print("命令执行成功！")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败：{e}")

try:
    # 启动getevent并将输出直接读取到变量中
    adb_command = 'adb shell su -c "wm size"'
    process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    line = process.stdout.readline()
    event_parts = re.split(r'\s+', line.strip())
    width=event_parts[0]
    length=event_part[2]
    time.sleep(0.2)
    print("width:", width)
    print("length:", length)
    process.terminate()
except Exception as e:
    print(f"发生异常：{e}")

width_half = int(width * 0.5)
length_start = int(length * 0.8)
length_end = int(length * 0.25)

start_coords = f"{width_half} {length_start}"
end_coords = f"{width_half} {length_end}"
scroll_steps = "10"

scroll_command = f"input touchscreen swipe {start_coords} {end_coords} {scroll_steps}"
run_adb_command(scroll_command)

# 截屏
filename = "/storage/emulated/0/Pictures/screenshot.png"
screenshot_command = f'su -c "screencap -p > {filename}"'
run_adb_command(screenshot_command)