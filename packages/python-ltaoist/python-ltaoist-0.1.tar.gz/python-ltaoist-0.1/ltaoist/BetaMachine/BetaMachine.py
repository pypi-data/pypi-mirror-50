
from collections import deque
from traceback import print_exc

class BetaMachineError(Exception):
    pass

class BetaMachine:

    def __init__(self):
        self._committed = deque([['beta', None]])
        self._progress = {}
        self._history = 0
        self._undfined = 0
        self._last = None

    def commit(self, beta, data):
        if beta == 'halt':
            self._committed.clear()
            return
        self._committed.append([beta, data])

    def to(self, beta):
        if beta in self._progress:
            raise BetaMachineError('Progress for %s defined.' % beta)
        def join(f):
            self._progress[beta] = f
            return f
        return join
    
    def beta(self, final_report=True):
        committed = self._committed
        progress = self._progress
        history = 0
        undefined = 0
        disfinish = 0
        beta = None
        data = None
        while True:
            try:
                beta, data = committed.popleft()
            except IndexError:
                break
            if (beta == 'halt') or (beta == 'dead'):
                break
            if beta not in progress:
                undefined += 1
                print("Undefined %s : %s" % (beta, data))
                continue
            try:
                progress[beta](beta, data)
            except:
                print("Disfinish %s : %s" % (beta, data))
                print_exc()
                disfinish += 1
            else:
                history += 1
        self._history = history
        self._undefined = undefined
        self._disfinish = disfinish
        self._last = (beta, data)
        if final_report or (self._undfined != 0) or (self._disfinish != 0):
            print("==============================================")
            print("BetaMachine ||| history:%d undefined:%d disfinish:%d" % (history, undefined, disfinish))
            print("  last: (%s, %s)" % self._last)

bm = BetaMachine()
commit = bm.commit
to = bm.to
beta = bm.beta
