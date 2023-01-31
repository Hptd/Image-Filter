import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import tkinter.messagebox as msgbox


class ImageFilter(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('图片筛选器')
        self.root.iconbitmap('image filter.ico')
        self.root.resizable(True, True)  # 可自由缩放窗口尺寸
        self.root.geometry('1000x800+400+0')  # 确定窗口打开之后的位置
        self.image_num = 0  # 全局参数，用于图片上一张 下一张的操作

    def get_image_path(self):
        """
        打开一个电脑对话框选择一个文件夹。
        :return: 返回选中的文件夹路径。
        """
        rootpath = filedialog.askdirectory(title="请选择要筛选图片的文件夹...")
        return rootpath

    def get_path_namelist(self):
        """
        os模块配合已经获取的图片路径，获取文件夹内所有图片的列表，后续用于图片的展示。
        :return: path: 图片的原始路径；name_list：文件路径内所有图片的列表集合。
        """
        path = self.get_image_path()
        name_list = os.listdir(path)
        return path, name_list

    def rename_image(self, in_path, out_path, image_name, name_add=None):
        """
        图片的更名。
        :param in_path: 输入图片的路径。
        :param out_path: 输出图片的路径(此处选择两个是同一个路径)，输出同一路径的时候，需要注意刷新更名之后的文件名列表（name_list[]）。
        :param image_name: 输入图片的名称，对应列表内的元素。
        :param name_add: 需要加上的前缀（可以修改为后缀），str 类型。
        :return: os 模块更名之后的名称，同时弹出消息框告知操作完成。
        """
        src = os.path.join(os.path.abspath(in_path), image_name)
        dst = os.path.join(os.path.abspath(out_path), name_add + image_name)
        os.rename(src, dst)
        msgbox.showinfo("提示", "成功重命名")

    def resize_image(self, image_weight, image_height):
        """
        将输入的图片做适应显示变化，此处定长宽分别不能超过800、640，小尺寸图片会等比放大，大尺寸图片会等比缩小。
        :param image_weight: 需要处理的图片的长。
        :param image_height: 需要处理的图片的宽。
        :return: 输出两个整型过后的长宽值。
        """
        new_w = 800
        new_h = 640
        if image_weight > image_height:  # 如果图片是横向。
            k = image_weight/800
            new_h = image_height/k
        elif image_weight < image_height:  # 如果图片是纵向。
            k = image_height/640
            new_w = image_weight/k
        elif image_weight == image_height:  # 主要处理长宽相等的正方形图片，直接输出640x640。
            new_w = 640
            new_h = 640
        return int(new_w), int(new_h)

    def button_next_prev(self):
        """
        按钮控制函数，包括上下翻页的功能，根据 self.open_image() 的标签”next“/”prev“判断全局参数的加减，从而实现前后翻页看图。
        :return: None
        """
        image_path, name_list = self.get_path_namelist()  # 打开对话框获取路径和列表。

        button_next = tk.Button(self.root, text='下一张', width=7, height=30, fg='red', command=lambda: self.open_image(image_path, name_list, "next"))
        button_next.place(x=930, y=100)

        button_prev = tk.Button(self.root, text='上一张', width=7, height=30, fg='red', command=lambda: self.open_image(image_path, name_list, "prev"))
        button_prev.place(x=10, y=100)

        self.open_image(image_path, name_list, "")  # 主要是在按钮函数没有起作用之前，这个需要调用图片显示函数显示第一张图。

    def button_get_star(self, image_path, num):
        """
        图片打星的方法，会调用重命名的方法，根据不同按钮的需求去执行相关的操作。
        :param image_path: 输入图片的路径。
        :param num: 获取当前图片的索引值，配合之前的name_list[]，从而知道操作的是哪一张图（或者说操作的是当前图片）。
        :return: 在更名操作之后返回一个新的name_list[]，起到刷新列表的作用，确保图片的上下翻页是在更名之后的最新列表内进行。
        """
        name_list = os.listdir(image_path)

        star_5 = tk.Button(self.root, text='保留使用', width=20, height=3,
                           command=lambda: self.rename_image(image_path, image_path, name_list[num], name_add='保留_'))
        star_5.place(x=100, y=710)

        star_3 = tk.Button(self.root, text='待定商议', width=20, height=3,
                           command=lambda: self.rename_image(image_path, image_path, name_list[num], name_add='待定_'))
        star_3.place(x=450, y=710)

        star_1 = tk.Button(self.root, text='直接淘汰', width=20, height=3,
                           command=lambda: self.rename_image(image_path, image_path, name_list[num], name_add='淘汰_'))
        star_1.place(x=750, y=710)

        # return 的作用是重新刷新图片名称列表
        return name_list

    def open_image(self, image_path, name_list, button_type):
        """
        tkinter + pillow 完成图片的显示加载：
        tkinter 本身只能显示 .gif 图，需要pillow库中转才能正常的显示 .jpg 和 .png。
        :param image_path: 图片的路径。
        :param name_list: 已经根据路径获取的文件夹内全部的图片名称列表。
        :param button_type: 配合上下张翻页图片的按钮使用，确定是点击的 上一张 还是 下一张 按钮。
        :return: None
        """
        if button_type == "next":
            self.image_num += 1
            if self.image_num == len(name_list):
                self.image_num = len(name_list) - 1
                msgbox.showerror('报错', '已经是最后一个了')
        elif button_type == "prev":
            self.image_num -= 1
            if self.image_num < 0:
                self.image_num = 0
                msgbox.showerror('报错', '已经是第一个了')
        else:
            pass

        # 重命名操作
        name_list = self.button_get_star(image_path, self.image_num)

        # 显示图片，需要做一次中转变化，单tkinter不能完成需求，pillow配合可显示其余格式；
        img_open = Image.open(image_path + '/' + name_list[self.image_num])
        new_width, new_height = self.resize_image(img_open.width, img_open.height)
        img_open = img_open.resize((new_width, new_height))
        img_all = ImageTk.PhotoImage(img_open)
        label_img_show = tk.Label(self.root, image=img_all, width=800, height=640)
        label_img_show.place(x=100, y=20)

        # 显示图片名称
        label_img_name = tk.Label(self.root, text=name_list[self.image_num], width=30, height=2)
        label_img_name.place(x=420, y=670)

        self.root.mainloop()


if __name__ == '__main__':
    ImageFilter().button_next_prev()
