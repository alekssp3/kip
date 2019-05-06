import tkinter as tk

class Check_and_merge_gui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.out = []
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # self.lable = tk.Label(self)
        # self.lable['text'] = "File name"
        # self.lable.pack()

        # self.filename = tk.Entry(self)
        # self.filename.pack()

        self.text = tk.Text(self)
        self.text.pack(side='top')

        self.combine = tk.Button(self)
        self.combine['text'] = 'Done'
        self.combine["command"] = self.get_lines_from_text
        self.combine.pack(side="bottom")

        # self.open_doc = tk.Checkbutton(self)
        # self.open_doc['text'] = 'Open file after combine'
        # self.open_doc.select()
        # self.open_doc.pack()

    def get_lines_from_text(self):
        out = []
        lines = ''.join(self.text.get('1.0', tk.END))
        for i in lines.split('\n'):
            if len(i) > 0:
                out.append(i)
        self.out = out
        self.master.destroy()

def tk_gui(title=''):
    root = tk.Tk()
    root.title = title
    app = Check_and_merge_gui(master=root)
    app.mainloop()
    return app.out