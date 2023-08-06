from collections import defaultdict
import math
import numpy as np
from numpy import ma
import netCDF4
from netCDF4 import Dataset, num2date
from scipy.spatial import Delaunay
import halem.Functions as Functions
from scipy.signal import argrelextrema
from scipy.interpolate import griddata
import datetime, time
from datetime import datetime
import pickle
from IPython.display import clear_output
import halem.Flow_class as Flow_class


class Graph_flow_model:
    def __init__(
        self,
        name_textfile_flow,
        dx_min,
        blend,
        nl,
        number_of_neighbor_layers,
        vship,
        Load_flow,
        WD_min,
        WVPI,
        compute_cost=None,
        compute_co2=None,
        WWL=20,
        LWL=80,
        ukc=1.5,
        nodes_on_land=Flow_class.nodes_on_land_None,
        repeat=False,
        optimization_type=["time", "space", "cost", "co2"],
        nodes_index=np.array([None]),
    ):
        def compute_cost_f(week_rate, fuel_rate):
            second_rate = week_rate / 7 / 24 / 60 / 60
            return lambda travel_time, speed: (
                travel_time * second_rate + fuel_rate * travel_time * speed ** 3
            )

        def compute_co2_f(fuel_rate):
            return lambda travel_time, speed: (fuel_rate * travel_time * speed ** 3)

        if compute_cost == None:
            compute_cost = compute_cost_f(700_000, 0.0008)
        if compute_co2 == None:
            compute_co2 = compute_co2_f(1)

        self.WWL = WWL
        self.LWL = LWL
        self.ukc = ukc
        self.WVPI = WVPI
        self.repeat = repeat
        self.vship = vship

        # 'Load Flow'
        flow = Load_flow(name_textfile_flow)  # ABC van maken
        print("1/4")

        # 'Calculate nodes and flow conditions in nodes'
        if nodes_index.all() == None:
            self.nodes_index, self.LS = Get_nodes(flow, nl, dx_min, blend)
        else:
            self.nodes_index = nodes_index

        nodes = flow.nodes[self.nodes_index]
        u = np.asarray(np.transpose(flow.u))[self.nodes_index]
        v = np.asarray(np.transpose(flow.v))[self.nodes_index]
        WD = np.asarray(np.transpose(flow.WD))[self.nodes_index]

        self.nodes, self.u, self.v, self.WD = nodes_on_land(nodes, u, v, WD)

        self.tria = Delaunay(self.nodes)
        self.t = flow.t
        self.mask = np.full(self.u.shape, False)
        self.mask[self.WD < WD_min.max() + ukc] = True
        self.WD_min = WD_min
        clear_output(wait=True)
        print("2/4")

        # 'Calculate edges'
        graph0 = Graph()
        for from_node in range(len(self.nodes)):
            to_nodes = find_neighbors2(from_node, self.tria, number_of_neighbor_layers)
            for to_node in to_nodes:
                L = haversine(self.nodes[from_node], self.nodes[int(to_node)])
                graph0.add_edge(from_node, int(to_node), L)
        clear_output(wait=True)

        self.graph = Graph()
        vship1 = vship[0]
        for edge in graph0.weights:
            for i in range(len(vship1)):
                for j in range(len(vship1)):
                    from_node = edge[0]
                    to_node = edge[1]
                    self.graph.add_edge((from_node, i), (to_node, j), 1)

        print("3/4")

        # 'Calculate Weights'

        if self.repeat == True:
            calc_weights = calc_weights_time
        else:
            calc_weights = calc_weights_time

        self.weight_space = []  # Moet een Dict worden
        self.weight_time = []
        self.weight_cost = []
        self.weight_co2 = []

        for vv in range(len(self.vship)):
            graph_time = Graph()
            graph_space = Graph()
            graph_cost = Graph()
            graph_co2 = Graph()
            vship = self.vship[vv]
            WD_min = self.WD_min[vv]
            WVPI = self.WVPI[vv]
            for edge in graph0.weights:
                for i in range(len(vship)):
                    for j in range(len(vship)):
                        from_node = edge[0]
                        to_node = edge[1]

                        L, W, euros, co2 = calc_weights(
                            edge,
                            i,
                            j,
                            vship,
                            WD_min,
                            WVPI,
                            self,
                            compute_cost,
                            compute_co2,
                            number_of_neighbor_layers,
                        )

                        graph_time.add_edge((from_node, i), (to_node, j), W)
                        graph_space.add_edge((from_node, i), (to_node, j), L)
                        graph_cost.add_edge((from_node, i), (to_node, j), euros)
                        graph_co2.add_edge((from_node, i), (to_node, j), co2)

            if "space" in optimization_type:
                self.weight_space.append(graph_space)
            if "time" in optimization_type:
                self.weight_time.append(graph_time)
            if "cost" in optimization_type:
                self.weight_cost.append(graph_cost)
            if "co2" in optimization_type:
                self.weight_co2.append(graph_co2)

            clear_output(wait=True)
            print(np.round((vv + 1) / len(self.vship) * 100, 2), "%")

        clear_output(wait=True)
        print("4/4")


class Graph:
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are directional
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight


def calc_weights_time(
    edge,
    i,
    j,
    vship,
    WD_min,
    WVPI,
    self_f,
    compute_cost,
    compute_co2,
    number_of_neighbor_layers,
):
    from_node = edge[0]
    W = (
        Functions.costfunction_timeseries(
            edge, vship[j], WD_min, self_f, WVPI, number_of_neighbor_layers, self_f.tria
        )
        + self_f.t
    )
    W = FIFO_maker2(W, self_f.mask[from_node]) - self_f.t

    L = Functions.costfunction_spaceseries(
        edge, vship[j], WD_min, self_f, WVPI, number_of_neighbor_layers, self_f.tria
    )
    L = L + np.arange(len(L)) * (1 / len(L))
    L = FIFO_maker2(L, self_f.mask[from_node]) - np.arange(len(L)) * (1 / len(L))
    euros = compute_cost(W, vship[j])
    co2 = compute_co2(W, vship[j])

    return L, W, euros, co2


def calc_weights_repeat(
    edge,
    i,
    j,
    vship,
    WD_min,
    WVPI,
    self_f,
    compute_cost,
    compute_co2,
    number_of_neighbor_layers,
):
    from_node = edge[0]
    W = (
        Functions.costfunction_timeseries(
            edge, vship[j], WD_min, self_f, WVPI, number_of_neighbor_layers, self_f.tria
        )
        + self_f.t
    )
    W = np.concatenate((W, W))
    W = FIFO_maker2(W, self_f.mask[from_node])
    W = W[: int(len(W) / 2)] - self_f.t

    L = Functions.costfunction_spaceseries(
        edge, vship[j], WD_min, self_f, WVPI, number_of_neighbor_layers, self_f.tria
    )
    L = L + np.arange(len(L)) * (1 / len(L))
    L = np.concatenate((L, L))
    L = FIFO_maker2(L, self_f.mask[from_node])
    L = L[: int(len(L) / 2)] - np.arange(int(len(L) / 2)) * (1 / int(len(L) / 2))

    euros = compute_cost(W, vship[j])
    co2 = compute_co2(W, vship[j])

    return L, W, euros, co2


def haversine(coord1, coord2):
    dist = Functions.haversine(coord1, coord2)
    return dist


def find_neighbors(pindex, triang):  # zou recursief moeten kunne
    return triang.vertex_neighbor_vertices[1][
        triang.vertex_neighbor_vertices[0][pindex] : triang.vertex_neighbor_vertices[0][
            pindex + 1
        ]
    ]


def find_neighbors2(
    index, triang, depth
):  # Controleren of die buren niet twee keer toevoegd
    buren = np.array([index])  # list van een set -> verzamelt de unieke
    for _ in range(depth):
        for buur in buren:
            buren_temp = np.array([])
            temp = find_neighbors(int(buur), triang)
            for j in temp:
                if j in buren:
                    None
                else:
                    buren_temp = np.append(buren_temp, int(j))
            buren = np.append(buren, buren_temp)
    buren = np.delete(buren, 0)
    return buren


def FIFO_maker2(y, N1):
    arg = np.squeeze(argrelextrema(y, np.less))
    if arg.shape == ():
        arg = np.array([arg])
    else:
        None
    y_FIFO = 1 * y
    for a in arg:
        loc = np.argwhere(y[: a + 1] <= y[a])[-2:]
        if loc.shape == (2, 1):
            if True in N1[int(loc[0]) : int(loc[1])]:
                None
            else:
                y_FIFO[int(loc[0]) : int(loc[1])] = y[a]
    return y_FIFO


def closest_node(node, nodes, node_list):
    node_x = node_list[node][1]
    node_y = node_list[node][0]

    nodes_x = node_list[nodes][:, 1]
    nodes_y = node_list[nodes][:, 0]

    nx = ((nodes_x - node_x) ** 2 + (nodes_y - node_y) ** 2) ** 0.5
    pt = np.argwhere(nx == nx.min())[0][0]
    pt = nodes[pt]
    return pt


def slope(xs, ys, zs):
    tmp_A = []
    tmp_b = []
    for i in range(len(xs)):
        tmp_A.append([xs[i], ys[i], 1])
        tmp_b.append(zs[i])
    b = np.matrix(tmp_b).T
    A = np.matrix(tmp_A)
    fit = (A.T * A).I * A.T * b

    return fit[0], fit[1]


def curl_func(node, flow):
    nb = find_neighbors(node, flow.tria)
    nb = np.append(nb, node)
    DUDY = []
    DVDX = []
    xs = flow.nodes[nb][:, 1]
    ys = flow.nodes[nb][:, 0]
    for i in range(len(flow.t)):
        u = flow.u[i, nb]
        v = flow.v[i, nb]
        dudy = float(slope(xs, ys, u)[1])
        dvdx = float(slope(xs, ys, v)[0])
        DUDY.append(dudy)
        DVDX.append(dvdx)
    DUDY = np.array(DUDY)
    DVDX = np.array(DVDX)
    curl = (np.abs(DUDY - DVDX)).max()
    return curl


def Length_scale(node, flow, blend, nl):
    nb = find_neighbors(node, flow.tria)
    mag = (flow.u[:, node] ** 2 + flow.v[:, node] ** 2) ** 0.5
    mag = mag.max()

    if len(nb) < 2:
        return 1

    curl = abs(curl_func(node, flow))

    LS_c = ma.array(1 / (1 + curl) ** nl[0])
    LS_m = ma.array(1 / (1 + mag) ** nl[1])
    LS = ma.array(blend * LS_c + (1 - blend) * LS_m)
    return LS


def Get_nodes(flow, nl, dx_min, blend):
    nodes = flow.nodes
    new_nodes = [0]
    LS = []
    q = int(0)
    qq = 1
    for i in range(len(nodes)):
        q = q + int(1)
        if q == 1000:
            clear_output(wait=True)
            print(np.round(qq / len(nodes) * 100000, 3), "%")
            q = int(0)
            qq += 1
        LS_node = Length_scale(i, flow, blend, nl)
        LS.append(LS_node)
        closest_nod = closest_node(i, new_nodes, nodes)

        y_dist = nodes[closest_nod][0] - nodes[i][0]
        x_dist = nodes[closest_nod][1] - nodes[i][1]
        distu = (y_dist ** 2 + x_dist ** 2) ** 0.5

        if LS_node.mask == True:
            None
        elif distu > dx_min * LS_node:
            new_nodes.append(i)
        else:
            None

    LS = ma.array(LS, fill_value=np.nan)

    return new_nodes, LS
