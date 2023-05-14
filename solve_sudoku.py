import time

import numpy as np


def extract_column(i: int, matrix: list[list[int]]):
    """
    行列から各列を取り出す
    Args:
        i[int]: 何列目を取り出すか表すインデックス
        matrix[List[List[int]]]: 取り出す元の行列
    Return:
        column[List[int]]: 行列のi列目の要素が入ったリスト
    """
    column = []
    for row in matrix:
        column.append(row[i])
    return column


def extract_mini_matrix(i: int, j: int, matrix: list[list[int]], nine_x_nine_index: bool = True):
    """
    9x9の行列からi, jに対応する位置の3x3の行列を取り出す。
    - nine_x_nine_indexがTrueの場合は、i, j は9x9の各要素のインデックスを表し、
      その要素が含まれる3x3の行列を返す
    - nine_x_nine_indexがFalseの場合は、i, jは3x3の行列の位置を表し、以下のような位置の行列を返す
                      |                 | 
      (i, j) = (0, 0) | (i, j) = (0, 1) | (i, j) = (0, 2)
                      |                 | 
      ---------------------------------------------------
                      |                 |
      (i, j) = (1, 0) | (i, j) = (1, 1) | (i, j) = (1, 2)
                      |                 |
      ---------------------------------------------------
                      |                 |
      (i, j) = (2, 0) | (i, j) = (2, 1) | (i, j) = (2, 2)
                      |                 |
    Args:
        i[int]: 抜き出す3x3の行列の位置を表すインデックス（行方向）
        j[int]: 抜き出す3x3の行列の位置を表すインデックス（列方向）
        matrix[List[List[int]]]: 抜き出す元の行列
        nine_x_nine_index[bool]: i, j の意味を決定する変数
                                 Trueの場合  : i, jは9x9行列の要素を指定する
                                 Falseの場合 : i, jは上に示した位置を表すインデックス
    Return:
        mini_matrix[List[List[int]]]: 3x3の行列
    """
    if nine_x_nine_index:
        i = i // 3
        j = j // 3

    mini_matrix = []
    for k, row in enumerate(matrix):
        if i * 3 <= k < i * 3 + 3:
            mini_matrix.append(row[j * 3:j * 3 + 3])
    return mini_matrix

def check_sudoku(matrix: list[list[int]], use_numpy: bool = False):
    """
    9x9の行列が数独のルールを満たしているかを判定する
    Args:
        matrix[List[List]]: 9x9の行列
    Return:
        return[bool]: 数独のルールを満たしていれば"True"
                      満たしていなければ"False"
    """
    one_to_nine_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if use_numpy:
        matrix = np.array(matrix)
        # 各行、列に関してチェック
        for i, row in enumerate(matrix):
            column = matrix[:, i]
            if sorted(row) != one_to_nine_list or sorted(column) != one_to_nine_list:
                return False
        # 3x3の行列についてチェック
        for i in range(3):
            for j in range(3):
                mini_matrix = matrix[i * 3:i * 3 + 3, j * 3: j * 3 * 3]
                if sorted(np.ravel(mini_matrix)) != one_to_nine_list:
                    return False
    else:
        # 各行についてチェック
        for row in matrix:
            if sorted(row) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return False
        # 各列についてチェック
        for i in range(9):
            column = extract_column(i)
            if sorted(column) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return False

        # 3x3の行列についてチェック
        for i in range(3):
            for j in range(3):
                mini_matrix = extract_mini_matrix(i, j, matrix)
                if sorted(sum(mini_matrix, [])) != one_to_nine_list:
                    return False
    return True


def init_answer(matrix: list[list[int]]):
    """
    数独の問題（空欄は0埋めされたもの）から、解答用の行列を作成
    空欄は空のリストを入れておく
    Args:
        matrix[List[List[int]]]: 解答する数独の行列（空欄は0埋めされたもの）
    Returns:
        answer_candidate[List[List[int]]]: 解答用の行列
    """
    answer_candidate = []
    for row in matrix:
        tmp = []
        for val in row:
            if val == 0:
                tmp.append([])
            else:
                tmp.append(val)
        answer_candidate.append(tmp)
    return answer_candidate


def delete_candidate(delete_number: int, candidates: list or list[list], matrix_mode=False):
    """
    候補から、delete_numberを削除
    Args:
        delete_number[int]: 削除する数字
        candidates[List[int or List[int]]]: 削除する候補リスト
        matrix_mode[bool]: 候補が2重リストかどうかを判定するフラグ
    """
    print(delete_number)
    print(candidates)
    if matrix_mode:
        for row in candidates:
            for val in row:
                if isinstance(val, list) and delete_number in val:
                    print(val.index(delete_number))
                    val.pop(val.index(delete_number))
    else:
        for val in candidates:
            if isinstance(val, list) and delete_number in val:
                val.pop(val.index(delete_number))

    print(candidates)
    print('')


def solve_sudoku(matrix):
    """
    Args:
        matrix[List[List[int]]]: 9x9の行列、解答が埋まっていない場所は"0"になっている
    """
    zero_to_nine_set = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    # 解答用行列の作成
    answer_candidates = init_answer(matrix)
    # 解答候補の探索
    for i, (answer_row, row) in enumerate(zip(answer_candidates, matrix)):
        for j, candidate in enumerate(answer_row):
            if isinstance(candidate, list):
                column = extract_column(j, matrix)
                flattened_mini_matrix = sum(extract_mini_matrix(i, j, matrix), [])
                answer_candidates[i][j] = list(zero_to_nine_set - set(row + column + flattened_mini_matrix))

    for row in answer_candidates:
        print(row)
    print('')
    # 解答候補から決定できるものを決定していく
    # 1. len(candidate) == 1のところを埋める->関係する候補から埋めた数字を消す
    # 2. [1, 2]が同じ列(行)に二つあったら1, 2を他の候補から削除する
    # 3. 周りの3行(3列)を確認して候補の絞り込み
    while True:
        break_flag = True

        for i, answer_row in enumerate(answer_candidates):
            for j, candidate in enumerate(answer_row):
                if isinstance(candidate, list) and len(candidate) == 1:
                    answer_candidates[i][j] = candidate[0]

                    answer_column = extract_column(j, answer_candidates)
                    mini_matrix = extract_mini_matrix(i, j, answer_candidates)

                    delete_candidate(candidate[0], answer_row)
                    delete_candidate(candidate[0], answer_column)
                    delete_candidate(candidate[0], mini_matrix, matrix_mode=True)

                    break_flag = False

        for row in answer_candidates:
            print(row)
        print('')
        if break_flag:
            break


if __name__ == '__main__':
    # answer = [
    #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
    #     [4, 5, 6, 7, 8, 9, 1, 2, 3],
    #     [7, 8, 9, 1, 2, 3, 4, 5, 6],
    #     [2, 3, 4, 5, 6, 7, 8, 9, 1],
    #     [5, 6, 7, 8, 9, 1, 2, 3, 4],
    #     [8, 9, 1, 2, 3, 4, 5, 6, 7],
    #     [3, 4, 5, 6, 7, 8, 9, 1, 2],
    #     [6, 7, 8, 9, 1, 2, 3, 4, 5],
    #     [9, 1, 2, 3, 4, 5, 6, 7, 8],
    # ]

    # middle = [
    #     [0, 3, 4, 9, 0, 6, 2, 7, 0],
    #     [1, 2, 0, 0, 7, 5, 6, 0, 0],
    #     [9, 0, 7, 8, 0, 0, 5, 1, 3],
    #     [6, 0, 0, 0, 0, 9, 4, 0, 0],
    #     [0, 0, 9, 2, 0, 0, 0, 6, 0],
    #     [0, 0, 5, 7, 0, 0, 0, 8, 0],
    #     [0, 0, 0, 0, 0, 0, 3, 9, 0],
    #     [8, 9, 0, 0, 0, 1, 0, 5, 4],
    #     [0, 7, 6, 0, 0, 3, 8, 2, 0],
    # ]

    hard = [
        [0, 8, 0, 5, 4, 6, 0, 0, 0],
        [0, 0, 9, 0, 0, 0, 0, 0, 4],
        [0, 5, 6, 0, 0, 9, 0, 2, 0],
        [0, 0, 0, 0, 5, 8, 0, 0, 3],
        [0, 0, 0, 6, 0, 2, 0, 0, 0],
        [6, 0, 0, 7, 9, 0, 0, 0, 0],
        [0, 3, 0, 9, 0, 0, 8, 7, 0],
        [9, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 8, 4, 0, 9, 0],
    ]


    # print(check_sudoku(answer))
    solve_sudoku(hard)
