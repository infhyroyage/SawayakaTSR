# coding: utf-8

import sys
from random import sample
from time import time
import matplotlib.pyplot as plt
from tsr import double_tree_algorithm, christofides_algorithm


def run_two_algorithms(costMatrix: list, start: int, times: int):
    """
    完全グラフのコスト行列の行と列のインデックスをシャッフルして、
    2つのアルゴリズムから近似巡回ルートを求める動作を、指定した実行回数分繰り返す

    Parameters
    ----------
    costMatrix : list
        完全グラフのコスト行列
    start : int
        近似巡回ルートのスタート地点
    times : int
        アルゴリズムの実行回数
    
    Returns
    -------
    doubleTreeRoutes : list
        2重木アルゴリズムで出力された近似巡回ルートのリスト
    doubleTreeCosts : list
        2重木アルゴリズムで出力された近似巡回ルートの合計コストのリスト
    doubleTreeTimes : list
        2重木アルゴリズムの実行時間(ms)のリスト
    christofidesRoutes : list
        Christofidesのアルゴリズムで出力された近似巡回ルートのリスト
    christofidesCosts : list
        Christofidesのアルゴリズムで出力された近似巡回ルートの合計コストのリスト
    christofidesTimes : list
        Christofidesのアルゴリズムの実行時間(ms)のリスト
    """

    # 返却値の初期化
    doubleTreeRoutes = []
    doubleTreeCosts = []
    doubleTreeTimes = []
    christofidesRoutes = []
    christofidesCosts = []
    christofidesTimes = []

    for _ in range(times):
        # コスト行列の行と列のインデックスをシャッフル
        shuffledCostMatrix, shuffledStart = _shuffle_cost_matrix(costMatrix, start)

        # 2重木アルゴリズムを実行し、実行時間を観測
        ready = time()
        doubleTreeRoute = double_tree_algorithm(shuffledCostMatrix, shuffledStart)
        finish = time()
        # 2重木アルゴリズムで出力された近似巡回ルートを格納
        doubleTreeRoutes.append(doubleTreeRoute)
        # 上記近似巡回ルートの合計コストを格納
        doubleTreeCost = _calc_total_cost(doubleTreeRoute, shuffledCostMatrix)
        doubleTreeCosts.append(doubleTreeCost)
        # 2重木アルゴリズムの実行時間を格納
        doubleTreeTimes.append((finish - ready) * 1000)

        # Christofidesのアルゴリズムを実行し、実行時間を観測
        ready = time()
        christofidesRoute = christofides_algorithm(shuffledCostMatrix, shuffledStart)
        finish = time()
        # Christofidesのアルゴリズムで出力された近似巡回ルートを格納
        christofidesRoutes.append(christofidesRoute)
        # 上記近似巡回ルートの合計コストを格納
        christofidesCost = _calc_total_cost(christofidesRoute, shuffledCostMatrix)
        christofidesCosts.append(christofidesCost)
        # Christofidesのアルゴリズムの実行時間を格納
        christofidesTimes.append((finish - ready) * 1000)
    
    return doubleTreeRoutes, doubleTreeCosts, doubleTreeTimes, christofidesRoutes, christofidesCosts, christofidesTimes


def _shuffle_cost_matrix(costMatrix: list, start: int):
    """
    コスト行列の行と列のインデックスをシャッフルする

    Parameters
    ----------
    costMatrix : list
        完全グラフのコスト行列
    start : int
        近似巡回ルートのスタート地点
    
    Returns
    -------
    shuffledCostMatrix : list
        シャッフルした完全グラフのコスト行列
    shuffledStart : int
        近似巡回ルートのシャッフルしたスタート地点
    """

    # シャッフルした完全グラフのコスト行列を初期化
    shuffledCostMatrix = []
    
    # 元のインデックスリストを生成
    indices = range(len(costMatrix))
    # 元のインデックスリストをシャッフルして生成
    shuffledIndices = sample(indices, len(indices))

    # シャッフルした完全グラフのコスト行列を1行ずつ格納
    for i in indices:
        tmpShuffledCostMatrix = []

        for j in indices:
            tmpShuffledCostMatrix.append(costMatrix[shuffledIndices[i]][shuffledIndices[j]])
        
        shuffledCostMatrix.append(tmpShuffledCostMatrix)
    
    return shuffledCostMatrix, shuffledIndices.index(start)


def _calc_total_cost(route: list, costMatrix: list):
    """
    巡回ルートから合計コストを計算する

    Parameters
    ----------
    route : list
        巡回ルート
    costMatrix : list
        完全グラフのコスト行列
    
    Returns
    -------
    totalCost : double
        合計コスト
    """

    # 合計コストの初期化
    totalCost = 0.0

    # 巡回ルートの1辺ごとに合計コストを足し合わせる
    for i in range(len(route) - 1):
        totalCost += costMatrix[route[i]][route[i + 1]]

    return totalCost


if __name__ == "__main__":
    # 完全グラフのコスト行列
    costMatrix =    [[None,    8,   14,   17,   10,    6,   15],
                     [   8, None,    6,   15,   18,    3,   12],
                     [  14,    6, None,    9,   13,    8,    7],
                     [  17,   15,    9, None,    7,   12,    3],
                     [  10,   18,   13,    7, None,   15,    6],
                     [   6,    3,    8,   12,   15, None,    9],
                     [  15,   12,    7,    3,    6,    9, None]]
    
    # 2つのアルゴリズムを1000回実行
    times = 1000
    _, doubleTreeCosts, doubleTreeTimes, _, christofidesCosts, christofidesTimes = run_two_algorithms(costMatrix, 0, times)
    print("Double Tree Average Time : " + str(sum(doubleTreeTimes) / float(times)) + "(ms)")
    print("Christofides Average Time : " + str(sum(christofidesTimes) / float(times)) + "(ms)")

    # ヒストグラムを描画してpng化
    fig = plt.figure(figsize=(14, 9))
    maxTick = int(max(max(doubleTreeCosts), max(christofidesCosts)))
    minTick = int(min(min(doubleTreeCosts), min(christofidesCosts)))
    bins = [i - 0.5 for i in range(minTick, maxTick + 2)]
    label = ["Double Tree", "Christofides"]
    plt.hist([doubleTreeCosts, christofidesCosts], bins=bins, label=label)
    plt.xlabel("Total cost", fontsize=30)
    plt.tick_params(labelsize=20)
    plt.xlim([minTick - 1, maxTick + 1])
    plt.xticks([i for i in range(minTick, maxTick + 1)])
    plt.legend(fontsize=25)
    fig.savefig("example_hist_times=1000.png", dpi=60)
