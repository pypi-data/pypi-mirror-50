from .out import *

import os


class TermSizeSkeleton:

    def __init__(self):
        self.Update()

    def Update(self):
        self.Rows, self.Columns = map(int, os.popen('stty size', 'r').read().split())

    def Rows(self, Update=True):
        if Update: self.Update()
        return self.Rows

    def Columns(self, Update=True):
        if Update: self.Update()
        return self.Rows


TermSize = TermSizeSkeleton()
