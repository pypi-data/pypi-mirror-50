
import candidate
import sudoku
import questions

def formatting(sudoku_str):
    n = int(len(sudoku_str) ** .25)
    the_range = range(0, n ** 4 + 1, n ** 2)
    item = ''
    result = "'"
    sudoku_lst = list(sudoku_str)
    for c in enumerate(sudoku_lst):
        item += c[1]
        if c[0] != 0 and c[0] + 1 in the_range:
            if c[0] != n ** 4 - 1:
                result += item + "' +\\\n'"
            else:
                result += item + "'"
            item = ''
    print(result)

if __name__ == '__main__':
    qhrd4 = sudoku.to_sudoku(
        questions.q_top95_4,
        elements = set([i for i in range(1, 10)])
    )
    print(qhrd4)
    print(qhrd4.submatrix(3))
    print(qhrd4.group('submatrix')[3])
    print(qhrd4.group('submatrix')[3].appearances(['col', 'submatrix']))
