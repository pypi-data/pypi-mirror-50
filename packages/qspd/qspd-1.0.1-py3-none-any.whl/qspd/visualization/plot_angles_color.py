import argparse
import json
import logging

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize, ListedColormap
from mpmath import nstr

from qspd.json_encoding import decode_data


def visualize(data, error_scale=False, left_aligned=False, auto_scale=False, n_scale=False,
        evens_only=False, odds_only=False, light=False, image_file=None, image_size=(640, 480),
        no_axes=False):
    logger = logging.getLogger("colorviz")
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
    if no_axes:
        fig.frameon = False
        ax.set_axis_off()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    if evens_only:
        data = [record for record in data if record["bigN"] % 2 == 0]
    elif odds_only:
        data = [record for record in data if record["bigN"] % 2 != 1]

    colormap = plt.get_cmap("hsv")
    ns = [record["n"] for record in data]
    if ns[1:] != ns[:-1]:  # https://stackoverflow.com/a/3844832
        # different values of n
        colormap_data = plt.get_cmap("hsv")(np.arange(256))
        colormap_data[0, :] = np.array([0, 0, 0, 0])  # zero is black
        colormap = ListedColormap(colormap_data)

    def add_padding(angles):
        padding = (max_num_angles - len(angles)) // 2
        if left_aligned:
            return np.pad(angles, (0, padding * 2), "constant")
        else:
            center = np.pad(angles[1:], (padding, padding), "constant")
            return np.insert(center, 0, np.array(angles)[0:1])

    angle_lists = [[float(angle) for angle in record["angles"]] for record in data]
    taus = [record["tau"] for record in data]
    errors = [record["error"] for record in data]
    angle_lists.reverse()
    taus.reverse()
    errors.reverse()
    ns.reverse()
    max_num_angles = max(len(angles) for angles in angle_lists)
    padded = [add_padding(angles) for angles in angle_lists]
    all_angles = np.stack(padded)
    all_angles[(0 < all_angles) & (all_angles < 1 / 40)] = 2 * np.pi

    tau_increment = data[1]["tau"] - data[0]["tau"] if len(data) > 1 else 1
    if auto_scale and not error_scale:
        min_tau = float(min(taus)) - tau_increment / 2
        max_tau = float(max(taus)) + tau_increment / 2
        extent = [-0.5, max_num_angles - 0.5, min_tau, max_tau]
    else:
        extent = None
    norm = Normalize(0, 2 * np.pi)
    plt.imshow(all_angles, norm=norm, aspect="auto", cmap=colormap, extent=extent)

    if no_axes:
        fig.subplots_adjust(bottom=0)
        fig.subplots_adjust(top=1)
        fig.subplots_adjust(right=1)
        fig.subplots_adjust(left=0)
    else:
        plt.xlabel("angle index")
        if n_scale:
            plt.ylabel("N").set_rotation(0)
            super_title = "Changing N, constant Tau = " + str(data[0]["tau"]) + " error = " + str(
                    data[0]["error"])
            plt.suptitle(super_title, fontsize=14, fontweight='bold')

        elif error_scale:
            plt.ylabel("error").set_rotation(0)
        else:
            plt.ylabel(r"$\tau$").set_rotation(0)

        if not auto_scale:
            if n_scale:
                plt.yticks(range(len(ns)), [int(n) for n in ns])
            elif error_scale:
                # TODO config scale ticks
                ticks = [tick for tick in range(len(errors)) if tick % 20 == 0]
                labels = [errors[tick] for tick in ticks]
                plt.yticks(ticks, labels)
            else:
                plt.yticks(range(len(taus)), [nstr(tau) for tau in taus])

    if image_file is None:
        plt.show()
    else:
        pad_inches = 0 if no_axes else None
        plt.savefig(image_file, transparent=True, pad_inches=pad_inches)


def main():
    parser = argparse.ArgumentParser(
            description="Visualize angles as colors for different values of tau")
    parser.add_argument("files", metavar="file", type=str, nargs="+",
                        help="The JSON file(s) to get data from")
    parser.add_argument("--error-scale", action="store_true",
                        help="Add if error is changing rather than tau")
    parser.add_argument("--auto-scale", action="store_true",
                        help="Add if there are no duplicates and there shouldn't be tick marks for all values of tau")
    parser.add_argument("--n-scale", action="store_true", help="Add if y axis should be N sweep")
    parser.add_argument("--left-aligned", action="store_true",
                        help="Add if colors should be left-aligned (default is centered)")
    parser.add_argument("--evens-only", action="store_true",
                        help="Add if you only want to plot even ns")
    parser.add_argument("--odds-only", action="store_true",
                        help="Add if you only want to plot odd ns")
    parser.add_argument("--no-axes", action="store_true",
                        help="Add if you don't want any axes, meaning that the image will be only the colors")
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

    visualize(data, error_scale=args.error_scale, left_aligned=args.left_aligned,
              auto_scale=args.auto_scale, n_scale=args.n_scale, evens_only=args.evens_only,
              odds_only=args.odds_only, light=args.light, image_file=args.image_file,
              image_size=image_size, no_axes=args.no_axes)


if __name__ == '__main__':
    main()
