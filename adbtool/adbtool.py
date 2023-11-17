import os
import re
import time
import tkinter as tk
import subprocess

def run_adb_command(command, success_message):
    subprocess.run(["python", os.path.join("function", command)])
    text_box.insert(tk.END, success_message + "\n")

def create_button(root, text, adb_command):
    btn = tk.Button(root, text=text, command=lambda: run_adb_command(adb_command, f"{text} success!"), **button_style)
    return btn

def get_button_style():
    return {"width": 15, "height": 2, "padx": 50, "pady": 10, "bd": 4, "relief": "raised", "bg": "lightblue", "fg": "black", "font": ('Helvetica', 12, 'bold')}

root = tk.Tk()
root.title("adb工具")

text_label = tk.Label(root, text="记录栏", font=('Helvetica', 12, 'bold'))
text_label.grid(row=0, column=2,columnspan=2, pady=10)



text_box = tk.Text(root, height=15, width=50)
text_box.grid(row=1, column=2, rowspan=3, columnspan=2,padx=10, pady=10)

def clear_text_box():
    text_box.delete("1.0", tk.END)

adb_commands = {
    "Log": "adb_log.py",
    "Back": "adb_back.py",
    "Reverse": "adb_reverse.py",
    "Monitor": "adb_activity.py",
    "Burp Open": "adb_burpopen.py",
    "Burp Close": "adb_burpclose.py",
    "Unlock": "adb_unlock.py",
}
button_style = get_button_style()



# 使用栈来记录用户点击的按钮
button_stack = []
run_stack=[]

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
            run_text=run_stack.pop()
            button_stack.append(run_text)
            last_command = adb_commands.get(run_text)
            if last_command:
                run_adb_command(last_command, f"Repeated {run_text} success!")

def show_previous_commands():
    text_box.insert(tk.END, "Previous Commands: " + " -> ".join(button_stack) + "\n")

def delete_stack_commands(delete_count_entry):
    try:
        delete_count = int(delete_count_entry.get())
        delete_count = max(1, delete_count)
    except ValueError:
        delete_count = 1

    for _ in range(delete_count):
        text_box.insert(tk.END, "Success delete "+button_stack.pop()+" !\n")

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

def retap(retap_count_entry):
    try:
        retap_count = int(retap_count_entry.get())
        retap_count = max(1, retap_count)
    except ValueError:
        retap_count = 10

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

    record_touch_events(retap_count, tap35_list=tap35_list, tap36_list=tap36_list)

    print("record over, soon to replay")
    # 在手机上进行你希望捕捉的点击操作
    time.sleep(1)

    # 第二步：停止getevent并模拟触摸事件
    replay_touch_events()

    text_box.insert(tk.END, "Success retap "+retap_count+" seconds!\n")

delete_count_entry = tk.Entry(root)
delete_count_entry.grid(row=len(adb_commands) // 2 + 5, column=2, pady=10)
delete_btn=tk.Button(root, text="Delete Stack", command=lambda: delete_stack_commands(delete_count_entry), **button_style)
delete_btn.grid(row=len(adb_commands) // 2 + 5, column=3, pady=10)

retap_count_entry = tk.Entry(root)
retap_count_entry.grid(row=len(adb_commands) // 2 + 6, column=2, padx=10, pady=10)

retap_btn = tk.Button(root, text="Retap", command=lambda:retap(retap_count_entry),**button_style)
retap_btn.grid(row=len(adb_commands) // 2 + 6, column=3, padx=10, pady=10)

def set_last_buttons_clicked(button_text):
    # 将点击的按钮入栈
    button_stack.append(button_text)
    update_label()

size_label = tk.Label(root, text="Size of Stack:"+str(len(button_stack)), font=('Helvetica', 12, 'bold'))
size_label.grid(row=len(adb_commands) // 2 + 1, column=2,columnspan=2, pady=10)

def update_label():
    # 使用当前的button_stack长度更新标签文本
    size_label.config(text="Size of Stack:" + str(len(button_stack)))
    
    # 根据button_stack的长度更新标签的位置
    size_label.grid(row=len(adb_commands) // 2 + 1, column=2, columnspan=2, pady=10)

root.mainloop()
