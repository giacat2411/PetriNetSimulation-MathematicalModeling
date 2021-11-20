from tkinter import *
import tkinter.messagebox
import threading
import random
import time
from PetriNet import PetriNet

class Item2(PetriNet):
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)

        self.markings = []
        self.state = 0
        self.transition = 0
        self.nums_sequence = 0

        self.init_wait = ""
        self.init_inside = ""
        self.init_done = ""

        self.wait = ""
        self.inside = ""
        self.done = ""

        self.flag_auto = -1
        self.isSet = -1
        self.deadlock = -1

        self.flag_fire_start = -1
        self.flag_fire_change = -1

        self.isClosed = -1

        self.createWidgets()
        

    def createWidgets(self):
        # ----------------------------------------------------------------------------------
        # CREATE GUI
        self.canvas = Canvas(self.master, bg="white", height="300")
        self.canvas.pack()
        self.canvas.grid(row=0, column=0, columnspan=6, sticky=W+E+N+S, padx=3, pady=3)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # CREATE PLACE AND LABEL IT
        self.canvas.create_oval(70, 50, 140, 120) # WAIT
        self.canvas.create_oval(210, 190, 280, 260) # INSIDE
        self.canvas.create_oval(350, 50, 420, 120) # DONE

        widget = Label(self.canvas, text='WAIT', bg="white")
        widget.pack()
        self.canvas.create_window(105, 35, window = widget)

        self.label_wait = Label(self.canvas, text = "0", bg="white")
        self.label_wait.pack()
        self.canvas.create_window(105, 85, window = self.label_wait)

        widget = Label(self.canvas, text='INSIDE', bg="white")
        widget.pack()
        self.canvas.create_window(245, 275, window = widget)

        self.label_inside = Label(self.canvas, text = "0", bg="white")
        self.label_inside.pack()
        self.canvas.create_window(245, 225, window = self.label_inside)

        widget = Label(self.canvas, text='DONE', bg="white")
        widget.pack()
        self.canvas.create_window(385, 35, window = widget)

        self.label_done = Label(self.canvas, text = "0", bg="white")
        self.label_done.pack()
        self.canvas.create_window(385, 85, window = self.label_done)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # CREATE TRANSITION, ADD USER CLICK AND LABEL IT
        self.canvas.create_rectangle(70, 190, 140, 260, tag="start") # START
        self.canvas.create_rectangle(350, 190, 420, 260, tag="change") # CHANGE

        widget = Label(self.canvas, text='START', bg="white")
        widget.pack()
        self.canvas.create_window(105, 275, window = widget)

        widget = Label(self.canvas, text='CHANGE', bg="white")
        widget.pack()
        self.canvas.create_window(385, 275, window = widget)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # FLOW RELATION
        self.canvas.create_line(140, 225, 210, 225, arrow=tkinter.LAST) # START -> INSIDE
        self.canvas.create_line(280, 225, 350, 225, arrow=tkinter.LAST) # INSIDE -> CHANGE
        self.canvas.create_line(105, 120, 105, 190, arrow=tkinter.LAST) # WAIT -> START
        self.canvas.create_line(385, 190, 385, 120, arrow=tkinter.LAST) # CHANGE -> DONE
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # FORM
        Label(self.master, text = "WAIT").grid(row = 1, column = 0)
        self.input_wait = Entry(self.master)
        self.input_wait.grid(row = 1, column = 1)

        Label(self.master, text = "INSIDE").grid(row = 1, column = 2)
        self.input_inside = Entry(self.master)
        self.input_inside.grid(row = 1, column = 3)

        Label(self.master, text = "DONE").grid(row = 1, column = 4)
        self.input_done = Entry(self.master)
        self.input_done.grid(row = 1, column = 5)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # BUTTON
        self.setup_button = Button(self.master, width=16, padx=3, pady=3)
        self.setup_button['text'] = "SETUP"
        self.setup_button['command'] = self.setup
        self.setup_button.grid(row=2, column=1, padx=2, pady=2)

        self.reset_button = Button(self.master, width=16, padx=3, pady=3)
        self.reset_button['text'] = "RESET"
        self.reset_button['command'] = self.reset
        self.reset_button.grid(row=3, column=1, padx=2, pady=2)

        self.auto_button = Button(self.master, width=16, padx=3, pady=3)
        self.auto_button['text'] = "AUTO FIRE"
        self.auto_button['command'] = self.auto_fire
        self.auto_button.grid(row=2, column=3, padx=2, pady=2)

        self.stop_button = Button(self.master, width=16, padx=3, pady=3)
        self.stop_button['text'] = "STOP FIRE"
        self.stop_button['command'] = self.stop_fire
        self.stop_button.grid(row=3, column=3, padx=2, pady=2)

        self.ts_button = Button(self.master, width=16, padx=3, pady=3)
        self.ts_button['text'] = "TRANSITION SYSTEM"
        self.ts_button['command'] = self.transition_system
        self.ts_button.grid(row=2, column=5, padx=2, pady=2)

        self.firing_sequence_button = Button(self.master, width=16, padx=3, pady=3)
        self.firing_sequence_button['text'] = "FIRING SEQUENCE"
        self.firing_sequence_button['command'] = self.firing_sequence
        self.firing_sequence_button.grid(row=3, column=5, padx=2, pady=2)

        self.canvas.bind("<Button-1>", self.onClick)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # LABEL MARKING
        self.label_marking = Label(self.canvas, text = "MARKING M = [" + str(self.wait) 
                                                        + ".wait, " + str(self.inside) + ",.inside " + str(self.done) +".done]" 
                                                , bg="white")
        self.label_marking.pack()
        self.canvas.create_window(245, 10, window = self.label_marking)
        # ----------------------------------------------------------------------------------

    def setup(self):
        print("SETUP")
        self.markings = []
        self.state = 0
        self.transition = 0

        if self.flag_auto == 1:
            tkinter.messagebox.showwarning('Lỗi', 'Không thể SET khi đang AUTO FIRE !!!')
            print("FAILED\n"  + "-"*30)
        else: 
            if (not (self.input_wait.get().isnumeric() and self.input_inside.get().isnumeric()
                            and self.input_done.get().isnumeric())):
                tkinter.messagebox.showwarning('Lỗi nhập', 'Vui lòng nhập các số nguyên không âm !!!')
                print("FAILED\n"  + "-"*30)
            else:
                self.isSet = 1
                self.wait = self.init_wait = int(self.input_wait.get())
                self.inside = self.init_inside = int(self.input_inside.get())
                self.done = self.init_done = int(self.input_done.get())

                self.label_wait.configure(text = str(self.init_wait))
                self.label_inside.configure(text = str(self.init_inside))
                self.label_done.configure(text = str(self.init_done))
                self.label_marking.configure(text = "MARKING M_0 = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done]")
                
                print("SUCCESSFUL")
                print("Initial Marking: M0 = [" + str(self.init_wait) + ".wait, "
                                + str(self.init_inside) + ".inside, " + str(self.init_done) + ".done]\n"   + "-"*30)
    
    def reset(self):
        print("RESET")
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SETUP để khởi tạo MARKING trước khi dùng các chức năng khác!')
            print("FAILED\n"  + "-"*30)

        elif self.flag_auto == 1:
            tkinter.messagebox.showwarning('Lỗi', 'Không thể RESET khi đang AUTO FIRE !!!')
            print("FAILED\n"  + "-"*30)

        else:
            self.wait = self.init_wait
            self.inside = self.init_inside
            self.done = self.init_done

            self.label_wait.configure(text = str(self.init_wait))
            self.label_inside.configure(text = str(self.init_inside))
            self.label_done.configure(text = str(self.init_done))

            self.label_marking.configure(text = "MARKING M_0 = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done]")
            print("SUCCESSFUL")
            print("Initial Marking: M0 = [" + str(self.init_wait) + ".wait, "
                                + str(self.init_inside) + ".inside, " + str(self.init_done) + ".done]\n"   + "-"*30)

    def auto_fire(self):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SET để khởi tạo MARKING trước khi dùng các chức năng khác!')
        elif self.flag_auto == 1: pass
        else:
            self.flag_auto *= -1

            print("AUTO FIRE MODE ON\n" + "-"*30)

            self.thread_auto_fire = threading.Thread(target=self.handle_fire)
            self.thread_auto_fire.start()   
    
    def stop_fire(self):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SET để khởi tạo MARKING trước khi dùng các chức năng khác!')
        elif self.flag_auto == -1: pass
        else:
            self.flag_auto *= -1
            print("AUTO FIRE MODE OFF\n" + "-"*30)

    def transition_system(self):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SET để khởi tạo MARKING trước khi dùng các chức năng khác!')
        else:
            # FORM MARKING: [x.wait, y.inside, z.done]
            print("TRANSITION SYSTEM")
            self.markings = []
            self.state = 0
            self.transition = 0

            current_marking = [self.init_wait, self.init_inside, self.init_done]
            self.markings.append(current_marking)
            self.state += 1

            self.find_transition_relation(self.markings[0])
            
            print(str(self.state) + " states")
            print(str(self.transition) + " transitions\n" + "-"*30)

    def find_transition_relation(self, marking): 
        near = self.find_near_marking(marking)
        for i in range (0, len(near)):
            self.find_transition_relation(near[i])
    
    def find_near_marking(self, current_marking):
        near = []
        if (current_marking[0] > 0):
            self.transition += 1
            marking = [current_marking[0] - 1, current_marking[1] + 1, current_marking[2]]
            print("[" + str(current_marking[0]) + ".wait, " + str(current_marking[1]) + ".inside, " 
                      + str(current_marking[2]) + ".done]"+ "; START> " 
                      + "[" + str(marking[0]) + ".wait, " + str(marking[1]) + ".inside, " 
                      + str(marking[2]) + ".done]")
            
            if (marking in self.markings): pass
            else: 
                near.append(marking)
                self.markings.append(marking)
                self.state += 1
                    
        if (current_marking[1] > 0):
            self.transition += 1
            marking = [current_marking[0], current_marking[1] - 1, current_marking[2] + 1]
            print("[" + str(current_marking[0]) + ".wait, " + str(current_marking[1]) + ".inside, " 
                      + str(current_marking[2]) + ".done]"+ "; CHANGE> " 
                      + "[" + str(marking[0]) + ".wait, " + str(marking[1]) + ".inside, " 
                      + str(marking[2]) + ".done]")
            
            if (marking in self.markings): pass
            else: 
                near.append(marking)
                self.markings.append(marking)
                self.state += 1     
        return near

    def firing_sequence(self):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SETUP để khởi tạo MARKING trước khi dùng các chức năng khác!')
        else:
            # FORM MARKING: [x.free, y.busy, z.docu]
            print("FIRING SEQUENCE")
            self.markings = []
            sequence = ""
            self.nums_sequence = 0

            current_marking = [self.init_wait, self.init_inside, self.init_done]
            self.markings.append(current_marking)

            self.find_firing_sequence(self.markings[0], sequence)
            print("Initial Marking: M0 = [" + str(self.init_wait) + ".wait, "
                                + str(self.init_inside) + ".inside, " + str(self.init_done) + ".done]")
            print(str(self.nums_sequence) + " firing sequence\n" + "-"*30)

    def find_firing_sequence(self, current_marking, sequence):
        next_sequence = self.find_next_sequence(current_marking, sequence)
        for i in range (0, len(next_sequence["next"])):
            self.find_firing_sequence(next_sequence["next"][i], next_sequence["firing"][i])

    def find_next_sequence(self, current_marking, sequence):
        next = []
        firing = []

        if current_marking[0] > 0:
            marking = [current_marking[0] - 1, current_marking[1] + 1, current_marking[2]]
            self.nums_sequence += 1

            if sequence == "":
                print("[M0 ; ("+ sequence + "START)> " 
                        + "[" + str(marking[0]) + ".wait, " + str(marking[1]) + ".inside, " 
                        + str(marking[2]) + ".done]")
            else:
                print("[M0 ; ("+ sequence + ", START)> " 
                        + "[" + str(marking[0]) + ".wait, " + str(marking[1]) + ".inside, " 
                        + str(marking[2]) + ".done]")
            
            if (marking in self.markings): pass
            else: 
                next.append(marking)

                if sequence == "": 
                    firing.append(sequence + "START")
                else:
                    firing.append(sequence + ", START")

                self.markings.append(marking)
                    
        if current_marking[1] > 0:
            marking = [current_marking[0], current_marking[1] - 1, current_marking[2] + 1]
            self.nums_sequence += 1

            if sequence == "":
                print("[M0 ; ("+ sequence + "CHANGE)> " 
                        + "[" + str(marking[0]) + ".wait, " + str(marking[1]) + ".inside, " 
                        + str(marking[2]) + ".done]")
            else:
                print("[M0 ; ("+ sequence + ", CHANGE)> " 
                        + "[" + str(marking[0]) + ".wait, " + str(marking[1]) + ".inside, " 
                        + str(marking[2]) + ".done]")
            
            if (marking in self.markings): pass
            else: 
                next.append(marking)

                if sequence == "": 
                    firing.append(sequence + "CHANGE")
                else:
                    firing.append(sequence + ", CHANGE")

                self.markings.append(marking)

        return { "next": next, "firing": firing }

    def onClick(self, event):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == ""):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng bấm SET để khởi tạo Marking ban đầu !!!')
        elif (self.flag_auto == 1):
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng tắt AUTO FIRE để có thể kích hoạt theo ý muốn !!!')
        else:
            item = self.canvas.find_closest(event.x, event.y)
            tag = self.canvas.itemcget(item, "tag")
            if tag == "start" and self.flag_fire_start != 1:
                if self.wait != 0:
                    print("FIRING START!!!")
                    self.fire_start()
                else:
                    tkinter.messagebox.showwarning('Lỗi', 'Chuyển tiếp START không tích cực!!!')

            elif tag == "change" and self.flag_fire_change != 1:
                if self.inside != 0:
                    print("FIRING CHANGE!!!")
                    self.fire_change()
                else:
                    tkinter.messagebox.showwarning('Lỗi', 'Chuyển tiếp CHANGE không tích cực!!!')

    def fire_start(self):
        if self.flag_fire_start == -1:
            self.start_dot = self.canvas.create_oval(100, 120, 110, 130, fill="black")

            self.flag_fire_start *= -1
            self.wait -= 1
            self.label_wait.configure(text = str(self.wait))

        if self.canvas.coords(self.start_dot)[1] != 220.0:
                self.canvas.move(self.start_dot, 0, 5)
        elif self.canvas.coords(self.start_dot)[0] != 200.0:
                self.canvas.move(self.start_dot, 5, 0)
        
        if self.canvas.coords(self.start_dot)[0] != 200.0:
                self.canvas.after(20, self.fire_start)
        else:
            self.canvas.delete(self.start_dot)

            self.inside += 1
            self.label_inside.configure(text = str(self.inside))
            self.label_marking.configure(text = "MARKING M = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done]")
            self.flag_fire_start *= -1

    def fire_change(self):
        if self.flag_fire_change == -1:
            self.change_dot = self.canvas.create_oval(280, 220, 290, 230, fill="black")

            self.flag_fire_change *= -1
            self.inside -= 1
            self.label_inside.configure(text = str(self.inside))

        if self.canvas.coords(self.change_dot)[0] != 380.0:
            self.canvas.move(self.change_dot, 5, 0)
        elif self.canvas.coords(self.change_dot)[1] != 120.0:
            self.canvas.move(self.change_dot, 0, -5)

        if self.canvas.coords(self.change_dot)[1] != 120.0:
            self.canvas.after(20, self.fire_change)
        else:
            self.canvas.delete(self.change_dot)

            self.done += 1
            self.label_done.configure(text = str(self.done))
            self.label_marking.configure(text = "MARKING M = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done]")
            self.flag_fire_change *= -1

    def handle_fire(self):        
        while (self.flag_auto == 1 and self.flag_fire_start != 1 and self.flag_fire_change != 1):
            self.check_deadlock()
            self.fire()
            time.sleep(1.35)

    def fire(self):
        if ((self.is_start_enable() and (not self.is_change_enable())) or
            ((not self.is_start_enable()) and (self.is_change_enable()))):
            if self.is_start_enable():
                self.fire_start()
            elif self.is_change_enable():
                self.fire_change()
        
        elif self.is_start_enable() and (self.is_change_enable()):
            prob = random.random()
            if prob <= 1.0/3:
                self.fire_start()
            elif prob <= 2.0/3:
                self.fire_change()
            else:
                self.fire_start()
                self.fire_change()
    
    def check_deadlock(self):
        if (self.wait == 0 and self.inside == 0):
            print("DEADLOCK")
            self.stop_fire()

    def is_start_enable(self):
        if self.wait > 0:
            return True
        else:
            return False
    
    def is_change_enable(self):
        if self.inside > 0:
            return True
        else:
            return False
    
    def handler(self):
        if self.flag_auto == 1: 
            self.stop_fire()

        if self.flag_fire_change == 1 or self.flag_fire_start == 1: 
            tkinter.messagebox.showwarning('Lỗi', 'Vui lòng chờ, đang ngừng các chuyển tiếp ...')

        if tkinter.messagebox.askokcancel("Quit app ?", "Are you sure to quit"):
            self.isClosed = 1
            self.master.destroy()