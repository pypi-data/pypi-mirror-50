
# START: Candidate #######################################################

class Candidate():
    '''Sudoku puzzle candidate collection.'''

    def __init__(self, candidates, elements = None):
        '''(Candidate, {(int, int): set of ints/strs}) -> None

        Precondition: 
        1. ints in "(int, int)" are from 0 to n ** 2 - 1 
        inclusive, where n is a Sudoku class attribute.
        2. objects in "set of objects" are elements of self.elements, 
        one of Sudoku class attributes.

        Initialize Candidate object.
        
        >>> eg = {(0, 1): {1, 2, 4}, (0, 2): {6, 9}}
        >>> eg = Candidate(
        ...     eg, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> eg.n
        3
        '''

        assert elements != None, \
            'elements of Candidate must be specified'
        elements = set(map(lambda x: str(x), list(elements)))
        n = int(len(elements) ** .5)

        if candidates != {}:
            for k, v in candidates.items():
                candidates[k] = set(map(lambda x: str(x), list(v)))

        self.show = candidates
        self.n = n
        self.elements = elements


    def __dict__(self):
        '''(Candidate) -> {(int, int): set of ints/strs}

        Return the dict representation of Candidate.

        >>> eg = {(0, 1): {1, 2, 4}, (0, 2): {6, 9}}
        >>> eg = Candidate(
        ...     eg, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> dict(eg) == {(0, 1): {'1', '2', '4'}, (0, 2): {'9', '6'}}
        True
        '''

        return self.show


    def __eq__(self, other):
        '''(Candidate, Candidate) -> bool

        Return True iff keys and values of each key matches between
        self and other.

        >>> eg1 = Candidate(
        ...     {(0, 1): {1, 2, 4}, (0, 2): {6, 9}}, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> eg2 = Candidate(
        ...     {(0, 1): {'1', '2', '4'}, (0, 2): {'9', '6'}}, 
        ...     elements = set([i for i in range(1, 10)])
        ... )
        ...
        >>> eg3 = Candidate(
        ...     {(0, 1): {1, 2, 7}, (0, 3): {6, 8}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> eg1 == eg2
        True
        >>> eg1 == eg3
        False
        '''

        return self.show == other.show and\
            self.elements == other.elements


    def __getitem__(self, key):
        '''(Candidate, (int, int)) -> set of str

        Return the value of self at key.

        >>> eg = {(0, 1): {1, 2, 4}, (0, 2): {6, 9}}
        >>> eg = Candidate(
        ...     eg, 
        ...     elements = set([i for i in range(1, 10)])
        ... )
        ...
        >>> eg[(0, 1)] == {'1', '2', '4'}
        True
        '''

        return self.show[key]


    def __repr__(self):
        '''(Candidate) -> Candidate

        Return the Candidate representation of self.
        '''

        n = self.n
        elements = self.elements
        headline = 'Candidate(\n{\n'
        mid = ''
        endline = "}},\nelements = {0}\n)\n(n: {1})".format(elements, n)
        si = self.items()
        for item in enumerate(si):
            if item[0] == 0:
                mid += "{0}: {1},\n".format(item[1][0], item[1][1])
            elif item[0] == len(si) - 1:
                mid += "{0}: {1},\n".format(item[1][0], item[1][1])
            else:
                mid += "{0}: {1},\n".format(item[1][0], item[1][1])
        return headline + mid + endline


    def __setitem__(self, key, value):
        '''(Candidate, (int, int), set of ints/strs) -> None

        Assign value to key that either already exists in self, or 
        initialize key with value if key doesn't already
        exist.

        >>> eg = {(0, 1): {1, 2, 4}, (0, 2): {6, 9}}
        >>> eg = Candidate(
        ...     eg, 
        ...     elements = set([i for i in range(1, 10)])
        ... )
        ...
        >>> eg[(1, 2)] = {7}
        >>> eg == Candidate(
        ...     {(0, 1): {1, 2, 4}, (0, 2): {6, 9}, (1, 2): {7}},
        ...     elements = set([i for i in range(1, 10)])
        ... )
        ...
        True
        >>> eg[(0, 1)] = {1}
        >>> eg == Candidate(
        ...     {(0, 1): {1}, (0, 2): {6, 9}, (1, 2): {7}},
        ...     elements = set([i for i in range(1, 10)])
        ... )
        ...
        True
        '''

        value = set(map(lambda x: str(x), list(value)))
        self.show[key] = value


    def appearances(self, names):
        '''(Candidate, [str, str]) -> Appearance

        Define union1 and union2 as the aggregated unions of self with
        name in names. Count the number of the same elements in union1 and 
        union2 respectively, record them into the very first element 
        (a list of two ints) of the resulting dictionary's value list, 
        and add the key of self to the second element (a set) of the value
        list if the value of self contains the element in either union1 or
        union2. Appearances in elements are to be counted.

        >>> V = Candidate({ # candidates of submatrix1
        ...         (0, 1): {'5', '4', '7', '9'}, 
        ...         (1, 0): {'9', '4'}, 
        ...         (1, 1): {'5', '4', '6', '9'}, 
        ...         (1, 2): {'5', '4', '6', '9'}, 
        ...         (2, 1): {'5', '4', '7', '9', '6'}
        ...     },
        ...     elements = set([i for i in range(1, 10)])
        ... )
        ...
        >>> appearances = V.appearances(names = ['row', 'col'])
        >>> appearances.show == {
        ...     '1': [[0, 0], set()], 
        ...     '2': [[0, 0], set()], 
        ...     '3': [[0, 0], set()], 
        ...     '4': [[3, 3], {(0, 1), (1, 2), (2, 1), (1, 0), (1, 1)}], 
        ...     '5': [[3, 2], {(0, 1), (2, 1), (1, 1), (1, 2)}], 
        ...     '6': [[2, 2], {(1, 2), (1, 1), (2, 1)}], 
        ...     '7': [[2, 1], {(0, 1), (2, 1)}], 
        ...     '8': [[0, 0], set()], 
        ...     '9': [[3, 3], {(0, 1), (1, 2), (2, 1), (1, 0), (1, 1)}]
        ... }
        ...
        True
        '''

        return Appearance(C = self, names = names)


    def copy(self):
        '''(Candidate) -> Candidate

        Return the deep copy of self.

        >>> eg = {(0, 1): {1, 2, 4}, (0, 2): {6, 9}}
        >>> eg = Candidate(
        ...     eg, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> eg_copy = eg.copy()
        >>> id(eg) != id(eg_copy)
        True
        >>> id(eg[(0, 2)]) != id(eg_copy[(0, 2)])
        True
        '''

        copied = {}
        for k, v in self.items():
            copied[k] = v.copy()
        return Candidate(copied.copy(), elements = self.elements)

    
    def group(self, by):
        '''(Candidate, str) -> {int: Candidate}

        Precondition: by == 'submatrix' or 'row' or 'col'

        Return the candidate values grouped by 'by', which is either
        'submatrix', 'row', or 'col'.

        >>> import sudsoln as ss
        >>> import sudsoln.questions as sq
        >>> q6 = ss.to_sudoku(sq.q6, elements = {1, 2, 3, 4})
        >>> q6 = q6.candidates()
        >>> q6.group(by = 'submatrix') == {
        ...     1: Candidate(
        ...         {
        ...             (0, 0): {'1'}, 
        ...             (1, 0): {'4', '1'}, 
        ...             (1, 1): {'4', '2', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     2: Candidate(
        ...         {
        ...             (0, 2): {'2'}, 
        ...             (1, 2): {'3', '2'}, 
        ...             (1, 3): {'3', '2', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     3: Candidate(
        ...         {
        ...             (2, 0): {'3', '4'}, 
        ...             (2, 1): {'4'}, 
        ...             (3, 1): {'4', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     4: Candidate(
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
        ...     0: Candidate(
        ...         {
        ...             (0, 0): {'1'}, 
        ...             (0, 2): {'2'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     1: Candidate(
        ...         {
        ...             (1, 0): {'4', '1'}, 
        ...             (1, 1): {'4', '2', '1'}, 
        ...             (1, 2): {'3', '2'}, 
        ...             (1, 3): {'3', '2', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     2: Candidate(
        ...         {
        ...             (2, 0): {'3', '4'}, 
        ...             (2, 1): {'4'}, 
        ...             (2, 3): {'3', '2'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     3: Candidate(
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
        ...     0: Candidate(
        ...         {
        ...             (0, 0): {'1'}, 
        ...             (1, 0): {'4', '1'}, 
        ...             (2, 0): {'3', '4'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     1: Candidate(
        ...         {
        ...             (1, 1): {'4', '2', '1'}, 
        ...             (2, 1): {'4'}, 
        ...             (3, 1): {'4', '1'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     2: Candidate(
        ...         {
        ...             (0, 2): {'2'}, 
        ...             (1, 2): {'3', '2'}, 
        ...             (3, 2): {'3', '4'}
        ...         },
        ...         elements = {1, 2, 3, 4}
        ...     ), 
        ...     3: Candidate(
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
                "by must be either 'submatrix', 'row', or 'col', not " +\
                "'" + str(by) + "'."
            )
        result = {}
        n = self.n
        if by == 'submatrix':
            for g in range(1, n ** 2 + 1):
                result[g] = Candidate({}, elements = self.elements)
            number = 0
            for i in range(n, n ** 2 + 1, n):
                for j in range(n, n ** 2 + 1, n):
                    number += 1
                    for k, v in self.items():
                        if i - n <= k[0] < i and j - n <= k[1] < j:
                            result[number].update({k: v})
            return result
        for g in range(n ** 2):
            result[g] = Candidate({}, elements = self.elements)
            for k, v in self.items():
                if (by == 'row' and k[0] == g) or\
                    (by == 'col' and k[1] == g):
                    result[g].update({k: v})
        return result

    
    def items(self):
        '''(Candidate) -> dict_items

        Return dict_items of self.
        '''

        return self.show.items()

    
    def keys(self):
        '''(Candidate) -> dict_keys

        Return dict_keys of self.

        >>> eg1 = {(0, 1): {1, 2, 4}, (0, 2): {6, 9}}
        >>> eg1 = Candidate(
        ...     eg1, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> eg1.keys()
        dict_keys([(0, 1), (0, 2)])
        '''

        return self.show.keys()


    def pop(self, key):
        '''(Candidate) -> None

        Pop out key and the respective value from self.

        >>> eg1 = Candidate(
        ...     {(0, 1): {1, 2, 4}, (0, 2): {6, 9}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> eg1 == Candidate(
        ...     {(0, 1): {1, 2, 4}, (0, 2): {9, 6}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        >>> eg1.pop((0, 1))
        >>> eg1 == Candidate(
        ...     {(0, 2): {9, 6}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        '''

        self.show.pop(key)

    
    def refine(
            self, 
            entries_to_mutate, 
            appearances = None, 
            names = None,
            sieve = False,
            condition = ['contains', 1],
            deep = False
        ):
        '''(Candidate, Candidate, Appearance or None, [str, str] or None,
            bool, [str, int], bool) -> None

        Preconditions: 
        1. names is not None if appearances is None
        2. (condition, deep) == (['contains', 1], False) or 
           (condition, deep) == (['contains', 2], True), irrespective of 
           whether sieve is True or False

        Update self and entries_to_mutate by the following rule(s):
        1. if (condition, deep) = (['contains', 1], False) (default), then:
            any unique candidate number and the respective entry according
            to appearances is added to entries_to_mutate, and any candidate
            number that should be eliminated from some values of self due 
            to the uniqueness of candidate number in a certain names[0]
            (e.g. row) or names[1] (e.g. column) in appearances is 
            eliminated. 
        2. if (condition, deep) = (['contains', 2], True), then:
            for keys in appearances (e.g. '1', '6') whose first item of 
            the value list contains 2 (i.e. [2, x] or [x, 2]) AND the 
            second item are the same, eliminate all candidates at 
            self's entries that belong to the second item of the value 
            list except those candidates that match keys in appearances.
        If sieve = False, then deep will be ignored; if sieve = True, then 
        appearances.sieve(condition, deep) will be applied. That is, 
        depending on (condition, deep), refinement process will be
        different.

        >>> candids_old = Candidate({
        ...     (0, 0): {'4', '9', '7', '5', '1'}, 
        ...     (0, 1): {'5', '4'}, 
        ...     (0, 2): {'9', '1', '7'}, 
        ...     (0, 3): {'8', '6'}, 
        ...     (0, 5): {'3', '8'}, 
        ...     (0, 6): {'1', '3', '5'}, 
        ...     (0, 7): {'5', '7', '3'}, 
        ...     (0, 8): {'1', '3', '5'}, 
        ...     (1, 2): {'2'}, 
        ...     (1, 6): {'5'}, 
        ...     (2, 0): {'2', '1', '7'}, 
        ...     (2, 2): {'2', '1', '7'}, 
        ...     (2, 4): {'3'}, 
        ...     (2, 7): {'2', '7', '3'}, 
        ...     (3, 0): {'2', '6'}, 
        ...     (3, 2): {'2', '8', '6'}, 
        ...     (3, 4): {'5', '7', '8', '6'}, 
        ...     (3, 6): {'5', '8', '6'}, 
        ...     (3, 7): {'5', '8', '6'}, 
        ...     (4, 0): {'3', '6'}, 
        ...     (4, 2): {'3', '8', '6'}, 
        ...     (4, 4): {'5', '8', '6'}, 
        ...     (4, 6): {'9', '8', '5', '3', '6'}, 
        ...     (4, 7): {'5', '3', '8', '6'}, 
        ...     (5, 0): {'3', '6', '4'}, 
        ...     (5, 3): {'8', '6'}, 
        ...     (5, 4): {'8', '6'}, 
        ...     (5, 5): {'9', '8'}, 
        ...     (5, 8): {'9', '3'}, 
        ...     (6, 0): {'9', '1', '5', '3', '6', '2'}, 
        ...     (6, 1): {'2', '8', '5'}, 
        ...     (6, 3): {'2', '8'}, 
        ...     (6, 4): {'3', '8'}, 
        ...     (6, 5): {'3', '8'}, 
        ...     (6, 7): {'8', '5', '3', '6', '2'}, 
        ...     (6, 8): {'9', '2', '5', '3', '1'}, 
        ...     (7, 0): {'9', '2', '3', '6', '1'}, 
        ...     (7, 1): {'2', '8'}, 
        ...     (7, 2): {'9', '1', '8', '3', '6', '2'}, 
        ...     (7, 4): {'3', '8', '4'}, 
        ...     (7, 6): {'9', '8', '3', '6', '1'}, 
        ...     (7, 7): {'4', '8', '3', '6', '2'}, 
        ...     (7, 8): {'9', '1', '3', '2'}, 
        ...     (8, 0): {'5', '7', '3', '2'}, 
        ...     (8, 1): {'2', '8', '5'}, 
        ...     (8, 2): {'2', '7', '8', '3'}, 
        ...     (8, 6): {'5', '3', '8'}, 
        ...     (8, 7): {'4', '8', '5', '3', '2'}, 
        ...     (8, 8): {'2', '3', '5'}
        ... },
        ... elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> candids = candids_old.copy()
        >>> candids == candids_old
        True
        >>> entries_to_mutate = Candidate(
        ...     {}, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>>
        >>> # Case 1: only candids changes
        >>> candids_part1 = candids.group('submatrix')[1]
        >>> appearances1 = candids_part1.appearances(['row', 'col'])
        >>> appearances1.sieve()
        >>> appearances1.show == {
        ...     '4': [[1, 2], {(0, 1), (0, 0)}], 
        ...     '9': [[1, 2], {(0, 0), (0, 2)}], 
        ...     '5': [[1, 2], {(0, 1), (0, 0)}]
        ... }
        ...
        True
        >>> candids.refine(entries_to_mutate, appearances1)
        >>> entries_to_mutate == Candidate(
        ...     {}, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        >>> candids == candids_old
        False
        >>> candids == Candidate({
        ...     (0, 0): {'5', '1', '9', '4', '7'}, 
        ...     (0, 1): {'5', '4'}, 
        ...     (0, 2): {'1', '9', '7'}, 
        ...     (0, 3): {'8', '6'}, 
        ...     (0, 5): {'8', '3'}, 
        ...     (0, 6): {'1', '3'}, # '5' eliminated
        ...     (0, 7): {'3', '7'}, # '5' eliminated
        ...     (0, 8): {'1', '3'}, # '5' eliminated
        ...     (1, 2): {'2'}, 
        ...     (1, 6): {'5'}, 
        ...     (2, 0): {'1', '2', '7'}, 
        ...     (2, 2): {'1', '2', '7'}, 
        ...     (2, 4): {'3'}, 
        ...     (2, 7): {'2', '3', '7'}, 
        ...     (3, 0): {'2', '6'}, 
        ...     (3, 2): {'8', '2', '6'}, 
        ...     (3, 4): {'5', '8', '6', '7'}, 
        ...     (3, 6): {'5', '8', '6'}, 
        ...     (3, 7): {'5', '8', '6'}, 
        ...     (4, 0): {'3', '6'}, 
        ...     (4, 2): {'8', '3', '6'}, 
        ...     (4, 4): {'5', '8', '6'}, 
        ...     (4, 6): {'5', '6', '9', '8', '3'}, 
        ...     (4, 7): {'5', '8', '3', '6'}, 
        ...     (5, 0): {'4', '3', '6'}, 
        ...     (5, 3): {'8', '6'}, 
        ...     (5, 4): {'8', '6'}, 
        ...     (5, 5): {'9', '8'}, 
        ...     (5, 8): {'9', '3'}, 
        ...     (6, 0): {'5', '6', '1', '9', '2', '3'}, 
        ...     (6, 1): {'5', '8', '2'}, 
        ...     (6, 3): {'8', '2'}, 
        ...     (6, 4): {'8', '3'}, 
        ...     (6, 5): {'8', '3'}, 
        ...     (6, 7): {'5', '6', '8', '2', '3'}, 
        ...     (6, 8): {'5', '1', '9', '2', '3'}, 
        ...     (7, 0): {'6', '1', '9', '2', '3'}, 
        ...     (7, 1): {'8', '2'}, 
        ...     (7, 2): {'2', '6', '1', '9', '8', '3'}, 
        ...     (7, 4): {'8', '3', '4'}, 
        ...     (7, 6): {'6', '1', '9', '8', '3'}, 
        ...     (7, 7): {'6', '8', '2', '3', '4'}, 
        ...     (7, 8): {'1', '9', '2', '3'}, 
        ...     (8, 0): {'5', '2', '3', '7'}, 
        ...     (8, 1): {'5', '8', '2'}, 
        ...     (8, 2): {'8', '2', '3', '7'}, 
        ...     (8, 6): {'5', '8', '3'}, 
        ...     (8, 7): {'5', '8', '2', '3', '4'}, 
        ...     (8, 8): {'5', '2', '3'}
        ... },
        ... elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        >>> 
        >>> # Case 2: only entries_to_mutate changes
        >>> candids_part2 = candids.group('submatrix')[2]
        >>> candids_old = candids.copy()
        >>> appearances2 = candids_part2.appearances(['row', 'col'])
        >>> appearances2.sieve()
        >>> appearances2.show == {
        ...     '8': [[1, 2], {(0, 3), (0, 5)}], 
        ...     '6': [[1, 1], {(0, 3)}]
        ... }
        ...
        True
        >>> candids.refine(entries_to_mutate, appearances2)
        >>> entries_to_mutate == Candidate(
        ...     {}, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        False
        >>> entries_to_mutate == Candidate(
        ...     {(0, 3): {'6'}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        True
        >>> candids == candids_old 
        True
        >>>
        >>> # Case 3: both candids and entries_to_mutate change
        >>> candids_part3 = candids.group('submatrix')[3]
        >>> appearances3 = candids_part3.appearances(['row', 'col'])
        >>> appearances3.sieve()
        >>> appearances3.show == {
        ...     '1': [[1, 2], {(0, 6), (0, 8)}], 
        ...     '2': [[1, 1], {(2, 7)}], 
        ...     '5': [[1, 1], {(1, 6)}],
        ...     '7': [[2, 1], {(2, 7), (0, 7)}]
        ... }
        ...
        True
        >>> candids.refine(entries_to_mutate, appearances3)
        >>> entries_to_mutate == Candidate(
        ...     {}, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        False
        >>> entries_to_mutate == Candidate(
        ...     {(0, 3): {'6'}, (1, 6): {'5'}, (2, 7): {'2'}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        >>> candids == candids_old
        False
        >>> candids == Candidate({
        ...     (0, 0): {'5', '9', '4', '7'}, # '1' eliminated
        ...     (0, 1): {'5', '4'}, 
        ...     (0, 2): {'9', '7'},           # '1' eliminated
        ...     (0, 3): {'8', '6'}, 
        ...     (0, 5): {'8', '3'}, 
        ...     (0, 6): {'1', '3'}, 
        ...     (0, 7): {'3', '7'}, 
        ...     (0, 8): {'1', '3'}, 
        ...     (1, 2): {'2'}, 
        ...     (1, 6): {'5'}, 
        ...     (2, 0): {'1', '2', '7'}, 
        ...     (2, 2): {'1', '2', '7'}, 
        ...     (2, 4): {'3'}, 
        ...     (2, 7): {'2', '3', '7'}, 
        ...     (3, 0): {'2', '6'}, 
        ...     (3, 2): {'8', '2', '6'}, 
        ...     (3, 4): {'5', '8', '6', '7'}, 
        ...     (3, 6): {'5', '8', '6'}, 
        ...     (3, 7): {'5', '8', '6'}, 
        ...     (4, 0): {'3', '6'}, 
        ...     (4, 2): {'8', '3', '6'}, 
        ...     (4, 4): {'5', '8', '6'}, 
        ...     (4, 6): {'5', '6', '9', '8', '3'}, 
        ...     (4, 7): {'5', '8', '3', '6'}, 
        ...     (5, 0): {'4', '3', '6'}, 
        ...     (5, 3): {'8', '6'}, 
        ...     (5, 4): {'8', '6'}, 
        ...     (5, 5): {'9', '8'}, 
        ...     (5, 8): {'9', '3'}, 
        ...     (6, 0): {'5', '6', '1', '9', '2', '3'}, 
        ...     (6, 1): {'5', '8', '2'}, 
        ...     (6, 3): {'8', '2'}, 
        ...     (6, 4): {'8', '3'}, 
        ...     (6, 5): {'8', '3'}, 
        ...     (6, 7): {'5', '6', '8', '2', '3'}, 
        ...     (6, 8): {'5', '1', '9', '2', '3'}, 
        ...     (7, 0): {'6', '1', '9', '2', '3'}, 
        ...     (7, 1): {'8', '2'}, 
        ...     (7, 2): {'2', '6', '1', '9', '8', '3'}, 
        ...     (7, 4): {'8', '3', '4'}, 
        ...     (7, 6): {'6', '1', '9', '8', '3'}, 
        ...     (7, 7): {'6', '8', '2', '3', '4'}, 
        ...     (7, 8): {'1', '9', '2', '3'}, 
        ...     (8, 0): {'5', '2', '3', '7'}, 
        ...     (8, 1): {'5', '8', '2'}, 
        ...     (8, 2): {'8', '2', '3', '7'}, 
        ...     (8, 6): {'5', '8', '3'}, 
        ...     (8, 7): {'5', '8', '2', '3', '4'}, 
        ...     (8, 8): {'5', '2', '3'}
        ... },
        ... elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        >>> 
        >>> # Case 4: (sieve = True, ['contains', 2], True)
        >>> V = Candidate(
        ...     {
        ...         (0, 6): {'7', '6', '3'}, 
        ...         (0, 7): {'3', '8', '6'}, 
        ...         (0, 8): {'7', '6', '8', '9', '3'}, 
        ...         (1, 6): {'4', '3', '2', '7'}, 
        ...         (1, 8): {'3', '8', '7'}, 
        ...         (2, 7): {'6', '8', '4', '3', '2'}, 
        ...         (2, 8): {'3', '8', '6', '7'}
        ...     },
        ...     elements = {'6', '7', '1', '8', '4', '5', '3', '9', '2'}
        ... )
        ...
        >>> etm = Candidate({}, elements = set([i for i in range(1, 10)]))
        >>> etm_before = etm.copy()
        >>> V.refine(
        ...     etm, 
        ...     names = ['row', 'col'], 
        ...     sieve = True, 
        ...     condition = ['contains', 2], 
        ...     deep = True
        ... )
        ...
        >>> etm == etm_before
        True
        >>> V == Candidate(
        ...     {
        ...         (0, 6): {'7', '6', '3'}, 
        ...         (0, 7): {'3', '8', '6'}, 
        ...         (0, 8): {'7', '6', '8', '9', '3'}, 
        ...         (1, 6): {'4', '2'},           # '3' and '7' gone
        ...         (1, 8): {'3', '8', '7'}, 
        ...         (2, 7): {'4', '2'},           # '3', '6', and '8' gone
        ...         (2, 8): {'3', '8', '6', '7'}
        ...     },
        ...     elements = {'6', '7', '1', '8', '4', '5', '3', '9', '2'}
        ... )
        ...
        True
        >>> # Case 5: (sieve = False, ['contains', 2], True)
        >>> V3 = Candidate(
        ...     {
        ...         (2, 2): {'6', '9', '7', '3'},
        ...         (2, 3): {'6', '9', '7', '5'},
        ...         (2, 4): {'6', '9'},
        ...         (2, 5): {'9', '7', '5'},
        ...         (2, 6): {'5', '6', '9', '3'},
        ...         (2, 7): {'3', '4', '9', '8', '5'},
        ...         (2, 8): {'6', '3', '4', '9', '8', '5'}
        ...     },
        ...     elements = {'6', '3', '1', '4', '9', '7', '2', '8', '5'}
        ... )
        ...
        >>> appearances3 = V3.appearances(['col', 'submatrix'])
        >>> appearances3.sieve(condition = ['contains', 2], deep = True)
        >>> V3.refine(
        ...     etm, 
        ...     appearances3, 
        ...     condition = ['contains', 2], 
        ...     deep = True
        ... )
        ...
        >>> V3 == Candidate(
        ...     {
        ...         (2, 2): {'9', '6', '7', '3'},
        ...         (2, 3): {'9', '5', '6', '7'},
        ...         (2, 4): {'9', '6'},
        ...         (2, 5): {'9', '5', '7'},
        ...         (2, 6): {'9', '5', '6', '3'},
        ...         (2, 7): {'8', '4'}, # '3', '5', and '9' gone
        ...         (2, 8): {'8', '4'}  # '3', 5', '6', and '9' gone
        ...     },
        ...     elements = {'5', '3', '4', '1', '6', '8', '9', '2', '7'}
        ... )
        ...
        True
        '''

        if appearances is None:
            assert names is not None, \
                'If appearances is None, then names must not be None.'
            appearances = self.appearances(names)
        if sieve:
            appearances.sieve(condition = condition, deep = deep)

        if (condition, deep) == (['contains', 1], False):
            for k3, v3 in appearances.items():
                if v3[0] == [1, 1]: # only candid value
                    entries_to_mutate[list(v3[1])[0]] = {k3}
                elif v3[0][0] == 1: # eliminate the same candid in names[0]
                    names0_exception = []
                    for v3_item1 in list(v3[1]):
                        names0_exception.append(v3_item1[1])
                    for k_g1, v_g1 in self.items():
                        if k_g1[0] == list(v3[1])[0][0] and\
                            k_g1[1] not in names0_exception and k3 in v_g1:
                            v_g1.remove(k3)
                elif v3[0][1] == 1: # eliminate the same candid in names[1]
                    names1_exception = []
                    for v3_item2 in list(v3[1]):
                        names1_exception.append(v3_item2[0])
                    for k_g2, v_g2 in self.items():
                        if k_g2[1] == list(v3[1])[0][1] and\
                            k_g2[0] not in names1_exception and k3 in v_g2:
                            v_g2.remove(k3)
        
        elif (condition[0], deep) == ('contains', True):
            m = condition[1]
            replacing_candids = set(appearances.keys()) # must be of len m
            ent_to_replace = set()
            for val_list in list(appearances.values()):
                ent_to_replace.update(val_list[1])
            ent_to_replace = list(ent_to_replace) # must be of len m also
            if len(replacing_candids) == m and len(ent_to_replace) == m:
                for entry in ent_to_replace:
                    if entry in self.keys():
                        self[entry] =\
                            self[entry].intersection(replacing_candids)


    def unions(self):
        '''(Candidate) -> Union

        Return the unions of candidates at each group.

        >>> V = Candidate(
        ...     { # candidates of submatrix1
        ...         (0, 1): {'5', '4', '7', '9'}, 
        ...         (1, 0): {'9', '4'}, 
        ...         (1, 1): {'5', '4', '6', '9'}, 
        ...         (1, 2): {'5', '4', '6', '9'}, 
        ...         (2, 1): {'5', '4', '7', '9', '6'}
        ...     },
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> unions = V.unions()
        >>> unions.show == {
        ...     'submatrix': {
        ...         1: {'7', '5', '9', '6', '4'}
        ...     }, 
        ...     'row': {
        ...         0: {'7', '4', '9', '5'}, 
        ...         1: {'4', '9', '6', '5'}, 
        ...         2: {'7', '9', '6', '4', '5'}
        ...     }, 
        ...     'col': {
        ...         0: {'9', '4'}, 
        ...         1: {'7', '5', '9', '6', '4'}, 
        ...         2: {'9', '6', '4', '5'}
        ...     }
        ... }
        ...
        True
        '''

        return Union(self)


    def update(self, other):
        '''(Candidate, Candidate or {(int, int): set of ints/strs}) -> None

        Update self using other.

        >>> eg1 = Candidate(
        ...     {(0, 1): {1, 2, 4}, (0, 2): {6, 9}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> eg1.update(
        ...     Candidate(
        ...         {(1, 2): {1, 7}},
        ...         elements = set([str(i) for i in range(1, 10)])
        ...     )
        ... )
        ...
        >>> eg1 == Candidate(
        ...     {(0, 1): {1, 2, 4}, (0, 2): {6, 9}, (1, 2): {1, 7}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        >>> eg1.update(
        ...     Candidate(
        ...         {(0, 1): {1}}, 
        ...         elements = set([str(i) for i in range(1, 10)])
        ...     )
        ... )
        ...
        >>> eg1 == Candidate(
        ...     {(0, 1): {1}, (0, 2): {6, 9}, (1, 2): {1, 7}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        >>> eg1.update({(0, 0): {3}, (1, 2): {7}})
        >>> eg1 == Candidate(
        ...     {(0, 0): {3}, (0, 1): {1}, (0, 2): {6, 9}, (1, 2): {7}},
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        True
        '''

        if type(other) == dict:
            for k, v in other.items():
                other[k] = set(map(lambda x: str(x), list(v)))
            self.show.update(other)
        elif type(other) == Candidate:
            if self.n != other.n:
                raise ValueError('self.n != other.n')
            self.show.update(other.show)


    def values(self):
        '''(Candidate) -> dict_values

        Return dict_values of self.
        '''

        return self.show.values()


# END: Candidate #########################################################


# START: Union ###########################################################

class Union():
    '''Union of candidates at each group.'''

    def __init__(self, C):
        '''(Union, Candidate) -> None

        Initialize Union.

        >>> V = Candidate(
        ...     { # candidates of submatrix1
        ...         (0, 1): {'5', '4', '7', '9'}, 
        ...         (1, 0): {'9', '4'}, 
        ...         (1, 1): {'5', '4', '6', '9'}, 
        ...         (1, 2): {'5', '4', '6', '9'}, 
        ...         (2, 1): {'5', '4', '7', '9', '6'}
        ...     },
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> unions = Union(V)
        '''
        
        elements = C.elements

        group_col = C.group('col')
        group_col_cp = group_col.copy()
        group_row = C.group('row')
        group_row_cp = group_row.copy()
        group_sub = C.group('submatrix')
        group_sub_cp = group_sub.copy()
        
        gcu = {}
        gru = {}
        gsu = {}
        
        for Kc, Vc in group_col_cp.items():
            if Vc == Candidate({}, elements = elements):
                group_col.pop(Kc)
        for Kr, Vr in group_row_cp.items():
            if Vr == Candidate({}, elements = elements):
                group_row.pop(Kr)
        for Ks, Vs in group_sub_cp.items():
            if Vs == Candidate({}, elements = elements):
                group_sub.pop(Ks)
                
        for ck, cv in group_col.items():
            gcu[ck] = set()
            for cvv in cv.values():
                gcu[ck] = gcu[ck].union(cvv)
        for rk, rv in group_row.items():
            gru[rk] = set()
            for rvv in rv.values():
                gru[rk] = gru[rk].union(rvv)
        for sk, sv in group_sub.items():
            gsu[sk] = set()
            for svv in sv.values():
                gsu[sk] = gsu[sk].union(svv)

        result = {'submatrix': gsu, 'row': gru, 'col': gcu}

        self.show = result
        self.n = C.n


    def __eq__(self, other):
        '''(Union, Union) -> bool
        
        Return True iff self.show == other.show and n are the same.
        '''

        return self.show == other.show and self.n == other.n


    def __repr__(self):
        '''(Union) -> Union

        Print the representation of Union.
        '''

        headline, endline = "Union(\n", "n: {0}\n)".format(self.n)
        itms = [(k, v) for k, v in self.show.items()]
        itms.sort()
        mid = "{{'{0}': {1},\n".format(itms[0][0], itms[0][1])
        for i in range(1, len(itms) - 1):
            mid += " '{0}': {1},\n".format(itms[i][0], itms[i][1])
        last = len(itms) - 1
        mid += " '{0}': {1}}},\n".format(itms[last][0], itms[last][1])

        return headline + mid + endline


    def aggregate(self, names):
        '''(Union, [str, str]) -> [strs], [strs]
        
        Preconditions:
        1. len(set(names)) == 2
        2. set(names).issubset(['col', 'row', 'submatrix'])
        
        Aggregate value sets of self by names, and return two lists of
        numbers/objects consisting of elements in value sets.

        >>> V = Candidate(
        ...     { # candidates of submatrix1 of 9x9 sudoku
        ...         (0, 1): {'5', '4', '7', '9'}, 
        ...         (1, 0): {'9', '4'}, 
        ...         (1, 1): {'5', '4', '6', '9'}, 
        ...         (1, 2): {'5', '4', '6', '9'}, 
        ...         (2, 1): {'5', '4', '7', '9', '6'}
        ...     },
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> unions = Union(V)
        >>> rows_union, cols_union = unions.aggregate(['row', 'col'])
        >>> rows_union.sort(); cols_union.sort()
        >>> rows_union == [
        ...     '4', '4', '4', '5', '5', '5', '6', '6', '7', '7', 
        ...     '9', '9', '9'
        ... ]
        ...
        True
        >>> cols_union == [
        ...     '4', '4', '4', '5', '5', '6', '6', '7', '9', '9', '9'
        ... ]
        ...
        True
        '''

        letter1, letter2 = names[0], names[1]
        union1, union2 = [], []
        for K, V in self.items():
            if K == letter1: # usually row
                for v in V.values():
                    union1.extend(list(v))
            elif K == letter2: # usually col
                for v in V.values():
                    union2.extend(list(v))
        return union1, union2
    
    
    def items(self):
        '''(Union) -> dict_items
        
        Return the dict_items of self.show.
        '''
        
        return self.show.items()
        

    def keys(self):
        '''(Union) -> dict_keys
        
        Return the keys of self.show.
        '''

        return self.show.keys()


    def values(self):
        '''(Union) -> dict_values
        
        Return the values of self.show.
        '''
        
        return self.show.values()


# END: Union #############################################################


# START: Appearance ######################################################

class Appearance():
    '''Appearance collection.'''

    def __init__(self, C, names = None):
        '''(Appearance, Candidate, [str, str]) -> None

        Preconditions:
        1. names is not None and len(set(names)) == 2
        2. set(names).issubset(['col', 'row', 'submatrix'])

        Initialize Appearance object.
        '''

        assert names is not None, 'names should be specified.'
        assert len(set(names)) == 2, 'len(set(names)) != 2'
        assert set(names).issubset(['col', 'row', 'submatrix']), \
            'Invalid name in names'

        elements = C.elements
        unions = C.unions()
        union1, union2 = unions.aggregate(names)
        appearances = {}
        for a in elements:
            appearances[a] = [[0, 0], set()]
        for number1 in union1:
            appearances[number1][0][0] += 1
            for kV, vV in C.items():
                if number1 in vV:
                    appearances[number1][1].update([kV])
        for number2 in union2:
            appearances[number2][0][1] += 1
            for kV2, vV2 in C.items():
                if number2 in vV2:
                    appearances[number2][1].update([kV2])

        self.show = appearances
        self.elements = elements
        self.n = C.n
        self.names = names


    def __repr__(self):
        '''(Appearance) -> Appearance

        Print the representation of Appearance.

        >>> V = Candidate(
        ...     {
        ...         (0, 1): {'4', '9', '7', '5'}, 
        ...         (1, 0): {'9', '4'}, 
        ...         (1, 1): {'4', '9', '6', '5'}, 
        ...         (1, 2): {'4', '9', '6', '5'},
        ...         (2, 1): {'7', '9', '6', '5', '4'}
        ...     }, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> names = ['row', 'col']
        >>> Appearance(V, names)
        Appearance(
        {
        '1': [[0, 0], set()],
        '2': [[0, 0], set()],
        '3': [[0, 0], set()],
        '4': [[3, 3], {(0, 1), (1, 2), (2, 1), (1, 0), (1, 1)}],
        '5': [[3, 2], {(0, 1), (2, 1), (1, 1), (1, 2)}],
        '6': [[2, 2], {(1, 2), (1, 1), (2, 1)}],
        '7': [[2, 1], {(0, 1), (2, 1)}],
        '8': [[0, 0], set()],
        '9': [[3, 3], {(0, 1), (1, 2), (2, 1), (1, 0), (1, 1)}]
        },
        n: 3
        elements: {1, 2, 3, 4, 5, 6, 7, 8, 9}
        names: 'row', 'col' (in this order)
        )
        '''

        elements = self.elements
        headline, mid, endline = 'Appearance(\n{\n', "", ""

        KVs = list(self.show.items())
        KVs.sort()
        lenKVs = len(KVs)
        i = 0
        for k, v in KVs:
            if i != len(KVs) - 1:
                mid += "'{0}': {1},\n".format(k, v)
            else:
                mid += "'{0}': {1}\n".format(k, v)
            i += 1

        elements_ord = list(elements)
        elements_ord.sort()
        el_strs = ''
        for ch in enumerate(elements_ord):
            if ch[0] != len(elements_ord) - 1:
                el_strs += ch[1] + ', '
            else:
                el_strs += ch[1]
        endline += '}},\nn: {0}\n'.format(self.n)
        endline += 'elements: {{{0}}}\n'.format(el_strs)
        endline += "names: '{0}', '{1}' (in this order)\n)".format(
            self.names[0], self.names[1]
        )

        return headline + mid + endline


    def keys(self):
        '''(Appearance) -> dict_keys

        Return dict_keys of self.show.
        '''

        return self.show.keys()


    def items(self):
        '''(Appearance) -> dict_items

        Return dict_items of self.show.
        '''

        return self.show.items()


    def sieve(self, condition = ['contains', 1], deep = False):
        '''(Appearance, [str, int][, bool]) -> None

        Precondition: 
        1. condition[0] in ['contains', 'both']
        2. condition[1] >= 0
        3. condition[1] == int(condition[1])

        Update self so that keys that satisfy the condition stay while
        others are removed. If deep = True (False by default), then the 
        second element of the value list is checked to see if they are 
        all the same AND all has length condition[1]; if not, then the 
        respective keys that passed condition are furthur removed from 
        self. For example:
        1. condition = ['contains', 1]:
            any key with its first element of the value list containing 1
            (i.e. [1, x] or [x, 1]) will stay while others are removed 
            from self.
        2. condition = ['both', 2]:
            any key with its first element of the value list being [2, 2]
            will stay while others get removed from self.
        3. condition = ['contains', 2], deep = True:
            among those keys with its first element of the value list 
            containing 2, the method will check to see if the second
            elements of these keys are the same AND has length 2.

        >>> # CASE 1: ['contains', 1]
        >>> V = Candidate(
        ...     {
        ...         (0, 1): {'4', '9', '7', '5'}, 
        ...         (1, 0): {'9', '4'}, 
        ...         (1, 1): {'4', '9', '6', '5'}, 
        ...         (1, 2): {'4', '9', '6', '5'},
        ...         (2, 1): {'7', '9', '6', '5', '4'}
        ...     }, 
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> names = ['row', 'col']
        >>> appearances = Appearance(V, names)
        >>> appearances
        Appearance(
        {
        '1': [[0, 0], set()],
        '2': [[0, 0], set()],
        '3': [[0, 0], set()],
        '4': [[3, 3], {(0, 1), (1, 2), (2, 1), (1, 0), (1, 1)}],
        '5': [[3, 2], {(0, 1), (2, 1), (1, 1), (1, 2)}],
        '6': [[2, 2], {(1, 2), (1, 1), (2, 1)}],
        '7': [[2, 1], {(0, 1), (2, 1)}],
        '8': [[0, 0], set()],
        '9': [[3, 3], {(0, 1), (1, 2), (2, 1), (1, 0), (1, 1)}]
        },
        n: 3
        elements: {1, 2, 3, 4, 5, 6, 7, 8, 9}
        names: 'row', 'col' (in this order)
        )
        >>> appearances.sieve()
        >>> appearances.show == {'7': [[2, 1], {(0, 1), (2, 1)}]}
        True
        >>>
        >>> # CASE 2: ['both', 2], deep == True
        >>> V2 = Candidate(
        ...     {
        ...         (3, 1): {'8', '2', '9'}, 
        ...         (3, 2): {'8', '7', '9', '6', '2'}, 
        ...         (4, 0): {'2', '9', '5'}, 
        ...         (4, 2): {'8', '2', '9'}, 
        ...         (5, 0): {'7', '5', '9', '6'}, 
        ...         (5, 1): {'5', '9'}
        ...     },
        ...     elements = set([str(i) for i in range(1, 10)])
        ... )
        ...
        >>> appearances2 = V2.appearances(names)
        >>> appearances2
        Appearance(
        {
        '1': [[0, 0], set()],
        '2': [[2, 3], {(4, 2), (3, 2), (3, 1), (4, 0)}],
        '3': [[0, 0], set()],
        '4': [[0, 0], set()],
        '5': [[2, 2], {(5, 1), (5, 0), (4, 0)}],
        '6': [[2, 2], {(3, 2), (5, 0)}],
        '7': [[2, 2], {(3, 2), (5, 0)}],
        '8': [[2, 2], {(4, 2), (3, 2), (3, 1)}],
        '9': [[3, 3], {(3, 2), (5, 1), (3, 1), (5, 0), (4, 2), (4, 0)}]
        },
        n: 3
        elements: {1, 2, 3, 4, 5, 6, 7, 8, 9}
        names: 'row', 'col' (in this order)
        )
        >>> appearances2.sieve(condition = ['both', 2])
        >>> appearances2.show == {        
        ...     '5': [[2, 2], {(5, 1), (5, 0), (4, 0)}],
        ...     '6': [[2, 2], {(3, 2), (5, 0)}],
        ...     '7': [[2, 2], {(3, 2), (5, 0)}],
        ...     '8': [[2, 2], {(4, 2), (3, 2), (3, 1)}]
        ... }
        ...
        True
        >>> appearances2.sieve(condition = ['both', 2], deep = True)
        >>> appearances2.show == {
        ...     '6': [[2, 2], {(3, 2), (5, 0)}],
        ...     '7': [[2, 2], {(3, 2), (5, 0)}],
        ... }
        ...
        True
        >>>
        >>> # CASE 3: ['contains', 2], deep == True
        >>> V3 = Candidate(
        ...     {
        ...         (2, 2): {'6', '9', '7', '3'},
        ...         (2, 3): {'6', '9', '7', '5'},
        ...         (2, 4): {'6', '9'},
        ...         (2, 5): {'9', '7', '5'},
        ...         (2, 6): {'5', '6', '9', '3'},
        ...         (2, 7): {'3', '4', '9', '8', '5'},
        ...         (2, 8): {'6', '3', '4', '9', '8', '5'}
        ...     },
        ...      elements = {'6', '3', '1', '4', '9', '7', '2', '8', '5'}
        ... )
        ...
        >>> appearances3 = V3.appearances(['col', 'submatrix'])
        >>> appearances3.show == {
        ...     '1': [[0, 0], set()],
        ...     '2': [[0, 0], set()],
        ...     '3': [[4, 2], {(2, 7), (2, 8), (2, 6), (2, 2)}],
        ...     '4': [[2, 1], {(2, 7), (2, 8)}],
        ...     '5': [[5, 2], {(2, 7), (2, 6), (2, 8), (2, 3), (2, 5)}],
        ...     '6': [[5, 3], {(2, 6), (2, 8), (2, 3), (2, 2), (2, 4)}],
        ...     '7': [[3, 2], {(2, 5), (2, 3), (2, 2)}],
        ...     '8': [[2, 1], {(2, 7), (2, 8)}],
        ...     '9': [
        ...         [7, 3], 
        ...         {(2, 7), (2, 6), (2, 8), 
        ...          (2, 3), (2, 2), (2, 5), (2, 4)}
        ...     ]
        ... }
        ...
        True
        >>> appearances3.sieve(['contains', 2], True)
        >>> appearances3.show == {
        ...     '4': [[2, 1], {(2, 7), (2, 8)}],
        ...     '8': [[2, 1], {(2, 7), (2, 8)}]
        ... }
        ...
        True
        '''

        assert condition[0] in ['contains', 'both'], \
            ".sieve() method only handles either 'contains' or 'both'" +\
            " condition"
        assert condition[1] >= 0, \
            ".sieve() method should have condition[1] >= 0"
        assert condition[1] == int(condition[1]), \
            ".sieve() doesn't understand a number other than integers"

        appearances_cp = self.show.copy()
        if condition[0] == 'contains':
            for k1, v1 in appearances_cp.items():
                if condition[1] not in v1[0]:
                    self.show.pop(k1)
        elif condition[0] == 'both':
            for k2, v2 in appearances_cp.items():
                if v2[0] != [condition[1], condition[1]]:
                    self.show.pop(k2)
        
        appearances_cp = self.show.copy() # new copy
        if deep:
            kv_lst = [[k3, v3[1]] for k3, v3 in appearances_cp.items()]
            v_lst = [v4[1] for v4 in appearances_cp.values()]
            v_lst2 = [(len(v5), v_lst.count(v5), v5) for v5 in v_lst]
            v_lst3 = list(filter(
                lambda x: x[0] == x[1] == condition[1], 
                v_lst2
            ))
            kv_dict = {}
            k_set = set()
            for item in kv_lst:
                for i in range(len(v_lst3)):
                    if item[1] == v_lst3[i][2]:
                        k_set.update(item[0])
            for k6 in appearances_cp.keys():
                if k6 not in k_set:
                    self.show.pop(k6)


    def values(self):
        '''(Appearance) -> dict_values

        Return dict_values of self.show.
        '''

        return self.show.values()


# END: Appearance ########################################################



if __name__ == '__main__':
    import doctest
    doctest.testmod()
