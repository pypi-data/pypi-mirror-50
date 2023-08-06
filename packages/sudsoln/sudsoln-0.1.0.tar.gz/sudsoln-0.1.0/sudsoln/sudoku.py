
import sudsoln.candidate as candidate
import sudsoln.sarray as sarray


class Sudoku():
    '''Sudoku puzzle.'''

    def __init__(self, array, empty = '.', elements = None):
        '''(Sudoku, 2d-array of object, str[, {objects}]) -> None
        
        Precondition: 
        1. each element in elements is of length 1 if specified.
        2. (elements is None) or (len(elements) >= 4)
        3. len(empty) == 1

        Initialize Sudoku puzzle.

        >>> q_small = [  # not a np.array, but acceptable
        ...        ['1', '.', '3', '.'],
        ...        ['.', '2', '.', '.'],
        ...        ['.', '.', '.', '.'],
        ...        ['.', '.', '.', '4']
        ... ]
        ...
        >>> q_small = Sudoku(q_small)
        >>> q_small.n
        2
        >>> question1 = [  # mixture of int and str, and not a np.array
        ...     ['.', '.', '.', '.',   2, '.', '.', '.', '.'],
        ...     [  8,   3, '.',   7,   1,   4, '.',   9,   6], 
        ...     ['.',   6, '.',   9, '.',   5,   4, '.',   8], 
        ...     ['.',   9, '.',   3, '.',   1, '.', '.',   4], 
        ...     ['.',   1, '.',   4, '.',   2, '.', '.',   7], 
        ...     ['.',   7,   5, '.', '.', '.',   2,   1, '.'], 
        ...     ['.', '.',   4, '.', '.', '.',   7, '.', '.'], 
        ...     ['.', '.', '.',   5, '.',   7, '.', '.', '.'], 
        ...     ['.', '.', '.',   1,   9,   6, '.', '.', '.']
        ... ]
        ...
        >>> q1 = Sudoku(question1)
        >>> q1.n
        3
        >>> question_big = [
        ...     ['1', '6', 'F', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'E', 'G', '7'], 
        ...     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'D', '3', 'A', 'F', '8', '.'],
        ...     ['.', '.', '.', '.', '.', '.', '.', 'E', 'B', '5', 'C', 'G', '.', '.', '.', '.'],
        ...     ['.', '.', '.', '.', '.', 'G', '3', 'D', 'A', '1', '.', '.', '.', '.', 'C', '2'],
        ...     ['3', '9', '8', '.', '.', '.', '.', '.', '.', '.', '.', '.', '5', '1', 'B', 'G'],
        ...     ['B', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'E', '6', 'F', '2', 'A', '.'],
        ...     ['.', '.', '.', 'C', '.', '.', '9', 'A', '8', '7', 'B', '2', '.', '.', '.', '.'],
        ...     ['.', 'A', '1', 'E', '.', 'D', '6', 'C', '5', '3', '.', '.', '.', '.', '.', '4'],
        ...     ['F', 'B', '4', '8', '.', '.', '.', '.', '.', '.', '.', '.', '1', '7', 'E', '3'],
        ...     ['C', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '8', 'D', '4', '.', '.'],
        ...     ['.', '.', '.', '.', '.', '1', '.', 'G', '3', 'D', '6', '4', '.', '.', '.', '.'],
        ...     ['.', '.', '.', '.', '.', '3', '8', 'F', '7', 'C', '5', '.', '.', '.', '2', '9'],
        ...     ['G', '4', 'D', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '2', '9', 'F', '5'],
        ...     ['.', '.', '.', '.', '.', '.', '.', '4', '.', '.', '7', 'D', 'E', '6', '.', '.'],
        ...     ['.', '.', '.', '.', '.', '.', '2', '5', 'C', 'G', '8', 'E', '7', '.', '.', '.'],
        ...     ['.', '.', '.', '2', '.', '.', 'A', '1', '9', 'F', '.', '.', '.', '.', '3', '8']
        ... ]
        ...
        >>> q_big = Sudoku(question_big)
        >>> q_big.n
        4
        '''

        # Array type and shape
        if type(array) == str:
            raise TypeError(
                'String object is not acceptable. If you want to ' +\
                'convert a string representation of Sudoku to ' +\
                'Sudoku object, use ' +\
                'sudsoln.to_sudoku(sudoku_str, elements, empty) ' +\
                'instead.'
            )
        array = sarray.Array(array)
        if len(set(array.shape)) != 1:
            raise ValueError(
                'The shape of array must be square, ' +\
                'i.e. number of rows must be equal to number of columns.'
            )

        # Size
        n = list(set(array.shape))[0] ** .5
        if n < 2:
            raise ValueError(
                'The number of rows of array is too small; ' +\
                'it has to be at least 4.'
            )
        if int(n) != n:
            raise ValueError(
                'The number of rows of array is not compatible ' +\
                'for Sudoku puzzle; it has to be a square ' +\
                'of some integer, e.g. 9 = 3 ** 2, 16 = 4 ** 2, etc.'
            )
        
        # elements and empty
        if type(empty) != str:
            raise TypeError('empty must be of type str.')
        if len(empty) != 1:
            raise ValueError('Length of empty must be 1.')
        if elements is None:
            elements = set(array.flatten())
            if empty not in elements:
                try: # assuming it is already an answer
                    Sudoku(
                        array = array,
                        elements = elements,
                        empty = empty
                    )
                except ValueError: 
                    # It isn't in its answer form.
                    # i.e. wrong specification of empty
                    raise KeyError(
                        "empty = '" + empty + "'" + " does not exist " +\
                        "in the array. Either specify the correct " +\
                        "string denoting the emptiness in the array, " +\
                        "or change the string denoting the emptiness " +\
                        "in the array by using " +\
                        "sudsoln.change_empty(array, old, new)."
                    )
            else:
                elements.remove(empty)
            if len(elements) != n ** 2:
                raise ValueError(
                    'Length of the guessed elements is ' +\
                    str(len(elements)) + ', not ' + str(int(n ** 2)) +\
                    '. Either make sure that: ' +\
                    '1. every element in the current array contains ' +\
                    'all of your intended elements at least once, or; ' +\
                    '2. specify elements explicitly, or; ' +\
                    '3. there is exactly one string, and only one, ' +\
                    'that denotes the emptiness in the array. ' +\
                    'For example, if you try to solve a 9-by-9 sudoku ' +\
                    'whose answer form consists of integers from 1 to ' +\
                    '9, either make sure that every integer from 1 to ' +\
                    '9 shows up in the current array at least once, ' +\
                    'or explicitly specify elements = set([str(i) for ' +\
                    'i in range(1, 10)]), or see if the array uses ' +\
                    "'.' and some other string, like ',' or ' ',  to " +\
                    'denote the emptiness.'
                )
        else:
            elements = set([str(item) for item in list(elements)])
        el_test = set(array.flatten()).difference(elements.union({empty}))
        if el_test != set():
            raise ValueError(
                'There exists an element in array that is not ' +\
                'a member of elements: ' + str(el_test)
            )
        if len(elements) != n ** 2:
            raise ValueError(
                'The number of elements in elements must be ' +\
                str(int(n ** 2)) + ', not ' + str(len(elements)) + '.'
            )
        
        self.show = array
        self.n = int(n)
        self.elements = elements
        self.empty = empty


    def __eq__(self, other):
        '''(Sudoku, Sudoku) -> bool

        Return True iff all the entries of self and other are the same.
        '''

        return self.show == other.show


    def __getitem__(self, key):
        '''(Sudoku, ints/lists/slices/tuples) -> str or Array

        Return the entry of self at key.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> q1
        Sudoku(
            .    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    .
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        >>> q1[(0, 0)]
        '.'
        >>> q1[(2, 1)]
        '6'
        '''

        return self.show[key]


    def __repr__(self):
        '''(Sudoku) -> Sudoku

        Return the Sudoku representation of self.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> q1
        Sudoku(
            .    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    .
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        >>> q_big = to_sudoku(sq.q7)
        >>> q_big
        Sudoku(
            1    6    F    .    |    .    .    .    .    |    .    .    .    .    |    .    E    G    7
            .    .    .    .    |    .    .    .    .    |    .    .    D    3    |    A    F    8    .
            .    .    .    .    |    .    .    .    E    |    B    5    C    G    |    .    .    .    .
            .    .    .    .    |    .    G    3    D    |    A    1    .    .    |    .    .    C    2
        ------------------------+------------------------+------------------------+------------------------
            3    9    8    .    |    .    .    .    .    |    .    .    .    .    |    5    1    B    G
            B    .    .    .    |    .    .    .    .    |    .    .    E    6    |    F    2    A    .
            .    .    .    C    |    .    .    9    A    |    8    7    B    2    |    .    .    .    .
            .    A    1    E    |    .    D    6    C    |    5    3    .    .    |    .    .    .    4
        ------------------------+------------------------+------------------------+------------------------
            F    B    4    8    |    .    .    .    .    |    .    .    .    .    |    1    7    E    3
            C    .    .    .    |    .    .    .    .    |    .    .    .    8    |    D    4    .    .
            .    .    .    .    |    .    1    .    G    |    3    D    6    4    |    .    .    .    .
            .    .    .    .    |    .    3    8    F    |    7    C    5    .    |    .    .    2    9
        ------------------------+------------------------+------------------------+------------------------
            G    4    D    B    |    .    .    .    .    |    .    .    .    .    |    2    9    F    5
            .    .    .    .    |    .    .    .    4    |    .    .    7    D    |    E    6    .    .
            .    .    .    .    |    .    .    2    5    |    C    G    8    E    |    7    .    .    .
            .    .    .    2    |    .    .    A    1    |    9    F    .    .    |    .    .    3    8
        n: 4
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F, G
        empty: .
        )
        '''

        n = self.n
        headline, endline = 'Sudoku(\n', ')'
        midline = ''
        sep = '-----' * n + '----'
        sepline = (sep + '+') * (n - 1) + sep + '\n'
        str_self = str(self) # This is why each element has to be len 1
        j = 0
        for ind in range(0, len(str_self), n ** 2):
            j += 1
            str_row = list(str_self[ind:(ind + n ** 2)])
            for i in range(len(str_row)):
                if i != 0 and i % n == 0:
                    midline += '    |    ' + str_row[i]
                elif i == len(str_row) - 1:
                    if j % n != 0 or j == n ** 2:
                        midline += '    ' + str_row[i] + '\n'
                    else:
                        midline += '    ' + str_row[i] + '\n' + sepline
                else:
                    midline += '    ' + str_row[i]
        subsize = 'n: ' + str(self.n) + '\n'
        lst_els = list(self.elements)
        lst_els.sort()
        els = 'elements: '
        for item in enumerate(lst_els):
            if item[0] != len(lst_els) - 1:
                els += item[1] + ', '
            else:
                els += item[1] + '\n'
        emp = 'empty: ' + self.empty + '\n'
        return headline + midline + subsize + els + emp + endline


    def __setitem__(self, key, value):
        '''(Sudoku, (int, int), int/str) -> None

        Assign value to self's key.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> q1
        Sudoku(
            .    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    .
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        >>> q1[(0, 0)] = 5
        >>> q1[(8, 8)] = '5'
        >>> q1
        Sudoku(
            5    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    5
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        '''

        self.show[key] = value


    def __str__(self):
        '''(Sudoku) -> str

        Return the string representation of self.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> str(q1)
        '....2....83.714.96.6.9.54.8.9.3.1..4.1.4.2..7.75...21...4...7.....5.7......196...'
        >>> q1.solve_logically()
        >>> str(q1)
        '549628371832714596761935428298371654613452987475869213154283769986547132327196845'
        '''

        result = ''
        for item in self.show.flatten():
            result += item
        return result


    def all_missings(self):
        '''(Sudoku) -> {str: {int: set of str}}

        Return all missing values of all submatrices, rows, and columns
        of self.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> q1
        Sudoku(
            .    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    .
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        >>> q1.all_missings() == {
        ...     'submatrix': {
        ...         1: {'9', '7', '1', '2', '5', '4'}, 
        ...         2: {'3', '6', '8'}, 
        ...         3: {'7', '1', '2', '5', '3'}, 
        ...         4: {'8', '2', '3', '6', '4'}, 
        ...         5: {'9', '7', '8', '5', '6'}, 
        ...         6: {'9', '8', '5', '3', '6'}, 
        ...         7: {'9', '7', '1', '8', '2', '5', '3', '6'}, 
        ...         8: {'2', '3', '4', '8'}, 
        ...         9: {'9', '1', '8', '2', '5', '3', '6', '4'}
        ...     }, 
        ...     'row': {
        ...         0: {'9', '7', '1', '8', '5', '3', '6', '4'}, 
        ...         1: {'2', '5'}, 
        ...         2: {'3', '7', '2', '1'}, 
        ...         3: {'7', '8', '2', '5', '6'}, 
        ...         4: {'9', '8', '5', '3', '6'}, 
        ...         5: {'9', '8', '3', '6', '4'}, 
        ...         6: {'9', '1', '8', '2', '5', '3', '6'}, 
        ...         7: {'9', '1', '8', '2', '3', '6', '4'}, 
        ...         8: {'7', '8', '2', '5', '3', '4'}
        ...     }, 
        ...     'col': {
        ...         0: {'9', '7', '1', '2', '5', '3', '6', '4'}, 
        ...         1: {'2', '5', '4', '8'}, 
        ...         2: {'9', '7', '1', '8', '2', '3', '6'}, 
        ...         3: {'2', '6', '8'}, 
        ...         4: {'7', '8', '5', '3', '6', '4'}, 
        ...         5: {'9', '3', '8'}, 
        ...         6: {'9', '1', '8', '5', '3', '6'}, 
        ...         7: {'7', '8', '2', '5', '3', '6', '4'}, 
        ...         8: {'9', '1', '2', '5', '3'}
        ...     }
        ... }
        ...
        True
        '''
        
        n = self.n
        result = {'submatrix': {}, 'row': {}, 'col': {}}
        for i in range(n ** 2):
            result['submatrix'].update({i + 1: self.missing(s = i + 1)})
            result['row'].update({i: self.missing(r = i)})
            result['col'].update({i: self.missing(c = i)})
        return result


    def candidates(self):
        '''(Sudoku) -> Candidate
        
        Return all numbers that can be entered at each entry of self 
        if that entry is self.empty.

        >>> import sudsoln.questions as sq
        >>> q6 = to_sudoku(sq.q6)
        >>> q6
        Sudoku(
            .    3    |    .    4
            .    .    |    .    .
        --------------+--------------
            .    .    |    1    .
            2    .    |    .    .
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        >>> q6.candidates() == candidate.Candidate(
        ...     {
        ...         (0, 0): {'1'}, 
        ...         (0, 2): {'2'}, 
        ...         (1, 0): {'1', '4'}, 
        ...         (1, 1): {'1', '2', '4'}, 
        ...         (1, 2): {'2', '3'}, 
        ...         (1, 3): {'1', '2', '3'}, 
        ...         (2, 0): {'4', '3'}, 
        ...         (2, 1): {'4'}, 
        ...         (2, 3): {'2', '3'}, 
        ...         (3, 1): {'1', '4'}, 
        ...         (3, 2): {'4', '3'}, 
        ...         (3, 3): {'3'}
        ...     },
        ...     elements = {1, 2, 3, 4}
        ... )
        ...
        True
        '''
        
        n = self.n
        empty = self.empty
        elements = self.elements
        entries = {}
        for i in range(1, n ** 2, n): # e.g. n == 3 => 1, 4, 7
            subm, subm_missing = {}, {}
            for j in range(n): # define submatrices first
                subm[i + j] = self.submatrix(i + j)
                subm_missing[i + j] = self.missing(s = i + j)
            for K in range(n): # iterate over rows of a binded submatrix
                row_missing = self.missing(r = i + K - 1)
                subm_index = 0
                col_iters = list(range(n - 1, n ** 2, n))
                for L in range(n ** 2): # iterate over columns
                    if self.show[(i + K - 1, L)] == empty:
                        col_missing = self.missing(c = L)
                        entries[(i + K - 1, L)] =\
                            subm_missing[i + subm_index].intersection(\
                                row_missing, col_missing
                            )
                    if L == col_iters[subm_index]:
                        subm_index += 1
        return candidate.Candidate(entries, elements = elements)


    def col(self, c):
        '''(Sudoku, int) -> Array
        
        Precondition: 0 <= c <= self.n ** 2 - 1
        
        Return one of self.n ** 2 columns of self selected by c.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> q1
        Sudoku(
            .    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    .
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        >>> q1.col(3).flatten()
        ['.', '7', '9', '3', '4', '.', '.', '5', '1']
        '''
        
        return self.show[:, c]


    def copy(self):
        '''(Sudoku) -> Sudoku
        
        Return a deep copy of self.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> q1_cp = q1.copy()
        >>> q1_cp == q1
        True
        >>> id(q1_cp) != id(q1)
        True
        >>> q1_cp[0, 0] = 5
        >>> q1_cp.row(0)
        Array([
        ['5', '.', '.', '.', '2', '.', '.', '.', '.']
        ])
        >>> q1.row(0)
        Array([
        ['.', '.', '.', '.', '2', '.', '.', '.', '.']
        ])
        '''
        
        puzzle_copy = self.show.copy()
        return Sudoku(
            puzzle_copy, 
            elements = self.elements, 
            empty = self.empty
        )


    def group(self, by):
        '''(Sudoku, str) -> {int: Candidate}

        Precondition: by in ['submatrix', 'row', 'col']

        Return the candidate values grouped by 'by', which is either 
        'submatrix', 'row', or 'col'.

        >>> import sudsoln.questions as sq
        >>> q6 = to_sudoku(sq.q6)
        >>> q6
        Sudoku(
            .    3    |    .    4
            .    .    |    .    .
        --------------+--------------
            .    .    |    1    .
            2    .    |    .    .
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        >>> q6.group(by = 'submatrix') == {
        ...     1: candidate.Candidate(
        ...         {
        ...             (0, 0): {'1'}, 
        ...             (1, 0): {'4', '1'}, 
        ...             (1, 1): {'4', '2', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     2: candidate.Candidate(
        ...         {
        ...             (0, 2): {'2'}, 
        ...             (1, 2): {'3', '2'}, 
        ...             (1, 3): {'3', '2', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     3: candidate.Candidate(
        ...         {
        ...             (2, 0): {'3', '4'}, 
        ...             (2, 1): {'4'}, 
        ...             (3, 1): {'4', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     4: candidate.Candidate(
        ...         {
        ...             (2, 3): {'3', '2'}, 
        ...             (3, 2): {'3', '4'}, 
        ...             (3, 3): {'3'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     )
        ... }
        ...
        True
        >>> q6.group(by = 'row') == {
        ...     0: candidate.Candidate(
        ...         {
        ...             (0, 0): {'1'}, 
        ...             (0, 2): {'2'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     1: candidate.Candidate(
        ...         {
        ...             (1, 0): {'4', '1'}, 
        ...             (1, 1): {'4', '2', '1'}, 
        ...             (1, 2): {'3', '2'}, 
        ...             (1, 3): {'3', '2', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     2: candidate.Candidate(
        ...         {
        ...             (2, 0): {'3', '4'}, 
        ...             (2, 1): {'4'}, 
        ...             (2, 3): {'3', '2'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     3: candidate.Candidate(
        ...         {
        ...             (3, 1): {'4', '1'}, 
        ...             (3, 2): {'3', '4'}, 
        ...             (3, 3): {'3'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     )
        ... }
        ...
        True
        >>> q6.group(by = 'col') == {
        ...     0: candidate.Candidate(
        ...         {
        ...             (0, 0): {'1'}, 
        ...             (1, 0): {'4', '1'}, 
        ...             (2, 0): {'3', '4'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     1: candidate.Candidate(
        ...         {
        ...             (1, 1): {'4', '2', '1'}, 
        ...             (2, 1): {'4'}, 
        ...             (3, 1): {'4', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     2: candidate.Candidate(
        ...         {
        ...             (0, 2): {'2'}, 
        ...             (1, 2): {'3', '2'}, 
        ...             (3, 2): {'3', '4'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     3: candidate.Candidate(
        ...         {
        ...             (1, 3): {'3', '2', '1'}, 
        ...             (2, 3): {'3', '2'}, 
        ...             (3, 3): {'3'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     )
        ... }
        ...
        True
        '''

        if by not in ['submatrix', 'row', 'col']:
            raise ValueError(
                "by must be either 'submatrix', 'row', or 'col'."
            )
        return self.candidates().group(by)        
        

    def is_valid_answer(self):
        '''(Sudoku) -> bool

        Return True iff self is a valid sudoku answer, and False otherwise.

        >>> q_small = [
        ...     [  1, '.',   3, '.'],
        ...     ['.',   2, '.', '.'],
        ...     ['.', '.', '.', '.'],
        ...     ['.', '.', '.',   4]
        ... ]
        ...
        >>> q_small = Sudoku(q_small)
        >>> q_small
        Sudoku(
            1    .    |    3    .
            .    2    |    .    .
        --------------+--------------
            .    .    |    .    .
            .    .    |    .    4
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        >>> q_small.is_valid_answer()
        False
        >>> q_small.solve_logically()
        >>> q_small
        Sudoku(
            1    4    |    3    2
            3    2    |    4    1
        --------------+--------------
            4    1    |    2    3
            2    3    |    1    4
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        >>> q_small.is_valid_answer()
        True
        '''

        n = self.n
        empty = self.empty
        elements = self.elements
        if empty in self.show.flatten(): # not even finished yet
            return False
        for i in range(n ** 2):
            if elements != set(self.submatrix(i + 1).flatten()):
                return False
            elif elements != set(self.row(i).flatten()):
                return False
            elif elements != set(self.col(i).flatten()):
                return False
        return True


    def itemset(self, entry, value):
        '''(Sudoku, (int, int), int/str) -> None

        Precondition: 
        1. value in self.elements
        2. each int in entry is from 0 to self.n ** 2 - 1 inclusive.

        Mutate entry number of self to value.

        >>> q_small = [
        ...     [  1, '.',   3, '.'],
        ...     ['.',   2, '.', '.'],
        ...     ['.', '.', '.', '.'],
        ...     ['.', '.', '.',   4]
        ... ]
        ...
        >>> q_small = Sudoku(q_small)
        >>> q_small
        Sudoku(
            1    .    |    3    .
            .    2    |    .    .
        --------------+--------------
            .    .    |    .    .
            .    .    |    .    4
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        >>> q_small.itemset((0, 1), 4)
        >>> q_small
        Sudoku(
            1    4    |    3    .
            .    2    |    .    .
        --------------+--------------
            .    .    |    .    .
            .    .    |    .    4
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        '''

        self.show.itemset(entry, value)


    def itemsets(self, entries):
        '''(Sudoku, Candidate or {(int, int): set of ints/strs}) -> None

        Precondition: each int in entries is exactly one element of 
        self.elements.

        Mutate entry number of self according to values given in entries 
        if the value set has length 1.

        >>> q_small = [
        ...     [  1, '.',   3, '.'],
        ...     ['.',   2, '.', '.'],
        ...     ['.', '.', '.', '.'],
        ...     ['.', '.', '.',   4]
        ... ]
        ...
        >>> q_small = Sudoku(q_small, elements = {'1', '2', '3', '4'})
        >>> candids = q_small.candidates()
        >>> candids == candidate.Candidate(
        ...     {
        ...         (0, 1): {'4'}, 
        ...         (0, 3): {'2'}, 
        ...         (1, 0): {'3', '4'}, 
        ...         (1, 2): {'1', '4'}, 
        ...         (1, 3): {'1'}, 
        ...         (2, 0): {'3', '2', '4'}, 
        ...         (2, 1): {'3', '1', '4'}, 
        ...         (2, 2): {'1', '2'}, 
        ...         (2, 3): {'3', '1', '2'}, 
        ...         (3, 0): {'3', '2'}, 
        ...         (3, 1): {'3', '1'}, 
        ...         (3, 2): {'1', '2'}
        ...     },
        ...     elements = {1, 2, 3, 4}
        ... )
        ...
        True
        >>> q_small
        Sudoku(
            1    .    |    3    .
            .    2    |    .    .
        --------------+--------------
            .    .    |    .    .
            .    .    |    .    4
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        >>> q_small.itemsets(candids)
        >>> q_small
        Sudoku(
            1    4    |    3    2
            .    2    |    .    1
        --------------+--------------
            .    .    |    .    .
            .    .    |    .    4
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        '''

        if type(entries) == dict:
            if entries == {}:
                return None
            for entry, values in entries.items():
                if len(values) == 1:
                    self.itemset(entry, list(values)[0])
        elif 'Candidate' in str(type(entries)):
            elements = self.elements
            if entries == candidate.Candidate({}, elements = elements):
                return None
            for entry, values in entries.items():
                if len(values) == 1:
                    self.itemset(entry, list(values)[0])


    def melt(self, include_empty = True):
        '''(Sudoku, bool) -> Candidate

        Return Candidate form of self, and include empty entries
        as well if include_empty is True (by default).

        >>> import numpy as np
        >>> q_small = np.array([
        ...     [  1, '.',   3, '.'],
        ...     ['.',   2, '.', '.'],
        ...     ['.', '.', '.', '.'],
        ...     ['.', '.', '.',   4]
        ... ])
        ...
        >>> q_small = Sudoku(q_small)
        >>> q_small.melt() == candidate.Candidate(
        ... {
        ...     (0, 0): {'1'}, (0, 1): {'.'}, (0, 2): {'3'}, (0, 3): {'.'}, 
        ...     (1, 0): {'.'}, (1, 1): {'2'}, (1, 2): {'.'}, (1, 3): {'.'}, 
        ...     (2, 0): {'.'}, (2, 1): {'.'}, (2, 2): {'.'}, (2, 3): {'.'}, 
        ...     (3, 0): {'.'}, (3, 1): {'.'}, (3, 2): {'.'}, (3, 3): {'4'}
        ... }, 
        ... elements = {1, 2, 3, 4}
        ... )
        ...
        True
        >>> q_small.melt(include_empty = False) == candidate.Candidate(
        ... {
        ...     (0, 0): {'1'}, (0, 2): {'3'}, (1, 1): {'2'}, (3, 3): {'4'}
        ... }, 
        ... elements = {1, 2, 3, 4}
        ... )
        ...
        True
        '''

        n = self.n
        empty = self.empty
        result = {}
        for i in range(n ** 2):
            for j in range(n ** 2):
                result[(i, j)] = {self.show[(i, j)]}
        if not include_empty:
            result_copy = result.copy()
            for k, v in result_copy.items():
                if list(v)[0] == empty:
                    result.pop(k)
        return candidate.Candidate(result, elements = self.elements)


    def missing(self, s = None, r = None, c = None):
        '''(Sudoku[, int, int, int]) -> set of str
        
        Precondition: 
        1. 1 <= s <= self.n ** 2
        2. 0 <= r <= self.n ** 2 - 1
        3. 0 <= c <= self.n ** 2 - 1
        
        Return all missing values of self at the specified submatrix 
        number s, the specified row number r, or the specified column 
        number c.
        If s is specified, then r and c will be ignored;
        if s is None and r is specified, then c will be ignored;
        If neither s, r, nor c are specified, the function returns None.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> q1
        Sudoku(
            .    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    .
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        >>> q1.missing(s = 1) == {'2', '5', '4', '9', '7', '1'}
        True
        >>> q1.missing(r = 3) == {'6', '2', '8', '5', '7'}
        True
        >>> q1.missing(c = 8) == {'3', '2', '5', '9', '1'}
        True
        '''
        
        elements = self.elements
        if s is not None:
            return elements.difference(set(self.submatrix(s).flatten()))
        elif r is not None:
            return elements.difference(set(self.row(r).flatten()))
        elif c is not None:
            return elements.difference(set(self.col(c).flatten()))


    def row(self, r):
        '''(Sudoku, int) -> Array
        
        Precondition: 0 <= r <= self.n ** 2 - 1
        
        Return one of self.n ** 2 rows of self selected by r.

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)        
        >>> q1
        Sudoku(
            .    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    .
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        >>> q1.row(2)
        Array([
        ['.', '6', '.', '9', '.', '5', '4', '.', '8']
        ])
        '''
        
        return self.show[r, :]


    def solve(self, max_trial = 200, quietly = False, seed = None):
        '''(Sudoku, int, bool[, int]) -> str, int

        Mutate self to the answer form, or until max_trial is met, and
        return the time it took to compute the answer and the number of 
        trials used. seed can be given for reproducibility. Set 
        quietly = True to display no messages.
        '''

        trial = 0
        import datetime
        n = self.n
        empty = self.empty
        start = datetime.datetime.now()
        self.solve_logically()
        sudoku_copy = self.copy()
        sudoku_copy_melted = sudoku_copy.melt()
        if empty in self.show.flatten():
            if not quietly:
                msg = "Logical approaches weren't enough. " +\
                    "Solving with a brute force..."
                print(msg)
            trial += self.solve_forcefully(
                max_trial = max_trial, 
                quietly = quietly,
                seed = seed
            )
        end = datetime.datetime.now()
        if self.is_valid_answer():
            return str(end - start), trial
        else:
            if not quietly:
                print('Mission failed; max_trial of', max_trial, 'met.')
            self.itemsets(sudoku_copy_melted)
            return str(end - start), max_trial


    def solve_by_hidden_pairs(self, by = 'submatrix', start = None):
        '''(Sudoku, str[, Candidate]) -> Candidate

        Mutate self using the hidden pairs method based on 'by'. Starting 
        candidate can be specified with 'start' argument; if start is 
        None, then self.candidates() will be the starting point.
        '''

        return self.solve_by(
            by = by, start = start,
            condition = ['contains', 2], deep = True
        )


    def solve_by(
            self, 
            by, 
            start = None, 
            condition = ['contains', 1], 
            deep = False
        ):
        '''(Sudoku, str[, Candidate, [str, int], bool]) -> Candidate

        Precondition: by in ['row', 'col', 'submatrix']

        Solve self by methods involving pairs, triples, or a higher order.
        '''

        elements = self.elements
        bases = ['row', 'col', 'submatrix']
        bases.remove(by)
        names = bases
        if start is None:
            candidates_global = self.candidates()
            candidates_group = self.group(by = by)
        else:
            candidates_global = start
            candidates_group = start.group(by = by)

        changing = True
        while changing:
            sudoku_copy = self.copy()
            etm = candidate.Candidate({}, elements = elements)
            cg_cp = candidates_group.copy()
            for V in cg_cp.values():
                appearances = V.appearances(names)
                appearances.sieve(condition = condition, deep = deep)
                candidates_global.refine(
                    etm, 
                    appearances = appearances,
                    condition = condition,
                    deep = deep
                )
            self.itemsets(etm)
            self.itemsets(candidates_global)
            candidates_group = candidates_global.group(by = by)
            if self == sudoku_copy and cg_cp == candidates_group:
                changing = False
        return candidates_global


    def solve_by_pointing_pairs(self, by = 'submatrix', start = None):
        '''(Sudoku, str[, Candidate]) -> Candidate

        Precondition: by in ['row', 'col', 'submatrix']

        Say bases = ['row', 'col', 'submatrix'], and one item is removed by
        bases.remove(by). Define the two leftovers in bases as group1 and 
        group2 respectively. This method eliminates candidate numbers in 
        other entries of the same group1 (e.g. rows) or group2 
        (e.g. columns) based on entries of 'by' (e.g. submatrix) it 
        belongs, mutate self into the closest answer form, and return a 
        refined Candidate (better than self.candidates() in a sense that 
        it has fewer, equal at worst, candidate numbers at each entry) 
        based on iterations. Starting candidate can be specified with
        'start' argument; if start is None, then self.candidates() will be
        the starting point.
        '''

        return self.solve_by(
            by = by, start = start,
            condition = ['contains', 1], deep = False
        )


    def solve_forcefully(
            self,
            max_trial = 300, 
            quietly = False,
            seed = None
        ):
        '''(Sudoku, int, bool[, int or None]) -> int

        Try out candidate numbers in each entry randomly until self is 
        mutated into the answer form, or until max_trial is met. seed
        can be given for reproducibility. Set quietly = True if you don't 
        want to display any messages.
        '''

        import random
        if seed is not None:
            random.seed(seed)
        trial = 1
        empty = self.empty
        sudoku_melt = self.melt()
        while empty in self.show.flatten():
            if empty not in self.show.flatten():
                return trial
            entries = self.solve_logically()
            if set() in list(entries.values()):
                if not quietly:
                    print(
                        "Trial number", trial, 
                        "out of", max_trial, "failed;",
                        "proceeding to the next trial..."
                    )
                trial += 1
                if trial == max_trial:
                    return max_trial
                self.itemsets(sudoku_melt)
            else:
                keys = list(entries.keys()); keys.sort()
                guess = random.choice(list(entries[keys[0]]))
                self.itemset(keys[0], guess)
                self.solve_logically()
                if empty not in self.show.flatten() and \
                    not self.is_valid_answer():
                    self.itemsets(sudoku_melt)
        return trial


    def solve_globally(self):
        '''(Sudoku) -> None

        Find the only possible number at each entry of self, plug it 
        into that entry, and repeat the process until no new mutation 
        is made.
        '''

        changing = True
        while changing:
            sudoku_copy = self.copy()
            possible_numbers = self.candidates()
            for k, v in possible_numbers.items():
                if len(v) == 1:
                    self.itemset(k, list(v)[0])
            if sudoku_copy == self:
                changing = False


    def solve_locally(self, by):
        '''(Sudoku, str) -> None

        Precondition: by in ['submatrix', 'row', 'col']

        Find the unique candidate number within each 'by' of self,
        plug that number into that entry, and repeat the process across
        every other groups until no new mutation is made.
        '''

        changing = True
        while changing:
            sudoku_copy = self.copy()
            possible_numbers = self.unique_candidates(by = by)
            for k, v in possible_numbers.items():
                if len(v) == 1:
                    self.itemset(k, list(v)[0])
            if sudoku_copy == self:
                changing = False


    def solve_logically(self):
        '''(Sudoku) -> Candidate or None

        Mutate self to the answer form as close as possible (that is, 
        having the least number of empty's), using only logical 
        approaches that don't involve randomness or brute force in number
        assignment. Return Candidate if .solve_by*() methods have involved,
        and None otherwise.
        '''

        empty = self.empty
        sudoku_copy = self.copy()

        bases = ['submatrix', 'row', 'col']
        not_ready = True
        there_is_a_progress = True
        
        while there_is_a_progress:
            sudoku_copy_after_iter = self.copy()
            self.solve_globally()
            if empty not in str(self):
                return None
            for component in bases:
                self.solve_locally(by = component)
                self.solve_globally()
                if empty not in str(self):
                    return None

            start = self.solve_by_pointing_pairs()
            for component2 in bases:
                self.solve_by_hidden_pairs(by = component2, start = start)
                self.solve_by_pointing_pairs(start = start)

            if (sudoku_copy == self or sudoku_copy_after_iter == self):
                there_is_a_progress = False
        return start


    def submatrix(self, s):
        '''(Sudoku, int) -> Array

        Precondition: 1 <= s <= self.n ** 2
        
        Return one of self.n ** 2 submatrices of self selected by s.        

        >>> import sudsoln.questions as sq
        >>> q1 = to_sudoku(sq.q1)
        >>> q1
        Sudoku(
            .    .    .    |    .    2    .    |    .    .    .
            8    3    .    |    7    1    4    |    .    9    6
            .    6    .    |    9    .    5    |    4    .    8
        -------------------+-------------------+-------------------
            .    9    .    |    3    .    1    |    .    .    4
            .    1    .    |    4    .    2    |    .    .    7
            .    7    5    |    .    .    .    |    2    1    .
        -------------------+-------------------+-------------------
            .    .    4    |    .    .    .    |    7    .    .
            .    .    .    |    5    .    7    |    .    .    .
            .    .    .    |    1    9    6    |    .    .    .
        n: 3
        elements: 1, 2, 3, 4, 5, 6, 7, 8, 9
        empty: .
        )
        >>> q1.submatrix(1)
        Array([
        ['.', '.', '.'],
        ['8', '3', '.'],
        ['.', '6', '.']
        ])
        >>> q1.submatrix(3)
        Array([
        ['.', '.', '.'],
        ['.', '9', '6'],
        ['4', '.', '8']
        ])
        >>> q1.submatrix(4)
        Array([
        ['.', '9', '.'],
        ['.', '1', '.'],
        ['.', '7', '5']
        ])
        '''
        
        n = self.n
        number = 0
        for i in range(n, n ** 2 + 1, n):
            for j in range(n, n ** 2 + 1, n):
                number += 1
                if number == s:
                    return self.show[(i - n):(i), (j - n):(j)]


    def unique_candidates(self, by):
        '''(Sudoku, str) -> Candidate

        Precondition: by in ['submatrix', 'row', 'col']
        
        Return the unique candidate number at each entry, within each 
        group of self, grouped by 'by'.
        
        >>> q_small = '1.3..2.........4'
        >>> q_small = to_sudoku(q_small, elements = {1, 2, 3, 4})
        >>> q_small
        Sudoku(
            1    .    |    3    .
            .    2    |    .    .
        --------------+--------------
            .    .    |    .    .
            .    .    |    .    4
        n: 2
        elements: 1, 2, 3, 4
        empty: .
        )
        >>> q_small.unique_candidates('submatrix') ==\\
        ...     candidate.Candidate({
        ...                    (0, 1): set(),                (0, 3): {'2'}, 
        ...     (1, 0): {'3'},                (1, 2): {'4'}, (1, 3): set(), 
        ...     (2, 0): set(), (2, 1): set(), (2, 2): set(), (2, 3): {'3'},
        ...     (3, 0): set(), (3, 1): set(), (3, 2): set()
        ...     }, 
        ...     elements = {1, 2, 3, 4}
        ... )
        ...
        True
        >>> q_small.unique_candidates('row') ==\\
        ...     candidate.Candidate({
        ...                    (0, 1): {'4'},                (0, 3): {'2'}, 
        ...     (1, 0): {'3'},                (1, 2): set(), (1, 3): set(), 
        ...     (2, 0): set(), (2, 1): set(), (2, 2): set(), (2, 3): set(),
        ...     (3, 0): set(), (3, 1): set(), (3, 2): set()
        ...     }, 
        ...     elements = {1, 2, 3, 4}
        ... )
        ...
        True
        >>> q_small.unique_candidates('col') ==\\
        ...     candidate.Candidate({
        ...                    (0, 1): set(),                (0, 3): set(),
        ...     (1, 0): set(),                (1, 2): {'4'}, (1, 3): set(),
        ...     (2, 0): set(), (2, 1): set(), (2, 2): set(), (2, 3): {'3'},
        ...     (3, 0): set(), (3, 1): set(), (3, 2): set()
        ...     }, 
        ...     elements = {1, 2, 3, 4}
        ... )
        ...
        True
        '''

        n = self.n
        start = self.group(by = by)
        elements = self.elements
        result = candidate.Candidate({}, elements = elements)
        for V in start.values():
            keys = list(V.keys()); keys.sort() # sorting is unnecessary
            for i in range(len(keys)):
                blacklist, the_rest = [], set()
                blacklist.append(keys[i])
                for k, v in V.items():
                    if k not in blacklist:
                        the_rest.update(v)
                possible_nums = V[keys[i]].difference(the_rest)
                result.update({keys[i]: possible_nums})
        return result



def change_empty(array, old, new):
    '''(2d-array of objects, str, str) -> None

    Precondition: len(new) == 1

    Mutate array by replacing olds with new.

    >>> eg = [  
    ...     ['1', '.', '3', '.'],
    ...     ['.', '2', '.', '.'],
    ...     ['.', '.', '.', '.'],
    ...     ['.', '.', '.', '4']
    ... ]
    ...
    >>> change_empty(eg, '.', ' ')
    >>> eg == [  
    ...     ['1', ' ', '3', ' '],
    ...     [' ', '2', ' ', ' '],
    ...     [' ', ' ', ' ', ' '],
    ...     [' ', ' ', ' ', '4']
    ... ]
    ...
    True
    '''

    assert len(new) == 1, 'len(new) != 1'
    ch_old = lambda x: new if x == old else x
    if 'ndarray' in str(type(array)) or 'list' in str(type(array)):
        for i in range(len(array)):
            array[i] = list(map(ch_old, array[i]))
    elif 'Array' in str(type(array)):
        shape = array.shape
        for i in range(len(array.show)):
            array.show[i] = list(map(ch_old, array.show[i]))
    else:
        raise TypeError(str(type(array)) + ' not supported')


def fprint(Sudoku):
    '''(Sudoku) -> None

    Print out the formatted version of Sudoku.
    '''

    n = Sudoku.n
    the_range = range(0, n ** 4 + 1, n ** 2)
    item = ''
    result = ''
    sudoku_lst = list(str(Sudoku))
    for c in enumerate(sudoku_lst):
        item += c[1]
        if c[0] != 0 and c[0] + 1 in the_range:
            if c[0] != n ** 4 - 1:
                result += item + '\n'
            else:
                result += item + ''
            item = ''
    print(result)


def to_sudoku(sudoku_str, elements = None, empty = '.'):
    '''(str[, {objects} or None, str]) -> Sudoku

    Preconditions if elements is not None:
    1. set(list(sudoku_str)).issubset(elements.union(empty))
    2. len(elements) == len(sudoku_str) ** .5
    3. All elements in elements has len 1, as well as empty.

    Return the Sudoku object of sudoku_str if it is a string 
    representation of Sudoku.
    '''

    n = int(len(sudoku_str) ** .25)
    array = sarray.Array(list(sudoku_str[:(n**4)])).reshape(n**2, n**2)
    return Sudoku(
        array = array, 
        elements = elements, 
        empty = empty
    )



if __name__ == '__main__':
    import doctest
    doctest.testmod()
