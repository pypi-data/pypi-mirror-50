class Block(object):
    def __init__(self, start:int, end:int, orientation:bool, zero_index=True):
        """Creates a new Block from start and end coordinates and its orientation.

        Parameters
        ----------
        start : int
            Starting coordinate
        end : int
            End coordinate
        orientation : bool
            `True` if in the forward direction, otherwise, `False`.
        zero_index : bool, optional
            `True` if the coordinates follow zero-based notation of
            inclusive start and exclusive end values.
            `False` if coordinates follow one-basednotation of
            inclusive start and end values, by default True

        Raises
        ------
        ValueError
            Raises a ValueError when the `start` value is greater than or
            equal to the end value.

        """
        if start > end:
            raise ValueError(
                'Start value must always be less than end. '
                'Set `orientation` to `False` to indicate reverse direction.')
        self.start = start
        self.end = end
        self.orientation = orientation
        self.zero_index = zero_index

    @classmethod
    def encode(cls, vec:list):
        start = vec[0]
        offset = 0
        blocks = []
        for i, v in enumerate(vec):
            if i == 0:
                continue
            if vec[i-1] + 1 == v:
                offset += 1          
            elif vec[i-1] - 1 == v:
                offset -= 1          
            else:
                if offset >= 0:
                    blocks.append(
                        cls(start, start+offset+1, True))
                else:
                    blocks.append(
                        cls(start+offset, start, False))
                start = v
                offset = 0
                orientation = None

        if offset >= 0:
            blocks.append(
                cls(start, start+offset+1, True))
        else:
            blocks.append(
                cls(start+offset, start, False))
        return blocks
    
    def decode(self):
        if not self.orientation:
            return list(range(self.end, self.start-1, -1))
        return list(range(self.start, self.end, 1))

    def zero_to_one(self):
        if not self.zero_index:
            raise Exception(f'{self} is already in one-index notation.')
        return type(self)(
            self.start+1, self.end, self.orientation, zero_index=False)

    def one_to_zero(self):
        if self.zero_index:
            raise Exception(f'{self} is already in zero-index notation.')
        return type(self)(
            self.start-1, self.end, self.orientation, zero_index=True)

    def __repr__(self):
        return (
            f'Block({self.start}, {self.end}, {self.orientation}, '
            f'zero_index={self.zero_index})'
        )
