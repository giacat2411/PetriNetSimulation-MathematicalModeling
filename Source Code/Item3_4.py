from tkinter import *
import tkinter.messagebox
import threading
import random
import time
from pyvis.network import Network
from pyvis.physics import Physics
from PetriNet import PetriNet

class Item3_4(PetriNet):        
    def createWidgets(self):
        # ----------------------------------------------------------------------------------
        # CREATE GUI
        self.canvas = Canvas(self.master, bg="white", height="550")
        self.canvas.pack()
        self.canvas.grid(row=0, column=0, columnspan=12, sticky=W+E+N+S, padx=3, pady=3)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # CREATE PLACE AND LABEL IT
        self.canvas.create_oval(370, 50, 440, 120) # WAIT
        self.canvas.create_oval(510, 190, 580, 260) # INSIDE
        self.canvas.create_oval(650, 50, 720, 120) # DONE
        self.canvas.create_oval(230, 190, 300, 260) # FREE
        self.canvas.create_oval(510, 330, 580, 400) # BUSY
        self.canvas.create_oval(510, 470, 580, 540) # DOCU

        widget = Label(self.canvas, text='WAIT', bg="white")
        widget.pack()
        self.canvas.create_window(405, 35, window = widget)

        self.label_wait = Label(self.canvas, text = "0", bg="white")
        self.label_wait.pack()
        self.canvas.create_window(405, 85, window = self.label_wait)

        widget = Label(self.canvas, text='INSIDE', bg="white")
        widget.pack()
        self.canvas.create_window(545, 175, window = widget)

        self.label_inside = Label(self.canvas, text = "0", bg="white")
        self.label_inside.pack()
        self.canvas.create_window(545, 225, window = self.label_inside)

        widget = Label(self.canvas, text='DONE', bg="white")
        widget.pack()
        self.canvas.create_window(685, 35, window = widget)

        self.label_done = Label(self.canvas, text = "0", bg="white")
        self.label_done.pack()
        self.canvas.create_window(685, 85, window = self.label_done)

        widget = Label(self.canvas, text='FREE', bg="white")
        widget.pack()
        self.canvas.create_window(265, 175, window = widget)

        self.label_free = Label(self.canvas, text = "0", bg="white")
        self.label_free.pack()
        self.canvas.create_window(265, 225, window = self.label_free)

        widget = Label(self.canvas, text='BUSY', bg="white")
        widget.pack()
        self.canvas.create_window(545, 315, window = widget)

        self.label_busy = Label(self.canvas, text = "0", bg="white")
        self.label_busy.pack()
        self.canvas.create_window(545, 365, window = self.label_busy)

        widget = Label(self.canvas, text='DOCU', bg="white")
        widget.pack()
        self.canvas.create_window(545, 455, window = widget)

        self.label_docu = Label(self.canvas, text = "0", bg="white")
        self.label_docu.pack()
        self.canvas.create_window(545, 505, window = self.label_docu)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # CREATE TRANSITION, ADD USER CLICK AND LABEL IT
        self.canvas.create_rectangle(370, 190, 440, 260, tag="start") # START
        self.canvas.create_rectangle(650, 190, 720, 260, tag="change") # CHANGE
        self.canvas.create_rectangle(230, 470, 300, 540, tag="end") # END

        widget = Label(self.canvas, text='START', bg="white", padx=0, pady=0)
        widget.pack()
        self.canvas.create_window(405, 250, window = widget)

        widget = Label(self.canvas, text='CHANGE', bg="white", padx=0, pady=0)
        widget.pack()
        self.canvas.create_window(685, 250, window = widget)

        widget = Label(self.canvas, text='END', bg="white", padx=0, pady=0)
        widget.pack()
        self.canvas.create_window(265, 530, window = widget)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # FLOW RELATION
        self.canvas.create_line(440, 225, 510, 225, arrow=tkinter.LAST) # START -> INSIDE
        self.canvas.create_line(580, 225, 650, 225, arrow=tkinter.LAST) # INSIDE -> CHANGE
        self.canvas.create_line(405, 120, 405, 190, arrow=tkinter.LAST) # WAIT -> START
        self.canvas.create_line(685, 190, 685, 120, arrow=tkinter.LAST) # CHANGE -> DONE
        self.canvas.create_line(300, 225, 370, 225, arrow=tkinter.LAST) # FREE -> START
        self.canvas.create_line(405, 260, 405, 365) # START -> BUSY
        self.canvas.create_line(405, 365, 510, 365, arrow=tkinter.LAST) # START -> BUSY
        self.canvas.create_line(685, 365, 685, 260, arrow=tkinter.LAST) # BUSY -> CHANGE
        self.canvas.create_line(580, 365, 685, 365) # BUSY -> CHANGE
        self.canvas.create_line(720, 225, 790, 225) # CHANGE -> DOCU
        self.canvas.create_line(790, 225, 790, 505) # CHANGE -> DOCU
        self.canvas.create_line(790, 505, 580, 505, arrow=tkinter.LAST) # CHANGE -> DOCU
        self.canvas.create_line(510, 505, 300, 505, arrow=tkinter.LAST) # DOCU -> END
        self.canvas.create_line(265, 470, 265, 260, arrow=tkinter.LAST) # END -> FREE
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
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

        Label(self.master, text = "WAIT").grid(row = 1, column = 6)
        self.input_wait = Entry(self.master)
        self.input_wait.grid(row = 1, column = 7)

        Label(self.master, text = "INSIDE").grid(row = 1, column = 8)
        self.input_inside = Entry(self.master)
        self.input_inside.grid(row = 1, column = 9)

        Label(self.master, text = "DONE").grid(row = 1, column = 10)
        self.input_done = Entry(self.master)
        self.input_done.grid(row = 1, column = 11)
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
        self.reset_button.grid(row=2, column=3, padx=2, pady=2)

        self.auto_button = Button(self.master, width=16, padx=3, pady=3)
        self.auto_button['text'] = "AUTO FIRE"
        self.auto_button['command'] = self.auto_fire
        self.auto_button.grid(row=2, column=5, padx=2, pady=2)

        self.stop_button = Button(self.master, width=16, padx=3, pady=3)
        self.stop_button['text'] = "STOP FIRE"
        self.stop_button['command'] = self.stop_fire
        self.stop_button.grid(row=2, column=7, padx=2, pady=2)

        self.ts_button = Button(self.master, width=16, padx=3, pady=3)
        self.ts_button['text'] = "TRANSITION SYSTEM"
        self.ts_button['command'] = self.transition_system
        self.ts_button.grid(row=2, column=9, padx=2, pady=2)

        self.firing_sequence_button = Button(self.master, width=16, padx=3, pady=3)
        self.firing_sequence_button['text'] = "FIRING SEQUENCE"
        self.firing_sequence_button['command'] = self.firing_sequence
        self.firing_sequence_button.grid(row=2, column=11, padx=2, pady=2)

        self.canvas.bind("<Button-1>", self.onClick)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # LABEL MARKING
        self.label_marking = Label(self.canvas, text = "MARKING M = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done, "
                                                    + str(self.free) + ".free, " + str(self.busy) + ".busy, "
                                                    + str(self.docu)+ ".docu]" 
                                                , bg="white")
        self.label_marking.pack()
        self.canvas.create_window(490, 10, window = self.label_marking)
        # ----------------------------------------------------------------------------------

    def setup(self):
        print("SETUP\n" + "-"*30)
        self.markings = []
        self.state = 0
        self.transition = 0

        if self.flag_auto == 1:
            tkinter.messagebox.showwarning('L???i', 'Kh??ng th??? SETUP khi ??ang AUTO FIRE !!!')
            print("FAILED\n"  + "-"*30)
        else: 
            if (not (self.input_wait.get().isnumeric() and self.input_inside.get().isnumeric()
                    and self.input_done.get().isnumeric() and self.input_free.get().isnumeric()
                    and self.input_busy.get().isnumeric() and self.input_docu.get().isnumeric())):
                tkinter.messagebox.showwarning('L???i nh???p', 'Vui l??ng nh???p c??c s??? nguy??n kh??ng ??m !!!')
                print("FAILED\n"  + "-"*30)
            else:
                self.free = self.init_free = int(self.input_free.get())
                self.busy = self.init_busy = int(self.input_busy.get())
                self.docu = self.init_docu = int(self.input_docu.get())
                self.wait = self.init_wait = int(self.input_wait.get())
                self.inside = self.init_inside = int(self.input_inside.get())
                self.done = self.init_done = int(self.input_done.get())

                self.label_free.configure(text = str(self.init_free))
                self.label_busy.configure(text = str(self.init_busy))
                self.label_docu.configure(text = str(self.init_docu))
                self.label_wait.configure(text = str(self.init_wait))
                self.label_inside.configure(text = str(self.init_inside))
                self.label_done.configure(text = str(self.init_done))
                self.label_marking.configure(text = "MARKING M_0 = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done, "
                                                    + str(self.free) + ".free, " + str(self.busy) + ".busy, "
                                                    + str(self.docu)+ ".docu]")
                print("SUCCESSFUL")
                print("Initial Marking: M0 = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done, "
                                                    + str(self.free) + ".free, " + str(self.busy) + ".busy, "
                                                    + str(self.docu)+ ".docu]\n"   + "-"*30)
    
    def reset(self):
        print("RESET")
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == "" 
            and self.init_free == "" and self.init_busy == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('L???i', 'Vui l??ng b???m SETUP ????? kh???i t???o MARKING tr?????c khi d??ng c??c ch???c n??ng kh??c!')
            print("FAILED\n"  + "-"*30)

        elif self.flag_auto == 1:
            tkinter.messagebox.showwarning('L???i', 'Kh??ng th??? RESET khi ??ang AUTO FIRE !!!')
            print("FAILED\n"  + "-"*30)

        else:
            self.wait = self.init_wait
            self.inside = self.init_inside
            self.done = self.init_done
            self.free = self.init_free
            self.busy = self.init_busy
            self.docu = self.init_docu

            self.label_wait.configure(text = str(self.init_wait))
            self.label_inside.configure(text = str(self.init_inside))
            self.label_done.configure(text = str(self.init_done))
            self.label_free.configure(text = str(self.init_free))
            self.label_busy.configure(text = str(self.init_busy))
            self.label_docu.configure(text = str(self.init_docu))

            self.label_marking.configure(text = "MARKING M_0 = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done, "
                                                    + str(self.free) + ".free, " + str(self.busy) + ".busy, "
                                                    + str(self.docu)+ ".docu]")
            print("SUCCESSFUL")
            print("Initial Marking: M0 = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done, "
                                                    + str(self.free) + ".free, " + str(self.busy) + ".busy, "
                                                    + str(self.docu)+ ".docu]\n"   + "-"*30)

    def auto_fire(self):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == "" 
            and self.init_free == "" and self.init_busy == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('L???i', 'Vui l??ng b???m SET ????? kh???i t???o Marking ban ?????u !!!')
        elif self.flag_auto == 1: pass
        else:
            self.flag_auto *= -1

            print("AUTO FIRE MODE ON\n" + "-"*30)

            self.thread_auto_fire = threading.Thread(target=self.handle_fire)
            self.thread_auto_fire.start()   
    
    def stop_fire(self):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == ""):
            tkinter.messagebox.showwarning('L???i', 'Vui l??ng b???m SET ????? kh???i t???o MARKING tr?????c khi d??ng c??c ch???c n??ng kh??c!')
        elif self.flag_auto == -1: pass
        else:
            self.flag_auto *= -1
            print("AUTO FIRE MODE OFF\n" + "-"*30)

    def transition_system(self):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == "" 
            and self.init_free == "" and self.init_busy == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('L???i', 'Vui l??ng b???m SET ????? kh???i t???o Marking ban ?????u !!!')
        else:
            # FORM MARKING: [x.wait, y.inside, z.done, a.free, b.busy, c.docu]
            print("TRANSITION SYSTEM")
            self.markings = []
            self.state = 0
            self.transition = 0
            self.graph = Network(directed = True)

            current_marking = [self.init_free, self.init_busy, self.init_docu, 
                                self.init_wait, self.init_inside, self.init_done]
            self.markings.append(current_marking)
            self.graph.add_node(0, label=str("[" + str(current_marking[3]) + ", " 
                                    + str(current_marking[4]) + ", " + str(current_marking[5]) + ", " 
                                    + str(current_marking[0]) + ", " 
                                    + str(current_marking[1]) + ", " + str(current_marking[2])+ "]"))
            self.state += 1

            self.find_transition_relation(self.markings[0])

            self.graph.show_buttons(filter_='physics')
            self.graph.show('Transition System.html')
            
            print(str(self.state) + " states")
            print(str(self.transition) + " transitions\n" + "-"*30)

    def find_transition_relation(self, marking): 
        near = self.find_near_marking(marking)
        for i in range (0, len(near)):
            self.find_transition_relation(near[i])
    
    def find_near_marking(self, current_marking):
        near = []
        if (current_marking[0] > 0 and current_marking[3] > 0):
            self.transition += 1
            marking = [current_marking[0] - 1, current_marking[1] + 1, current_marking[2]   
                      ,current_marking[3] - 1, current_marking[4] + 1, current_marking[5]]

            node = str("[" + str(marking[3]) + ", " 
                                    + str(marking[4]) + ", " + str(marking[5]) + ", " 
                                    + str(marking[0]) + ", " 
                                    + str(marking[1]) + ", " + str(marking[2])+ "]")

            if not (marking in self.markings):
                self.graph.add_node(len(self.markings), label = node)
                near.append(marking)
                self.markings.append(marking)
                self.state += 1

            self.graph.add_edge(self.markings.index(current_marking), self.markings.index(marking), label = "START")

            print("[" + str(current_marking[0]) + ".free, " + str(current_marking[1]) + ".busy, " 
                      + str(current_marking[2]) + ".docu, "
                      + str(current_marking[3]) + ".wait, " + str(current_marking[4]) + ".inside, " 
                      + str(current_marking[5]) + ".done]"
                      + "; START> " 
                      + "[" + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                      + str(marking[2]) + ".docu, "
                      + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                      + str(marking[5]) + ".done]")
                 
        if (current_marking[1] > 0 and current_marking[4] > 0):
            self.transition += 1
            marking = [current_marking[0], current_marking[1] - 1, current_marking[2] + 1 
                      ,current_marking[3], current_marking[4] - 1, current_marking[5] + 1]

            node = str("[" + str(marking[3]) + ", " 
                                    + str(marking[4]) + ", " + str(marking[5]) + ", " 
                                    + str(marking[0]) + ", " 
                                    + str(marking[1]) + ", " + str(marking[2])+ "]")

            if not (marking in self.markings):
                self.graph.add_node(len(self.markings), label = node)
                near.append(marking)
                self.markings.append(marking)
                self.state += 1

            self.graph.add_edge(self.markings.index(current_marking), self.markings.index(marking), label = "CHANGE")

            print("[" + str(current_marking[0]) + ".free, " + str(current_marking[1]) + ".busy, " 
                      + str(current_marking[2]) + ".docu, "
                      + str(current_marking[3]) + ".wait, " + str(current_marking[4]) + ".inside, " 
                      + str(current_marking[5]) + ".done]"
                      + "; CHANGE> " 
                      + "[" + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                      + str(marking[2]) + ".docu, "
                      + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                      + str(marking[5]) + ".done]")
            
        if (current_marking[2] > 0):
            self.transition += 1
            marking = [current_marking[0] + 1, current_marking[1], current_marking[2] - 1 
                      ,current_marking[3], current_marking[4], current_marking[5]]

            node = str("[" + str(marking[3]) + ", " 
                                    + str(marking[4]) + ", " + str(marking[5]) + ", " 
                                    + str(marking[0]) + ", " 
                                    + str(marking[1]) + ", " + str(marking[2])+ "]")

            if not (marking in self.markings):
                self.graph.add_node(len(self.markings), label = node)
                near.append(marking)
                self.markings.append(marking)
                self.state += 1

            self.graph.add_edge(self.markings.index(current_marking), self.markings.index(marking), label = "END")

            print("[" + str(current_marking[0]) + ".free, " + str(current_marking[1]) + ".busy, " 
                      + str(current_marking[2]) + ".docu, "
                      + str(current_marking[3]) + ".wait, " + str(current_marking[4]) + ".inside, " 
                      + str(current_marking[5]) + ".done]"
                      + "; END> " 
                      + "[" + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                      + str(marking[2]) + ".docu, "
                      + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                      + str(marking[5]) + ".done]")
        return near

    def firing_sequence(self):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == "" 
            and self.init_free == "" and self.init_busy == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('L???i', 'Vui l??ng b???m SET ????? kh???i t???o Marking ban ?????u !!!')
        else:
            # FORM MARKING: [x.wait, y.inside, z.done, a.free, b.busy, c.docu]
            print("FIRING SEQUENCE")
            self.markings = []
            sequence = ""
            self.nums_sequence = 0

            current_marking = [self.init_free, self.init_busy, self.init_docu, self.init_wait, self.init_inside, self.init_done]
            self.markings.append(current_marking)

            self.find_firing_sequence(self.markings[0], sequence)
            print("Initial Marking: M0 = [" + str(self.init_wait) + ".wait, " 
                                                    + str(self.init_inside) + ".inside, " + str(self.init_done) +".done, "
                                                    + str(self.init_free) + ".free, " + str(self.init_busy) + ".busy, "
                                                    + str(self.init_docu)+ ".docu]\n"   + "-"*30)
            print(str(self.nums_sequence) + " firing sequence\n" + "-"*30)

    def find_firing_sequence(self, current_marking, sequence):
        next_sequence = self.find_next_sequence(current_marking, sequence)
        for i in range (0, len(next_sequence["next"])):
            self.find_firing_sequence(next_sequence["next"][i], next_sequence["firing"][i])

    def find_next_sequence(self, current_marking, sequence):
        next = []
        firing = []

        if (current_marking[0] > 0 and current_marking[3] > 0):
            marking = [current_marking[0] - 1, current_marking[1] + 1, current_marking[2]   
                      ,current_marking[3] - 1, current_marking[4] + 1, current_marking[5]]
            self.nums_sequence += 1

            if sequence == "":
                print("[M0 ; ("+ sequence + "START)> " 
                        + "[" + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                        + str(marking[5]) + ".done, "
                        + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                        + str(marking[2]) + ".docu]")
            else:
                print("[M0 ; ("+ sequence + ", START)> " 
                        + "[" + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                        + str(marking[5]) + ".done, "
                        + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                        + str(marking[2]) + ".docu]")
            
            if (marking in self.markings): pass
            else: 
                next.append(marking)

                if sequence == "": 
                    firing.append(sequence + "START")
                else:
                    firing.append(sequence + ", START")

                self.markings.append(marking)

        if (current_marking[1] > 0 and current_marking[4] > 0):
            self.nums_sequence += 1
            marking = [current_marking[0], current_marking[1] - 1, current_marking[2] + 1 
                      ,current_marking[3], current_marking[4] - 1, current_marking[5] + 1]    

            if sequence == "":
                print("[M0 ; ("+ sequence + "CHANGE)> " 
                        + "[" + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                        + str(marking[5]) + ".done, "
                        + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                        + str(marking[2]) + ".docu]")
            else:
                print("[M0 ; ("+ sequence + ", CHANGE)> " 
                        + "[" + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                        + str(marking[5]) + ".done, "
                        + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                        + str(marking[2]) + ".docu]")
            
            if (marking in self.markings): pass
            else: 
                next.append(marking)

                if sequence == "": 
                    firing.append(sequence + "CHANGE")
                else:
                    firing.append(sequence + ", CHANGE")

                self.markings.append(marking)

        if (current_marking[2] > 0):
            self.nums_sequence += 1
            marking = [current_marking[0] + 1, current_marking[1], current_marking[2] - 1 
                      ,current_marking[3], current_marking[4], current_marking[5]]    

            if sequence == "":
                print("[M0 ; ("+ sequence + "END)> " 
                        + "[" + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                        + str(marking[5]) + ".done, "
                        + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                        + str(marking[2]) + ".docu]")
            else:
                print("[M0 ; ("+ sequence + ", END)> " 
                        + "[" + str(marking[3]) + ".wait, " + str(marking[4]) + ".inside, " 
                        + str(marking[5]) + ".done, "
                        + str(marking[0]) + ".free, " + str(marking[1]) + ".busy, " 
                        + str(marking[2]) + ".docu]")
            
            if (marking in self.markings): pass
            else: 
                next.append(marking)

                if sequence == "": 
                    firing.append(sequence + "END")
                else:
                    firing.append(sequence + ", END")

                self.markings.append(marking)

        return { "next": next, "firing": firing }

    def onClick(self, event):
        if (self.init_wait == "" and self.init_inside == "" and self.init_done == "" 
            and self.init_free == "" and self.init_busy == "" and self.init_docu == ""):
            tkinter.messagebox.showwarning('L???i', 'Vui l??ng b???m SET ????? kh???i t???o Marking ban ?????u !!!')
        elif (self.flag_auto == 1):
            tkinter.messagebox.showwarning('L???i', 'Vui l??ng t???t AUTO FIRE ????? c?? th??? k??ch ho???t theo ?? mu???n !!!')
        else:
            item = self.canvas.find_closest(event.x, event.y)
            tag = self.canvas.itemcget(item, "tag")
            if tag == "start" and self.flag_fire_start != 1:
                if self.wait != 0 and self.free != 0:
                    print("FIRING START!!!")
                    self.fire_start()
                else:
                    tkinter.messagebox.showwarning('L???i', 'Chuy???n ti???p START kh??ng t??ch c???c!!!')

            elif tag == "change" and self.flag_fire_change != 1:
                if self.inside != 0 and self.busy != 0:
                    print("FIRING CHANGE!!!")
                    self.fire_change()
                else:
                    tkinter.messagebox.showwarning('L???i', 'Chuy???n ti???p CHANGE kh??ng t??ch c???c!!!')
            
            elif tag == "end" and self.flag_fire_end != 1:
                if self.docu != 0:
                    print("FIRING END!!!")
                    self.fire_end()
                else:
                    tkinter.messagebox.showwarning('L???i', 'Chuy???n ti???p END kh??ng t??ch c???c!!!')

    def fire_start(self):
        if self.flag_fire_start == -1:
            self.start_dot_1 = self.canvas.create_oval(300, 220, 310, 230, fill="black")
            self.start_dot_2 = self.canvas.create_oval(400, 120, 410, 130, fill="black")

            self.flag_fire_start *= -1
            self.wait -= 1
            self.free -= 1

            self.label_wait.configure(text = str(self.wait))
            self.label_free.configure(text = str(self.free))

        if self.canvas.coords(self.start_dot_1)[0] < 500.0:
            self.canvas.move(self.start_dot_1, 100.0/24, 0)

        if self.canvas.coords(self.start_dot_2)[1] < 219.0:
            self.canvas.move(self.start_dot_2, 0, 100.0/24)
        elif self.canvas.coords(self.start_dot_2)[1] < 355.0:
            self.canvas.move(self.start_dot_2, 0, 10)
        else:
            self.canvas.move(self.start_dot_2, 10, 0)
        
        if self.canvas.coords(self.start_dot_2)[0] <= 500.0:
            self.canvas.after(20, self.fire_start)
        else:
            self.canvas.delete(self.start_dot_1)
            self.canvas.delete(self.start_dot_2)

            self.inside += 1
            self.busy +=1

            self.label_inside.configure(text = str(self.inside))
            self.label_busy.configure(text = self.busy)

            self.label_marking.configure(text = "MARKING M = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done, "
                                                    + str(self.free) + ".free, " + str(self.busy) + ".busy, "
                                                    + str(self.docu)+ ".docu]")
            
            self.flag_fire_start *= -1

    def fire_change(self):
        if self.flag_fire_change == -1:            
            self.change_dot_1 = self.canvas.create_oval(580, 220, 590, 230, fill="black")
            self.change_dot_2 = self.canvas.create_oval(580, 360, 590, 370, fill="black")

            self.flag_fire_change *= -1
            self.inside -= 1
            self.busy -=1

            self.label_inside.configure(text = str(self.inside))
            self.label_busy.configure(text = str(self.busy))

        if (self.canvas.coords(self.change_dot_1)[0] < 680.0 
            and self.canvas.coords(self.change_dot_1)[1] == 220.0):
            self.canvas.move(self.change_dot_1, 100.0/8, 0)
        elif (self.canvas.coords(self.change_dot_1)[0] < 785.0
            and self.canvas.coords(self.change_dot_1)[1] == 220.0):
            self.canvas.move(self.change_dot_1, 105.0/8, 0)
        elif self.canvas.coords(self.change_dot_1)[1] < 500.0:
            self.canvas.move(self.change_dot_1, 0, 280.0/16)
        elif self.canvas.coords(self.change_dot_1)[0] > 580.0:
            self.canvas.move(self.change_dot_1, -205.0/16, 0)

        if self.canvas.coords(self.change_dot_2)[0] < 680.0:
            self.canvas.move(self.change_dot_2, 100.0/4, 0)       
        elif self.canvas.coords(self.change_dot_2)[1] > 220.0:
            self.canvas.move(self.change_dot_2, 0, -140.0/4)        
        elif self.canvas.coords(self.change_dot_2)[1] > 120.0:
            self.canvas.move(self.change_dot_2, 0, -100.0/40)


        if (self.canvas.coords(self.change_dot_1)[0] != 580.0 
            or self.canvas.coords(self.change_dot_1)[1] != 500.0):
            self.canvas.after(20, self.fire_change)
        else:
            self.canvas.delete(self.change_dot_1)
            self.canvas.delete(self.change_dot_2)

            self.done += 1
            self.docu += 1

            self.label_done.configure(text = str(self.done))
            self.label_docu.configure(text = str(self.docu))

            self.label_marking.configure(text = "MARKING M = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done, "
                                                    + str(self.free) + ".free, " + str(self.busy) + ".busy, "
                                                    + str(self.docu)+ ".docu]")
            
            self.flag_fire_change *= -1

    def fire_end(self):
        if self.flag_fire_end == -1: 
            self.end_dot = self.canvas.create_oval(510, 500, 500, 510, fill="black")

            self.flag_fire_end *= -1
            self.docu -= 1

            self.label_docu.configure(text = str(self.docu))

        if self.canvas.coords(self.end_dot)[0] > 260.0:
            self.canvas.move(self.end_dot, -10, 0)
        elif self.canvas.coords(self.end_dot)[1] > 260.0:
            self.canvas.move(self.end_dot, 0, -10)

        if self.canvas.coords(self.end_dot)[1] != 260.0:
                self.canvas.after(20, self.fire_end)
        else:
            self.canvas.delete(self.end_dot)

            self.free += 1
            self.label_free.configure(text = str(self.free))

            self.label_marking.configure(text = "MARKING M = [" + str(self.wait) + ".wait, " 
                                                    + str(self.inside) + ".inside, " + str(self.done) +".done, "
                                                    + str(self.free) + ".free, " + str(self.busy) + ".busy, "
                                                    + str(self.docu)+ ".docu]")
            
            self.flag_fire_end *= -1

    def handle_fire(self):        
        while (self.flag_auto == 1 and self.flag_fire_start != 1 
               and self.flag_fire_change != 1 and self.flag_fire_end != 1):
            self.check_deadlock()
            self.fire()
            time.sleep(1.8)

    def fire(self):
        if ((self.is_start_enable() and (not self.is_change_enable()) and (not self.is_end_enable())) or
            ((not self.is_start_enable()) and (self.is_change_enable()) and (not self.is_end_enable())) or
            ((not self.is_start_enable()) and (not self.is_change_enable()) and (self.is_end_enable()))):
            if self.is_start_enable():
                self.fire_start()
            elif self.is_change_enable():
                self.fire_change()
            elif self.is_end_enable():
                self.fire_end()
        
        elif self.is_start_enable() and (self.is_change_enable()) and (not self.is_end_enable()):
            prob = random.random()
            if prob <= 1.0/3:
                self.fire_start()
            elif prob <= 2.0/3:
                self.fire_change()
            else:
                self.fire_start()
                self.fire_change()
        
        elif self.is_start_enable() and (not self.is_change_enable()) and (self.is_end_enable()):
            prob = random.random()
            if prob <= 1.0/3:
                self.fire_start()
            elif prob <= 2.0/3:
                self.fire_end()
            else:
                self.fire_start()
                self.fire_end()
        
        elif (not self.is_start_enable()) and (self.is_change_enable()) and (self.is_end_enable()):
            prob = random.random()
            if prob <= 1.0/3:
                self.fire_end()
            elif prob <= 2.0/3:
                self.fire_change()
            else:
                self.fire_end()
                self.fire_change()

        elif self.is_start_enable() and self.is_change_enable() and self.is_end_enable():
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
        if (not self.is_start_enable()) and (not self.is_change_enable()) and (not self.is_end_enable()):
            print("DEADLOCK")
            self.stop_fire()

    def is_start_enable(self):
        if self.wait > 0 and self.free > 0:
            return True
        else:
            return False
    
    def is_change_enable(self):
        if self.inside > 0 and self.busy > 0:
            return True
        else:
            return False
    
    def is_end_enable(self):
        if self.docu > 0:
            return True
        else: 
            return False

    def handler(self):
        if self.flag_auto == 1: 
            self.stop_fire()
            
        if self.flag_fire_change == 1 or self.flag_fire_end == 1 or self.flag_fire_start == 1: 
            tkinter.messagebox.showwarning('L???i', 'Vui l??ng ch???, ??ang ng???ng c??c chuy???n ti???p ...')

        if tkinter.messagebox.askokcancel("Quit app ?", "Are you sure to quit"):
            self.isClosed = 1
            self.master.destroy()