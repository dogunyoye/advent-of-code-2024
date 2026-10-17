import os.path
from collections import defaultdict

DATA = os.path.join(os.path.dirname(__file__), 'day23.txt')


# https://github.com/alanmc-zz/python-bors-kerbosch/blob/master/bors-kerbosch.py
def bors_kerbosch(r, p, x, g, c):
    if len(p) == 0 and len(x) == 0:
        if len(r) > 2:
            c.append(sorted(r))
        return

    pivot = max([(len(g[v]), v) for v in p.union(x)])

    for v in p.difference(g[pivot]):
        bors_kerbosch(r.union({v}), p.intersection(g[v]), x.intersection(g[v]), g, c)
        p.remove(v)
        x.add(v)


def __build_network(data) -> dict:
    network = defaultdict(set)
    for line in data.splitlines():
        computers = line.split("-")
        network[computers[0]].add(computers[1])
        network[computers[1]].add(computers[0])
    return network


def part_one(data) -> int:
    network = __build_network(data)
    three_node_networks = set()
    result = 0

    for k, v in network.items():
        for c in v:
            intersect = network[c].intersection(v)
            for i in intersect:
                three_node_networks.add(tuple(sorted([k, c, i])))

    for n in three_node_networks:
        for c in n:
            if c[0] == 't':
                result += 1
                break

    return result


def part_two(data) -> str:
    network = __build_network(data)
    maximal_cliques = []
    bors_kerbosch(set([]), set(network.keys()), set([]), network, maximal_cliques)
    return ",".join(max(sorted(maximal_cliques), key=len))


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + part_two(data))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
