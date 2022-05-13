import json
from threading import Thread, Event

json_file_path = 'config.json'

INT_MAX = 16
TIME_TO_SHARE_IN_SECONDS = 3


class MyThread(Thread):
    def __init__(self, event, f):
        Thread.__init__(self)
        self.stopped = event
        self.f = f

    def run(self):
        while not self.stopped.wait(TIME_TO_SHARE_IN_SECONDS):
            self.f()


class TGraph:
    def __init__(self):
        self.stopFlag = Event()
        self.graph_changed = False
        self.dict = dict()
        self.next_hop = dict()
        self.current_step = 1

    def _add_edge(self, v, u, w):
        if v not in self.dict:
            self.dict[v] = dict()
            self.next_hop[v] = dict()
        self.dict[v][u] = w
        self.next_hop[v][u] = u

    def add_edge(self, a, b):
        self._add_edge(a, b, 1)
        self._add_edge(b, a, 1)
        self._add_edge(a, a, 0)
        self._add_edge(b, b, 0)

    def _get_dist(self, a, b):
        if a in self.dict:
            if b in self.dict[a]:
                return self.dict[a][b]
        return INT_MAX

    def try_to_update(self, vertex_from, vertex_to, vertex_using):
        if self._get_dist(vertex_using, vertex_to) + 1 < self._get_dist(vertex_from, vertex_to):
            self.dict[vertex_from][vertex_to] = self.dict[vertex_using][vertex_to] + 1
            self.next_hop[vertex_from][vertex_to] = vertex_using
            return True
        return False

    def update(self):
        print(f'Step {self.current_step} simulation')

        graph_changed = False

        for (v, xs) in self.dict.items():
            for (u, w) in xs.items():
                if w != 1:  # пропускаем не соседей
                    continue
                for k in self.dict.keys():
                    graph_changed |= self.try_to_update(u, k, v)

        self.print_current_state()
        self.current_step += 1
        if not graph_changed:
            self.stopFlag.set()

    def init(self):
        MyThread(self.stopFlag, self.update).start()

    def print_current_state(self):
        for (v, xs) in self.dict.items():
            print(f'Vertex {v}, step {self.current_step}')
            for (u, w) in xs.items():
                if w != 0:
                    print(f'{v} ---{w}--> {u} [through {self.next_hop[v][u]}]')


def json_to_graph(json_data):
    g = TGraph()
    for i in json_data:
        g.add_edge(i['v'], i['u'])
    return g


def rip(graph):
    graph.init()


with open(json_file_path) as json_data:
    data = json.load(json_data)
    rip(json_to_graph(data))
