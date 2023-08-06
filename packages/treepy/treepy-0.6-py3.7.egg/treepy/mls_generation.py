#!/usr/bin/env python
# -*- coding: utf-8

import treepy

import os
import math
import itertools

from pathlib import Path
from colored import fore, back, style


class MultiLS(object):
    def __init__(self, args):
        self.args = args
        self.root = Path(args['path']).resolve()
        self.num_parents = args['P']
        self.max_rows = args['R']

        terminal_size = int(os.popen('stty size', 'r').read().split()[1])
        self.max_text_width = max([args.get('max_text_width') if args.get('max_text_width') else terminal_size, 0])

        self.display_data = []
        self.display_lines = []


    def get_parents(self, path, include_self=True):
        if include_self:
            yield path

        for i in range(self.num_parents - 1 if include_self else self.num_parents):
            if path.parent == path:
                break

            path = path.parent
            yield path


    def process(self):
        _getatime = lambda entry: entry.stat().st_atime

        for depth, parent in enumerate(self.get_parents(self.root)):
            children = sorted((child
                               for child in parent.iterdir()
                               if self.criteria(child)), key=_getatime, reverse=True)

            self.display_data.append((self.display_parent(parent, depth), self.display_children(children, depth)))

        self.display_data = list(reversed(self.display_data))
        for parent, children in self.display_data:
            self.display_lines.append(parent)
            self.display_lines.extend(children)


    def display_children(self, children, depth):
        # arbitrary parameters
        max_num_columns = 6
        max_num_rows = self.args['R']
        truncate_len = min([30, self.max_text_width])
        tab_len = 4

        if self.args['r']:
            dotdot_prefix = '../' * depth if depth > 0 else './'
        else:
            dotdot_prefix = ''

        # how long can a child string be?
        max_child_len = min([truncate_len, max([len(child.name) \
                                                + (1 if child.is_dir() else 0) \
                                                + len(dotdot_prefix) \
                                                for child in children])])

        num_columns = (self.max_text_width + tab_len) // (max_child_len + tab_len)
        if num_columns > max_num_columns: num_columns = max_num_columns

        num_rows = math.ceil(len(children) / num_columns)
        if max_num_rows and num_rows > max_num_rows: num_rows = max_num_rows

        def L(children):
            for child in children:
                yield child
        child_generator = L(children)

        table = {col:[] for col in range(num_columns)}
        for col in range(num_columns):
            for row in range(num_rows):
                try:
                    child = next(child_generator)
                except StopIteration:
                    break

                child_str = dotdot_prefix + str(child.name)

                diff = max_child_len - len(child_str)
                if diff < 0:
                    child_str = child_str[:truncate_len-1] + '…' + ' ' * tab_len

                child_str = self.stylize_child(child, child_str)
                child_str += ' ' * (diff + tab_len)
                table[col].append(child_str)
            else:
                continue # column finished. fill next column
            break # all children displayed

        try:
            next(child_generator)
            more = treepy.STYLIZE_MORE('…')
        except StopIteration:
            more = ''

        rows = [''.join(row).rstrip() for row in itertools.zip_longest(*table.values(), fillvalue='')]
        if more: rows.append(more)
        return rows


    def stylize_child(self, child, child_str):
        STYLIZE = treepy.STYLIZE_DIR if child.is_dir() else treepy.STYLIZE_FILE
        return STYLIZE(child_str)


    def display_parent(self, parent, depth):
        prefix = '▶ '
        parent_str = str(parent) + '/'
        diff = self.max_text_width - (len(prefix) + len(parent_str))

        if diff < 0:
            display = prefix + '…' + parent_str[1-diff:]
        else:
            display = prefix + parent_str

        display = treepy.STYLIZE_DIR_HEADER(display)
        return display


    def criteria(self, path):
        if self.args['d'] and not path.is_dir():
            return False

        if not self.args['a'] and str(path.name).startswith('.'):
            return False

        return True
