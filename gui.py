import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import functions as fu

canvas_size1 = 640
canvas_size2 = 480

sg.theme("DarkTeal2")

label = sg.Text("Enter High Frequency")
high_freq = sg.InputText(tooltip="Enter High Frequency", key="high_freq", default_text="1218")

label2 = sg.Text("Enter Tilt at High Frequency")
tilt_at_high_freq = sg.InputText(tooltip="Enter Tilt at High Frequency", key="tilt_at_high_freq", default_text="17")

label3 = sg.Text("Enter Carrier level")
carrier_level = sg.InputText(tooltip="Enter Carrier level", key="carrier_level", default_text="52")

label4 = sg.Text("Enter Carrier Frequency")
carrier_freq = sg.InputText(tooltip="Enter Carrier Frequency", key="carrier_freq", default_text="1218")

label5 = sg.Text("Frequency Split")
values = ["Low", "Mid", "High"]
split = sg.Combo(values=values, tooltip="Select Frequency Split", key="split", default_value="Low")

label6 = sg.Text("System Levels Plot")
canvas = sg.Canvas(size=(canvas_size1, canvas_size2), key="-canvas-", background_color='white')
calculate = sg.Button("Calculate", key="calculate")
frame = sg.Frame("System Levels", [[label, sg.Push(), high_freq],
                           [label2, sg.Push(), tilt_at_high_freq],
                           [label3, sg.Push(), carrier_level],
                           [label4, sg.Push(), carrier_freq],
                           [label5, sg.Push(), split]], size=(640, 150))

window = sg.Window("System Levels",
                   layout=[[frame],
                           [sg.Push(), label6, sg.Push()],
                           [canvas],
                           [sg.Push(), calculate, sg.Exit(key="Exit"), sg.Push()],
                           ],
                   finalize=True,
                   font=("Helvetica", 10))


while True:
    event, values = window.read()
    match event:
        case "calculate":
            x, y = fu.system_levels(float(values['high_freq']), float(values['tilt_at_high_freq']),\
                                    float(values['carrier_level']), float(values['carrier_freq']), values['split'])

            my_plt = fu.plot_levels(x, y)
            fu.draw_figure_on_canvas(window["-canvas-"].TKCanvas, my_plt)

        case "Exit":
            break
        case sg.WIN_CLOSED:
            break


window.close()
