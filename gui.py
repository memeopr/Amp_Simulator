import PySimpleGUI as sg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import functions as fu

canvas_size1 = 640
canvas_size2 = 480

color1 = "#0d3446"
color2 = "#394a6d"

input_size = (15, 1)

sg.theme("DarkTeal2")

use_two_pilots_checkbox = sg.Checkbox("Use High/Low pilots method instead.", key="use_two_pilots", enable_events=True)

label = sg.Text("Enter High Frequency (MHz)", key="label")
high_freq = sg.InputText(tooltip="Enter High Frequency", key="high_freq", default_text="1218")

label2 = sg.Text("Enter Tilt at High Frequency (dB)", key="label2")
tilt_at_high_freq = sg.InputText(tooltip="Enter Tilt at High Frequency", key="tilt_at_high_freq", default_text="17")

label3 = sg.Text("Enter Carrier level (dBmV)", key="label3")
carrier_level = sg.InputText(tooltip="Enter Carrier level", key="carrier_level", default_text="52")

label4 = sg.Text("Enter Carrier Frequency (MHz)", key="label4")
carrier_freq = sg.InputText(tooltip="Enter Carrier Frequency", key="carrier_freq", default_text="1218")

label5 = sg.Text("Frequency Split")
values = ["Low", "Mid", "High"]
split = sg.Combo(values=values, tooltip="Select Frequency Split", key="split", default_value="Low", expand_x=True)

label6 = sg.Text("System Levels Plot")
canvas = sg.Canvas(size=(canvas_size1, canvas_size2), key="-canvas-", background_color='white')
calculate = sg.Button("Calculate", key="calculate")
total_power_text = sg.Text("", key="total_power", justification="right")

frame = sg.Frame("System Levels", [[label, sg.Push(), high_freq],
                                   [label2, sg.Push(), tilt_at_high_freq],
                                   [label3, sg.Push(), carrier_level],
                                   [label4, sg.Push(), carrier_freq],
                                   [label5, sg.Push(), split]], size=(640, 150))
frame2 = sg.Frame("Find Level", [[sg.Text("   Frequency (MHz)"),
                                  sg.InputText(tooltip="Enter Carrier Frequency", key="-mystery_frequency-",
                                               enable_events=True, size=input_size),
                                  sg.Text("", key="mystery_level")]], size=(640, 50))

frame3 = sg.Frame("Find Tilt", [[sg.Text("         Pilot 1 (MHz)"),
                                 sg.InputText(tooltip="Enter Pilot #1", key="-pilot1-", enable_events=True,
                                              size=input_size), sg.Text("Pilot 2 (MHz) "),
                                 sg.InputText(tooltip="Enter Pilot #2", key="-pilot2-", enable_events=True,
                                              size=input_size), sg.Text("", key="mystery_tilt")]], size=(640, 50))

frame4 = sg.Frame("CH <-> Frequency Converter", [[sg.Text("Frequency (MHz)   "),
                                                  sg.InputText(tooltip="Enter Frequency (MHz)", key="convert_freq",
                                                               enable_events=True, size=input_size),
                                                  sg.Text("", key="CH_NUMBER")],
                                                 [sg.Text("CH Number           "),
                                                  sg.InputText(tooltip="Enter ch number", key="convert_ch",
                                                               enable_events=True, size=input_size),
                                                  sg.Text("", key="CH_FREQ")]
                                                 ], size=(640, 75))
column = sg.Column(scrollable=True, expand_x=False, expand_y=True, vertical_scroll_only=True,
                   layout=[[use_two_pilots_checkbox],
                           [frame],
                           [sg.Push(), label6, sg.Push()],
                           [canvas],
                           [sg.Push(), calculate, sg.Exit(key="Exit"), sg.Push(), total_power_text],
                           [frame2],
                           [frame3],
                           [frame4]])

window = sg.Window("System Levels by Tito Velez",
                   layout=[[column]],
                   finalize=True,
                   resizable=True,
                   font=("Helvetica", 10), icon=r"K:\PythonProjects\pythonProject\Amp_Simulator\icon.ico")

# matplotlib
fig = Figure(figsize=(6.40, 4.80))
fig.add_subplot(111).bar([], [])
figure_canvas_agg = FigureCanvasTkAgg(fig, window["-canvas-"].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

while True:
    event, values = window.read()
    match event:
        case "calculate":
            try:
                if values["use_two_pilots"]:

                    x, y = fu.system_levels2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                             float(values["carrier_level"]), float(values["carrier_freq"]),
                                             values['split'])

                    fu.plot_levels(x, y, fig, figure_canvas_agg)

                    window["-mystery_frequency-"].update("")
                    window["mystery_level"].update("")
                    window["mystery_tilt"].update("")
                    window["-pilot1-"].update("")
                    window["-pilot2-"].update("")

                else:
                    x, y = fu.system_levels(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                            float(values['carrier_level']), float(values['carrier_freq']),
                                            values['split'])

                    fu.plot_levels(x, y, fig, figure_canvas_agg)

                    window["-mystery_frequency-"].update("")
                    window["mystery_level"].update("")
                    window["mystery_tilt"].update("")
                    window["-pilot1-"].update("")
                    window["-pilot2-"].update("")
                total_power = fu.total_power(y)
                window["total_power"].update(f"Total Power: {round(total_power, 4)} dBmV")
            except ValueError:
                sg.popup_error("Values must be numeric")
        case "-mystery_frequency-":
            freq = values["-mystery_frequency-"]
            if values["use_two_pilots"]:
                if freq.isnumeric():

                    z, w = fu.mystery_freq2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                            float(values["carrier_level"]), float(values["carrier_freq"]), float(freq),
                                            values['split'])
                    window["mystery_level"].update(f"Level is : {round(w, 2)} dBmV")
                else:
                    window["mystery_level"].update("")
            else:
                if freq.isnumeric():
                    z, w = fu.mystery_freq(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                           float(values['carrier_level']), float(values['carrier_freq']),
                                           float(freq), values['split'])
                    window["mystery_level"].update(f"Level is : {round(w, 2)} dBmV")
                else:
                    window["mystery_level"].update("")
        case ("-pilot1-" | "-pilot2-"):
            pilot1 = values["-pilot1-"]
            pilot2 = values["-pilot2-"]
            if values["use_two_pilots"]:

                if pilot1.isnumeric() and pilot2.isnumeric():
                    z1, w1 = fu.mystery_freq2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                              float(values["carrier_level"]), float(values["carrier_freq"]),
                                              float(pilot1),
                                              values['split'])
                    z2, w2 = fu.mystery_freq2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                              float(values["carrier_level"]), float(values["carrier_freq"]),
                                              float(pilot2),
                                              values['split'])
                    tilt = w2 - w1
                    window["mystery_tilt"].update(f"Tilt is : {round(tilt, 2)} dB")
                else:
                    window["mystery_tilt"].update("")
            else:
                if pilot1.isnumeric() and pilot2.isnumeric():
                    z1, w1 = fu.mystery_freq(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                             float(values['carrier_level']), float(values['carrier_freq']),
                                             float(pilot1), values['split'])
                    z2, w2 = fu.mystery_freq(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                             float(values['carrier_level']), float(values['carrier_freq']),
                                             float(pilot2), values['split'])
                    tilt = w2 - w1
                    window["mystery_tilt"].update(f"Tilt is : {round(tilt, 2)} dB")
                else:
                    window["mystery_tilt"].update("")
        case "convert_freq":
            freq_to_convert = values["convert_freq"]
            if freq_to_convert.isnumeric():
                ch_num = fu.find_channel(float(freq_to_convert))
                window["CH_NUMBER"].update(f"CH {ch_num}")
            else:
                window["CH_NUMBER"].update("")
        case "convert_ch":
            ch_to_convert = values["convert_ch"]
            if ch_to_convert.isnumeric():
                freq_num = fu.find_freq(float(ch_to_convert))
                if freq_num is not None:
                    window["CH_FREQ"].update(f"QAM frequency is {freq_num} MHz - Analog frequency is {freq_num - 1.75}")
                else:
                    window["CH_FREQ"].update("")
            else:
                window["CH_FREQ"].update("")
        case "use_two_pilots":
            if values["use_two_pilots"]:
                window["label"].update("Enter High Pilot Frequency (MHz)", background_color=color1)
                window["label2"].update("Enter High Pilot Level (dBmV)", background_color=color1)
                window["label3"].update("Enter Low Pilot Frequency (MHz)", background_color=color1)
                window["label4"].update("Enter Low Pilot Level (dBmV)", background_color=color1)
                window["high_freq"].set_tooltip("Enter High Pilot Frequency")
                window["tilt_at_high_freq"].set_tooltip("Enter High Pilot Level")
                window["carrier_level"].set_tooltip("Enter Low Pilot Frequency")
                window["carrier_freq"].set_tooltip("Enter Low Pilot Level")
            else:
                window["label"].update("Enter High Frequency (MHz)", background_color=color2)
                window["label2"].update("Enter Tilt at High Frequency (dB)", background_color=color2)
                window["label3"].update("Enter Carrier level (dBmV)", background_color=color2)
                window["label4"].update("Enter Carrier Frequency (MHz)", background_color=color2)
                window["high_freq"].set_tooltip("Enter High Frequency")
                window["tilt_at_high_freq"].set_tooltip("Enter Tilt at High Frequency")
                window["carrier_level"].set_tooltip("Enter Carrier level")
                window["carrier_freq"].set_tooltip("Enter Carrier Frequency")
        case "Exit":
            break
        case sg.WIN_CLOSED:
            break

window.close()
