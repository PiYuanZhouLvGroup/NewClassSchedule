import datetime
import sys
import tkinter
import time
import tkinter.ttk
import json
import io
from tkinter import messagebox
from pygame import mixer

mixer.init()

root = tkinter.Tk()
root.title('课程表')
root.attributes('-topmost', True)
root.attributes('-toolwindow', True)
root.resizable(False, False)
# root.attributes('-transparent', 'white')
root.overrideredirect(True)
closed = False
rop = None
root.update()
root.geometry((geo_info := '+%s+%s' % (root.winfo_screenwidth() - root.winfo_width() - 60, 15)))

close_time = -1
last_close_after = None
on_close_event = False


def on_close(*args):
    global close_time, on_close_event, last_close_after
    if UI_type == 'simple':
        swap_UI()
        return
    on_close_event = True
    close_time += 1
    for b, actions in map(lambda x: (eval(x, globals(), {"n": close_time + 1}), click_events[x]), click_events):
        if b:
            for action in actions:
                root.after(10, action)
    # close_time %= len(close_events)
    if last_close_after:
        root.after_cancel(last_close_after)
    now_time.set(close_events[close_time % len(close_events)][0])
    last_close_after = root.after(2000, close_event)


def on_see_through(*args):
    if not closed:
        close()
    else:
        reopen()


def close_event():
    global close_time, on_close_event
    close_events[close_time % len(close_events)][1]()
    close_time = -1
    on_close_event = False


unlocked = False
e_count = 0


def change_weekday(*args):
    global weekday

    def _f(*args):
        global weekday
        global unlocked, e_count
        try:
            egg = json.loads((file_tmp := open('egg.json', encoding='utf-8')).read())
            file_tmp.close()
        except BaseException as err:
            from tkinter import messagebox
            import traceback
            messagebox.showerror(str(err), traceback.format_exc())
        if (wd := wdv.get()) in class_list:
            weekday = wd
            window.destroy()
        elif wdv.get() == '/kill' and sys.argv[0].endswith('.pyw'):
            unlocked = True
            root.destroy()
        elif wdv.get() == '':
            weekday = datetime.datetime.today().weekday() if "-w" not in sys.argv else int(
                sys.argv[sys.argv.index("-w") + 1])
        elif wdv.get() == '肌鲵肽酶':
            from tkinter import messagebox
            messagebox.showinfo('提示', '已解锁')
            unlocked = True
        elif wdv.get() == '/lock':
            messagebox.showinfo('提示', '儿童锁已上锁')
            unlocked = False
        elif wdv.get() == '我会记得关电脑':
            from tkinter import messagebox
            e_count -= 1
            messagebox.showinfo('提示', '使用次数+1')
            wdv.set('')
            if sum(map(lambda x: x[0].count(x[1]),
                       zip([window.clipboard_get()] * len('我会记得关电脑'), '我会记得关电脑'))) > 0:
                window.clipboard_clear()
                window.clipboard_append('不要耍小聪明')
        elif wdv.get() == 'ngm':
            root.after(10, play_ngm)
        elif wdv.get().startswith('/exec'):
            exec(wdv.get()[6:])
        elif (wd := wdv.get()) in egg:
            import webbrowser
            import random
            if e_count < 5:
                webbrowser.open(random.choice(egg[wd]))
                e_count += 1
            else:
                from tkinter import messagebox
                messagebox.showerror('已达上限', '彩蛋使用次数已达上限，输入 我会记得关电脑 获得更多次数')

        else:
            from tkinter import messagebox
            messagebox.showwarning("错误", "输入的编号不存在")

    window = tkinter.Toplevel(root)
    window.title("选择星期")
    wdv = tkinter.StringVar(window, value='')
    tkinter.Label(window, text='请输入星期编号(默认0为星期一，空为默认):').pack()
    tkinter.Entry(window, textvariable=wdv).pack()
    tkinter.Button(window, text='确认', command=_f).pack()


def on_really_close():
    from tkinter import messagebox
    if messagebox.askokcancel("关闭确认", "确定要关闭吗?", default="cancel"):
        if not unlocked:
            messagebox.showinfo("开玩笑", "该功能已被禁用")
            return
        root.destroy()


def play_ngm():
    if not mixer.music.get_busy():
        mixer.music.load("hkd/ngm-15-19.mp3")
        mixer.music.play()
    else:
        mixer.music.queue("hkd/ngm-15-19.mp3")


close_events = [
    ("隐藏/显示", on_see_through),
    ("更改星期", change_weekday),
    ("刷新时间", lambda: (root.after(0, update_now_time), root.after(0, update_info))),
    ("再按3次关闭", lambda: None),
    ("再按2次关闭", lambda: None),
    ("再按1次关闭", lambda: None),
    ("关闭", on_really_close),
    ("取消", lambda: None)
]
click_events = {
    "n == 10": [lambda: now_time.set("别点了!!!")],
    "n == 15": [lambda: now_time.set('我要叫了!')],
    "n % 10 == 0 and n >= 20": [play_ngm]
}


def close(*args):
    global closed, rop
    root.attributes('-alpha', 0.4)
    closed = True
    root.attributes('-transparentcolor', '#F0F0F0')
    rop = root.after(10 * 60 * 1000, reopen)


def reopen(*args):
    global closed
    root.after_cancel(rop)
    root.attributes('-alpha', 1)
    closed = False
    root.attributes('-transparentcolor', '')


# geo_last = root.geometry()
# moving = False
# def move_back():
#     global geo_last, moving
#     geo_now = root.geometry()
#     if geo_now != geo_info:
#         if not moving:
#             if geo_now != geo_last:
#                 ...
#             else:
#                 moving = True
#         else:
#             x, y = filter(int, geo_now.split('+')[-2:])
#             dx, dy = (root.winfo_screenwidth() - root.winfo_width() - 10, 1)
#             if x > dx:
#                 x -= 1
#             elif x < dx:
#                 x += 1
#             if y > dy:
#                 y -= 1
#             elif y < dy:
#                 y += 1
#             root.geometry('250x130+%s+%s' % (x, y))
#     geo_last = geo_info
#     root.after(10, move_back)
# root.after(10, move_back)

UI_parts = []
now_time_label = ...


def UI_normal():
    global now_time_label
    UI_destroy()
    (
        tmp := tkinter.Label(root, text=f'{datetime.date.today().month}月{datetime.date.today().day}日  '
                                        f'星期{ {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}[datetime.date.today().weekday()]}'
                             )
    ).pack()
    tmp.bind('<Button-3>', change_weekday)
    UI_parts.append(tmp)
    (
        tmp := tkinter.Label(root, textvariable=now_time,
                             anchor='center', font=('default', 25, 'bold'), cursor='fleur'
                             )
    ).pack()
    now_time_label = tmp
    UI_parts.append(tmp)
    (
        tmp := tkinter.Label(root, textvariable=now_class,
                             anchor='w')
    ).pack()
    UI_parts.append(tmp)
    (
        tmp := tkinter.ttk.Progressbar(root, length=250, maximum=1, variable=remain_time)
    ).pack()
    tmp.bind('<Double-1>', swap_UI)
    UI_parts.append(tmp)
    (
        tmp := tkinter.Label(root, textvariable=next_class,
                             anchor='w')
    ).pack()
    UI_parts.append(tmp)


def UI_simple():
    global now_time_label
    UI_destroy()
    (
        tmp := tkinter.Label(root, textvariable=now_time, font=('default', 20, 'bold'), anchor='center', cursor='fleur')
    ).pack(side=('top' if sim_type == 'v' else 'left'))
    now_time_label = tmp
    UI_parts.append(tmp)
    (
        tmp := tkinter.ttk.Progressbar(root, orient=("vertical" if sim_type == 'v' else 'horizontal'), maximum=1,
                                       length=250, variable=remain_time)
    ).pack(side=('top' if sim_type == 'v' else 'left'))
    tmp.bind('<Double-1>', swap_UI)
    tmp.bind('<Button-2>', swap_sim)
    UI_parts.append(tmp)
    (
        tmp := tkinter.Label(root, textvariable=now_class)
    ).pack(side=('top' if sim_type == 'v' else 'left'))
    UI_parts.append(tmp)
    (
        tmp := tkinter.Label(root, textvariable=next_class)
    ).pack(side=('top' if sim_type == 'v' else 'left'))
    UI_parts.append(tmp)


def UI_destroy():
    for part in UI_parts:
        part.destroy()


UI_type = 'normal'
sim_type = 'v'


def swap_UI(*args):
    global UI_type
    if UI_type == "normal":
        UI_simple()
        UI_type = "simple"
    else:
        UI_normal()
        UI_type = "normal"
    now_time_label.bind('<B1-Motion>', dragging)
    now_time_label.bind('<ButtonRelease-1>', end_drag)
    now_time_label.bind('<Button-3>', on_close)


def swap_sim(*args):
    global sim_type
    if sim_type == 'v':
        sim_type = 'h'
    else:
        sim_type = 'v'
    UI_simple()
    now_time_label.bind('<B1-Motion>', dragging)
    now_time_label.bind('<ButtonRelease-1>', end_drag)
    now_time_label.bind('<Button-3>', on_close)


class_list = json.loads(open(sys.argv[0].rsplit('.')[0] + '.json', encoding='utf-8').read())
now_time = tkinter.StringVar(root, datetime.datetime.now().strftime('%H:%M:%S'))


def update_now_time(*args):
    global now_time
    try:
        if not (on_close_event or on_key_event):
            if UI_type == 'normal' or in_disappear:
                now_time.set(datetime.datetime.now().strftime('%H:%M:%S'))
            else:
                now_time.set(datetime.datetime.now().strftime(
                    f'%H\n{":" if datetime.datetime.now().microsecond <= 500000 else " "}\n%M'.replace('\n', (
                        '\n' if sim_type == 'v' else ''))))
    except:
        now_time.set('出现问题了')
    finally:
        root.after(100, update_now_time)


root.after(100, update_now_time)


def show_time(d=..., nx=..., titv=..., subv=..., tp=..., clsn=..., tm=..., start=True):
    global st_window
    if start:
        st_window = tkinter.Toplevel(root)
        st_window.attributes('-topmost', True)
        st_window.protocol("WM_DELETE_WINDOW", lambda: ...)
        st_window.overrideredirect(True)
        titv = tkinter.StringVar()
        tkinter.Label(st_window, textvariable=titv,
                      anchor='center', font=('default', 30, 'bold')).pack()
        subv = tkinter.StringVar()
        tkinter.Label(st_window, textvariable=subv,
                      anchor='w', font=('default', 10)).pack()
        d = root.winfo_screenwidth() / 1000
        nx = root.winfo_screenwidth()
        st_window.geometry('+%s+%s' % (int(nx), 15))
        root.after(10, lambda *_: show_time(d, nx, titv, subv, tp, clsn, tm, False))
    else:
        titv.set(datetime.datetime.now().strftime('%H:%M:%S'))
        subv.set((
                     f'现在是：{clsn}' if datetime.datetime.now() > tm else f'接下来：{clsn}') if tp == 'clscg' else f'{(rt := tm - datetime.datetime.now()).seconds // 60}:{rt.seconds % 60:0>2}后: {clsn}')
        nx -= d
        st_window.geometry('+%s+%s' % (int(nx), 15))
        if nx < min(0, -st_window.winfo_width()):
            st_window.destroy()
        else:
            root.after(10, lambda *_: show_time(d, nx, titv, subv, tp, clsn, tm, False))


now_class = tkinter.StringVar(root, '')
remain_time = tkinter.DoubleVar(root, 0.0)
next_class = tkinter.StringVar(root, '')
weekday = datetime.datetime.today().weekday() if "-w" not in sys.argv else int(sys.argv[sys.argv.index("-w") + 1])
UI_normal()
had_shown = False


def update_info(*args):
    global had_shown
    try:
        now = datetime.datetime.today()
        now_t = datetime.time(now.hour, now.minute, now.second, now.microsecond)
        classes = class_list[str(weekday)]
        # classes = class_list[0] # Test
        if classes[0][1:] not in ((0, 0), [0, 0]):
            classes.insert(0, ('新的一天', 0, 0))
        if classes[-1][1:] not in ((23, 59), [23, 59]):
            classes.append(('迎接新的一天', 23, 59))
        classes = classes.copy()
        classes.reverse()
        for i, c in enumerate(classes):
            t = datetime.time(c[1], c[2], 0)
            if now_t > t:
                index = i
                break
        c = classes[index]
        ct = datetime.datetime(now.year, now.month, now.day, c[1], c[2], 0)
        nc = classes[index - 1]
        nct = datetime.datetime(now.year, now.month, now.day, nc[1], nc[2], 0)
        at = nct - ct
        rt = nct - now
        remain_time.set(1 - rt / at)
        if UI_type == 'normal' and not in_disappear:
            now_class.set(f'{1 - rt / at:.2%} ' + classes[index][0])
            next_class.set(f'{rt.seconds // 60}:{rt.seconds % 60:0>2}后: {nc[0]}')
        else:
            now_class.set(f'{1 - rt / at:.2%}')
            next_class.set(f'{rt.seconds // 60}:{rt.seconds % 60:0>2}')
        if rt.seconds <= 5 and not had_shown:
            show_time(tp='clscg', clsn=nc[0], tm=nct)
            had_shown = True
        elif now.minute % 20 == 19 and now.second >= 55 and not had_shown:
            show_time(tp='20min', clsn=nc[0], tm=nct)
            had_shown = True
        elif had_shown and rt.seconds > 5 and not (now.minute % 20 == 19 and now.second >= 55):
            had_shown = False
    except:
        now_class.set('出现问题了')
        next_class.set('出现问题了')
    finally:
        root.after(10, update_info)


root.after(0, update_info)


def check_iconic():
    if root.state() == "iconic":
        root.deiconify()
        global UI_type
        UI_type = "simple"
        UI_simple()
    if UI_type == 'simple' and int((geo := root.geometry()).split('+')[-2]) < 0:
        root.geometry('+0+' + geo.split('+')[-1])
    root.geometry(f'+{max(0, min(root.winfo_screenwidth() - root.winfo_width(), int(root.geometry().split("+")[-2])))}'
                  f'+{max(0, min(root.winfo_screenheight() - root.winfo_height() - 30, int(root.geometry().split("+")[-1])))}')
    root.after(10, check_iconic)


root.after(0, check_iconic)
in_disappear = False


def disappear():
    global in_disappear

    def on_appear(*args):
        global in_disappear
        dw.destroy()
        root.deiconify()
        in_disappear = False

    def upp(count=0):
        # print(int((root.winfo_screenwidth() - dw.winfo_width()) * (float(now_class.get()[:-1]) / 100)))
        dw.geometry(f'+{int((root.winfo_screenwidth() - dw.winfo_width()) * float(now_class.get()[:-1]) / 100)}+{0}')
        btnv.set(f'now {now_time.get()}' if (count // 1000) % 3 == 0
                 else (f'{now_class.get()}' if (count // 1000) % 3 == 1
                       else f'left {next_class.get()}'))
        btn['fg'] = ('blue' if (count // 1000) % 3 == 0
                     else ('green' if (count // 1000) % 3 == 1
                           else 'red'))
        count += 1
        count %= 1000 * 3
        dw.after(10, lambda: upp(count))

    dw = tkinter.Toplevel(root)
    btnv = tkinter.StringVar()
    (btn := tkinter.Button(dw, bg='white', textvariable=btnv, command=on_appear)).pack()
    dw.attributes('-topmost', True)
    dw.overrideredirect(True)
    dw.update()
    dw.after(10, upp)
    dw.after(40 * 60 * 1000, on_appear)
    root.withdraw()
    in_disappear = True


def lock():
    global unlocked
    unlocked = False
    messagebox.showinfo('提示', '儿童锁已上锁')


import webbrowser

c_list = []
c_after = None
on_key_event = False
commands = {
    '/xsbj': ['<消失不见>', disappear],  #
    '/ngm': ['<你干嘛~>', play_ngm],
    '/cgwd': ['<更改星期>', change_weekday],
    '/lock': ['<上锁>', lock],
    '/close': ['<关闭>', on_really_close],
    '/114514': ['<好臭啊>', lambda: webbrowser.open("https://www.bilibili.com/video/BV123411c787/?spm_id_from=333.337.search-card.all.click")],
    '/b': ['<打开 B站>', lambda: webbrowser.open("https://www.bilibili.com")],
    '/xwzk': ["<打开 新闻周刊>", lambda: webbrowser.open("https://tv.cctv.com/lm/xwzk/index.shtml")]
}


def on_key(event):
    global c_after, on_key_event
    # messagebox.showinfo('按键', event.keycode)
    if event.keycode != 191 and not on_key_event:
        return
    on_key_event = True
    if c_after:
        root.after_cancel(c_after)
    c_list.append(event.char if event.keycode != 191 else '/')
    c_after = root.after(10000, command_cancel)
    if ''.join(c_list) in commands:
        now_time.set(commands[''.join(c_list)][0])
    else:
        now_time.set(''.join(c_list))


def on_command(*args):
    global on_key_event, c_list
    if not on_key_event:
        return
    on_key_event = False
    if ''.join(c_list) not in commands:
        messagebox.showerror('未知命令', f'未知的命令"{"".join(c_list)}"')
    else:
        root.after(0, commands[''.join(c_list)][1])
    c_list = []


def command_cancel(*args):
    global on_key_event, c_list
    on_key_event = False
    c_list = []


on_drag = False
start_x = ...
start_y = ...
rsx = ...
rsy = ...


def dragging(event):
    global on_drag, start_x, start_y, rsx, rsy
    if not on_drag:
        on_drag = True
        start_x, start_y = root.winfo_pointerxy()
        rsx = root.winfo_x()
        rsy = root.winfo_y()
    else:
        root.geometry(f"+{rsx - start_x + root.winfo_pointerx()}+{rsy - start_y + root.winfo_pointery()}")


def end_drag(*args):
    global on_drag
    on_drag = False


root.bind('<Key>', on_key)
root.bind('<Return>', on_command)
root.bind('<Escape>', command_cancel)
root.bind('<Enter>', lambda *args: root.attributes('-alpha', 0.4 if not closed else 0.4))
root.bind('<Leave>', lambda *args: root.attributes('-alpha', 1.0 if not closed else 0.4))
root.protocol("WM_DELETE_WINDOW", on_close)
now_time_label.bind('<B1-Motion>', dragging)
now_time_label.bind('<ButtonRelease-1>', end_drag)
now_time_label.bind('<Button-3>', on_close)
root.mainloop()
