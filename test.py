import tkinter as tk
from functions import *
from datetime import datetime, timedelta


def run_shutdown_based_on_input():
    stop_shutdown()
    input_hour, input_minute = process_string(entry.get())
    if input_minute is None:
        estimate_time.config(text="請輸入數字", fg="#ff0000")
        return None
    shutdown_time = datetime.now() + timedelta(hours=input_hour, minutes=input_minute)
    estimate_time.config(text=f'預計關機時間：{shutdown_time.strftime("%H:%M:%S")}', fg="#000000")
    run_shutdown(input_hour * 60 * 60 + input_minute * 60)


def shutdown_and_show_text(time: int):
    stop_shutdown()
    run_shutdown(time * 60 * 60)
    shutdown_time = datetime.now() + timedelta(hours=time)
    estimate_time.config(text=f'預計關機時間：{shutdown_time.strftime("%H:%M:%S")}')


def cancel_shutdown():
    stop_shutdown()
    estimate_time.config(text="取消關機")


window = tk.Tk()
window.title('定時關機程式')
window.geometry('300x300')
window.iconbitmap("C:\Program Files\Gamania\MapleStory\MapleStory.ico")
window.resizable(False, False)

# buttons and layout

# first frame for time
frame = tk.Frame(window)
frame.pack()
# estimate shutdown time
estimate_time = tk.Label(frame, text="預計關機時間：", font=('Arial', 20, 'bold'))
estimate_time.grid(column=0, row=0)

# second frame
second_frame = tk.Frame(window)
second_frame.pack()

# entry area
entry = tk.Entry(second_frame, width=8)
entry.grid(column=0, row=1)

# "hr" label
hr = tk.Label(second_frame, text="小時")
hr.grid(column=1, row=1)
# create task area
create_task_button = tk.Button(second_frame, text="建立定時關機", command=run_shutdown_based_on_input)
create_task_button.grid(column=2, row=1)

# third frame
third_frame = tk.Frame(window, pady=20)
third_frame.pack()
# quick setting label
qs = tk.Label(third_frame, text="快速設定")
qs.grid(column=1, row=0, columnspan=2)
# 2 hour button
eight_hour_button = tk.Button(third_frame, text="2小時", command=lambda: shutdown_and_show_text(2))
eight_hour_button.grid(column=0, row=1)
# 4 hour button
eight_hour_button = tk.Button(third_frame, text="4小時", command=lambda: shutdown_and_show_text(4))
eight_hour_button.grid(column=1, row=1)
# 6 hour button
eight_hour_button = tk.Button(third_frame, text="6小時", command=lambda: shutdown_and_show_text(6))
eight_hour_button.grid(column=2, row=1)
# 8 hour button
eight_hour_button = tk.Button(third_frame, text="8小時", command=lambda: shutdown_and_show_text(8))
eight_hour_button.grid(column=3, row=1)

# Cancel schedule shutdown
cancel_button = tk.Button(third_frame, text="取消關機", command=cancel_shutdown)
cancel_button.grid(column=1, row=2, columnspan=2)
window.mainloop()
