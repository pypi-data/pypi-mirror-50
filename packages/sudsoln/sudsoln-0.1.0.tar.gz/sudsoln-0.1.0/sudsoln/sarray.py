
class Array():
    '''A 2-dimensional array.'''

    def __init__(self, array):
        '''(Array, list of ints/strs or [ints/strs]) -> None

        Initialize the 2-dimensional Array object.

        >>> test = [
        ...     [1, 2, 3, 2], 
        ...     [5, 2, 0, 4], 
        ...     [7, 5, 1, 0],
        ... ]
        ...
        >>> test = Array(test)
        >>> test.show
        [['1', '2', '3', '2'], ['5', '2', '0', '4'], ['7', '5', '1', '0']]
        >>> test.nrow
        3
        >>> test.ncol
        4
        >>> test.shape
        (3, 4)
        >>> test.size
        12
        >>> test2_1 = ['1', '5', 2]
        >>> test2_2 = [['1', '5', 2]]
        >>> test2_1 = Array(test2_1)
        >>> test2_1
        Array([
        ['1'],
        ['5'],
        ['2']
        ])
        >>> test2_2 = Array(test2_2)
        >>> test2_2
        Array([
        ['1', '5', '2']
        ])
        '''

        if 'ndarray' in str(type(array)):
            array = list(array)
        elif 'Array' in str(type(array)):
            array = array.show
        mkstr = lambda x: str(x) if type(x) != str else x
        lena = len(array)
        ncols = []
        for i in range(lena):
            try:
                ncols.append(len(array[i]))
                array[i] = list(map(mkstr, array[i]))
            except TypeError: # e.g. Array([2, 3])
                ncols.append(len([array[i]]))
                array[i] = list(map(mkstr, [array[i]]))
        if len(set(ncols)) != 1:
            raise ValueError(
                'All sublists of array should have the same length.'
            )

        self.show = array
        self.nrow = lena
        self.ncol = ncols[0]
        self.shape = (self.nrow, self.ncol)
        self.size = sum(ncols)


    def __eq__(self, other):
        '''(Array, Array) -> bool

        Return True iff self and other are identical element-wise.
        '''

        if self.shape != other.shape:
            return False
        return self.show == other.show


    def __getitem__(self, key):
        '''(Array, ints/lists/slices/tuples) -> str or Array

        Return the entry of self at key.
        
        >>> test = [
        ...     [1, 2, 3, 4], 
        ...     [5, 2, 0, 3], 
        ...     [7, 5, 1, 0], 
        ...     [2, 6, 2, 4]
        ... ]
        ...
        >>> test = Array(test)
        >>> test[(0, 1)]
        '2'
        >>> test[2, 3]
        '0'
        >>> test[2, :]
        Array([
        ['7', '5', '1', '0']
        ])
        >>> test[:, 3]
        Array([
        ['4'],
        ['3'],
        ['0'],
        ['4']
        ])
        >>> test[(1, -1, 2), :]
        Array([
        ['5', '2', '0', '3'],
        ['2', '6', '2', '4'],
        ['7', '5', '1', '0']
        ])
        >>> test[:, (2, 0)]
        Array([
        ['3', '1'],
        ['0', '5'],
        ['1', '7'],
        ['2', '2']
        ])
        >>> test[2:, [0, 2, 3]]
        Array([
        ['7', '1', '0'],
        ['2', '2', '4']
        ])
        >>> test[:, :2]
        Array([
        ['1', '2'],
        ['5', '2'],
        ['7', '5'],
        ['2', '6']
        ])
        >>> test[::2, ::2]
        Array([
        ['1', '3'],
        ['7', '1']
        ])
        >>> test[::3, ::2]
        Array([
        ['1', '3'],
        ['2', '2']
        ])
        >>> test[(1, 3), (2, 2)]
        Array([
        ['0', '2']
        ])
        '''
        
        key0_is_int   = isinstance(key[0], int)
        key0_is_slice = isinstance(key[0], slice)
        key0_is_tl    = isinstance(key[0], (tuple, list))
        key1_is_int   = isinstance(key[1], int)
        key1_is_slice = isinstance(key[1], slice)
        key1_is_tl    = isinstance(key[1], (tuple, list))
        
        # 9 cases
        result = []
        if key0_is_int and key1_is_int:
            return self.show[key[0]][key[1]]
        elif key0_is_int and key1_is_slice:
            return Array([self.show[key[0]][key[1]]])
        elif key0_is_int and key1_is_tl:
            [result.append(self[key[0], i]) for i in key[1]]
            return Array([result])
        
        elif key0_is_slice and key1_is_int:
            cols = [list(row) for row in list(zip(*self.show))]
            return Array(cols[key[1]][key[0]])
        elif key0_is_slice and key1_is_slice:
            lz_inner = list(zip(*self.show[key[0]]))[key[1]]
            lz = [list(row) for row in zip(*lz_inner)]
            return Array(lz)
        elif key0_is_slice and key1_is_tl:
            base = self[key[0], :]
            [result.append(base[:, i].flatten()) for i in key[1]]
            return Array(list(zip(*result)))
            
        elif key0_is_tl and key1_is_int:
            [result.append(self[i, key[1]]) for i in key[0]]
            return Array([result])
        elif key0_is_tl and key1_is_slice:
            [result.append(self[i, key[1]].show[0]) for i in key[0]]
            return Array(result)
        elif key0_is_tl and key1_is_tl:
            if len(key[0]) != len(key[1]):
                raise IndexError(
                    'Indexing arrays having different lengths cannot ' +\
                    'be broadcasted together.'
                )
            entries = list(zip(key[0], key[1]))
            [result.append(self[item]) for item in entries]
            return Array([result])
        else:
            raise TypeError('Invalid key type')


    def __repr__(self):
        '''(Array) -> Array

        Return the Array representation of self.
        >>> test = [
        ...     [1, 2, 3, 4], 
        ...     [5, 2, 0, 3], 
        ...     [7, 5, 1, 0], 
        ...     [2, 6, 2, 4]
        ... ]
        ...
        >>> test = Array(test)
        >>> test
        Array([
        ['1', '2', '3', '4'],
        ['5', '2', '0', '3'],
        ['7', '5', '1', '0'],
        ['2', '6', '2', '4']
        ])
        '''

        headline, midline, endline = 'Array([\n', '', '])'
        for i in range(len(self.show)):
            if i != len(self.show) - 1:
                midline += str(self.show[i]) + ',\n'
            else:
                midline += str(self.show[i]) + '\n'
        return headline + midline + endline


    def __setitem__(self, key, value):
        '''(Array, (int, int), int/str) -> None

        Assign value to self's key.

        >>> test = [
        ...     [1, 2, 3, 4], 
        ...     [5, 2, 0, 3], 
        ...     [7, 5, 1, 0], 
        ...     [2, 6, 2, 4]
        ... ]
        ...
        >>> test = Array(test)
        >>> test[0, 0] = 3
        >>> test
        Array([
        ['3', '2', '3', '4'],
        ['5', '2', '0', '3'],
        ['7', '5', '1', '0'],
        ['2', '6', '2', '4']
        ])
        >>> test[(3, 2)] = '.'
        >>> test
        Array([
        ['3', '2', '3', '4'],
        ['5', '2', '0', '3'],
        ['7', '5', '1', '0'],
        ['2', '6', '.', '4']
        ])
        '''
    
        if not (isinstance(key[0], int) and isinstance(key[1], int)):
            raise TypeError('Broadcasting not supported.')
        self.show[key[0]][key[1]] = str(value)


    def copy(self):
        '''(Array) -> Array

        Return the deep copy of self.
        '''

        return Array([row[:] for row in self.show])


    def flatten(self):
        '''(Array) -> list of str

        Return the flattened version of self.

        >>> test = [
        ...     [1, 2, 3], 
        ...     [5, 2, 0], 
        ...     [7, 5, 1]
        ... ]
        ...
        >>> test = Array(test)
        >>> test.flatten()
        ['1', '2', '3', '5', '2', '0', '7', '5', '1']
        '''

        array = self.show
        nrow = self.nrow
        ncol = self.ncol
        return [array[i][j] for i in range(nrow) for j in range(ncol)]


    def itemset(self, key, value):
        '''(Array, (int, int), int/str) -> None
        
        Mutate key number of self to value; this is exactly the same as 
        .__setitem__().

        >>> test = [
        ...     [1, 2, 3, 4], 
        ...     [5, 2, 0, 3], 
        ...     [7, 5, 1, 0], 
        ...     [2, 6, 2, 4]
        ... ]
        ...
        >>> test = Array(test)
        >>> test.itemset((3, 3), '6')
        >>> test
        Array([
        ['1', '2', '3', '4'],
        ['5', '2', '0', '3'],
        ['7', '5', '1', '0'],
        ['2', '6', '2', '6']
        ])
        '''

        self[key] = value


    def reshape(self, key0, key1):
        '''(Array, int, int) -> Array

        Reshape self to have key0 rows and key1 columns if applicable.
        
        >>> test = [
        ...     [1, 2, 3, 4], 
        ...     [5, 2, 0, 3], 
        ...     [7, 5, 1, 0], 
        ...     [2, 6, 2, 4]
        ... ]
        ...
        >>> test = Array(test)
        >>> test.reshape(8, 2)
        Array([
        ['1', '2'],
        ['3', '4'],
        ['5', '2'],
        ['0', '3'],
        ['7', '5'],
        ['1', '0'],
        ['2', '6'],
        ['2', '4']
        ])
        >>> test.reshape(2, 8)
        Array([
        ['1', '2', '3', '4', '5', '2', '0', '3'],
        ['7', '5', '1', '0', '2', '6', '2', '4']
        ])
        '''

        if self.size != key0 * key1:
            raise ValueError(
                'cannot reshape the Array of size ' + str(self.size) +\
                ' into shape (' + str(key0) + ', ' + str(key1) + ')'
            )
        result = [[] for i in range(key0)]
        k = 0
        for i in range(key0):
            for j in range(key1):
                result[i].append(self.flatten()[k])
                k += 1
        return Array(result)



if __name__ == '__main__':
    import doctest
    doctest.testmod()
