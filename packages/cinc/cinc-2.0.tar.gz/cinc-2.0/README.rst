cinc provides fixed-width C-like integer types. The speed of these types are
comparable to python ints.

=====
Usage
=====

Signed types are named "intN" and unsigned types are named "uintN", where "N"
is the number of bits. Types for 8, 16, 32 and 64 bits are provided.

cinc integers can be constructed from Python ints or cast from another cinc
type. If the source integer has more bits than the cinc type then it is
truncated:

.. code:: python

    >>> x = uint32(0xFFFFFFFF)
    >>> x
    cinc.uint32(4294967295)
    >>> uint16(x)
    cinc.uint16(65535)

==========
Arithmetic
==========

cinc integers are compatible with python ints. Comparisons and operators cast
the integer to their cinc type before performing the comparison or operation.

The result of the operation has the same type as the left operand:

.. code:: python

    >>> x = uint32(2)
    >>> y = int32(2)
    >>> x + y
    cinc.uint32(4)
    >>> y + x
    cinc.int32(4)

This applies to operations with python ints too:

.. code:: python

    >>> x = uint32(2)
    >>> x + 2
    cinc.uint32(4)
    >>> 2 + x
    4

There are also methods for bit rotate operations and bit insertion and
extraction:

.. code:: python

    >>> x = uint32(0x000000ff)
    >>> hex(x.rrotate(8))
    '0xff000000'
    >>> y = uint32(0xff000000)
    >>> hex(y.insert(0xff, 8, 8))
    '0xff00ff00'
    >>> hex(y.extract(16, 16))
    '0xff00'

===============
Python Fallback
===============

If no C++ compiler is available during installation, then a Python source module
based on ctypes is used instead. The Python version is significantly slower than
the compiled C
extension.
