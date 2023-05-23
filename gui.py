import PySimpleGUI as sg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import functions as fu


def load_cable_descriptions():
    return pd.read_csv("cable_descriptions.csv", encoding="UTF-8")


def load_cable_data_100f():
    return pd.read_csv("new_coax_db_per_100_feet.csv", encoding="UTF-8")


def load_cable_100m():
    return pd.read_csv("new_coax_db_per_100_meters.csv", encoding="UTF-8")


#############################################################################################################
#         TAB 1 -System Levels
#############################################################################################################


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

label3 = sg.Text("Enter Carrier Frequency (MHz)", key="label3")
carrier_freq = sg.InputText(tooltip="Enter Carrier Frequency (MHz)", key="carrier_freq", default_text="54")

label4 = sg.Text("Enter Carrier Level (dBmV)", key="label4")
carrier_level = sg.InputText(tooltip="Enter Carrier Level (dBmV)", key="carrier_level", default_text="35")

label5 = sg.Text("Frequency Split")
values = ["Low", "Mid", "High"]
split = sg.Combo(values=values, tooltip="Select Frequency Split", key="split", default_value="Low", expand_x=True)

label6 = sg.Text("System Levels Plot")
canvas = sg.Canvas(size=(canvas_size1, canvas_size2), key="-canvas-", background_color='white')
calculate = sg.Button("Calculate", key="calculate")
total_power_text = sg.Text("", key="total_power", justification="right", s=33)

frame = sg.Frame("System Levels", [[label, sg.Push(), high_freq],
                                   [label2, sg.Push(), tilt_at_high_freq],
                                   [label3, sg.Push(), carrier_freq],
                                   [label4, sg.Push(), carrier_level],
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
                           [sg.Push(), calculate, sg.Exit(key="Exit"), total_power_text],
                           [frame2],
                           [frame3],
                           [frame4]])
tab1 = sg.Tab("System Levels", layout=[[column]])

#############################################################################################################
#         TAB 2 -Coax Loss
#############################################################################################################

cable_length_units_label = sg.Text("Select Length Units")
feet_radio = sg.Radio("Feet", group_id=1, default=True, enable_events=True, key="feet_radio")
meters_radio = sg.Radio("Meters", group_id=1, enable_events=True, key="meters_radio")
cable_length_label = sg.Text("Enter Cable Length in Feet", key="cable_length_label")
cable_length = sg.InputText(tooltip="Enter Cable Length", key="-cable_length-", default_text="200", enable_events=True)

layout1_tab2 = [[cable_length_units_label],
                [feet_radio, meters_radio],
                [cable_length_label],
                [cable_length]]

frame_t1 = sg.Frame("Coax Cable Parameters", layout=layout1_tab2, size=(640, 135))

##################################################################################################################

coax_data_f = load_cable_data_100f()
coax_data_m = load_cable_100m()

cable_descriptions = load_cable_descriptions()

cable_types = list(coax_data_f.columns.values)[1:]

select_cable_combo = sg.Combo(cable_types, key="cable_type", default_value="QR® 540 JCAT 3G AJ SM", enable_events=True)

cable_desc = sg.Text(cable_descriptions[cable_descriptions["Part Name"] == "QR® 540 JCAT 3G AJ SM"]["Description"].
                     squeeze(), key="cable_desc", size=(60, 2))

layout2_tab2 = [[select_cable_combo],
                [cable_desc]]

frame_t2 = sg.Frame("Select Coax Cable", layout=layout2_tab2, size=(640, 90))

temp_slider_label = sg.Text("Temperature (F)")
temp_slider = sg.Slider(range=(-80, 200), default_value=68, enable_events=True, key="-temperature-",
                        orientation="horizontal", size=(60, 20))

choice1 = sg.Combo(["Full", "Return", "Forward"], key="choice1", default_value="Full", enable_events=True)
choice2 = sg.Combo(["Low", "Mid", "High"], key="choice2", default_value="Low", enable_events=True, visible=False)

canvas2 = sg.Canvas(size=(canvas_size1, canvas_size2), key="-canvas2-", background_color='white')

column2 = sg.Column(scrollable=True, expand_x=False, expand_y=True, vertical_scroll_only=True,
                    layout=[[frame_t1],
                            [frame_t2],
                            [sg.HorizontalSeparator()],
                            [temp_slider_label],
                            [temp_slider],
                            [sg.HorizontalSeparator()],
                            [sg.Text("Select Frequency Range to Plot"), choice1,
                             sg.Text("Select Split to Plot", visible=False, key="choice 2 text"), choice2],
                            [canvas2]])

tab2 = sg.Tab("Coax Loss", layout=[[column2]])

window = sg.Window("System Levels by Tito Velez",
                   layout=[[sg.TabGroup([[tab1, tab2]], expand_y=True)]],
                   finalize=True,
                   resizable=True,
                   font=("Helvetica", 10), icon=r"K:\PythonProjects\pythonProject\Amp_Simulator\icon.ico")

# matplotlib System levels

fig = Figure(figsize=(6.40, 4.80))
fig.add_subplot(111).bar([], [])
fig.set_facecolor(color2)
figure_canvas_agg = FigureCanvasTkAgg(fig, window["-canvas-"].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

# matplotlib Coax Plot

fig2 = Figure(figsize=(6.40, 4.80))
fig2.add_subplot(111).plot([], [])
fig2.set_facecolor(color2)
figure_canvas_agg2 = FigureCanvasTkAgg(fig2, window["-canvas2-"].TKCanvas)
figure_canvas_agg2.draw()
figure_canvas_agg2.get_tk_widget().pack()

coax = coax_data_f
fu.plot_coax(coax, 200, 68, "QR® 540 JCAT 3G AJ SM", fig2, figure_canvas_agg2)

x, y = fu.system_levels(1218, 17, 54, 35)

fu.plot_levels(x, y, fig, figure_canvas_agg)

while True:
    event, values = window.read()
    print(event, values)
    match event:
        case "calculate":
            try:
                if values["use_two_pilots"]:

                    x, y = fu.system_levels2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                             float(values["carrier_freq"]), float(values["carrier_level"]),
                                             values['split'])

                    fu.plot_levels(x, y, fig, figure_canvas_agg)

                    window["-mystery_frequency-"].update("")
                    window["mystery_level"].update("")
                    window["mystery_tilt"].update("")
                    window["-pilot1-"].update("")
                    window["-pilot2-"].update("")

                else:
                    x, y = fu.system_levels(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                            float(values['carrier_freq']), float(values['carrier_level']),
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
            try:
                freq = values["-mystery_frequency-"]
                if values["use_two_pilots"]:
                    if freq.isnumeric():

                        z, w = fu.mystery_freq2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                                float(values["carrier_freq"]), float(values["carrier_level"]),
                                                float(freq),
                                                values['split'])
                        window["mystery_level"].update(f"Level is : {round(w, 2)} dBmV")
                    else:
                        window["mystery_level"].update("")
                else:
                    if freq.isnumeric():
                        z, w = fu.mystery_freq(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                               float(values['carrier_freq']), float(values['carrier_level']),
                                               float(freq), values['split'])
                        window["mystery_level"].update(f"Level is : {round(w, 2)} dBmV")
                    else:
                        window["mystery_level"].update("")
            except ValueError:
                sg.popup_error("Values must be numeric - check 'System Levels' Input Boxes")
        case ("-pilot1-" | "-pilot2-"):
            try:
                pilot1 = values["-pilot1-"]
                pilot2 = values["-pilot2-"]
                if values["use_two_pilots"]:

                    if pilot1.isnumeric() and pilot2.isnumeric():
                        z1, w1 = fu.mystery_freq2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                                  float(values["carrier_freq"]), float(values["carrier_level"]),
                                                  float(pilot1),
                                                  values['split'])
                        z2, w2 = fu.mystery_freq2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                                  float(values["carrier_freq"]), float(values["carrier_level"]),
                                                  float(pilot2),
                                                  values['split'])
                        tilt = w2 - w1
                        window["mystery_tilt"].update(f"Tilt is : {round(tilt, 2)} dB")
                    else:
                        window["mystery_tilt"].update("")
                else:
                    if pilot1.isnumeric() and pilot2.isnumeric():
                        z1, w1 = fu.mystery_freq(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                                 float(values['carrier_freq']), float(values['carrier_level']),
                                                 float(pilot1), values['split'])
                        z2, w2 = fu.mystery_freq(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                                 float(values['carrier_freq']), float(values['carrier_level']),
                                                 float(pilot2), values['split'])
                        tilt = w2 - w1
                        window["mystery_tilt"].update(f"Tilt is : {round(tilt, 2)} dB")
                    else:
                        window["mystery_tilt"].update("")
            except ValueError:
                sg.popup_error("Values must be numeric - check 'System Levels' Input Boxes")
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
                    window["CH_FREQ"].update(
                        f"QAM frequency is {freq_num} MHz - Analog frequency is {freq_num - 1.75} MHz")
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
                window["label3"].update("Enter Carrier Frequency (MHz)", background_color=color2)
                window["label4"].update("Enter Carrier level (dBmV)", background_color=color2)
                window["high_freq"].set_tooltip("Enter High Frequency")
                window["tilt_at_high_freq"].set_tooltip("Enter Tilt at High Frequency")
                window["carrier_level"].set_tooltip("Enter Carrier Frequency (MHz)")
                window["carrier_freq"].set_tooltip("Enter Carrier Level (dBmV)")
        case "feet_radio":
            window["cable_length_label"].update("Enter Cable Length in Feet")
            coax = coax_data_f
            # fu.plot_coax(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"], fig2,
            #              figure_canvas_agg2)
            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)
        case "meters_radio":
            window["cable_length_label"].update("Enter Cable Length in Meters")
            coax = coax_data_m
            # fu.plot_coax(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"], fig2,
            #              figure_canvas_agg2)
            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)
        case "cable_type":
            window["cable_desc"].update(cable_descriptions[cable_descriptions["Part Name"] == values["cable_type"]]
                                        ["Description"].squeeze())
            # fu.plot_coax(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"], fig2,
            #              figure_canvas_agg2)
            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)
        case "-cable_length-":
            if values["-cable_length-"].isnumeric():
                # fu.plot_coax(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"], fig2,
                #              figure_canvas_agg2)
                fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                              values["choice1"], values["choice2"], fig2,
                              figure_canvas_agg2)
            else:
                sg.popup_error("Length must be numeric")
        case "-temperature-":
            # fu.plot_coax(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"], fig2,
            #              figure_canvas_agg2)

            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)
        case "choice1":
            if values["choice1"] != "Full":
                window["choice 2 text"].update(visible=True)
                window["choice2"].update(visible=True)
            else:
                window["choice 2 text"].update(visible=False)
                window["choice2"].update(visible=False)

            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)

        case "choice2":
            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)
        case "Exit":
            break
        case sg.WIN_CLOSED:
            break

window.close()
