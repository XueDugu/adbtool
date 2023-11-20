import os
import re
import time
import tkinter as tk
import subprocess

# 运行按钮
def run_adb_command(command, success_message):
    subprocess.run(["python", os.path.join("function", command)])
    text_box.insert(tk.END, success_message + "\n")

# 创建按钮
def create_button(root, text, adb_command):
    btn = tk.Button(root, text=text, command=lambda: run_adb_command(adb_command, f"{text} success!"), **button_style)
    return btn

# 设定按钮样式
def get_button_style():
    return {"width": 15, "height": 2, "padx": 50, "pady": 10, "bd": 4, "relief": "raised", "bg": "lightblue", "fg": "black", "font": ('Helvetica', 12, 'bold')}

root = tk.Tk()
root.title("adb工具")

text_label = tk.Label(root, text="记录栏", font=('Helvetica', 12, 'bold'))
text_label.grid(row=0, column=2, columnspan=2, pady=10)

text_box = tk.Text(root, height=15, width=50)
text_box.grid(row=1, column=2, rowspan=3, columnspan=2, padx=10, pady=10)

# 清除记录栏
def clear_text_box():
    text_box.delete("1.0", tk.END)

adb_commands = {
    "Log": "adb_log.py",
    "Reverse": "adb_reverse.py",
    "Back": "adb_back.py",
    "Home": "adb_home.py",
    "Monitor": "adb_activity.py",
    "Burp Open": "adb_burpopen.py",
    "Burp Close": "adb_burpclose.py",
    "Unlock": "adb_unlock.py",
}
button_style = get_button_style()

# 使用栈来记录用户点击的按钮
button_stack = []
run_stack = []

# 通过记忆栈重复最近的操作
def repeat_last_command(repeat_count_entry):
    try:
        repeat_count = int(repeat_count_entry.get())
        repeat_count = max(1, repeat_count)
    except ValueError:
        repeat_count = 1

    # 从栈中取出最近的按钮进行重复操作
    run_stack.clear()
    for _ in range(repeat_count):
        if button_stack:
            button_text = button_stack.pop()
            run_stack.append(button_text)

    # 从栈中取出最近的按钮进行重复操作
    for _ in range(repeat_count):
        if run_stack:
            run_text = run_stack.pop()
            button_stack.append(run_text)
            last_command = adb_commands.get(run_text)
            if last_command:
                run_adb_command(last_command, f"Repeated {run_text} success!")

# 展示记忆栈中的内容
def show_previous_commands():
    text_box.insert(tk.END, "Previous Commands: " + " -> ".join(button_stack) + "\n")

# 删除记忆栈中指定次数的内容
def delete_stack_commands(delete_count_entry):
    try:
        delete_count = int(delete_count_entry.get())
        delete_count = max(1, delete_count)
    except ValueError:
        delete_count = 1

    for _ in range(delete_count):
        text_box.insert(tk.END, "Success delete " + button_stack.pop() + " !\n")

    update_label()

for i, (button_text, adb_command) in enumerate(adb_commands.items()):
    btn = create_button(root, button_text, adb_command)
    btn.grid(row=i // 2 + 1, column=i % 2)
    btn.bind("<Button-1>", lambda event, btn=button_text: set_last_buttons_clicked(btn))

clear_btn = tk.Button(root, text="Clear", command=clear_text_box, **button_style)
clear_btn.grid(row=len(adb_commands) // 2 + 2, column=3, pady=10)

repeat_count_entry = tk.Entry(root)
repeat_count_entry.grid(row=len(adb_commands) // 2 + 3, column=2, pady=10)

repeat_btn = tk.Button(root, text="Repeat", command=lambda: repeat_last_command(repeat_count_entry), **button_style)
repeat_btn.grid(row=len(adb_commands) // 2 + 3, column=3, pady=10)

previous_btn = tk.Button(root, text="Use History", command=show_previous_commands, **button_style)
previous_btn.grid(row=len(adb_commands) // 2 + 4, column=3, pady=10)

# 根据操作次数进行Retap
def retap_count(retap_count_entry):
    try:
        retap_count = int(retap_count_entry.get())
        retap_count = max(1, retap_count)
        retap_count = min(600, retap_count)
    except ValueError:
        retap_count = 1

    # 根据操作次数记录tap
    def record_touch_events(count=1, tap35_list=None, tap36_list=None):
        try:
            # 启动getevent并将输出直接读取到变量中
            adb_command = 'adb shell su -c "getevent | grep -e \'0035\' -e \'0036\'"'
            process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            start_time = time.time()
            while time.time() - start_time < 600 and len(tap35_list) < count and len(tap36_list) < count:
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
            print(f"getevent 记录了 {count} 次操作，已停止。")

        except Exception as e:
            print(f"发生异常：{e}")

    # 读取tap的对应数据
    def extract_touch_value(line):
        event_parts = re.split(r'\s+', line.strip())
        return event_parts[3]  # 修正为第4个元素

    # 用来复现存储的操作
    def replay_touch_events():
        min_length = min(len(tap35_list), len(tap36_list))
        if min_length > 0:
            for i in range(min_length):
                subprocess.run(["adb", "shell", "input", "tap", str(tap35_list[i]), str(tap36_list[i])])
                time.sleep(0.1)  # 适当的延迟，确保事件顺利执行
        else:
            print("没有可重放的触摸事件。")

    # 第一步：捕捉触摸事件
    tap35_list = []
    tap36_list = []

    record_touch_events(retap_count, tap35_list=tap35_list, tap36_list=tap36_list)

    print("Record over, soon to replay")
    # 在手机上进行你希望捕捉的点击操作
    time.sleep(1)

    # 第二步：停止getevent并模拟触摸事件
    replay_touch_events()

    text_box.insert(tk.END, "Success retap for " + str(retap_count) + " taps\n")

# 根据时间进行Retap
def retap_time(retap_count_entry):
    try:
        retap_count = int(retap_count_entry.get())
        retap_count = max(1, retap_count)
        retap_count = min(600, retap_count)
    except ValueError:
        retap_count = 10

    # 根据时间记录tap
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

    # 读取tap的对应数据
    def extract_touch_value(line):
        event_parts = re.split(r'\s+', line.strip())
        return event_parts[3]  # 修正为第4个元素

    # 用来复现存储的操作
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

    record_touch_events(retap_count, tap35_list=tap35_list, tap36_list=tap36_list)

    print("Record over, soon to replay")
    # 在手机上进行你希望捕捉的点击操作
    time.sleep(1)

    # 第二步：停止getevent并模拟触摸事件
    replay_touch_events()

    text_box.insert(tk.END, "Success retap for " + str(retap_count) + " seconds!\n")

delete_count_entry = tk.Entry(root)
delete_count_entry.grid(row=len(adb_commands) // 2 + 5, column=2, pady=10)
delete_btn = tk.Button(root, text="Delete Stack", command=lambda: delete_stack_commands(delete_count_entry), **button_style)
delete_btn.grid(row=len(adb_commands) // 2 + 5, column=3, pady=10)

# 切换Retap函数
def switch_display():
    current_text = retap_btn.cget("text")
    if current_text == "Retap Time":
        retap_btn.config(text="Retap Count", command=lambda: retap_count(retap_count_entry))
    else:
        retap_btn.config(text="Retap Time", command=lambda: retap_time(retap_count_entry))

# 切换按钮
switch_btn = tk.Button(root, text="Switch Function", command=switch_display)
switch_btn.grid(row=len(adb_commands) // 2 + 6, column=1, pady=10)

retap_count_entry = tk.Entry(root)
retap_count_entry.grid(row=len(adb_commands) // 2 + 6, column=2, padx=10, pady=10)

retap_btn = tk.Button(root, text="Retap Time", command=lambda: retap_time(retap_count_entry), **button_style)
retap_btn.grid(row=len(adb_commands) // 2 + 6, column=3, padx=10, pady=10)

# 记录操作并存储在按钮中
def create_new_button(root, adb_commands, button_style, create_count_entry, retap_count_entry, tap35, tap36, button_stack, function):
    global create_num
    if create_count_entry.get() == "":
        name = str(create_num)
    else:
        name = create_count_entry.get()

    try:
        count = int(retap_count_entry.get())
        count = max(1, count)
        count = min(600, count)
    except ValueError:
        count = 10

    # 更新 tap35 和 tap36 列表
    tap35.append([])
    tap36.append([])

    # 记录tap
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

    # 读取tap的对应数据
    def extract_touch_value(line):
        event_parts = re.split(r'\s+', line.strip())
        return event_parts[3]  # 修正为第4个元素
    
    # 用来复现存储的操作
    def replay_touch_events(num):
        min_length = min(len(tap35[num]), len(tap36[num]))
        if min_length > 0:
            for i in range(min_length):
                subprocess.run(["adb", "shell", "input", "tap", str(tap35[num][i]), str(tap36[num][i])])
                time.sleep(0.1)  # 适当的延迟，确保事件顺利执行
        else:
            print("没有可重放的触摸事件。")

    # 使用一个列表存储函数，以便后续调用
    record_touch_events(count, tap35_list=tap35[create_num], tap36_list=tap36[create_num])

    button_stack.append(name)
    function.append(lambda num=create_num: replay_touch_events(num))
    tk.Button(root, text=name, command=function[create_num], **button_style).grid(row=len(adb_commands) // 2 + (create_num + 1) // 2 + 1, column=(create_num + 1) % 2, pady=10)
    update_label(button_stack)

    create_num += 1

# 添加Create按钮，用来记录操作并存储在按钮中
create_count_entry = tk.Entry(root)
create_count_entry.grid(row=len(adb_commands) // 2 + 7, column=2, padx=10, pady=10)
tap35=[[]]
tap36=[[]]
function = []
create_num=0
create_btn = tk.Button(root, text="Create", command=lambda: create_new_button(root, adb_commands, button_style, create_count_entry, retap_count_entry, tap35, tap36, button_stack,function), **button_style)
create_btn.grid(row=len(adb_commands) // 2 + 7, column=3, pady=10)

def set_last_buttons_clicked(button_text):
    # 将点击的按钮入栈
    button_stack.append(button_text)
    update_label()

size_label = tk.Label(root, text="Size of Stack:" + str(len(button_stack)), font=('Helvetica', 12, 'bold'))
size_label.grid(row=len(adb_commands) // 2 + 1, column=2, columnspan=2, pady=10)

# 使用当前的button_stack长度更新标签文本的函数
def update_label():
    # 使用当前的button_stack长度更新标签文本
    size_label.config(text="Size of Stack:" + str(len(button_stack)))

    # 根据button_stack的长度更新标签的位置
    size_label.grid(row=len(adb_commands) // 2 + 1, column=2, columnspan=2, pady=10)

root.mainloop()
