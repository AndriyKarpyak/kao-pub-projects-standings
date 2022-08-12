# -*- coding=utf-8 -*-


class Project:

    def __init__(self, number, name, budget, votes, size, category):
        self._number = number
        self._name = name
        self._budget = budget
        self._size = size
        self._type = category
        self._votes = votes

    def parsed_number(self):
        return self._number.split()[1]

    def __str__(self):
        return str(self._votes) + "     \t| "\
               + self._number + ": \t" + self._name + " - " + self._budget

