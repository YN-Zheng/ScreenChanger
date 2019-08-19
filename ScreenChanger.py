# coding=utf-8
# coding=utf-8

import os
from random import randint
import win32api
import win32con
import win32gui
import tkinter


class Screenchanger(object):
    def __init__(self):
        # 初始化壁纸设置
        self.mode_temp='10'
        self.screen_initialize()
        # 默认路径设置
        self.pictures = []
        self.path = 'D:/Biking/'
        get_path(self.path, self.pictures)
        self.length = len(self.pictures)

        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        self.fm1 = tkinter.Frame(self.root)
        self.fm2 = tkinter.Frame(self.root)

        #单选框
        self.mode = tkinter.IntVar()
        tkinter.Label(self.fm1, text='最后一行：照片文件夹路径').pack(side='top', anchor='w', fill='x', expand='yes')

        selection1 = tkinter.Radiobutton(self.fm1, text="填充", variable=self.mode, value='10', command=self.sel)
        selection1.pack(side='left')
        selection1.select()
        selection2 = tkinter.Radiobutton(self.fm1, text="适应", variable=self.mode, value='6', command=self.sel)
        selection2.pack(side='right')


        #self.fm1.pack()
        # 给主窗口设置标题内容
        self.root.title("Handsome Zheng 帮你换壁纸")
        # 创建一个输入框,并设置尺寸
        self.ip_input = tkinter.Entry(self.fm2, width=50)
        # 目录框
        var = tkinter.StringVar()
        var.set(self.path)
        self.path_input = tkinter.Entry(self.fm2, width=50, textvariable=var)
        # 创建一个回显列表
        self.display_info = tkinter.Listbox(self.fm2, width=50, height=2)
        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.fm2, command=self.find_position, text="点我")

    # 完成布局
    def gui_arrang(self):
        self.ip_input.pack()
        self.display_info.pack()
        self.result_button.pack(fill='x')
        self.path_input.pack()
        self.fm1.pack(fill ='both',expand = 1)
        self.fm2.pack(side='left',padx=10)

    def sel(self):
        selection = "You selected the option " + str(self.mode.get())
        if self.mode_temp != str(self.mode.get()):
            self.mode_temp = str(self.mode.get())
            self.screen_initialize()
            try:
                set_wallpaper(self.path2)
            except:
                pass
        print(selection)



    # 根据文件夹路径，改变桌面壁纸
    def find_position(self):
        # 若路径变化，根据输入，更新路径及图片列表
        if self.path != self.path_input.get():
            self.pictures.clear()
            self.path = self.path_input.get()
            get_path(self.path, self.pictures)
            self.length = len(self.pictures)
        # 若不存在目录/其中没有jpg图片，不做响应，return
        if self.length == 0:
            the_ip_info = ['请在下方正确输入目录']
            self.display_info.insert(1, the_ip_info)
            return
        # 从图片列表中选一张图片作为壁纸。若不输入编号，或者编号大于当前范围，随机选一张。
        try:
            ip_num = self.ip_input.get()
            index = int(ip_num)
            self.path2 = self.pictures[index]
            the_ip_info = ["第" + str(ip_num)+'号照片']
        except:
            index = randint(0, self.length)
            self.path2 = self.pictures[index]
            the_ip_info = ['该文件夹共有'+str(self.length)+'张图片',"第" + str(index)+"号照片（随机）"]
        # 设定壁纸
        set_wallpaper(self.path2)

        # 清空回显列表可见部分,类似clear命令
        for item in range(2):
            self.display_info.insert(0, "")
        # 为回显列表赋值
        for item in the_ip_info:
            self.display_info.insert(0, item)


    def screen_initialize(self):
        # 打开指定注册表路径
        reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
        win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, self.mode_temp)
        # 最后的参数:1表示平铺,拉伸居中等都是0
        win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")



def set_wallpaper(img_path):
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path, win32con.SPIF_SENDWININICHANGE)


def get_path(path, list_name):
    # 获取该文件夹下所有的.JPG图片地址
    print('af')
    try:
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.splitext(file_path)[1] in ['.JPG', '.jpg']:
                list_name.append(file_path)
    except:
        list_name.clear()


if __name__ == '__main__':
    SG = Screenchanger()
    SG.gui_arrang()
    tkinter.mainloop()
    pass

    # index = random.randint(0, length)
    # set_wallpaper(pictures[index])
