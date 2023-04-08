import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_figure_on_canvas(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def add_labels(x, y):
    for i in range(len(x)):
        plt.text(x[i], y[i], np.round(y[i]), fontsize='x-small', horizontalalignment='center', color='purple')


def plot_levels(x, y):
    fig, ax = plt.subplots()
    ax.bar(x, y, width=3)
    ax.grid()

    samples = 5
    freq_labels = np.append(x[::int(round(len(x) / samples))], x[-1])
    level_labels = np.append(y[::int(round(len(y) / samples))], y[-1])

    add_labels(freq_labels, level_labels)

    cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

    return plt.gcf()


def system_levels(high_freq, tilt_at_high_freq, carrier_level, carrier_freq, split_arg="Low"):
    split = {"Low": (42, 54),
             "Mid": (85, 102),
             "High": (204, 254)}
    low_freq = split[split_arg.capitalize()][1]

    freq = np.array([54,
                    55,
                    55.25,
                    61.25,
                    67.25,
                    77.25,
                    83.25,
                    85,
                    91.25,
                    97.25,
                    102,
                    103.25,
                    109.25,
                    115.25,
                    121.25,
                    127.25,
                    133.25,
                    139.25,
                    145.25,
                    151.25,
                    157.25,
                    163.25,
                    169.25,
                    175.25,
                    181.25,
                    187.25,
                    193.25,
                    199.25,
                    205.25,
                    211.25,
                    217.25,
                    223.25,
                    229.25,
                    235.25,
                    241.25,
                    247.25,
                    253.25,
                    254,
                    259.25,
                    265.25,
                    271.25,
                    277.25,
                    283.25,
                    289.25,
                    295.25,
                    301.25,
                    307.25,
                    313.25,
                    319.25,
                    325.25,
                    331.25,
                    337.25,
                    343.25,
                    349.25,
                    355.25,
                    361.25,
                    367.25,
                    373.25,
                    379.25,
                    385.25,
                    391.25,
                    397.25,
                    403.25,
                    409.25,
                    415.25,
                    421.25,
                    427.25,
                    433.25,
                    439.25,
                    445.25,
                    450,
                    451.25,
                    457.25,
                    463.25,
                    469.25,
                    475.25,
                    481.25,
                    487.25,
                    493.25,
                    499.25,
                    505.25,
                    511.25,
                    517.25,
                    523.25,
                    529.25,
                    535.25,
                    541.25,
                    547.25,
                    550,
                    553.25,
                    559.25,
                    565.25,
                    571.25,
                    577.25,
                    583.25,
                    589.25,
                    595.25,
                    601.25,
                    607.25,
                    613.25,
                    619.25,
                    625.25,
                    631.25,
                    637.25,
                    643.25,
                    649.25,
                    655.25,
                    661.25,
                    667.25,
                    673.25,
                    679.25,
                    685.25,
                    691.25,
                    697.25,
                    703.25,
                    709.25,
                    715.25,
                    721.25,
                    727.25,
                    733.25,
                    739.25,
                    745.25,
                    750,
                    751.25,
                    757.25,
                    763.25,
                    769.25,
                    775.25,
                    781.25,
                    787.25,
                    793.25,
                    799.25,
                    805.25,
                    811.25,
                    817.25,
                    823.25,
                    829.25,
                    835.25,
                    841.25,
                    847.25,
                    853.25,
                    859.25,
                    860,
                    865.25,
                    870,
                    871.25,
                    877.25,
                    883.25,
                    889.25,
                    895.25,
                    901.25,
                    907.25,
                    913.25,
                    919.25,
                    925.25,
                    931.25,
                    937.25,
                    943.25,
                    949.25,
                    955.25,
                    961.25,
                    967.25,
                    973.25,
                    979.25,
                    985.25,
                    991.25,
                    997.25,
                    1000,
                    1003.25,
                    1009.25,
                    1015.25,
                    1021.25,
                    1027.25,
                    1033.25,
                    1039.25,
                    1045.25,
                    1051.25,
                    1057.25,
                    1063.25,
                    1069.25,
                    1075.25,
                    1081.25,
                    1087.25,
                    1093.25,
                    1099.25,
                    1105.25,
                    1111.25,
                    1117.25,
                    1123.25,
                    1129.25,
                    1135.25,
                    1141.25,
                    1147.25,
                    1153.25,
                    1159.25,
                    1165.25,
                    1171.25,
                    1177.25,
                    1183.25,
                    1189.25,
                    1195.25,
                    1201.25,
                    1207.25,
                    1213.25,
                    1218])
    freq = freq[np.where(freq == low_freq)[0][0]:np.where(freq <= high_freq)[0][-1] + 1]
    level = tilt_at_high_freq/(high_freq - low_freq) * (freq - carrier_freq) + carrier_level
    return freq, level


def mystery_freq(high_freq, tilt_at_high_freq, carrier_level, carrier_freq, freq, split_arg="Low"):
    split = {"Low": (42, 54),
             "Mid": (85, 102),
             "High": (204, 254)}
    low_freq = split[split_arg.capitalize()][1]
    level = tilt_at_high_freq / (high_freq - low_freq) * (freq - carrier_freq) + carrier_level
    return freq, level


if __name__ == "__main__":
    x, y = system_levels(1200, 14.5, 52, 1200, split_arg="low")
    w, z = mystery_freq(1200, 14.5, 52, 1200, 1201, split_arg="low")
    print(w, z)
    plot_levels(x, y)




