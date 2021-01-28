#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import sys

import device_manager_setup
from app.http.http_utils import update_ip, update_device_time, get_default_gateway_ip
import ipaddress

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    import tkinter.messagebox

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    device_manager_setup.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    device_manager_setup.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("600x450+650+150")
        top.minsize(148, 1)
        top.maxsize(3204, 2405)
        top.resizable(1, 1)
        top.title("Onvif Device Manager")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.05, rely=0.044, relheight=0.278, relwidth=0.9)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.259, rely=0.064, height=27, width=260)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Thanks for choosing Device Manager''')

        self.Labelframe1 = tk.LabelFrame(self.Frame1)
        self.Labelframe1.place(relx=0.056, rely=0.24, relheight=0.648
                               , relwidth=0.889)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Functions''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")

        self.Label2 = tk.Label(self.Labelframe1)
        self.Label2.place(relx=0.125, rely=0.247, height=20, width=270
                          , bordermode='ignore')
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''1. Sync computer datetime to device''')

        self.Label3 = tk.Label(self.Labelframe1)
        self.Label3.place(relx=0.125, rely=0.617, height=20, width=255
                          , bordermode='ignore')
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''2. Update device network settings''')

        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.083, rely=0.330, height=20, width=100)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Current IP''')

        self.Label5 = tk.Label(top)
        self.Label5.place(relx=0.417, rely=0.330, height=20, width=100)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(activeforeground="black")
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(text='''Username''')

        self.Label6 = tk.Label(top)
        self.Label6.place(relx=0.733, rely=0.330, height=20, width=100)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(activeforeground="black")
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(disabledforeground="#a3a3a3")
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(highlightbackground="#d9d9d9")
        self.Label6.configure(highlightcolor="black")
        self.Label6.configure(text='''Password''')

        self.Text1 = tk.Text(top)
        self.Text1.place(relx=0.05, rely=0.370, relheight=0.060, relwidth=0.25)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="blue")
        self.Text1.configure(selectforeground="white")
        self.Text1.configure(wrap="word")

        self.Text2 = tk.Text(top)
        self.Text2.place(relx=0.375, rely=0.370, relheight=0.060, relwidth=0.25)
        self.Text2.configure(background="white")
        self.Text2.configure(font="TkTextFont")
        self.Text2.configure(foreground="black")
        self.Text2.configure(highlightbackground="#d9d9d9")
        self.Text2.configure(highlightcolor="black")
        self.Text2.configure(insertbackground="black")
        self.Text2.configure(selectbackground="blue")
        self.Text2.configure(selectforeground="white")
        self.Text2.configure(wrap="word")

        self.Text3 = tk.Text(top)
        self.Text3.place(relx=0.7, rely=0.370, relheight=0.060, relwidth=0.25)
        self.Text3.configure(background="white")
        self.Text3.configure(font="TkTextFont")
        self.Text3.configure(foreground="black")
        self.Text3.configure(highlightbackground="#d9d9d9")
        self.Text3.configure(highlightcolor="black")
        self.Text3.configure(insertbackground="black")
        self.Text3.configure(selectbackground="blue")
        self.Text3.configure(selectforeground="white")
        self.Text3.configure(wrap="word")

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.0, rely=0.450, relwidth=1.0)

        self.Label8 = tk.Label(top)
        self.Label8.place(relx=0.017, rely=0.470, height=20, width=252)
        self.Label8.configure(activebackground="#f9f9f9")
        self.Label8.configure(activeforeground="black")
        self.Label8.configure(background="#d9d9d9")
        self.Label8.configure(disabledforeground="#a3a3a3")
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(highlightbackground="#d9d9d9")
        self.Label8.configure(highlightcolor="black")
        self.Label8.configure(text='''Please click the following button to''')

        self.Label10 = tk.Label(top)
        self.Label10.place(relx=0.017, rely=0.510, height=20, width=245)
        self.Label10.configure(activebackground="#f9f9f9")
        self.Label10.configure(activeforeground="black")
        self.Label10.configure(background="#d9d9d9")
        self.Label10.configure(disabledforeground="#a3a3a3")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(highlightbackground="#d9d9d9")
        self.Label10.configure(highlightcolor="black")
        self.Label10.configure(text='''sync computer datetime to device''')

        self.Label9 = tk.Label(top)
        self.Label9.place(relx=0.017, rely=0.550, height=20, width=360)
        self.Label9.configure(activebackground="#f9f9f9")
        self.Label9.configure(activeforeground="black")
        self.Label9.configure(background="#d9d9d9")
        self.Label9.configure(disabledforeground="#a3a3a3")
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(highlightbackground="#d9d9d9")
        self.Label9.configure(highlightcolor="black")
        self.Label9.configure(text='''and update datetime format to MM-dd-yyyy HH:mm:ss''')

        self.TButton1 = ttk.Button(top)
        self.TButton1.place(relx=0.7, rely=0.480, height=40, width=118)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''Sync datetime''')
        self.TButton1.configure(command=self.update_timezone_and_datetime)

        ################IP

        self.TSeparator2 = ttk.Separator(top)
        self.TSeparator2.place(relx=0.0, rely=0.600, relwidth=1.0)

        self.Label7 = tk.Label(top)
        self.Label7.place(relx=0.067, rely=0.635, height=20, width=122)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(activeforeground="black")
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(text='''New IP Address''')

        self.Text4 = tk.Text(top)
        self.Text4.place(relx=0.283, rely=0.630, relheight=0.060, relwidth=0.30)
        self.Text4.configure(background="white")
        self.Text4.configure(font="TkTextFont")
        self.Text4.configure(foreground="black")
        self.Text4.configure(highlightbackground="#d9d9d9")
        self.Text4.configure(highlightcolor="black")
        self.Text4.configure(insertbackground="black")
        self.Text4.configure(selectbackground="blue")
        self.Text4.configure(selectforeground="white")
        self.Text4.configure(wrap="word")

        self.Label11 = tk.Label(top)
        self.Label11.place(relx=0.067, rely=0.730, height=20, width=122)
        self.Label11.configure(activebackground="#f9f9f9")
        self.Label11.configure(activeforeground="black")
        self.Label11.configure(background="#d9d9d9")
        self.Label11.configure(disabledforeground="#a3a3a3")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(highlightbackground="#d9d9d9")
        self.Label11.configure(highlightcolor="black")
        self.Label11.configure(text='''Subnet Mask''')

        self.Text5 = tk.Text(top)
        self.Text5.place(relx=0.283, rely=0.720, relheight=0.060, relwidth=0.30)
        self.Text5.bind("<FocusIn>", self.get_sub_mask)
        self.Text5.configure(background="white")
        self.Text5.configure(font="TkTextFont")
        self.Text5.configure(foreground="black")
        self.Text5.configure(highlightbackground="#d9d9d9")
        self.Text5.configure(highlightcolor="black")
        self.Text5.configure(insertbackground="black")
        self.Text5.configure(selectbackground="blue")
        self.Text5.configure(selectforeground="white")
        self.Text5.configure(wrap="word")

        self.Label12 = tk.Label(top)
        self.Label12.place(relx=0.067, rely=0.820, height=20, width=122)
        self.Label12.configure(activebackground="#f9f9f9")
        self.Label12.configure(activeforeground="black")
        self.Label12.configure(background="#d9d9d9")
        self.Label12.configure(disabledforeground="#a3a3a3")
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(highlightbackground="#d9d9d9")
        self.Label12.configure(highlightcolor="black")
        self.Label12.configure(text='''Default gateway''')

        self.Text6 = tk.Text(top)
        self.Text6.place(relx=0.283, rely=0.810, relheight=0.060, relwidth=0.30)
        self.Text6.bind("<FocusIn>", self.get_default_gateway)
        self.Text6.configure(background="white")
        self.Text6.configure(font="TkTextFont")
        self.Text6.configure(foreground="black")
        self.Text6.configure(highlightbackground="#d9d9d9")
        self.Text6.configure(highlightcolor="black")
        self.Text6.configure(insertbackground="black")
        self.Text6.configure(selectbackground="blue")
        self.Text6.configure(selectforeground="white")
        self.Text6.configure(wrap="word")

        self.TButton2 = ttk.Button(top)
        self.TButton2.place(relx=0.7, rely=0.700, height=40, width=118)
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='''Update IP''')
        self.TButton2.configure(command=self.update_ip)

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

    def get_sub_mask(self, event):
        try:
            if len(self.Text4.get("1.0", 'end-1c')) > 0:
                net = ipaddress.ip_network(self.Text4.get("1.0", 'end-1c') + '/24', strict=False)
                if len(self.Text5.get("1.0", 'end-1c')) > 0:
                    self.Text5.delete('1.0', 'end')
                self.Text5.insert(1.0, str(net.netmask))
            else:
                print("please input new ip address to get sub mask")
        except Exception as e:
            print(e)
            self.Text5.delete('1.0', 'end')

    def get_default_gateway(self, event):
        try:
            if len(self.Text4.get("1.0", 'end-1c')) > 0:
                default_gateway_ip = get_default_gateway_ip(self.Text4.get("1.0", 'end-1c'))
                if default_gateway_ip is not None:
                    if len(self.Text6.get("1.0", 'end-1c')) > 0:
                        self.Text6.delete('1.0', 'end')
                    self.Text6.insert(1.0, default_gateway_ip)
                else:
                    print("default_gateway_ip is None")
            else:
                print("please input new ip address to get default gateway")
        except Exception as e:
            print(e)
            self.Text6.delete('1.0', 'end')

    def update_timezone_and_datetime(self):
        try:
            result = update_device_time(
                self.Text1.get("1.0", 'end-1c'),
                self.Text2.get("1.0", 'end-1c'),
                self.Text3.get("1.0", 'end-1c'))
            if result == 'success':
                tkinter.messagebox.showinfo("Information", "Update Device time success")
            else:
                tkinter.messagebox.showinfo("Information", "Update Device time failed")
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", "Please check input and connection then try again")

    def update_ip(self):
        try:
            result = update_ip(
                self.Text1.get("1.0", 'end-1c'),
                self.Text2.get("1.0", 'end-1c'),
                self.Text3.get("1.0", 'end-1c'),
                self.Text4.get("1.0", 'end-1c'),
                self.Text6.get("1.0", 'end-1c'))
            if result == 'success':
                tkinter.messagebox.showinfo("Information", "Update Device IP success")
            else:
                tkinter.messagebox.showinfo("Information", "Update Device IP failed")
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", "Please check input and connection then try again")


if __name__ == '__main__':
    vp_start_gui()
