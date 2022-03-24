"""Displays some RGB colorgrids in the terminal."""

import time
import colorsys
from argparse import ArgumentParser, Namespace
from pytermgui import tim, terminal, ColorSystem, to_html


def _normalize(_rgb: tuple[float, float, float]) -> str:
    normalized = tuple(str(int(_col * 255)) for _col in _rgb)

    return normalized[0], normalized[1], normalized[2]


def _get_colorbox(width: int) -> str:
    _buff = ""
    for y_pos in range(0, 5):
        for x_pos in range(width):
            # Mmmm, spiky code
            _hue = x_pos / width
            _lightness = 0.1 + ((y_pos / 5) * 0.7)
            _rgb1 = colorsys.hls_to_rgb(_hue, _lightness, 1.0)
            _rgb2 = colorsys.hls_to_rgb(_hue, _lightness + 0.7 / 10, 1.0)

            _bg_color = ";".join(_normalize(_rgb1))
            _color = ";".join(_normalize(_rgb2))
            _buff += f"[{_bg_color} @{_color}]▀"

        _buff += "[/]\n"

    return _buff


def _highlight(timing: float) -> str:
    """Highlights a timing based on whether it is under 60 fps."""

    if timing < 1 / 60:
        return f"[#57A773] {timing}"

    return f"[red] {timing}"


def print_colorboxes(args: Namespace) -> None:
    """Prints some color boxes."""

    tim.print("[210 bold]Note:")
    tim.print(
        "   These results are gathered using [dim italic]tim.should_cache = False[/]."
    )

    print("   Thus, these only show unoptimized, one cold and one warm cache")
    print("   timings, which are magnitudes slower than the optimized end-user")
    print("   performance.")
    print()

    if not args.cache:
        tim.should_cache = False

    _buff = _get_colorbox(args.width)
    _html_buff = ""
    for system in reversed(ColorSystem):
        terminal.forced_colorsystem = system

        tim.print(str(system).center(args.width))
        start = time.time()
        tim.print(_buff)

        if not args.no_timings:
            tim.print(
                f"[dim italic]Rendered in ([blue]cold[/]):"
                + _highlight(time.time() - start)
            )
            warm_start = time.time()

            _html_buff += tim.parse(_buff)

            tim.print(
                f"[dim italic]Rendered in ([208]warm[/]):"
                + _highlight(time.time() - warm_start)
            )
            print()

    terminal.forced_colorsystem = None

    with open("colorgrids.html", "w") as html:
        html.write(to_html(_html_buff))


def main() -> None:
    """Main method."""

    open("colorgrids.html", "w").close()

    parser = ArgumentParser()
    parser.add_argument(
        "--no-timings", help="Don't show timing information.", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--cache",
        help="Use TIM caching. Will likely cause some issues.",
        action="store_true",
    )
    parser.add_argument(
        "-w", "--width", help="Width of color grids.", default=70, type=int
    )
    print_colorboxes(parser.parse_args())


if __name__ == "__main__":
    main()