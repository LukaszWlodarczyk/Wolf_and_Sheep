from src.Simulation_logic import Wolf, Sheep
import tkinter as tk
from tkinter import messagebox as msb
from tkinter import filedialog
from tkinter import ttk
import time


import json


class Interface:
    def __init__(self):
        self.__START_SIZE = 5
        self.__AMOUNT_OF_SHEEP = 0
        self.__AMOUNT_OF_ROUNDS = 500
        self.__INIT_POS_LIMIT = 500.0
        self.__SHEEP_MOVE_DISTANCE = 10
        self.__WOLF_MOVE_DISTANCE = 25
        self.SIZE = self.__INIT_POS_LIMIT * 1.5
        self.start_flag = False
        self.__PAUSE_DURATION = 1.0
        Sheep.max_x = self.SIZE
        Sheep.max_y = self.SIZE
        Wolf.max_x = self.SIZE
        Wolf.max_y = self.SIZE
        self.wolf = Wolf(1)
        self.sheep_list = []
        self.sheep_list_for_gui = []
        # Scene settings
        self.window = tk.Tk()
        self.window.title("Wilk i Owce")
        self.window.geometry("1400x900")
        self.window.resizable(False, False)
        self.frame = tk.Frame(self.window, width=self.SIZE+100, height=self.SIZE+100)
        self.frame.pack(side="left", padx="50")
        self.simulation = tk.Canvas(self.frame, width=self.SIZE, height=self.SIZE)
        self.simulation.pack(side="left", fill="both", padx="25", pady="25")
        self.board = self.simulation.create_rectangle((0, 0, self.SIZE, self.SIZE), fill="#008000")
        self.wolf_gui = self.simulation.create_oval(self.wolf.get_pos_x() - self.__START_SIZE,
                                                    self.wolf.get_pos_y() - self.__START_SIZE,
                                                    self.wolf.get_pos_x() + self.__START_SIZE,
                                                    self.wolf.get_pos_y() + self.__START_SIZE, fill="red")

        self.simulation_menu = tk.Frame(self.window, width=self.SIZE+50, height=self.SIZE+50)
        self.simulation_menu.pack(padx="50", pady="75")

        self.main_menu = tk.Menu(self.window)
        self.window.config(menu=self.main_menu)

        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)

        self.settings_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Settings", command=self.set_settings)

        # Buttons and Labels
        self.step_btn = tk.Button(self.simulation_menu, text="STEP", bg="blue", fg="white", width="100",
                                  command=self.make_step)
        self.step_btn.pack()
        self.reset_btn = tk.Button(self.simulation_menu, text="RESET", bg="red", fg="white", width="100",
                                   command=self.reset)
        self.reset_btn.pack()
        self.start_btn = tk.Button(self.simulation_menu, text="START", bg="yellow", fg="black", width="100",
                                   command=self.start_simulation)
        self.start_btn.pack()
        self.string_to_counter = tk.StringVar()
        self.string_to_counter.set("Dodaj owce i nacisnij step aby zaczac gre")
        self.counter = tk.Label(self.simulation_menu, textvariable=self.string_to_counter)
        self.counter.pack()
        self.zoom = tk.Scale(self.frame, from_=1, to=30, command=self.zooming)
        self.zoom.set(5)
        self.zoom.pack()

        # Actions
        self.simulation.bind("<Button-3>", self.move_wolf)
        self.simulation.bind("<Button-1>", self.spawn_sheep)

    def draw_wolf(self, size_of_wolf):
        self.simulation.delete(self.wolf_gui)
        self.wolf_gui = self.simulation.create_oval(self.wolf.get_pos_x() - size_of_wolf,
                                                    self.wolf.get_pos_y() - size_of_wolf,
                                                    self.wolf.get_pos_x() + size_of_wolf,
                                                    self.wolf.get_pos_y() + size_of_wolf, fill="red")

    def draw_sheep(self, size_of_sheep):
        for sheep in self.sheep_list_for_gui:
            self.simulation.delete(sheep)
        self.sheep_list_for_gui = []
        for sheep in self.sheep_list:
            self.sheep_list_for_gui.append(
                simulation.create_oval(sheep.get_pos_x() - size_of_sheep,
                                       sheep.get_pos_y() - size_of_sheep,
                                       sheep.get_pos_x() + size_of_sheep,
                                       sheep.get_pos_y() + size_of_sheep, fill="blue")
            )

    def zooming(self, event):
        self.draw_wolf(self.zoom.get())
        self.draw_sheep(self.zoom.get())

    def get_init_pos_limit(self):
        return self.__INIT_POS_LIMIT

    def get_sheep_move_distace(self):
        return self.__SHEEP_MOVE_DISTANCE

    def get_wolf_move_distance(self):
        return self.__WOLF_MOVE_DISTANCE

    def set_amount_of_sheep(self, nr):
        self.__AMOUNT_OF_SHEEP = nr

    def set_amount_of_rounds(self, nr):
        self.__AMOUNT_OF_ROUNDS = nr

    def set_init_pos_limit(self, nr):
        self.__INIT_POS_LIMIT = nr

    def set_sheep_move_distance(self, nr):
        self.__SHEEP_MOVE_DISTANCE = nr

    def set_wolf_move_distance(self, nr):
        self.__WOLF_MOVE_DISTANCE = nr

    def create_wolf(self):
        self.wolf = Wolf(self.__WOLF_MOVE_DISTANCE)

    def create_sheep(self):
        sheep = Sheep(len(self.sheep_list), self.__INIT_POS_LIMIT, self.__SHEEP_MOVE_DISTANCE)
        self.sheep_list.append(sheep)

    def one_step(self):
        for sheep in self.sheep_list:
            sheep.move_sheep()

        target = self.wolf.choose_sheep(self.sheep_list)

        if self.wolf.calculate_distance_to_sheep(target) <= self.wolf.get_distance():
            self.wolf.attack(target)
            tmp = self.sheep_list.index(target)
            self.sheep_list.remove(target)
            self.sheep_list_for_gui.remove(self.sheep_list_for_gui[tmp])
            msb.showinfo("Info", "Owca nr: " + str(target.get_nr()) + " zostala zjedzona")
        else:
            self.wolf.chase_target(target)

    def move_wolf(self, event):
        simulation.move(self.wolf_gui, -self.wolf.get_pos_x(), -self.wolf.get_pos_y())
        simulation.move(self.wolf_gui, event.x, event.y)
        self.wolf.set_pos_x(event.x)
        self.wolf.set_pos_y(event.y)

    def spawn_sheep(self, event):
        self.create_sheep()
        self.sheep_list[-1].set_pos_x(event.x)
        self.sheep_list[-1].set_pos_y(event.y)
        self.sheep_list_for_gui.append(simulation.create_oval(self.sheep_list[-1].get_pos_x() - self.zoom.get(),
                                                              self.sheep_list[-1].get_pos_y() - self.zoom.get(),
                                                              self.sheep_list[-1].get_pos_x() + self.zoom.get(),
                                                              self.sheep_list[-1].get_pos_y() + self.zoom.get(),
                                                              fill="blue"))

    def make_step(self):
        if len(self.sheep_list_for_gui) == 0:
            msb.showerror("Blad", "Nie ma zadnej zywej owcy!")
        else:
            for i in range(len(self.sheep_list_for_gui)):
                simulation.move(self.sheep_list_for_gui[i], -self.sheep_list[i].get_pos_x(),
                                -self.sheep_list[i].get_pos_y())
            simulation.move(self.wolf_gui, -self.wolf.get_pos_x(), -self.wolf.get_pos_y())
            self.one_step()
            for i in range(len(self.sheep_list_for_gui)):
                simulation.move(self.sheep_list_for_gui[i], self.sheep_list[i].get_pos_x(),
                                self.sheep_list[i].get_pos_y())

            simulation.move(self.wolf_gui, self.wolf.get_pos_x(), self.wolf.get_pos_y())
            self.string_to_counter.set("Pozostalo zywych owiec: " + str(len(self.sheep_list_for_gui)))

    def reset(self):
        self.simulation.delete('all')
        self.board = self.simulation.create_rectangle((0, 0, self.SIZE, self.SIZE), fill="#008000")
        self.draw_wolf(self.zoom.get())
        self.simulation.bind("<Button-3>", self.move_wolf)
        self.simulation.bind("<Button-1>", self.spawn_sheep)
        self.sheep_list_for_gui = []
        self.sheep_list = []
        self.simulation.move(self.wolf_gui, -self.wolf.get_pos_x(), -self.wolf.get_pos_y())
        self.simulation.move(self.wolf_gui, self.SIZE / 2, self.SIZE / 2)
        self.wolf.set_pos_x(self.SIZE / 2)
        self.wolf.set_pos_y(self.SIZE / 2)
        self.string_to_counter.set("Dodaj owce i nacisnij step aby zaczac gre")

    def open(self):
        file_name = filedialog.askopenfilename(initialdir=".", title="Select file",
                                               filetypes=(("json files", "*.json"), ("all files", "*.*")))
        tmp = {}
        with open(file_name, 'r') as file:
            tmp = json.load(file)
        self.simulation.delete('all')
        a, b = tmp["wolf"]
        self.wolf.set_pos_x(a)
        self.wolf.set_pos_y(b)
        self.board = self.simulation.create_rectangle((0, 0, self.SIZE, self.SIZE), fill="#008000")
        self.draw_wolf(self.zoom.get())
        self.simulation.bind("<Button-3>", self.move_wolf)
        self.simulation.bind("<Button-1>", self.spawn_sheep)
        self.sheep_list_for_gui = []
        self.sheep_list = []
        self.string_to_counter.set("Dodaj owce i nacisnij step aby zaczac gre")
        for key in tmp:
            if key == "wolf":
                continue
            a, b = tmp[key]
            self.create_sheep()
            self.sheep_list[-1].set_pos_x(a)
            self.sheep_list[-1].set_pos_y(b)
            self.sheep_list[-1].set_nr(key)
            self.sheep_list_for_gui.append(simulation.create_oval(self.sheep_list[-1].get_pos_x() - self.zoom.get(),
                                                                  self.sheep_list[-1].get_pos_y() - self.zoom.get(),
                                                                  self.sheep_list[-1].get_pos_x() + self.zoom.get(),
                                                                  self.sheep_list[-1].get_pos_y() + self.zoom.get(),
                                                                  fill="blue"))

    def save(self):
        file_name = filedialog.asksaveasfilename(initialdir=".", title="Select file",
                                                 filetypes=(("json files", "*.json"), ("all files", "*.*")))
        tmp = {}
        with open(file_name, 'w') as file:
            tmp["wolf"] = [self.wolf.get_pos_x(), self.wolf.get_pos_y()]
            for sheep in self.sheep_list:
                tmp[sheep.get_nr()] = [sheep.get_pos_x(), sheep.get_pos_y()]
            json.dump(tmp, file)

    def exit(self):
        self.window.quit()
        self.window.destroy()
        exit()

    def set_settings(self):
        def set_wolf_color(event):
            self.simulation.itemconfig(self.wolf_gui, fill=colors_list_for_wolf.get())

        def set_sheep_color(event):
            for sheep in self.sheep_list_for_gui:
                self.simulation.itemconfig(sheep, fill=colors_list_for_sheep.get())

        def set_background_color(event):
            self.simulation.itemconfig(self.board, fill=colors_list_for_background.get())

        def set_pause(event):
            self.__PAUSE_DURATION = float(values_list_for_pause.get())

        settings_window = tk.Toplevel(self.window)
        settings_window.title("Settings")
        settings_window.geometry("300x300")
        settings_window.resizable(False, False)
        label_top_for_wolf = tk.Label(settings_window, text="Wolf color:")
        label_top_for_wolf.pack(pady=10)
        colors_list_for_wolf = ttk.Combobox(settings_window, values=[
            "red",
            "black",
            "brown"])
        colors_list_for_wolf.current(0)
        colors_list_for_wolf.pack()
        colors_list_for_wolf.bind("<<ComboboxSelected>>", set_wolf_color)

        label_top_for_sheep = tk.Label(settings_window, text="Sheep color:")
        label_top_for_sheep.pack(pady=10)
        colors_list_for_sheep = ttk.Combobox(settings_window, values=[
            "blue",
            "pink",
            "gray"])
        colors_list_for_sheep.current(0)
        colors_list_for_sheep.pack()
        colors_list_for_sheep.bind("<<ComboboxSelected>>", set_sheep_color)

        label_top_for_background = tk.Label(settings_window, text="Background color:")
        label_top_for_background.pack(pady=10)
        colors_list_for_background = ttk.Combobox(settings_window, values=[
            "green",
            "yellow",
            "white"])
        colors_list_for_background.current(0)
        colors_list_for_background.pack()
        colors_list_for_background.bind("<<ComboboxSelected>>", set_background_color)

        label_top_for_pause = tk.Label(settings_window, text="Pause duration:")
        label_top_for_pause.pack(pady=10)
        values_list_for_pause = ttk.Combobox(settings_window, values=[
            0.5,
            1,
            1.5,
            2])
        if self.__PAUSE_DURATION == 0.5:
            index = 0
        elif self.__PAUSE_DURATION == 2:
            index = 3
        elif self.__PAUSE_DURATION == 1.5:
            index = 2
        else:
            index = 1
        values_list_for_pause.current(int(index))
        values_list_for_pause.pack()
        values_list_for_pause.bind("<<ComboboxSelected>>", set_pause)

    def start_simulation(self):
        if self.start_btn['text'] == "START":
            if not len(self.sheep_list):
                self.make_step()
            else:
                self.start_btn.configure(text="STOP")
                self.simulation.unbind('<Button-3>')
                self.simulation.unbind('<Button-1>')
                self.step_btn['state'] = "disabled"
                self.reset_btn['state'] = "disabled"
                tmp = self.__AMOUNT_OF_ROUNDS
                self.start_flag = True
                while tmp > 0 and len(self.sheep_list) > 0 and self.start_flag:
                    self.make_step()
                    self.window.update()
                    time.sleep(self.__PAUSE_DURATION)
                    tmp -= 1
                self.step_btn['state'] = "normal"
                self.reset_btn['state'] = "normal"
                self.simulation.bind("<Button-3>", self.move_wolf)
                self.simulation.bind("<Button-1>", self.spawn_sheep)
                self.start_flag = False
                self.start_btn.configure(text="START")
        else:
            self.start_btn.configure(text="START")
            self.step_btn['state'] = "normal"
            self.reset_btn['state'] = "normal"
            self.simulation.bind("<Button-3>", self.move_wolf)
            self.simulation.bind("<Button-1>", self.spawn_sheep)
            self.start_flag = False


if __name__ == '__main__':
    interface = Interface()
    interface.create_wolf()
    simulation = interface.simulation

    tk.mainloop()
