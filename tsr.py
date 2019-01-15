# coding: utf-8

from random import randint
import networkx as nx


def double_tree_algorithm(costMatrix: list, start: int):
    """
    2重木アルゴリズムで近似巡回ルートを生成する

    Parameters
    ----------
    costMatrix : list
        完全グラフのコスト行列
        対角成分はNoneとする
    start : int
        近似巡回ルートのスタート地点
    
    Returns
    -------
    route : list
        近似巡回ルート
    """

    # 0. コスト行列から重み付き完全グラフを生成
    graph = _create_weighted_graph(costMatrix)

    # 1. Primのアルゴリズムで最小全域木を生成
    spanningTree = nx.minimum_spanning_tree(graph, algorithm="prim")

    # 2. 最小全域木の各辺を2重化
    duplicatedSpanningTree = _duplicate_weighted_graph(spanningTree)

    # 3. 2重化した最小全域木からオイラー路を生成
    eulerianPath = _create_eulerian_path(duplicatedSpanningTree, start)

    # 4. オイラー路からハミルトン閉路を生成
    route = _create_hamiltonian_path(eulerianPath)

    # 5. ハミルトン閉路を出力して終了
    return route


def christofides_algorithm(costMatrix: list, start: int):
    """
    Christofidesのアルゴリズムで近似巡回ルートを生成する

    Parameters
    ----------
    costMatrix : list
        完全グラフのコスト行列
        対角成分はNoneとする
    start : int
        近似巡回ルートのスタート地点
    
    Returns
    -------
    route : list
        近似巡回ルート
    """

    # 0. コスト行列から重み付き完全グラフを生成
    graph = _create_weighted_graph(costMatrix)

    # 1. Primのアルゴリズムで最小全域木を生成
    spanningTree = nx.minimum_spanning_tree(graph, algorithm="prim")

    # 2. 最小全域木から偶数次数の頂点を除去
    removedGraph = _remove_even_degree_vertices(graph, spanningTree)

    # 3. 除去された最小全域木から最小コストの完全マッチングによるグラフを生成
    matchingGraph = _match_minimal_weight(removedGraph)

    # 4. 最小全域木と完全マッチングによるグラフを合体
    mergedGraph = _merge_two_graphs(spanningTree, matchingGraph)

    # 5. 合体したグラフからオイラー路を生成
    eulerianPath = _create_eulerian_path(mergedGraph, start)

    # 6. オイラー路からハミルトン閉路を生成
    route = _create_hamiltonian_path(eulerianPath)

    # 7. ハミルトン閉路を出力して終了
    return route


def _create_weighted_graph(costMatrix: list):
    """
    完全グラフの合計コストで重み付けした完全グラフを生成する

    Parameters
    ----------
    costMatrix : list
        完全グラフのコスト行列
        対角成分はNoneとする
    
    Returns
    -------
    graph : networkx.Graph
        重み付き完全グラフ
    """

    # 重み付き完全グラフのインスタンスを初期化
    graph = nx.Graph()

    # 重み付き完全グラフに辺を追加
    for i in range(len(costMatrix)):
        for j in range(i + 1, len(costMatrix[i])):
            graph.add_edge(i, j, weight=costMatrix[i][j])

    return graph


def _duplicate_weighted_graph(graph: nx.Graph):
    """
    重み付けグラフの辺を2重化する

    Parameters
    ----------
    graph : networkx.Graph
        重み付けグラフ
    
    Returns
    -------
    duplicatedGraph : networkx.MultiGraph
        引数の重み付けグラフの辺を2重化した重み付けグラフ
    """

    # 各辺を2重化する
    duplicatedGraph = nx.MultiGraph()
    for v in graph:
        for w in graph[v]:
            duplicatedGraph.add_edge(v, w, weight=graph[v][w]["weight"])
    
    return duplicatedGraph


def _create_eulerian_path(eulerianGraph: nx.MultiGraph, start: int):
    """
    オイラーグラフからオイラー路を生成する

    Parameters
    ----------
    eulerianGraph : networkx.MultiGraph
        オイラーグラフ
    start : int
        オイラー路のスタート地点
    
    Returns
    -------
    eulerianPath : list
        オイラー路を辿る頂点の順番のリスト
    """
    
    # オイラー路の辺リストを生成
    eulerianEdges = list(nx.eulerian_circuit(eulerianGraph, start))

    # オイラー路を辿る頂点の順番のリストを生成
    eulerianPath = [edge[0] for edge in eulerianEdges]
    # スタート地点とゴール地点を一致させる
    eulerianPath.append(eulerianEdges[len(eulerianEdges) - 1][1])

    return eulerianPath


def _create_hamiltonian_path(eulerianPath: list):
    """
    オイラー路からハミルトン閉路を生成する

    Parameters
    ----------
    eulerian_path : list
        オイラー路を辿る頂点の順番のリスト
    
    Returns
    -------
    hamiltonianPath : list
        ハミルトン閉路を辿る頂点の順番のリスト
    """

    # ハミルトン閉路を辿る頂点の順番のリストを初期化
    hamiltonianPath = []
    # 既出の頂点集合を初期化
    existedVertice = set()

    # オイラー路を辿る各頂点を辿り、2回目以降に現れた頂点は無視する
    for vertex in eulerianPath:
        if vertex not in existedVertice:
            hamiltonianPath.append(vertex)
            existedVertice.add(vertex)

    # スタート地点とゴール地点を一致させる
    hamiltonianPath.append(eulerianPath[0])

    return hamiltonianPath


def _remove_even_degree_vertices(graph: nx.Graph, spanningTree: nx.Graph):
    """
    全域木から偶数次数の頂点をグラフから取り除く

    Parameters
    ----------
    graph : networkx.Graph
        グラフ
    spanningTree : networkx.Graph
        全域木
    
    Returns
    -------
    removedGraph : networkx.Graph
       頂点を取り除いたグラフ
    """

    # 頂点を取り除いたグラフを引数のグラフで初期化
    removedGraph = nx.Graph(graph)

    for v in spanningTree:
        # 全域木の偶数次数の頂点のみグラフから削除
        if spanningTree.degree[v] % 2 == 0:
            removedGraph.remove_node(v)
    
    return removedGraph


def _match_minimal_weight(graph: nx.Graph):
    """
    グラフの最小コストの完全マッチングを生成する

    Parameters
    ----------
    graph : networkx.Graph
        グラフ
    
    Returns
    -------
    matchingGraph : set
        マッチングを構成する辺(2要素のみ持つタプル)のみ持つグラフ
    """

    # 全コストの大小関係を反転させるため、全コストの符号を逆にしたグラフをコピー
    tmpGraph = nx.Graph()
    for edgeData in graph.edges.data():
        tmpGraph.add_edge(edgeData[0], edgeData[1], weight=-edgeData[2]["weight"])
    # ブロッサムアルゴリズムで最大重み最大マッチングを生成
    matching = nx.max_weight_matching(tmpGraph, maxcardinality=True)

    # マッチングを構成するのみ持つグラフの生成
    matchingGraph = nx.Graph()
    for edge in matching:
        matchingGraph.add_edge(edge[0], edge[1], weight=graph[edge[0]][edge[1]]["weight"])

    return matchingGraph


def _merge_two_graphs(graph1: nx.Graph, graph2: nx.Graph):
    """
    辺が2重化されていない2つのグラフを合体する

    Parameters
    ----------
    graph1 : networkx.Graph
        1つ目のグラフ
    graph2 : networkx.Graph
        2つ目のグラフ
    
    Returns
    -------
    mergedGraph : networkx.MultiGraph
        合体したグラフ
    """

    # 合体したグラフを、1つ目のグラフで初期化
    mergedGraph = nx.MultiGraph(graph1)

    # 2つ目のグラフを構成する辺を追加していく
    for edgeData in graph2.edges.data():
        mergedGraph.add_edge(edgeData[0], edgeData[1], weight=edgeData[2]["weight"])
    
    return mergedGraph


if __name__ == "__main__":
    # 完全グラフのコスト行列
    costMatrix =    [[None,    8,   14,   17,   10,    6,   15],
                     [   8, None,    6,   15,   18,    3,   12],
                     [  14,    6, None,    9,   13,    8,    7],
                     [  17,   15,    9, None,    7,   12,    3],
                     [  10,   18,   13,    7, None,   15,    6],
                     [   6,    3,    8,   12,   15, None,    9],
                     [  15,   12,    7,    3,    6,    9, None]]
    
    # 2重木アルゴリズムによって近似巡回ルートを生成
    route = double_tree_algorithm(costMatrix, 0)
    print(route)
    # Christofidesのアルゴリズムによって近似巡回ルートを生成
    route = christofides_algorithm(costMatrix, 0)
    print(route)
