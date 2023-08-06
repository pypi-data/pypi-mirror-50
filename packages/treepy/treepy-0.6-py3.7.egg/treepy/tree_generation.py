#!/usr/bin/env python
# -*- coding: utf-8

import treepy

import os

from pathlib import Path
from colored import fore, back, style

class DisplayablePath(object):
    terminal_width = int(os.popen('stty size', 'r').read().split()[1])

    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '
    num_paths = 0

    @classmethod
    def load_args(cls, args):
        cls.args = args

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        def _getatime(entry):
            try:
                return entry.stat().st_atime
            except:
                return 0.0
        children = sorted((path for path in root.iterdir() if criteria(path)), key=_getatime, reverse=True)

        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                for obj in cls.make_tree(path, parent=displayable_root, is_last=is_last, criteria=criteria):
                    if cls.args.get('D') and obj.depth > cls.args.get('D'):
                        continue
                    yield obj

                    if cls.is_max_paths_per_depth_exceeded(count, is_last):
                        yield cls('...', displayable_root, True)
                        return
            else:
                yield cls(path, displayable_root, is_last)

                if cls.is_max_paths_per_depth_exceeded(count, is_last):
                    yield cls('...', displayable_root, True)
                    return

            count += 1

    @classmethod
    def is_max_paths_per_depth_exceeded(cls, count, is_last):
        max_paths_per_depth_exceeded = True if cls.args.get('M') and count == cls.args.get('M') else False
        return max_paths_per_depth_exceeded and not is_last

    @classmethod
    def _default_criteria(cls, path):
        if cls.args['d'] and not path.is_dir():
            return False

        if not cls.args['a'] and str(path.name).startswith('.'):
            return False

        return True

    @classmethod
    def increment_number_paths(cls):
        cls.num_paths += 1

    def truncate(self, display, quickaccess_display):
        m = self.args['max_text_width'] if self.args.get('max_text_width') else self.terminal_width
        diff1 = m - len(quickaccess_display) - 4 * self.depth
        diff2 = m - len(quickaccess_display) - len(display) - 4 * self.depth

        if diff1 < 0: # extreme case when max text width is smaller than the quickaccess_display
            display = ''
            quickaccess_display = '…' + quickaccess_display[-diff1 + 1:]
        elif diff2 < 0: # display + quickaccess_display extends beyond max text width
            display = '…' + display[-diff2 + 1:]

        return display, quickaccess_display

    @property
    def displayname(self):
        if self.args.get('f'):
            display = str(self.path.absolute())
        else:
            display = self.path.name

        if self.args.get('q') and not self.path.name == '...':
            slash = '/' if self.path.is_dir() else ''
            quickaccess_display = ' → $' + treepy.ENV_PREFIX + str(self.num_paths) + slash
        else:
            quickaccess_display = ''

        display, quickaccess_display = self.truncate(display, quickaccess_display)

        if self.path.is_dir():
            display = treepy.STYLIZE_DIR(display + '/')

        if self.path.is_file():
            display = treepy.STYLIZE_FILE(display)

        if self.path.name == '...':
            display = treepy.STYLIZE_MORE(display)

        if quickaccess_display:
            display += treepy.STYLIZE_QUICKACCESS(quickaccess_display)

        if not self.path.name == '...': self.increment_number_paths()

        return display

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(treepy.STYLIZE_BRANCHES(_filename_prefix),
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            extra = (self.display_parent_prefix_middle
                     if parent.is_last
                     else self.display_parent_prefix_last)

            parts.append(treepy.STYLIZE_BRANCHES(extra))
            parent = parent.parent

        return ''.join(reversed(parts))
