import PySimpleGUI as sg
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import functions as fu



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

coax_data_f = fu.load_cable_data_100f()
coax_data_m = fu.load_cable_100m()

cable_descriptions = fu.load_cable_descriptions()

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

show_system_levels_checkbox = sg.Checkbox("Display System levels", key="display_system_levels", enable_events=True)
canvas3 = sg.Canvas(size=(canvas_size1, canvas_size2), key="-canvas3-", background_color='white')

distance_slider_label = sg.Text("Distance Slider")
distance_slider = sg.Slider(range=(0, 200), default_value=0, enable_events=True, key="-distance-",
                            orientation="horizontal", size=(60, 20))

frame_t3 = sg.Frame("System Levels vs Frequency", layout=[[distance_slider_label],
                                                          [distance_slider],
                                                          [canvas3]], visible=False, key="system_levels_frame")

column2 = sg.Column(scrollable=True, expand_x=False, expand_y=True, vertical_scroll_only=True,
                    layout=[[frame_t1],
                            [frame_t2],
                            [sg.HorizontalSeparator()],
                            [temp_slider_label],
                            [temp_slider],
                            [sg.HorizontalSeparator()],
                            [sg.Text("Select Frequency Range to Plot"), choice1,
                             sg.Text("Select Split to Plot", visible=False, key="choice 2 text"), choice2],
                            [canvas2],
                            [sg.HorizontalSeparator()],
                            [show_system_levels_checkbox],
                            [frame_t3]])

tab2 = sg.Tab("Coax Loss", layout=[[column2]])

#############################################################################################################
#         TAB 3 -Tap Loss
#############################################################################################################

taps_df = pd.read_csv(fu.resource_path("FFT-Q_TAPS.csv"))
taps_types = taps_df.columns.to_list()[1:]


two_way = [x for x in taps_types if "FFT2" in x.split("-")[0]]
four_way = [x for x in taps_types if "FFT4" in x.split("-")[0]]
eight_way = [x for x in taps_types if "FFT8" in x.split("-")[0]]

tap_layout = []
for i, text in enumerate(two_way):
    tap_layout.append([sg.Text(text, size=10), sg.Spin(list(range(0, 21)), size=10, enable_events=True, key=f"{text}")])
for i, text in enumerate(four_way):
    tap_layout[i].append(sg.Text(text, size=10))
    tap_layout[i].append(sg.Spin(list(range(0, 21)), size=10, enable_events=True, key=f"{text}"))
for i, text in enumerate(eight_way):
    tap_layout[i].append(sg.Text(text, size=10))
    tap_layout[i].append(sg.Spin(list(range(0, 21)), size=10, enable_events=True, key=f"{text}"))

f1 = [[sg.Text("2-Way TAPs", size=22), sg.Text("4-Way TAPs", size=22), sg.Text("8-Way TAPs", size=22)]]
f2 = [[sg.HorizontalSeparator()]]
f3 = [[sg.Button("Reset", key='tap_reset')]]
f4 = [[sg.HorizontalSeparator()]]
f5 = [[sg.Canvas(size=(640, 480), key="-canvas4-", background_color='white')]]
frame_layout = f1 + f2 + tap_layout + f3 + f4 + f5

tap_frame = sg.Frame("RF Taps Selection", layout=frame_layout)
tap_column = sg.Column(scrollable=True, expand_x=False, expand_y=True, vertical_scroll_only=True,
                       layout=[[tap_frame]])

tab3 = sg.Tab("Taps Loss", layout=[[tap_column]])

#############################################################################################################
#         TAB 4 -Amps
#############################################################################################################

amp_specs = pd.read_csv(fu.resource_path("amp_specs.csv"))

eqs_df = pd.read_csv(fu.resource_path("EQ.csv"))
eqs = eqs_df.columns.to_list()[1:]

amps_df = pd.read_csv(fu.resource_path("amps.csv"))
amps = amps_df.columns.to_list()[1:]

amp_image = sg.Image(fu.resource_path("images/MB120.png"), size=(640, 480), key="amp_image")
select_amp_label = sg.Text(" Select Amplifier")
amp_combo = sg.Combo(amps, key="amp_type", default_value="MB120", enable_events=True)


canvas5 = sg.Canvas(size=(640, 480), key="-canvas5-", background_color='white')

amps_frame_layout = [[select_amp_label, amp_combo],
                     [amp_image]]
amp_frame = sg.Frame("Amplifier Type", layout=amps_frame_layout)

amp_specs_text = sg.Text(amp_specs[amp_specs['Amplifier'] == "MB120"]['Specs'].squeeze(),
                         key="amp_specs_text", justification='center', size=(80,5))

amp_frame2 = sg.Frame("Amplifier Specifications", layout=[[amp_specs_text]], size=(640, 120))


amp_column = sg.Column(scrollable=True, expand_x=False, expand_y=True, vertical_scroll_only=True,
                       layout=[[amp_frame],
                               [amp_frame2],
                               [canvas5]])

tab4 = sg.Tab("Amplifiers", layout=[[amp_column]])

#############################################################################################################
#         TAB 5 -Amp Balancing
#############################################################################################################

select_input_eq_label = sg.Text("Select Input EQ", size=20)
eq_combo = sg.Combo(eqs, key="eq_type", default_value="CE-120-0", enable_events=True, size=20)
select_input_pad_label = sg.Text("Select Input PAD", size=20)
# input_pad_spinner = sg.Spin(list(range(0, 25)), key="input_pad_type", initial_value=0, enable_events=True, size=20)
input_pad_spinner = sg.Slider(range=(0, 25), key="input_pad_type", enable_events=True, orientation="horizontal", size=(50, 20))
select_output_pad_label = sg.Text("Select Output PAD", size=20)
# output_pad_spinner = sg.Spin(list(range(0, 25)), key="output_pad_type", initial_value=0, enable_events=True, size=20)
output_pad_spinner = sg.Slider(range=(0, 25), key="output_pad_type", enable_events=True, orientation="horizontal", size=(50, 20))

canvas6 = sg.Canvas(size=(640, 480), key="-canvas6-", background_color='white')

amps_balancing_frame_layout = [[select_input_eq_label, eq_combo],
                               [select_input_pad_label, input_pad_spinner],
                               [select_output_pad_label, output_pad_spinner]]
amp_balancing_frame = sg.Frame("RF Amplifier Setup", layout=amps_balancing_frame_layout)

signal_selection = sg.Combo(["Amplifier Input", "Amplifier Input after PAD and EQ", "Amplifier Output"],
                            default_value="Amplifier Input", enable_events=True, size=30, key="signal_selection")

amp_balancing_column = sg.Column(scrollable=True, expand_x=False, expand_y=True, vertical_scroll_only=True,
                                 layout=[[amp_balancing_frame],
                                         [sg.HorizontalSeparator(pad=((10, 10), (20, 20)))],
                                         [signal_selection],
                                         [canvas6]])

tab5 = sg.Tab("Amplifier Balancing", layout=[[amp_balancing_column]])


#############################################################################################################
window = sg.Window("System Levels by Tito Velez",
                   layout=[[sg.TabGroup([[tab1, tab2, tab3, tab4, tab5]], expand_y=True)]],
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

# matplotlib System Plots 3

fig3 = Figure(figsize=(6.40, 4.80))
fig3.add_subplot(111).plot([], [])
fig3.set_facecolor(color2)
figure_canvas_agg3 = FigureCanvasTkAgg(fig3, window["-canvas3-"].TKCanvas)
figure_canvas_agg3.draw()
figure_canvas_agg3.get_tk_widget().pack()

# matplotlib System Plots 4

fig4 = Figure(figsize=(6.40, 4.80))
fig4.add_subplot(111).plot([], [])
fig4.set_facecolor(color2)
figure_canvas_agg4 = FigureCanvasTkAgg(fig4, window["-canvas4-"].TKCanvas)
figure_canvas_agg4.draw()
figure_canvas_agg4.get_tk_widget().pack()


# matplotlib System Plots 5

fig5 = Figure(figsize=(6.40, 4.80))
fig5.add_subplot(111).plot([], [])
fig5.set_facecolor(color2)
figure_canvas_agg5 = FigureCanvasTkAgg(fig5, window["-canvas5-"].TKCanvas)
figure_canvas_agg5.draw()
figure_canvas_agg5.get_tk_widget().pack()

# matplotlib System Plots 6

fig6 = Figure(figsize=(6.40, 4.80))
fig6.add_subplot(111).plot([], [])
fig6.set_facecolor(color2)
figure_canvas_agg6 = FigureCanvasTkAgg(fig6, window["-canvas6-"].TKCanvas)
figure_canvas_agg6.draw()
toolbar = NavigationToolbar2Tk(figure_canvas_agg6, window["-canvas6-"].TKCanvas)
toolbar.update()
figure_canvas_agg6.get_tk_widget().pack()

fu.plot_amp_gain(amps_df["Frequency"].to_list(), amps_df["MB120"].to_list(), fig5, figure_canvas_agg5)

coax = coax_data_f
fu.plot_coax2(coax, 200, 68, "QR® 540 JCAT 3G AJ SM", "Full", "Low", fig2, figure_canvas_agg2)

x, y = fu.system_levels(1218, 17, 54, 35)

fu.plot_levels(x, y, fig, figure_canvas_agg)

taps_freq = taps_df["Frequency"]
s = np.zeros(len(taps_freq))
fu.plot_tap_loss(taps_freq, s, fig4, figure_canvas_agg4)

values = {"eq_type": "CE-120-2", "input_pad_type": 0, "output_pad_type": 0, "amp_type": "MB120"}


cable_selected = cable_types[0]
coax_balancing = coax_data_f[["Frequency", cable_selected]]
coax_balancing = coax_balancing[coax_balancing["Frequency"].isin(x)].reset_index(drop=True)
taps = taps_df[taps_df["Frequency"].isin(x)]

taps_selected = np.random.randint(0, 2, len(taps_types))
taps_loss = taps.iloc[:, 1:].dot(taps_selected)

temperature = 68
distance = 700

coax_balancing["coax_loss"] = coax_balancing[cable_selected].map(lambda x: fu.total_loss(x, distance))
coax_balancing["coax_loss"] = coax_balancing["coax_loss"].map(lambda x: fu.temp_change(x, temperature))

total_passive_loss = coax_balancing["coax_loss"] + taps_loss
amplifier_input = y + total_passive_loss

input_pad_selected = values["input_pad_type"] * np.ones(len(x))
output_pad_selected = values["output_pad_type"] * np.ones(len(x))
input_eq_selected = eqs_df[eqs_df["Frequency"].isin(x)][values["eq_type"]]

amplifier_input_after_pad_and_eq = amplifier_input - input_pad_selected \
                                   + input_eq_selected

amp_selected_gain = amps_df[amps_df["Frequency"].isin(x)][values["amp_type"]]

amplifier_output = amplifier_input_after_pad_and_eq + amp_selected_gain - output_pad_selected

fu.plot_amp_gain(x, amplifier_input.to_list(), fig6, figure_canvas_agg6)
fig6.axes[0].set_title('Amplifier Input')
figure_canvas_agg6.draw()
figure_canvas_agg6.get_tk_widget().pack()


while True:
    event, values = window.read()
    taps_dict = {i: values[i] for i in taps_types}
    taps_selected = taps_dict.values()
    if event in taps_types:
        taps_dict = {i: values[i] for i in taps_types}

        mult = taps_dict.values()

        # calculating the sum-product excel style
        s = taps_df.iloc[:, 1:].dot(list(mult))
        taps_freq = taps_df["Frequency"]
        fu.plot_tap_loss(taps_freq, s, fig4, figure_canvas_agg4)

    if values["use_two_pilots"]:
        x, y = fu.system_levels2(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                 float(values['carrier_freq']), float(values['carrier_level']),
                                 values['split'])
    else:
        x, y = fu.system_levels(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                float(values['carrier_freq']), float(values['carrier_level']),
                                values['split'])

    if values["feet_radio"]:
        coax_balancing = coax_data_f[["Frequency", values["cable_type"]]]
    elif values["meters_radio"]:
        coax_balancing = coax_data_m[["Frequency", values["cable_type"]]]
    taps = taps_df[taps_df["Frequency"].isin(x)]
    taps_loss = taps.iloc[:, 1:].dot(list(taps_selected))

    coax_balancing = coax_balancing[coax_balancing["Frequency"].isin(x)].reset_index(drop=True)
    # coax_balancing["coax_loss"] = coax_balancing[values["cable_type"]].map(lambda x: fu.total_loss(x, values["-distance-"]))
    coax_balancing["coax_loss"] = coax_balancing[values["cable_type"]].map(lambda x: fu.total_loss(x, float(values["-cable_length-"])))
    coax_balancing["coax_loss"] = coax_balancing["coax_loss"].map(lambda x: fu.temp_change(x, values["-temperature-"]))

    total_passive_loss = coax_balancing["coax_loss"] + taps_loss.reset_index(drop=True)
    # print(type(total_passive_loss))
    # total_passive_loss = total_passive_loss.dropna()

    amplifier_input = y + total_passive_loss.to_list()
    input_pad_selected = values["input_pad_type"] * np.ones(len(x))
    output_pad_selected = values["output_pad_type"] * np.ones(len(x))
    input_eq_selected = eqs_df[eqs_df["Frequency"].isin(x)][values["eq_type"]]

    amplifier_input_after_pad_and_eq = amplifier_input - input_pad_selected \
                                       + input_eq_selected

    amp_selected_gain = amps_df[amps_df["Frequency"].isin(x)][values["amp_type"]]

    amplifier_output = amplifier_input_after_pad_and_eq + amp_selected_gain - output_pad_selected

    if event in ["input_pad_type", "output_pad_type", "eq_type", "signal_selection"]:
        if values["signal_selection"] == "Amplifier Input":
            fu.plot_amp_gain(x, amplifier_input.to_list(), fig6, figure_canvas_agg6)
            fig6.axes[0].set_title('Amplifier Input')
            figure_canvas_agg6.draw()
            figure_canvas_agg6.get_tk_widget().pack()
        elif values["signal_selection"] == "Amplifier Input after PAD and EQ":
            fu.plot_amp_gain(x, amplifier_input_after_pad_and_eq.to_list(), fig6, figure_canvas_agg6)
            fig6.axes[0].set_title('Amplifier Input After Input PAD and EQ')
            figure_canvas_agg6.draw()
            figure_canvas_agg6.get_tk_widget().pack()
        elif values["signal_selection"] == "Amplifier Output":
            fu.plot_amp_gain(x, amplifier_output.to_list(), fig6, figure_canvas_agg6)
            fig6.axes[0].set_title('Amplifier Output')
            figure_canvas_agg6.draw()
            figure_canvas_agg6.get_tk_widget().pack()

    match event:
        case "calculate":
            try:
                if values["use_two_pilots"]:

                    x, y = fu.system_levels2(float(values['high_freq']), float(values["tilt_at_high_freq"]),
                                             float(values["carrier_freq"]), float(values["carrier_level"]),
                                             values['split'])

                    fu.plot_levels(x, y, fig, figure_canvas_agg)
                    fu.plot_levels(x, y, fig3, figure_canvas_agg3)

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
                    fu.plot_levels(x, y, fig3, figure_canvas_agg3)

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

            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)
        case "meters_radio":
            window["cable_length_label"].update("Enter Cable Length in Meters")
            coax = coax_data_m

            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)
        case "cable_type":
            window["cable_desc"].update(cable_descriptions[cable_descriptions["Part Name"] == values["cable_type"]]
                                        ["Description"].squeeze())

            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)
        case "-cable_length-":
            if values["-cable_length-"].isnumeric():

                fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                              values["choice1"], values["choice2"], fig2,
                              figure_canvas_agg2)
                window["-distance-"].update(range=(0, values["-cable_length-"]))
            else:
                sg.popup_error("Length must be numeric")
        case "-temperature-":

            fu.plot_coax2(coax, float(values["-cable_length-"]), values["-temperature-"], values["cable_type"],
                          values["choice1"], values["choice2"], fig2,
                          figure_canvas_agg2)

            if values["use_two_pilots"]:
                x, y = fu.system_levels2(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                         float(values['carrier_freq']), float(values['carrier_level']),
                                         values['split'])
            else:
                x, y = fu.system_levels(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                        float(values['carrier_freq']), float(values['carrier_level']),
                                        values['split'])

            df = pd.DataFrame(list(zip(x, y)), columns=["Frequency (MHz)", "Level (dBmV)"])

            coax_Freq_Modified = coax[coax["Frequency"].isin(x)]

            coax_Freq_Modified["at_new_temp"] = coax_Freq_Modified["at_new_temp"].map(lambda x: fu.total_loss(x, values["-distance-"] / float(values['-cable_length-']) * 100))
            coax_Freq_Modified.reset_index(inplace=True, drop=True)
            y = coax_Freq_Modified["at_new_temp"] + df["Level (dBmV)"]

            fu.plot_levels(x, y.values, fig3, figure_canvas_agg3)

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
        case "display_system_levels":
            if values["display_system_levels"]:
                window["system_levels_frame"].update(visible=True)

            else:
                window["system_levels_frame"].update(visible=False)
        case "-distance-":
            if values["use_two_pilots"]:
                x, y = fu.system_levels2(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                         float(values['carrier_freq']), float(values['carrier_level']),
                                         values['split'])
            else:
                x, y = fu.system_levels(float(values['high_freq']), float(values['tilt_at_high_freq']),
                                        float(values['carrier_freq']), float(values['carrier_level']),
                                        values['split'])

            df = pd.DataFrame(list(zip(x, y)), columns=["Frequency (MHz)", "Level (dBmV)"])

            coax_Freq_Modified = coax[coax["Frequency"].isin(x)]

            coax_Freq_Modified["at_new_temp"] = coax_Freq_Modified["at_new_temp"].map(lambda x: fu.total_loss(x, values["-distance-"] / float(values['-cable_length-']) * 100))
            #coax_Freq_Modified["at_new_temp"] = coax_Freq_Modified.loc[:, "at_new_temp"].map(lambda x: fu.total_loss(x, values["-distance-"] / float(values['-cable_length-']) * 100))
            coax_Freq_Modified.reset_index(inplace=True, drop=True)
            y = coax_Freq_Modified["at_new_temp"] + df["Level (dBmV)"]

            fu.plot_levels(x, y.values, fig3, figure_canvas_agg3)

        case "tap_reset":
            for i in taps_dict.keys():
                window[i].update(value=0)

        case "amp_type":
            window["amp_image"].update(source=fu.resource_path(f"images/{values['amp_type']}.png"))
            window["amp_specs_text"].update(
                value=amp_specs[amp_specs['Amplifier'] == values["amp_type"]]['Specs'].squeeze())
            fu.plot_amp_gain(amps_df["Frequency"].to_list(), amps_df[values["amp_type"]].to_list(), fig5,
                             figure_canvas_agg5)

        case "Exit":
            break
        case sg.WIN_CLOSED:
            break

window.close()
