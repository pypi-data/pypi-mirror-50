import ctypes


__all__ = (
    'int8',  'int16',  'int32',  'int64',
    'uint8', 'uint16', 'uint32', 'uint64',
    )


def binaryop(name):
    def op(self, other):
        if not isinstance(other, int):
            return NotImplemented

        other = type(self)(other)
        f = getattr(super(Base, self), name)
        return type(self)(f(other))

    op.__name__ = name
    return op


class Base(int):
    c_type = None

    def __new__(cls, x=0):
        if type(x) == cls:
            return x
        elif not isinstance(x, int):
            fmt = '{}() argument must be an int, not "{}"'
            raise TypeError(fmt.format(cls.__name__, type(x).__name__))
        else:
            x = cls.c_type(x).value
            return super().__new__(cls, x)

    def __repr__(self):
        return '{}.{}({})'.format(
            type(self).__module__,
            type(self).__qualname__,
            super().__repr__(),
            )

    def __eq__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        other = type(self)(other)
        return super().__eq__(other)

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        other = type(self)(other)
        return super().__lt__(other)

    def __le__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        other = type(self)(other)
        return super().__le__(other)

    def __gt__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        other = type(self)(other)
        return super().__gt__(other)

    def __ge__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        other = type(self)(other)
        return super().__ge__(other)

    __hash__ = int.__hash__

    __add__ = binaryop('__add__')
    __sub__ = binaryop('__sub__')
    __mul__ = binaryop('__mul__')
    __floordiv__ = binaryop('__floordiv__')
    __mod__ = binaryop('__mod__')
    __lshift__ = binaryop('__lshift__')
    __rshift__ = binaryop('__rshift__')
    __and__ = binaryop('__and__')
    __or__ = binaryop('__or__')
    __xor__ = binaryop('__xor__')

    def __divmod__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        other = type(self)(other)
        div, mod = super().__divmod__(other)
        return type(self)(div), type(self)(mod)

    def __pow__(self, other, modulo=None):
        if not isinstance(other, int):
            return NotImplemented

        other = type(self)(other)

        if modulo is not None:
            if not isinstance(modulo, int):
                return NotImplemented

            modulo = type(self)(modulo)
            return type(self)(super().__pow__(other, modulo))
        else:
            return type(self)(super().__pow__(other))

    def __neg__(self):
        return type(self)(super().__neg__())

    def __pos__(self):
        return self

    def __abs__(self):
        return type(self)(super().__abs__())

    def __invert__(self):
        return type(self)(super().__invert__())

    def __round__(self):
        return self

    def __trunc__(self):
        return self

    def __floor__(self):
        return self

    def __ceil__(self):
        return self

    def conjugate(self):
        return self

    def bit_length(self):
        return ctypes.sizeof(self.c_type) * 8

    @classmethod
    def from_bytes(cls, bytesobj, byteorder):
        bytesobj = bytes(bytesobj)
        maxlen = ctypes.sizeof(cls.c_type)
        if len(bytesobj) > maxlen:
            fmt = "bytes object must have a length of {} or less"
            msg = fmt.format(maxlen)
            raise OverflowError(msg)

        return super().from_bytes(bytesobj, byteorder, signed=cls.signed)

    def extract(self, pos, size):
        mask = (1 << size) - 1
        return type(self)((self >> pos) & mask)

    def insert(self, value, pos, size):
        value <<= pos
        mask = ((1 << size) - 1) << pos
        result = self ^ ((self ^ value) & mask)
        return result

    def lrotate(self, shift):
        bits = ctypes.sizeof(self.c_type) * 8
        shift &= bits-1
        uvalue = int(self) & ((1 << bits)-1)

        result = (uvalue << shift) | (uvalue >> (bits - shift))
        return type(self)(result)

    def rrotate(self, shift):
        bits = ctypes.sizeof(self.c_type) * 8
        shift &= bits-1
        uvalue = int(self) & ((1 << bits)-1)

        result = (uvalue >> shift) | (uvalue << (bits - shift))
        return type(self)(result)


class int8(Base):
    c_type = ctypes.c_int8
    signed = True


class int16(Base):
    c_type = ctypes.c_int16
    signed = True


class int32(Base):
    c_type = ctypes.c_int32
    signed = True


class int64(Base):
    c_type = ctypes.c_int64
    signed = True


class uint8(Base):
    c_type = ctypes.c_uint8
    signed = False


class uint16(Base):
    c_type = ctypes.c_uint16
    signed = False


class uint32(Base):
    c_type = ctypes.c_uint32
    signed = False


class uint64(Base):
    c_type = ctypes.c_uint64
    signed = False
