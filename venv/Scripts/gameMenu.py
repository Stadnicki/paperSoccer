from tkinter import *
import gameWindow
from resultsFile import *


class HintEntry(Text):
    def __init__(self, master=None, hint=''):
        super().__init__(master, bd = 5, height=1, font=("Georgia", 25), bg='black',
                         fg='white', selectbackground='black', insertbackground='white',
                         padx=10, pady=10)
        self.master = master
        self.hint = hint

        self.tag_configure("center", justify='center')

        self.bind('<FocusIn>', lambda x: self.focus_in())
        self.bind('<FocusOut>', lambda x: self.focus_out())
        self.bind('<Key>', lambda x: self.center_nick())

        self.insert_hint()

    def insert_hint(self):
        self.insert(END, self.hint)
        self.tag_add("center", "1.0", "end")

    def focus_in(self):
        print('focus in')
        if self.get("1.0", END).strip() == self.hint:
            self.delete('1.0', END)

    def center_nick(self):
        self.tag_add('center', '1.0', 'end')

    def focus_out(self):
        print('focus out')
        if self.get("1.0", END).strip() == self.hint or self.get("1.0", END).strip()  == '':
            self.insert_hint()

    def get_name(self):
        return self.get("1.0", END).strip()


class Menu(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.init_window()
        self.res_file = ResultsFile('results')
        self.first_player = HintEntry(self, 'First player')
        self.first_player.grid(row=0, column=0, pady=(0, 5))
        self.second_player = HintEntry(self, 'Second player')
        self.second_player.grid(row=1, column=0, pady=(0, 5))
        self.start_button = Button(self, text='START GAME', height=1, bd=5, command=self.start_game, bg='darkgreen',
                                    fg='white',  font=("Georgia", 25), activebackground='green')
        self.start_button.grid(row=3, column=0, sticky=E+W, pady=(0, 5))
        self.results_button = Button(self, text='RESULTS', height=1, bd=5, command=self.show_results, bg='darkblue',
                                    fg='white',  font=("Georgia", 25), activebackground='dodgerblue')
        self.results_button.grid(row=4, column=0, sticky=E + W, pady=(0, 5))
        self.exit_button = Button(self, text='EXIT GAME', height=1, bd=5, fg='white', command=self.master.destroy,
                                  bg='darkred', font=('Georgia', 25), activebackground='red')
        self.exit_button.grid(row=5, column=0, sticky=E+W)
        self.first_name = ''
        self.second_name = ''

    def start_game(self):
        self.first_name = self.first_player.get_name()
        self.second_player = self.second_player.get_name()
        print('nicki ', self.first_name, self.second_player)
        self.master.destroy()
        if self.first_name == '':
            self.first_name = 'First player'
        if self.second_name == '':
            self.second_name = 'Second player'
        gameWindow.main_loop((self.first_name, self.second_player))

    def init_window(self):
        self.master.title("Paper Soccer")
        self.master.minsize(width=400, height=375)
        self.master.maxsize(1600, 299)
        self.pack()
        self.grid_columnconfigure(0, weight=1)
        self.master.geometry('400x375')

    def show_results(self):
        res_frame = Toplevel()
        res_frame.title("RESULTS")
        res_frame.geometry('400x375')
        res_field = Text(res_frame, height=15, width=55, wrap="word")
        res_field.insert('1.0', self.res_file.get_result())
        res_field.config(state=DISABLED)
        scr = Scrollbar(res_frame)
        scr.config(command=res_field.yview)
        res_field.config(yscrollcommand=scr.set)
        scr.pack(side="right", fill="y", expand=False)
        res_field.pack(side="left", fill="both", expand=True)

def main():
    root = Tk()
    Menu(root)
    root.mainloop()


if __name__ == "__main__":
    main()

