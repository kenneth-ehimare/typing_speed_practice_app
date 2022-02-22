from tkinter import *
from wordlist import Wordlist

SECONDS = 61


def reload(frame, root):
    frame.destroy()
    TypingInterface(root)


def score_board(root, score_cpm, score_wpm):
    frame = Frame(root)
    frame.grid(column=0, columnspan=4, row=2)

    canvas = Canvas(frame, width=400, height=100)
    canvas.create_text(200, 50, text=f"Your typing speed\nCPM:    {score_cpm}       WPM:    {score_wpm}",
                       font=('Comic Sans Ms', 16, 'bold'), justify='center')
    canvas.grid(column=0, columnspan=2, row=0)

    restart_button = Button(frame, text='Go again?!', width=20, font=('Comic Sans Ms', 16, 'bold'),
                            command=lambda: reload(frame, root))
    restart_button.grid(column=0, row=1, pady=30, sticky='w')

    quit_button = Button(frame, text='Maybe next time', width=20, font=('Comic Sans Ms', 16, 'bold'),
                         command=root.quit)
    quit_button.grid(column=1, row=1, pady=30, sticky='e')


class TypingInterface:
    def __init__(self, master):
        self.timer = None
        self.event_tracker = 0
        self.num_correct = 0
        self.space_char = 0
        self.net_cpm = 0
        self.net_wpm = 0
        self.text = Wordlist().word_selection
        self.root = master

        self.frame = Frame(self.root)
        self.frame.grid(column=0, row=0, padx=30, pady=30)

        self.display = Text(self.frame, width=60, height=5, font=('Arial', 16), wrap='word', spacing1=15, spacing2=15,
                            yscrollcommand=set(), padx=10, )
        self.display.insert(1.0, self.text)
        self.display.tag_config('typed', overstrike=1)
        self.display.tag_config('missed', background='#FF6464')
        self.display.tag_config('correct', foreground='#91C483')
        self.display.grid(column=0, columnspan=4, row=0, pady=30)

        self.cpm_label = Label(self.frame, text='CPM:', font=('Comic Sans Ms', 12), width=10)
        self.cpm_label.grid(column=0, row=1, sticky='e')

        self.cpm = Label(self.frame, text=0, font=('Comic Sans Ms', 12), width=10)
        self.cpm.grid(column=1, row=1, sticky='w')

        self.countdown_label = Label(self.frame, text='Timer:', font=('Comic Sans Ms', 12), width=10)
        self.countdown_label.grid(column=2, row=1, sticky='e')

        self.countdown = Label(self.frame, text=60, font=('Comic Sans Ms', 12), width=10)
        self.countdown.grid(column=3, row=1, sticky='w')

        self.text_input = Text(self.frame, width=60, height=5, font=('Arial', 16), wrap='word', spacing1=15,
                               spacing2=15, yscrollcommand=set(), padx=10)
        self.text_input.grid(column=0, columnspan=4, row=2)
        self.text_input.bind('<KeyPress>', self.type_master)

    def stop_timer(self):
        self.frame.after_cancel(self.timer)
        self.frame.bell()
        self.cpm_label.destroy()
        self.cpm.destroy()
        self.countdown_label.destroy()
        self.countdown.destroy()
        self.text_input.destroy()
        score_board(self.root, self.net_cpm, self.net_wpm)

    def start_timer(self, count):
        self.timer = self.frame.after(1000, self.start_timer, count - 1)
        self.countdown.config(text=count)
        if count == 0:
            self.stop_timer()

    def type_master(self, event):
        self.event_tracker += 1
        widget = event.widget
        pointer_loc = widget.index('insert')
        self.display.see(f'{pointer_loc} + 100c')
        if self.display.get(pointer_loc) != ' ' and self.display.tag_names(pointer_loc) != ('typed',):
            self.display.tag_add('typed', pointer_loc)
        if self.event_tracker > 1:
            if self.display.tag_names(f'{pointer_loc} - 1c') == ('typed',):
                if widget.get(f'{pointer_loc} - 1c') == self.display.get(f'{pointer_loc} - 1c'):
                    self.display.tag_add('correct', f'{pointer_loc} - 1c')
                    self.num_correct += 1
                else:
                    self.display.tag_add('missed', f'{pointer_loc} - 1c')
            if widget.get(f'{pointer_loc} - 1c') == self.display.get(f'{pointer_loc} - 1c') == ' ':
                self.space_char += 1
        self.net_cpm = self.num_correct + self.space_char
        self.net_wpm = round(self.net_cpm / 5)
        self.cpm.config(text=self.net_cpm)
        if self.event_tracker == 1:
            self.start_timer(SECONDS)
