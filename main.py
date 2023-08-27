from pynput import mouse
from tkinter import *
from time import sleep
import time
import _thread

root=Tk()
root.title("模仿器")
root.geometry("300x180")

f_top=Frame(root)
f_top.pack(side=TOP)
setting_bottom=Button(f_top,text="高级",command=lambda:sheting_btncomm())
setting_bottom.pack(side=LEFT,ipady=5,ipadx=10,padx=10,pady=5)
lable1=Label(f_top,text="录制时间(秒)",pady=20)
lable1.pack(side=LEFT)
in_put_Entry=StringVar(value='2')
entry0=Entry(f_top,textvariable=in_put_Entry,width=8)
entry0.pack(side=RIGHT)


#高级菜单
f_cent=Frame(root)
f_cent.pack(side=TOP)
f_cent.pack_forget()

setting_f2=Frame(f_cent)
setting_f2.pack(side=TOP)
lable3=Label(setting_f2,text="重复次数(无限次填-1)",pady=20)
lable3.pack(side=LEFT)
in_put_re_number=StringVar(value='0')
entry2=Entry(setting_f2,textvariable=in_put_re_number,width=8)
entry2.pack(side=RIGHT)

setting_f1=Frame(f_cent)
setting_f1.pack(side=TOP)
lable2=Label(setting_f1,text="重复执行延迟时间(秒)",pady=20)
lable2.pack(side=LEFT)
in_put_re_second=StringVar(value='0')
entry1=Entry(setting_f1,textvariable=in_put_re_second,width=8)
entry1.pack(side=RIGHT)



f_bottom=Frame(root)
f_bottom.pack(side=BOTTOM)

get_motion_bt=Button(f_bottom,text="录制动作",command=lambda:get_motion_btncomm())
get_motion_bt.pack(side=LEFT,ipady=20,ipadx=20,padx=10,pady=10)

execute_motion_bt=Button(f_bottom,text="执行动作",command=lambda:execute_motion_btncomm())
execute_motion_bt.pack(side=LEFT,ipady=20,ipadx=20,padx=10,pady=10)

data=[]    #TYPE:{'mouse_data':{'x':0,'y':0,'bt_left':0,'bt_right':0,'scroll':(0,1)},'keyboard_data':{}}
mymouse = mouse.Controller()
bt_left=False
bt_right=False
scroll=(0,1)
EXIT=0#是否让listener线程退出

#显示和隐藏高级菜单
def sheting_btncomm():
    if f_cent.winfo_viewable():
        _thread.start_new_thread(update_windows_not_setting, ())

    else:
        _thread.start_new_thread(update_windows_setting, ())

def update_windows_setting():
    i = 180
    while i < 280:
        sleep(0.001)
        i += 1
        root.geometry("300x{0}".format(i))
    f_cent.pack()
def update_windows_not_setting():
    i = 280
    while i > 180:
        sleep(0.001)
        i -= 1
        root.geometry("300x{0}".format(i))
    f_cent.pack_forget()


#录制
def on_click(x, y, button, pressed):
    global EXIT
    global bt_left
    global bt_right
    if button==mouse.Button.left:
        bt_left=pressed
    if button==mouse.Button.right:
        bt_right=pressed

    if EXIT:
        return False
    # print('{0} at {1} btn is {2}'.format(
    #     'Pressed' if pressed else 'Released',
    #     (x, y),button))
def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))
def get_motion_btncomm():
    _thread.start_new_thread(get_motion_btncomm_run, ())
    get_motion_lable()
def get_motion_btncomm_run():
    global EXIT
    global mymouse
    global bt_left
    global bt_right
    bt_left,bt_right=False,False
    bt_left_last,bt_right_last=False,False#保存上一次的按键情况


    EXIT = 0
    sleep(0.1)
    listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    listener.start()
    second=int(entry0.get())
    data.clear()

    one_time = int(time.time())
    while (int(time.time())<one_time+second):
        sleep(0.01)
        x,y=mymouse.position
        if(bt_left_last != bt_left):
            bt_left_last=bt_left
            bt_left_buf=int(bt_left)
        else:
            bt_left_buf=-1

        if (bt_right_last != bt_right):
            bt_right_last = bt_right
            bt_right_buf = int(bt_right)
        else:
            bt_right_buf = -1
        buf={'mouse_data':{'x':x,'y':y,'bt_left':bt_left_buf,'bt_right':bt_right_buf,'scroll':(0,1)},'keyboard_data':{}}
        data.append(buf)
        #print('The current pointer position is {0}'.format(mouse.position))
    EXIT=1
    get_motion_bt.config(text="录制动作")
def get_motion_lable():
    get_motion_bt.config(text="  录制中  ")

#执行
def execute_motion_btncomm():
    _thread.start_new_thread(execute_motion_run,())
    execute_motion_lable()
def execute_motion_run():
    global mymouse
    x=-1
    y=-1
    n=0
    while n-1<int(entry2.get()) or int(entry2.get())==-1:
        if n!=0:
            sleep(int(entry1.get()))
        n+=1
        for i in range(len(data)):
            sleep(0.01)
            # _thread.start_new_thread(, (int(x_buf[i]), int(y_buf[i],)))
            x_tmp=data[i]['mouse_data']['x']
            y_tmp=data[i]['mouse_data']['y']
            if x_tmp!=x or y_tmp!=y:
                mymouse.position = (x_tmp, y_tmp)
                x,y=x_tmp,y_tmp
            #鼠标左右按键
            if data[i]['mouse_data']['bt_left'] ==1:
                print("鼠标左按")
                mymouse.press(mouse.Button.left)


            elif data[i]['mouse_data']['bt_left']==0:
                mymouse.release(mouse.Button.left)
                print("鼠标左放")


            if data[i]['mouse_data']['bt_right'] ==1:
                mymouse.press(mouse.Button.right)
                print("鼠标右按")

            elif data[i]['mouse_data']['bt_right']==0:
                mymouse.release(mouse.Button.right)
                print("鼠标右放")


        # mymouse.click(mouse.Button.left, 1)
        sleep(0.1)
        mymouse.release(mouse.Button.left)
        sleep(0.1)
        mymouse.release(mouse.Button.right)
    execute_motion_bt.config(text="执行动作")

    # macOS
    # mouse.click(Button.left, 2)

    # other
    # mouse.press(Button.left)
    # mouse.release(Button.left)
def execute_motion_lable():
    execute_motion_bt.config(text="  执行中  ")

root.mainloop()