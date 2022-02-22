from tkinter import *
from typing_interface import TypingInterface


def call_interface():
    frame.destroy()
    interface = TypingInterface(root)
    return interface


root = Tk()
root.title('TypeStar')

frame = Frame(root)
frame.grid()


canvas = Canvas(frame, width=600, height=300)
heading = canvas.create_text(300, 50, text='TypeStar', font=('Comic Sans Ms', 30, 'bold'))
intro_text = canvas.create_text(300, 200, font=('Comic Sans Ms', 16, 'normal'), justify='center',
                                text='Welcome to TypeStar!\n'
                                     'The app that lets improve your typing skills.\n'
                                     'Level up your typing speed with practice texts.\n'
                                     'Pull up your speed history and track your progress.', )
canvas.grid(column=0, row=0)

start_button = Button(frame, text='Jump right in!', width=30, font=('Comic Sans Ms', 16, 'bold'), command=call_interface)
start_button.grid(column=0, row=1, pady=50)

root.mainloop()
