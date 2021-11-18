from tkinter import *
import tkinter.messagebox
import threading
import random
import time

class Petri:
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)
        self.init_free = ""
        self.init_busy = ""
        self.init_docu = ""
        self.markings = []
        self.state = 0
        self.transition = 0
        self.free = ""
        self.busy = ""
        self.docu = ""
        self.flag_auto = -1
        self.flag_fire_start = -1
        self.flag_fire_change = -1
        self.flag_fire_end = -1
        self.isSet = -1
        self.deadlock = -1
        self.createWidgets()
        

    def createWidgets(self):
        # _____ CREATE GUI _____
        self.canvas = Canvas(self.master, bg="white", height="300")
        self.canvas.pack()
        self.canvas.grid(row=0, column=0, columnspan=6, sticky=W+E+N+S, padx=3, pady=3)

        # CREATE PLACE AND LABEL IT
        self.canvas.create_oval(70, 50, 140, 120) # FREE
        self.canvas.create_oval(210, 190, 280, 260) # BUSY
        self.canvas.create_oval(350, 50, 420, 120) # DOCU

        widget = Label(self.canvas, text='FREE', bg="white")
        widget.pack()
        self.canvas.create_window(105, 35, window = widget)

        self.label_free = Label(self.canvas, text = "0", bg="white")
        self.label_free.pack()
        self.canvas.create_window(105, 85, window = self.label_free)

        widget = Label(self.canvas, text='BUSY', bg="white")
        widget.pack()
        self.canvas.create_window(245, 275, window = widget)

        self.label_busy = Label(self.canvas, text = "0", bg="white")
        self.label_busy.pack()
        self.canvas.create_window(245, 225, window = self.label_busy)

        widget = Label(self.canvas, text='DOCU', bg="white")
        widget.pack()
        self.canvas.create_window(385, 35, window = widget)

        self.label_docu = Label(self.canvas, text = "0", bg="white")
        self.label_docu.pack()
        self.canvas.create_window(385, 85, window = self.label_docu)

        # CREATE TRANSITION, ADD USER CLICK AND LABEL IT
        self.canvas.create_rectangle(70, 190, 140, 260, tag="start") # START
        self.canvas.create_rectangle(210, 50, 280, 120, tag="end") # END
        self.canvas.create_rectangle(350, 190, 420, 260, tag="change") # CHANGE

        widget = Label(self.canvas, text='START', bg="white")
        widget.pack()
        self.canvas.create_window(105, 275, window = widget)

        widget = Label(self.canvas, text='END', bg="white")
        widget.pack()
        self.canvas.create_window(245, 35, window = widget)

        widget = Label(self.canvas, text='CHANGE', bg="white")
        widget.pack()
        self.canvas.create_window(385, 275, window = widget)

        # FLOW RELATION
        self.canvas.create_line(210, 85, 140, 85, arrow=tkinter.LAST) # END -> FREE
        self.canvas.create_line(350, 85, 280, 85, arrow=tkinter.LAST) # DOCU -> END
        self.canvas.create_line(140, 225, 210, 225, arrow=tkinter.LAST) # START -> BUSY
        self.canvas.create_line(280, 225, 350, 225, arrow=tkinter.LAST) # BUSY -> CHANGE
        self.canvas.create_line(105, 120, 105, 190, arrow=tkinter.LAST) # FREE -> START
        self.canvas.create_line(385, 190, 385, 120, arrow=tkinter.LAST) # CHANGE -> DOCU

        # FORM
        Label(self.master, text = "FREE").grid(row = 1, column = 0)
        self.input_free = Entry(self.master)
        self.input_free.grid(row = 1, column = 1)

        Label(self.master, text = "BUSY").grid(row = 1, column = 2)
        self.input_busy = Entry(self.master)
        self.input_busy.grid(row = 1, column = 3)

        Label(self.master, text = "DOCU").grid(row = 1, column = 4)
        self.input_docu = Entry(self.master)
        self.input_docu.grid(row = 1, column = 5)

        # BUTTON
        self.init_button = Button(self.master, width=16, padx=3, pady=3)
        self.init_button['text'] = "SET"
        self.init_button['command'] = self.setup
        self.init_button.grid(row=2, column=1, padx=2, pady=2)

        self.auto_button = Button(self.master, width=16, padx=3, pady=3)
        self.auto_button['text'] = "AUTO FIRE"
        self.auto_button['command'] = self.auto_fire
        self.auto_button.grid(row=2, column=3, padx=2, pady=2)

        self.stop_button = Button(self.master, width=16, padx=3, pady=3)
        self.stop_button['text'] = "STOP FIRE"
        self.stop_button['command'] = self.stop_fire
        self.stop_button.grid(row=3, column=3, padx=2, pady=2)

        self.marking_button = Button(self.master, width=16, padx=3, pady=3)
        self.marking_button['text'] = "MARKING"
        self.marking_button['command'] = self.marking
        self.marking_button.grid(row=2, column=5, padx=2, pady=2)

        self.canvas.bind("<Button-1>", self.onClick)

        # LABEL MARKING
        self.label_marking = Label(self.canvas, text = "MARKING M = [" + str(self.free) 
                                                        + ".free, " + str(self.busy) + ",.busy " + str(self.docu) +".docu]" 
                                                , bg="white")
        self.label_marking.pack()
        self.canvas.create_window(245, 10, window = self.label_marking)

    def setup(self):
        print("SETUP\n" + "-"*30)
        self.markings = []
        self.state = 0
        self.transition = 0

        if self.flag_auto == 1:
            tkinter.messagebox.showwarning('Lỗi', 'Không thể SET khi đang AUTO FIRE !!!')
        else: 
            if (not (self.input_free.get().isnumeric() and self.input_busy.get().isnumeric()
                            and self.input_docu.get().isnumeric())):
                tkinter.messagebox.showwarning('Lỗi nhập', 'Vui lòng nhập các số nguyên không âm !!!')
            else:
                self.free = self.init_free = int(self.input_free.get())
                self.busy = self.init_busy = int(self.input_busy.get())
                self.docu = self.init_docu = int(self.input_docu.get())

                self.label_free.configure(text = str(self.init_free))
                self.label_busy.configure(text = str(self.init_busy))
                self.label_docu.configure(text = str(self.init_docu))
                self.label_marking.configure(text = "MARKING M_0 = [" + str(self.free) + ".free, " 
                                                    + str(self.busy) + ".busy, " + str(self.docu) +".docu]")

    def auto_fire(self):
        if (self.init_busy == "" and self.init_free == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SET để khởi tạo MARKING trước khi dùng các chức năng khác!')
        elif self.flag_auto == 1: pass
        else:
            self.flag_auto *= -1
            # while (self.flag_auto == 1):
            print("AUTO FIRE MODE ON\n" + "-"*30)
            self.thread_auto_fire = threading.Thread(target=self.handle_fire)
            self.thread_auto_fire.start()   
    
    def stop_fire(self):
        if (self.init_busy == "" and self.init_free == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SET để khởi tạo MARKING trước khi dùng các chức năng khác!')
        else:
            self.flag_auto *= -1
            print("AUTO FIRE MODE OFF\n" + "-"*30)

    def marking(self):
        if (self.init_busy == "" and self.init_free == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SET để khởi tạo MARKING trước khi dùng các chức năng khác!')
        else:
            # FORM MARKING: [x.free, y.busy, z.docu]
            print("TRANSITION SYSTEM")
            self.markings = []
            self.state = 0
            self.transition = 0

            current_marking = [self.init_free, self.init_busy, self.init_docu]
            self.markings.append(current_marking)
            self.state += 1

            self.find_marking(self.markings[0])
            
            print(str(self.state) + " states")
            print(str(self.transition) + " transitions\n" + "-"*30)

    def find_marking(self, marking): 
        near = self.near_marking(marking)
        for i in range (0, len(near)):
            self.find_marking(near[i])
    
    def near_marking(self, current_marking):
        near = []
        if (current_marking[0] > 0):
            self.transition += 1
            marking = [current_marking[0] - 1, current_marking[1] + 1, current_marking[2]]
            print("[" + str(current_marking) + "; START> " + str(marking))
            
            if (marking in self.markings): pass
            else: 
                near.append(marking)
                self.markings.append(marking)
                self.state += 1
                    
        if (current_marking[1] > 0):
            self.transition += 1
            marking = [current_marking[0], current_marking[1] - 1, current_marking[2] + 1]
            print("[" + str(current_marking) + "; CHANGE> " + str(marking))
            
            if (marking in self.markings): pass
            else: 
                near.append(marking)
                self.markings.append(marking)
                self.state += 1
                    
        if (current_marking[2] > 0):
            self.transition += 1
            marking = [current_marking[0] + 1, current_marking[1], current_marking[2] - 1]
            print("[" + str(current_marking) + "; END> " + str(marking))

            if (marking in self.markings): pass
            else: 
                near.append(marking)
                self.markings.append(marking)
                self.state += 1
        return near

    def onClick(self, event):
        if (self.init_busy == "" and self.init_free == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SET để khởi tạo Marking ban đầu !!!')
        elif (self.flag_auto == 1):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng tắt AUTO FIRE để có thể kích hoạt theo ý muốn !!!')
        else:
            item = self.canvas.find_closest(event.x, event.y)
            tag = self.canvas.itemcget(item, "tag")
            if tag == "start" and self.flag_fire_start != 1:
                if self.free != 0:
                    print("FIRING START!!!")
                    self.fire_start()
                else:
                    tkinter.messagebox.showwarning('Lỗi', 'Chuyển tiếp START không tích cực!!!')

            elif tag == "end" and self.flag_fire_end != 1:
                if self.docu != 0:
                    print("FIRING END!!!")
                    self.fire_end()
                else:
                    tkinter.messagebox.showwarning('Lỗi', 'Chuyển tiếp END không tích cực!!!')

            elif tag == "change" and self.flag_fire_change != 1:
                if self.busy != 0:
                    print("FIRING CHANGE!!!")
                    self.fire_change()
                else:
                    tkinter.messagebox.showwarning('Lỗi', 'Chuyển tiếp CHANGE không tích cực!!!')

    def fire_start(self):
        if self.flag_fire_start == -1:
            self.start_dot = self.canvas.create_oval(100, 120, 110, 130, fill="black")
            self.flag_fire_start *= -1

        if self.canvas.coords(self.start_dot)[1] != 220.0:
                self.canvas.move(self.start_dot, 0, 5)
        elif self.canvas.coords(self.start_dot)[0] != 200.0:
                self.canvas.move(self.start_dot, 5, 0)
        
        if self.canvas.coords(self.start_dot)[0] != 200.0:
                self.canvas.after(20, self.fire_start)
        else:
            self.canvas.delete(self.start_dot)
            self.free -= 1
            self.busy += 1
            self.label_free.configure(text = str(self.free))
            self.label_busy.configure(text = str(self.busy))
            self.label_marking.configure(text = "MARKING M = [" + str(self.free) + ", " 
                                                    + str(self.busy) + ", " + str(self.docu) +"]")
            self.flag_fire_start *= -1

    def fire_end(self):
        if self.flag_fire_end == -1:
            self.end_dot = self.canvas.create_oval(340, 80, 350, 90, fill="black")
            self.flag_fire_end *= -1

        if self.canvas.coords(self.end_dot)[0] != 135.0:
                self.canvas.move(self.end_dot, -5, 0)

        if self.canvas.coords(self.end_dot)[0] != 135.0:
                self.canvas.after(20, self.fire_end)
        else:
            self.canvas.delete(self.end_dot)
            self.free += 1
            self.docu -= 1
            self.label_free.configure(text = str(self.free))
            self.label_docu.configure(text = str(self.docu))
            self.label_marking.configure(text = "MARKING M = [" + str(self.free) + ", " 
                                                    + str(self.busy) + ", " + str(self.docu) +"]")
            self.flag_fire_end *= -1

    def fire_change(self):
        if self.flag_fire_change == -1:
            self.change_dot = self.canvas.create_oval(280, 220, 290, 230, fill="black")
            self.flag_fire_change *= -1

        if self.canvas.coords(self.change_dot)[0] != 380.0:
            self.canvas.move(self.change_dot, 5, 0)
        elif self.canvas.coords(self.change_dot)[1] != 120.0:
            self.canvas.move(self.change_dot, 0, -5)

        if self.canvas.coords(self.change_dot)[1] != 120.0:
            self.canvas.after(20, self.fire_change)
        else:
            self.canvas.delete(self.change_dot)
            self.docu += 1
            self.busy -= 1
            self.label_docu.configure(text = str(self.docu))
            self.label_busy.configure(text = str(self.busy))
            self.label_marking.configure(text = "MARKING M = [" + str(self.free) + ", " 
                                                    + str(self.busy) + ", " + str(self.docu) +"]")
            self.flag_fire_change *= -1

    def handle_fire(self):        
        while (self.flag_auto == 1 and self.flag_fire_start != 1 and self.flag_fire_change != 1 and self.flag_fire_end != 1):
            self.check_deadlock()
            self.fire()
            time.sleep(1.35)

    def fire(self):
        if ((self.free > 0 and self.docu == 0 and self.busy == 0) or
            (self.free == 0 and self.docu > 0 and self.busy == 0) or
            (self.free == 0 and self.docu == 0 and self.busy > 0)):
            if self.free > 0:
                self.fire_start()
            if self.docu > 0:
                self.fire_end()
            if self.busy > 0:
                self.fire_change()
        
        elif (self.free > 0 and self.docu > 0 and self.busy == 0):
            prob = random.random()
            if prob <= 1.0/3:
                self.fire_start()
            elif prob <= 2.0/3:
                self.fire_end()
            else:
                self.fire_start()
                self.fire_end()

        elif (self.free > 0 and self.docu == 0 and self.busy > 0):
            prob = random.random()
            if prob <= 1.0/3:
                self.fire_start()
            elif prob <= 2.0/3:
                self.fire_change()
            else:
                self.fire_start()
                self.fire_change()
        
        elif (self.free == 0 and self.docu > 0 and self.busy > 0):
            prob = random.random()
            if prob <= 1.0/3:
                self.fire_end()
            elif prob <= 2.0/3:
                self.fire_change()
            else:
                self.fire_end()
                self.fire_change()

        elif (self.free > 0 and self.docu > 0 and self.busy > 0):
            prob = random.random()
            if prob <= 1.0/7:
                self.fire_start()
            elif prob <= 2.0/7:
                self. fire_change()
            elif prob <= 3.0/7:
                self.fire_end()
            elif prob <= 4.0/7:
                self.fire_start()
                self.fire_end()
            elif prob <= 5.0/7:
                self.fire_start()
                self.fire_change()
            elif prob <= 6.0/7:
                self.fire_end()
                self.fire_change()
            else:
                self.fire_start()
                self.fire_change()
                self.fire_end()

    def check_deadlock(self):
        if (self.free == 0 and self.docu == 0 and self.busy == 0):
            print("DEADLOCK")
            self.stop_fire()

    def handler(self):
        if self.flag_auto == 1: 
            self.flag_auto = -1
        if self.flag_fire_change == 1 or self.flag_fire_end == 1 or self.flag_fire_start == 1: 
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng chờ, đang ngừng các chuyển tiếp ...')
        if tkinter.messagebox.askokcancel("Quit app ?", "Are you sure to quit"):
            if self.isSet == 1: self.stop_fire()
            self.master.destroy()

if __name__ == "__main__":
    root = Tk()

    app = Petri(root)
    app.master.title("Item 1bii - Assignment - Petri Net")

    root.mainloop()
