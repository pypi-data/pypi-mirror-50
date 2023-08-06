"""Bare-bones CLI for displaying a tree of file structure"""

import re
from pathlib import Path
from colored import fore, back, style

def get_non_ANSI_line_length(line):
    regex = re.compile(r"""
                       \x1b     # literal ESC
                       \[       # literal [
                       [;\d]*   # zero or more digits or semicolons
                       [A-Za-z] # a letter
                       """, re.VERBOSE)
    actual = regex.sub("", line)
    return len(actual)

ENV_PREFIX = 'TREE'

TEMP_FILE = Path.home() / '.treepy_temp.sh'

COLOR_DIR = fore.CYAN
STYLE_DIR = COLOR_DIR

COLOR_FILE = fore.ORANGE_RED_1
STYLE_FILE = COLOR_FILE

COLOR_MORE = fore.CORNSILK_1
STYLE_MORE = COLOR_MORE

COLOR_BRANCHES = fore.LIGHT_GOLDENROD_2C
STYLE_BRANCHES = COLOR_BRANCHES + style.BOLD

COLOR_DIR_HEADER = fore.CORNSILK_1 + back.DEEP_SKY_BLUE_4A
STYLE_DIR_HEADER = COLOR_DIR_HEADER

COLOR_QUICKACCESS = fore.GREY_42
STYLE_QUICKACCESS = COLOR_QUICKACCESS

STYLE_RESET = style.RESET

STYLIZE_DIR = lambda string: STYLE_DIR + string + STYLE_RESET
STYLIZE_FILE = lambda string: STYLE_FILE + string + STYLE_RESET
STYLIZE_MORE = lambda string: STYLE_MORE + string + STYLE_RESET
STYLIZE_BRANCHES = lambda string: STYLE_BRANCHES + string + STYLE_RESET
STYLIZE_DIR_HEADER = lambda string: STYLE_DIR_HEADER + string + STYLE_RESET
STYLIZE_QUICKACCESS = lambda string: STYLE_QUICKACCESS + string + STYLE_RESET

def tabulate(*args, **kwargs):
    """
    Uses the function `tabulate` in the `tabulate` module to tabulate data. This function behaves
    almost identically, but exists because currently multiline cells that have ANSI colors break the
    formatting of the table grid. These issues can be tracked to assess the status of this bug and
    whether or not it has been fixed:

    https://bitbucket.org/astanin/python-tabulate/issues/170/ansi-color-code-doesnt-work-with-linebreak
    https://bitbucket.org/astanin/python-tabulate/issues/176/ansi-color-codes-create-issues-with

    Until then, this overwrites a function in the module to preserve formatting when using multiline
    cells with ANSI color codes.
    """
    import tabulate

    def _align_column(strings, alignment, minwidth=0, has_invisible=True, enable_widechars=False, is_multiline=False):
        strings, padfn = tabulate._align_column_choose_padfn(strings, alignment, has_invisible)
        width_fn = tabulate._choose_width_fn(has_invisible, enable_widechars, is_multiline)
        s_widths = list(map(width_fn, strings))
        maxwidth = max(max(s_widths), minwidth)
        if is_multiline:
            if not enable_widechars and not has_invisible:
                padded_strings = [
                    "\n".join([padfn(maxwidth, s) for s in ms.splitlines()])
                    for ms in strings]
            else:
                lines = [line.splitlines() for line in strings]
                lines_pad = [[(s, maxwidth + len(s) - width_fn(s)) for s in group]
                             for group in lines]
                padded_strings = ["\n".join([padfn(w, s) for s, w in group])
                                  for group in lines_pad]
        else:
            if not enable_widechars and not has_invisible:
                padded_strings = [padfn(maxwidth, s) for s in strings]
            else:
                s_lens = list(map(len, strings))
                visible_widths = [maxwidth - (w - l) for w, l in zip(s_widths, s_lens)]
                padded_strings = [padfn(w, s) for s, w in zip(strings, visible_widths)]
        return padded_strings

    tabulate._align_column = _align_column
    return tabulate.tabulate(*args, **kwargs)


