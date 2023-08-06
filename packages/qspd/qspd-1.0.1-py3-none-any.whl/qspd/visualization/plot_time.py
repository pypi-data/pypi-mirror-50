import argparse
import json
import logging
from collections import defaultdict

import numpy as np
from matplotlib import pyplot as plt
from mpmath import log, nint

from qspd.json_encoding import decode_data


def plot(data, light=False, image_file=None, image_size=(640, 480), line_colors=None, best_fit_start=None):
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

    time_dict = defaultdict(dict)
    for record in data:
        time_dict[record["error"]][record["tau"]] = record["times"]["total"]

    for color_index, (error, tau_time) in enumerate(reversed(list(time_dict.items()))):
        taus, times = zip(*tau_time.items())
        color = line_colors[color_index % len(line_colors)] if line_colors is not None else None
        exponent = int(nint(log(error, b=10)))
        plt.scatter(taus, times, label=f"error $= 10^{{{exponent}}}$", color=color)
        if best_fit_start is not None:
            tau_indices = [i for i, tau in enumerate(taus) if taus[i] >= best_fit_start]
            large_taus = np.array([float(taus[i]) for i in tau_indices])
            large_times = np.array([times[i] for i in tau_indices])
            log_taus = np.log10(large_taus)
            log_times = np.log10(np.array(large_times))
            fit = np.polyfit(log_taus, log_times, 1)
            poly = np.poly1d(fit)
            plt.plot(large_taus, 10 ** poly(log_taus), color=color, linestyle=":")
    plt.legend()
    plt.ylabel("running time (s)")
    plt.xlabel(r"$\tau$")
    plt.xscale("log")
    plt.yscale("log")
    if image_file is None:
        plt.show()
    else:
        plt.savefig(image_file, transparent=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Plot runtime as a function of tau")
    parser.add_argument("files", metavar="file", type=str, nargs="+",
                        help="The JSON file(s) to get data from")
    parser.add_argument("--best-fit-start", type=float,
                        help="Adds a best-fit line to all points after (including) the given tau")
    parser.add_argument("--line-colors", type=str, nargs="+",
                        help="The colors of the plotted lines")
    parser.add_argument("--light", action="store_true", help="Add a light background")
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

    plot(data, light=args.light, image_file=args.image_file, image_size=image_size,
         line_colors=args.line_colors, best_fit_start=args.best_fit_start)
