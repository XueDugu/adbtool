import subprocess
import re
import time

def record_touch_events(duration=10, tap35_list=None, tap36_list=None):
    try:
        # 启动getevent并将输出直接读取到变量中
        adb_command = 'adb shell su -c "getevent | grep -e \'0035\' -e \'0036\'"'
        process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        start_time = time.time()
        while time.time() - start_time < duration:
            line = process.stdout.readline()
            if not line:
                break
            print(line)
            if tap35_list is not None and "0035" in line:
                tap35_list.append(int(extract_touch_value(line), 16))
            elif tap36_list is not None and "0036" in line:
                tap36_list.append(int(extract_touch_value(line), 16))

        print("x:", tap35_list)
        print("y:", tap36_list)


        # 结束getevent的进程
        process.terminate()
        print(f"getevent 运行 {duration} 秒，已停止。")

    except Exception as e:
        print(f"发生异常：{e}")

def extract_touch_value(line):
    event_parts = re.split(r'\s+', line.strip())
    return event_parts[3]  # 修正为第4个元素

def replay_touch_events():
    min_length = min(len(tap35_list), len(tap36_list))
    if min_length > 0:
        for i in range(min_length):
            subprocess.run(["adb", "shell", "input", "tap", str(tap35_list[i]), str(tap36_list[i])])
            time.sleep(0.1)  # 适当的延迟，确保事件顺利执行
    else:
        print("没有可重放的触摸事件。")


# 第一步：捕捉触摸事件，持续10秒
tap35_list = []
tap36_list = []

def touch_event_callback(line):
    if "ABS_MT_TOUCH" in line:
        if "0035" in line:
            tap35_list.append(extract_touch_value(line))
        elif "0036" in line:
            tap36_list.append(extract_touch_value(line))

record_touch_events(duration=10, tap35_list=tap35_list, tap36_list=tap36_list)

print("record over, soon to replay")
# 在手机上进行你希望捕捉的点击操作
time.sleep(1)

# 第二步：停止getevent并模拟触摸事件
replay_touch_events()
