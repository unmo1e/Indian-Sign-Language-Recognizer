import tkinter as tk
import subprocess
import pandas as pd
import tensorflow as tf
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from io import StringIO
from tkinterdnd2 import DND_FILES, TkinterDnD

characters_label = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
model = tf.keras.models.load_model("isl_model.keras")

def process_file(f_path):
    opt = subprocess.check_output("powershell -command ./sobel.exe " + f_path + " " + "output.csv")
    inpt = pd.read_csv(StringIO(opt.decode('utf-8')[0:-1]), header=None)
    predictions = model.predict(inpt.values)

    fig = Figure()
    bar_plot = fig.add_subplot()
    bar_plot.bar(characters_label, predictions[0])
    bar_plot.set_xlabel('Prediction is ' + characters_label[np.argmax(predictions)])

    canvas = FigureCanvasTkAgg(fig, master=second_label)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, master=second_label)
    toolbar.update()
    canvas.get_tk_widget().pack

root = TkinterDnD.Tk()
root.geometry("720x720")
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', lambda e: (process_file(e.data), second_label_string.set(e.data))[-1])

top_label_string = tk.StringVar()
top_label_string.set("Drag and Drag file in this window")
top_label = tk.Label(root, textvariable=top_label_string)
top_label.pack()

second_label_string = tk.StringVar()
second_label_string.set("")
second_label = tk.Label(root, textvariable=second_label_string)
second_label.pack()

root.mainloop()
