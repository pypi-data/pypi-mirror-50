
#
#            3333333
#            3222223
#            3211123
#            3210123
#            3211123
#            3222223
#
#           Beta Machine
#


from collections import deque
from traceback import print_exc

class BetaMachine:

    def __init__(self):
        self._committed = {
            0: deque([['beta', None]])
        }
        self._progress = {}
        self._history = 0
        self._undefined = 0
        self._last = None

    def commit(self, beta, data, serious=0):
        if (not isinstance(serious, int)) and\
           (not isinstance(serious, float)):
            raise StandardError("Serious should be int or float but %s" % serious)
        if serious not in self._committed:
            self._committed[serious] = deque([[beta, data]])
        else:
            self._committed[serious].append([beta, data])

    def to(self, beta, serious=0):
        if (not isinstance(serious, int)) and\
           (not isinstance(serious, float)):
            raise StandardError("Serious should be int or float but %s" % serious)
        if serious not in self._progress:
            self._progress[serious] = {}
        if beta in self._progress[serious]:
            raise StandardError('Progress for %s of serious %s defined.' % (beta, serious))
        def join(f):
            self._progress[serious][beta] = f
            return f
        return join

    def act(self, seriouses_count=1, ignore_undefined=False, ignore_disfinish=False, print_exc=True):
        seriouses = self._committed.keys()
        if (seriouses_count is not None) and \
           (seriouses_count != len(seriouses)):
            raise StandardError("Unmatch seriouses_count %s but %s" % (seriouses_count, len(seriouses)))
        seriouses.sort()
        for s in seriouses:
            committed = self._committed[s]
            progress = self._progress[s]
            while True:
                try:
                    beta, data = committed.popleft()
                except IndexError:
                    break
                if (beta == 'halt') or (beta == 'dead'):
                    break
                if beta not in progress:
                    if not ignore_undefined :
                        raise StandardError("Undefined %s of serious : %s" % (beta, s, data))
                    continue
                try:
                    progress[beta](beta, data)
                except:
                    if print_exc :
                        print_exc()                    
                    if not ingore_disfinish:
                        raise StandardError("Disfinish %s of serious : %s" % (beta, s, data))

machine = BetaMachine()
commit = machine.commit
to = machine.to
act = machine.act
