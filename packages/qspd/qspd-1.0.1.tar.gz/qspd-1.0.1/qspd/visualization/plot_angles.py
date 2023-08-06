import argparse
import json
import logging
import math
from collections import defaultdict

import matplotlib.pyplot as plt
from mpmath import pi, ceil, floor
from sympy import fft

from qspd.json_encoding import decode_data


def visualize(data, angle_indices=None, fourier=False, center_pi=False, error=False,
        light=False, transparent=False, image_file=None, image_size=(640, 480), marker=False, line_colors=None,
        pi_x=False, derivative=False):
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    if not light:
        plt.style.use("dark_background")
    brightness = 1 if light else 0
    alpha = 1 if image_file is None else 0
    face_color = (brightness, brightness, brightness, alpha)
    width, height = image_size
    fig = plt.figure(facecolor=face_color, figsize=(width / 100, height / 100))
    ax = fig.add_subplot(111)
    ax.set_facecolor((0, 0, 0, 0))
    plt.grid()

    angle_dict = defaultdict(dict)
    x_handle = "error" if error else "tau"
    for record in data:
        angles = record["angles"]
        for angle_index, angle in enumerate(angles):
            x_val = record[x_handle]
            angle_dict[angle_index][x_val] = float(angle)
    if angle_indices is None or len(angle_indices) == 0:
        angle_indices = angle_dict.keys()
    for color_index, angle_index in enumerate(angle_indices):
        x_vals, y_vals = zip(*sorted(angle_dict[angle_index].items()))
        color = line_colors[color_index % len(line_colors)] if line_colors is not None else None
        if fourier:
            if center_pi:
                y_vals = [y_val - pi for y_val in y_vals]
            y_vals = [float(abs(coeff)) for coeff in fft(y_vals, dps=15)]
            x_vals = range(len(y_vals))
        elif derivative:
            y_vals = [(y_vals[i + 1] - y_vals[i]) / (x_vals[i + 1] - x_vals[i]) for i in
                      range(len(y_vals) - 1)]
            x_vals = [(x_vals[i] + x_vals[i + 1]) / 2 for i in range(len(x_vals) - 1)]
        marker_pattern = "." if marker else None
        plt.plot(x_vals, y_vals, marker=marker_pattern, color=color, label=angle_index)

    if fourier:
        plt.xticks([])
        plt.yticks([])
    else:
        if error:
            plt.xlabel("error bounds")
            plt.xscale("log")
        else:
            plt.xlabel(r"$\tau$")

            if pi_x:
                min_tau = min(record["tau"] for record in data)
                min_tick_over_2pi = int(floor(min_tau / 2 * pi))

                max_tau = max(record["tau"] for record in data)
                ticks_over_2pi = list(range(min_tick_over_2pi, int(ceil(max_tau / (2 * pi)))))
                ticks = [tick_over_2pi * 2 * math.pi for tick_over_2pi in ticks_over_2pi]

                def label_tick(tick_over_2pi):
                    if tick_over_2pi == 0:
                        return "0"
                    else:
                        return f"${tick_over_2pi * 2}\\pi$"

                labels = [label_tick(tick_over_2pi) for tick_over_2pi in ticks_over_2pi]
                plt.xticks(ticks, labels)
        if derivative:
            y_label = "derivative of angle value"
        else:
            y_label = "angle value"
            plt.ylim(0, 2 * math.pi)
            y_labels = ["0", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"]
            plt.yticks([0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi], y_labels)
        plt.ylabel(y_label)

    plt.legend()
    if image_file is not None:
        plt.savefig(image_file, transparent=transparent)
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(
            description="Visualize line plots of angles for different values of tau")
    parser.add_argument("files", metavar="file", type=str, nargs="+",
                        help="The JSON file(s) to get data from")
    parser.add_argument("--angle-indices", metavar="angle-index", type=int, nargs="+",
                        help="Specific angle indices to plot")
    parser.add_argument("--error", action="store_true",
                        help="Plot angles changing with respect to the error tolerance, rather than tau")
    parser.add_argument("--derivative", action="store_true",
                        help="take the derivative of the angle value")
    parser.add_argument("--fourier", action="store_true",
                        help="Take the Fourier transform of the desired angle indices")
    parser.add_argument("--center-pi", action="store_true",
                        help="Subtract pi from all angles before taking the Fourier transform")
    parser.add_argument("--pi-x", action="store_true", help="x axis in terms of pi")
    parser.add_argument("--marker", action="store_true",
                        help="Display circles at each point along the plot")
    parser.add_argument("--line-colors", type=str, nargs="+",
                        help="The colors of the plotted lines")
    parser.add_argument("--light", action="store_true", help="Add a light background")
    parser.add_argument("--transparent", action="store_true", help="Make background transparent")
    parser.add_argument("--image-file", type=str, help="The name of the image file to save")
    parser.add_argument("--image-size", type=int, nargs=2, default=[640, 480],
                        help="The width and height of the image")
    args = parser.parse_args()

    data = []
    for filename in args.files:
        with open(filename) as file:
            data.extend(decode_data(json.load(file)))
    image_size_list = args.image_size
    image_size = (image_size_list[0], image_size_list[1])

    visualize(data, angle_indices=args.angle_indices, fourier=args.fourier,
              center_pi=args.center_pi, error=args.error, light=args.light, transparent=args.transparent,
              image_file=args.image_file, image_size=image_size, marker=args.marker,
              line_colors=args.line_colors, pi_x=args.pi_x, derivative=args.derivative)


if __name__ == '__main__':
    main()
