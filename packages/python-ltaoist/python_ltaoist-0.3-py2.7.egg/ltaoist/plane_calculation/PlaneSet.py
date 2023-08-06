import os

class PlaneSet:

    def __init__(self):
        self._result = {}
        self._derive = {}
        self._explain = {}
        self._original = {}

    def original(self, label, explain=None):
        def join(f):
            self._result[label] = f()
            self._explain[label] = explain
            self._derive[label] = [[], None]
            return f
        return join

    def _check_deps(self, source, colored):
        for x in source :
            colored[x] = True
            s1, _ = self._derive[x]
            if not self._check_deps(s1, colored):
                return False
        return True

    def derive(self, label, source, explain=None): # no
        if label in self._derive:
            raise StandardError("Forbid to redefine an defined plane %s" % label)
        if not self._check_deps(source, {label: True}):
            raise StandardError("Circular dependency %s" % label)
        if source == None:
            source = []
        def join(f):
            self._derive[label] = [source, f]
            self._explain[label] = explain
        return join

    def dump(self, label, path):
        pass

    def load(self, label, path):
        pass

    def get_explain(self, label):
        return self._explain[label]
    
    def query(self, label):
        if label in self._result :
            return self._result[label]
        source, f = self._derive[label]
        source_plane = [self.query(x) for x in source]
        stack = []
        stack_pos = [(0,0)]
        result = []
        maxlevel = len(source_plane)
        def select(selected, level):
            if level == maxlevel:
                item = f(*selected)
                if item:
                    result.append(item)
                return
            for x in source_plane[level]:
                selected.append(x)
                select(selected, level+1)
                selected.pop()
        select([], 0)
        self._result[label] = result
        return result
    
plane_set = PlaneSet()
original = plane_set.original
derive = plane_set.derive
dump = plane_set.dump
load = plane_set.load
get_explain = plane_set.get_explain
query = plane_set.query
