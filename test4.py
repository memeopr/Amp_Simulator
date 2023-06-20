import PySimpleGUI as sg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import functions as fu
import numpy as np

sg.theme("DarkTeal2")

color1 = "#0d3446"
color2 = "#394a6d"

coax_data_f = fu.load_cable_data_100f()
coax_data_m = fu.load_cable_100m()

cable_types = list(coax_data_f.columns.values)[1:]

cable_selected = cable_types[0]

taps_df = pd.read_csv("FFT-Q_TAPS.csv")
taps_types = taps_df.columns.to_list()[1:]

amp_specs = pd.read_csv("amp_specs.csv")

eqs_df = pd.read_csv("EQ.csv")
eqs = eqs_df.columns.to_list()[1:]

amps_df = pd.read_csv("amps.csv")
amps = amps_df.columns.to_list()[1:]

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

window = sg.Window("My Window", layout=[[sg.TabGroup([[tab5]], expand_y=True, enable_events=True, key="tab_group")]],
                   resizable=True, finalize=True, size=(700, 900))

# matplotlib System Plots 6

fig6 = Figure(figsize=(6.40, 4.80))
fig6.add_subplot(111).plot([], [])
fig6.set_facecolor(color2)
figure_canvas_agg6 = FigureCanvasTkAgg(fig6, window["-canvas6-"].TKCanvas)
figure_canvas_agg6.draw()
toolbar = NavigationToolbar2Tk(figure_canvas_agg6, window["-canvas6-"].TKCanvas)
toolbar.update()
figure_canvas_agg6.get_tk_widget().pack()


temperature = 68
distance = 700

values = {"eq_type": "CE-120-2", "input_pad_type": 0, "output_pad_type": 0, "amp_type": "MB120"}

x, y = fu.system_levels2(1000, 52, 54, 35)
coax_balancing = coax_data_f[["Frequency", cable_selected]]
coax_balancing = coax_balancing[coax_balancing["Frequency"].isin(x)].reset_index(drop=True)
taps = taps_df[taps_df["Frequency"].isin(x)]

coax_balancing["coax_loss"] = coax_balancing[cable_selected].map(lambda x: fu.total_loss(x, distance))
coax_balancing["coax_loss"] = coax_balancing["coax_loss"].map(lambda x: fu.temp_change(x, temperature))

taps_selected = np.random.randint(0, 2, len(taps_types))
taps_loss = taps.iloc[:, 1:].dot(taps_selected)

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
    print(event)
    print(values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    input_pad_selected = values["input_pad_type"] * np.ones(len(x))
    output_pad_selected = values["output_pad_type"] * np.ones(len(x))
    input_eq_selected = eqs_df[eqs_df["Frequency"].isin(x)][values["eq_type"]]

    amplifier_input_after_pad_and_eq = amplifier_input - input_pad_selected \
                                       + input_eq_selected

    amp_selected_gain = amps_df[amps_df["Frequency"].isin(x)]["MB120"]

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

window.close()
