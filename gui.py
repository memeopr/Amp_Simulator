import PySimpleGUI as sg
import matplotlib
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

# matplotlib
fig = matplotlib.figure.Figure(figsize=(7, 5.5))
fig.add_subplot(111).bar([], [])
figure_canvas_agg = FigureCanvasTkAgg(fig, window["-canvas-"].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

while True:
    event, values = window.read()
    match event:
        case "calculate":

            x, y = fu.system_levels(float(values['high_freq']), float(values['tilt_at_high_freq']),\
                                    float(values['carrier_level']), float(values['carrier_freq']), values['split'])

            fu.plot_levels(x, y, fig, figure_canvas_agg)

        case "Exit":
            break
        case sg.WIN_CLOSED:
            break


window.close()
