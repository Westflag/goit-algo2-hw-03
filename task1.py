from typing import Dict, Tuple, List

import networkx as nx
import pandas as pd


def build_graph() -> nx.DiGraph:
    G = nx.DiGraph()
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)
    return G


def compute_max_flow(G: nx.DiGraph, sources: List[str], sinks: List[str]) -> Tuple[int, Dict[str, Dict[str, int]]]:
    G = G.copy()
    super_source, super_sink = "Джерело", "Стік"
    for source in sources:
        G.add_edge(super_source, source, capacity=float('inf'))
    for sink in sinks:
        G.add_edge(sink, super_sink, capacity=float('inf'))
    flow_value, flow_dict = nx.maximum_flow(G, super_source, super_sink, flow_func=nx.algorithms.flow.edmonds_karp)
    return flow_value, flow_dict


def extract_terminal_to_store_paths(flow_dict: Dict[str, Dict[str, int]],
                                    terminals: List[str],
                                    warehouses: List[str],
                                    stores: List[str]) -> pd.DataFrame:
    data = []
    for terminal in terminals:
        for warehouse in flow_dict.get(terminal, {}):
            if warehouse not in warehouses:
                continue
            flow_to_warehouse = flow_dict[terminal][warehouse]
            if flow_to_warehouse == 0:
                continue
            for store in flow_dict.get(warehouse, {}):
                if store not in stores:
                    continue
                flow_to_store = flow_dict[warehouse][store]
                if flow_to_store > 0:
                    flow_amount = min(flow_to_warehouse, flow_to_store)
                    data.append((terminal, store, flow_amount))
                    # віднімаємо витрачений потік
                    flow_dict[terminal][warehouse] -= flow_amount
                    flow_dict[warehouse][store] -= flow_amount
    df = pd.DataFrame(data, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"])
    return df


def run_analysis():
    G = build_graph()
    terminals = ["Термінал 1", "Термінал 2"]
    warehouses = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
    stores = [f"Магазин {i}" for i in range(1, 15)]
    max_flow, flow_dict = compute_max_flow(G, terminals, stores)
    df = extract_terminal_to_store_paths(flow_dict, terminals, warehouses, stores)
    return max_flow, df


def main():
    max_flow_value, flow_table = run_analysis()
    print(f"Максимальний потік через мережу: {max_flow_value}")
    print("\nТаблиця фактичних потоків між терміналами та магазинами:")
    print(flow_table)


if __name__ == "__main__":
    main()
