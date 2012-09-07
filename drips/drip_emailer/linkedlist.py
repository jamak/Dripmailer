import itertools

class LinkedList(object):
    """Immutable linked list class."""

    def __new__(cls, l):
        if isinstance(l, LinkedList):
            return l # Immutable, so no copy needed.
        i = iter(l)
        try:
            head = i.next()
        except StopIteration:
            return cls.EmptyList   # Return empty list singleton.

        tail = LinkedList(i)

        obj = super(LinkedList, cls).__new__(cls)
        obj._head = head
        obj._tail = tail
        return obj

    @classmethod
    def cons(cls, head, tail):
        ll =  cls([head])
        if not isinstance(tail, cls):
            tail = cls(tail)
        ll._tail = tail
        return ll

    # head and tail are not modifiable
    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    def __nonzero__(self):
        return True

    def __len__(self):
        return sum(1 for _ in self)

    def __add__(self, other):
        other = LinkedList(other)

        if not self:
            return other   # () + l = l
        start = l = LinkedList(iter(self))  # Create copy, as we'll mutate

        while l:
            if not l._tail: # Last element?
                l._tail = other
                break
            l = l._tail
        return start

    def __radd__(self, other):
        return LinkedList(other) + self

    def __iter__(self):
        x=self
        while x:
            yield x.head
            x=x.tail

    def __getitem__(self, idx):
        """Get item at specified index"""
        if isinstance(idx, slice):
            # Special case: Avoid constructing a new list, or performing O(n) length
            # calculation for slices like l[3:].  Since we're immutable, just return
            # the appropriate node. This becomes O(start) rather than O(n).
            # We can't do this for  more complicated slices however (eg [l:4]
            start = idx.start or 0
            if (start >= 0) and (idx.stop is None) and (idx.step is None or idx.step == 1):
                no_copy_needed=True
            else:
                length = len(self)  # Need to calc length.
                start, stop, step = idx.indices(length)
                no_copy_needed = (stop == length) and (step == 1)

            if no_copy_needed:
                l = self
                for i in range(start):
                    if not l: break # End of list.
                    l=l.tail
                return l
            else:
                # We need to construct a new list.
                if step < 1 :  # Need to instantiate list to deal with -ve step
                    return LinkedList(list(self)[start:stop:step])
                else:
                    return LinkedList(itertools.islice(iter(self), start, stop, step))
        else:
            # Non-slice index.
            if idx < 0 :
                idx = len(self)+idx
            if not self: raise IndexError("list index out of range")
            if idx == 0 :
                return self.head
            return self.tail[idx-1]

    def __mul__(self, n):
        if n <= 0 :
            return Nil
        l=self
        for i in range(n-1): l += self
        return l
    def __rmul__(self, n):
        return self * n

    # Ideally we should compute the has ourselves rather than construct
    # a temporary tuple as below.  I haven't impemented this here
    def __hash__(self): return hash(tuple(self))

    def __eq__(self, other):
        return self._cmp(other) == 0
    def __ne__(self,  other):
        return not self == other
    def __lt__(self, other):
        return self._cmp(other) < 0
    def __gt__(self, other):
        return self._cmp(other) > 0
    def __le__(self, other):
        return self._cmp(other) <= 0
    def __ge__(self, other):
        return self._cmp(other) >= 0

    def _cmp(self, other):
        """Acts as cmp(): -1 for self<other, 0 for equal, 1 for greater"""
        if not isinstance(other, LinkedList):
            return cmp(LinkedList,type(other))  # Arbitrary ordering.

        A, B = iter(self), iter(other)
        for a,b in itertools.izip(A,B):
            if a<b: return -1
            elif a > b: return 1

        try:
            A.next()
            return 1  # a has more items.
        except StopIteration: pass

        try:
            B.next()
            return -1  # b has more items.
        except StopIteration: pass

        return 0  # Lists are equal

    def __repr__(self):
        return "LinkedList([%s])" % ', '.join(map(repr,self))

class EmptyList(LinkedList):
    """A singleton representing an empty list."""
    def __new__(cls):
        return object.__new__(cls)

    def __iter__(self): return iter([])
    def __nonzero__(self): return False

    @property
    def head(self): raise IndexError("End of list")

    @property
    def tail(self): raise IndexError("End of list")

# Create EmptyList singleton
LinkedList.EmptyList = EmptyList()
del EmptyList
