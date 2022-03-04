# Slightly edited version of h5tree
# https://github.com/johnaparker/h5tree

import h5py
from dataclasses import dataclass
from termcolor import colored
from collections import defaultdict

@dataclass
class TreeRenderer():
    # globals
    total_groups = 0
    total_datasets = 0
    group_color = 'green'
    dataset_color = 'yellow'
    attr_color = 'red'
    scalar_color = attr_color
    short_gap = ' '*2
    long_gap = ' '*4

    T_branch = '├── '
    L_branch = '└── '
    I_branch = '│   '
    blank = ' '*4

    terminated = defaultdict(lambda: False)

    verbose = True
    attributes = False
    groups = True
    level = None
    pattern = None

    tree_string = ""

    def str_count(self, n, name):
        """ return a string representing number of groups/datasets """
        if n != 1:
            return "{} {}s".format(n, name)
        else:
            return "{} {}".format(n, name)

    def display_header(self, group, grouppath, filepath, verbose = False):
        """ display the tree header """
        if grouppath == "/":
            header = filepath
        else:
            header = "{}/{}".format(filepath, grouppath)

        if verbose:
            message = self.str_count(len(group), "object")
            if group.attrs:
                message += ", " + self.str_count(len(group.attrs), "attribute")
            header += self.short_gap + "({})".format(message)

        self.tree_string += colored(header, self.group_color) + "\n"

    def display_attributes(self, group, n, verbose = False):
        """ display the attribute on a single line """
        num_attrs = len(group.attrs)
        front = ""
        for i in range(n):
            if self.terminated[i]:
                front = front + self.blank
            else:
                front = front + self.I_branch

        if num_attrs > 0:
            for i,attr in enumerate(group.attrs):
                if i == num_attrs - 1 and (len(group.keys()) == 0 or self.groups):
                    front_edit = front + self.L_branch
                else:
                    front_edit = front + self.T_branch
                attr_output = front_edit + colored(attr, self.attr_color)

                if verbose:
                    attr_output += colored(self.short_gap + str(group.attrs[attr]), None)
                self.tree_string += attr_output + "\n"

    def display(self, name, obj):
        """ display the group or dataset on a single line """

        if self.pattern and self.pattern not in name:
            return

        depth = name.count('/')
        # abort if below level
        if self.level and depth >= self.level:
            return

        # reset self.terminated dict
        for d in self.terminated:
            if d > depth:
                self.terminated[d] = False

        # construct text at the front of line
        subname = name[name.rfind('/')+1:]
        front = ""
        for i in range(depth):
            if self.terminated[i]:
                front = front + self.blank
            else:
                front = front + self.I_branch

        if list(obj.parent.keys())[-1] == subname:
            front += self.L_branch
            self.terminated[depth] = True
        else:
            front += self.T_branch

        # is group
        if isinstance(obj, h5py.Group):
            output = front + colored(subname, self.group_color)
            if self.verbose:
                message = self.str_count(len(obj), "object")
                if obj.attrs:
                    message += ", " + self.str_count(len(obj.attrs), "attribute")
                output += colored(self.short_gap + '({})'.format(message), self.group_color)

            self.total_groups += 1
            self.tree_string += output + "\n"

        # is dataset
        elif not self.groups:
            color = self.dataset_color
            if not obj.shape:
                color = self.scalar_color 
            output = front + colored(subname, self.dataset_color)

            if self.verbose:
                output += self.short_gap + '{}, {}'.format(obj.shape, obj.dtype) 

            self.total_datasets += 1
            self.tree_string += output + "\n"

        # include attributes
        if self.attributes:
            self.display_attributes(obj, depth + 1, True)

    def render_tree(self, path):

        # parse the parsed input
        locater = '.h5'
        nxs_locater = '.nxs'

        sep_index = path.find(nxs_locater) + len(nxs_locater)

        filepath = path[:sep_index]
        grouppath = path[sep_index+1:]
        if not grouppath:
            grouppath = "/"

        # open file and print tree
        with h5py.File(filepath, 'r') as f:
            group = f[grouppath]
            self.display_header(group, grouppath, filepath, True)
            if self.attributes:
                self.display_attributes(group, 1, True)

            group.visititems(self.display)

        if self.verbose:
            footer = '{}, {}'.format(self.str_count(self.total_groups, "group"), self.str_count(self.total_datasets, "dataset"))
            self.tree_string += '\n ' + footer

        return self.tree_string