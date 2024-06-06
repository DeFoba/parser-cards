from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry

class App(CTk):
    def __init__(self):
        super().__init__()

        self.geometry('600x400')
        self.title('GUI')

    def mainloop(self):
        super().mainloop()

if __name__ == '__main__':
    App().mainloop()