#include <Python.h>
#include <cstdint>
#include <new>
#include <sstream>
#include <type_traits>


/*
 * cinc integer type template.
 */
template<typename T>
struct cinc_integer : public PyLongObject
{
    static PyTypeObject typeobj;

    static PyObject* create_object(PyTypeObject* type, T initvalue);
    static PyObject* new_object(PyTypeObject* type, PyObject* args, PyObject* kwds);

    static PyObject* repr(cinc_integer<T>* self);

    static PyObject* compare(cinc_integer<T>* self, PyObject* other, int op);

    // Number protocol
    static PyObject* add(PyObject* op1, PyObject* op2);
    static PyObject* subtract(PyObject* op1, PyObject* op2);

    static PyObject* multiply(PyObject* op1, PyObject* op2);
    static PyObject* divide(PyObject* op1, PyObject* op2);
    static PyObject* remainder(PyObject* op1, PyObject* op2);
    static PyObject* divmod(PyObject* op1, PyObject* op2);
    static PyObject* power(PyObject* op1, PyObject* op2, PyObject* mod);

    static PyObject* negative(cinc_integer<T>* self);
    static PyObject* positive(cinc_integer<T>* self);
    static PyObject* abs(cinc_integer<T>* self);

    static PyObject* invert(cinc_integer<T>* self);

    static PyObject* lshift(PyObject* op1, PyObject* op2);
    static PyObject* rshift(PyObject* op1, PyObject* op2);

    static PyObject* bitwise_and(PyObject* op1, PyObject* op2);
    static PyObject* bitwise_or(PyObject* op1, PyObject* op2);
    static PyObject* bitwise_xor(PyObject* op1, PyObject* op2);

    // Methods
    static PyObject* mathfunc(PyObject* self, PyObject*);

    static PyObject* bit_length(PyObject*, PyObject*);
    static PyObject* from_bytes(PyTypeObject* self, PyObject* args, PyObject* kw);

    static PyObject* extract(cinc_integer<T>* self, PyObject* args, PyObject* kw);
    static PyObject* insert(cinc_integer<T>* self, PyObject* args, PyObject* kw);

    static PyObject* lrotate(cinc_integer<T>* self, PyObject* object);
    static PyObject* rrotate(cinc_integer<T>* self, PyObject* object);
};


/*
 * create_object
 *   Construct a cinc_integer object.
 *   If the type is not a derived class, the object is created directly.
 */
template<typename T>
PyObject* cinc_integer<T>::create_object(PyTypeObject* type, T initvalue)
{
    PyObject* x;

    if (std::is_unsigned<T>::value)
        x = PyLong_FromUnsignedLongLong(initvalue);
    else
        x = PyLong_FromLongLong(initvalue);

    if (x == NULL)
        return NULL;

    PyObject* args = PyTuple_New(1);
    if (args == NULL)
    {
        Py_DECREF(x);
        return NULL;
    }
    PyTuple_SET_ITEM(args, 0, x);

    PyObject* newobject = PyObject_Call((PyObject*)type, args, NULL);
    Py_DECREF(args);
    return (PyObject*)newobject;
}


/*
 * new method.
 *   Takes a single argument. Which can be a python int or a cinc type.
 */
static const char* new_keywords[] = {"x", NULL};
template<typename T>
PyObject* cinc_integer<T>::new_object(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    PyObject* x = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O",
            const_cast<char**>(new_keywords),
            &x))
        return NULL;

    if (x == NULL)
    {
        // no argument given, x defaults to 0.
        x = PyLong_FromLong(0);
    }
    else if (x->ob_type == type)
    {
        // x is the same type.
        // Just return x instead of making a copy.
        Py_INCREF(x);
        return x;
    }
    else
    {
        if (!PyLong_Check(x))
        {
            PyErr_Format(PyExc_TypeError,
                "%s() argument must be an int, not '%s'",
                type->tp_name, x->ob_type->tp_name);
            return NULL;
        }

        unsigned long long fullvalue = PyLong_AsUnsignedLongLongMask(x);
        T value = (T)fullvalue;

        if (std::is_unsigned<T>::value)
            x = PyLong_FromUnsignedLong(value);
        else
            x = PyLong_FromLongLong(value);
    }
    if (x == NULL)
        return NULL;

    // x is now set to an owned reference of an int.
    PyObject* call_args = PyTuple_New(1);
    if (call_args == NULL)
    {
        Py_DECREF(x);
        return NULL;
    }
    PyTuple_SET_ITEM(call_args, 0, x);

    cinc_integer<T>* newobject = (cinc_integer<T>*)PyLong_Type.tp_new(type, call_args, NULL);

    Py_DECREF(call_args);

    return (PyObject*)newobject;
}


/*
 * repr method.
 */
template<typename T>
PyObject* cinc_integer<T>::repr(cinc_integer<T>* self)
{
    T value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    if (std::is_unsigned<T>::value)
        return PyUnicode_FromFormat("%s(%llu)",
                                    Py_TYPE(self)->tp_name,
                                    (unsigned long long)value);
    else
        return PyUnicode_FromFormat("%s(%lld)",
                                    Py_TYPE(self)->tp_name,
                                    (long long)value);
}


/*
 * Comparison for cinc objects.
 */
template<typename T>
PyObject* cinc_integer<T>::compare(cinc_integer<T>* self, PyObject* other, int op)
{
    assert((PyObject_TypeCheck(self, &cinc_integer<T>::typeobj)));

    if (!PyLong_Check(other))
        Py_RETURN_NOTIMPLEMENTED;

    T value, othervalue;
    value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    othervalue = PyLong_AsUnsignedLongLongMask(other);

    bool result = false;
    switch (op)
    {
        case Py_LT:
            result = value < othervalue;
            break;
        case Py_LE:
            result = value <= othervalue;
            break;
        case Py_EQ:
            result = value == othervalue;
            break;
        case Py_NE:
            result = value != othervalue;
            break;
        case Py_GT:
            result = value > othervalue;
            break;
        case Py_GE:
            result = value >= othervalue;
            break;
    }

    PyObject* resultobject = result ? Py_True : Py_False;
    Py_INCREF(resultobject);
    return resultobject;
}


/*
 * Number protocol methods
 */

#define GET_OPARGS(op1, op1value, op2, op2value) \
    if (!PyObject_TypeCheck(op1, &cinc_integer<T>::typeobj) \
            || !PyLong_Check(op2))\
        Py_RETURN_NOTIMPLEMENTED; \
    op1value = PyLong_AsUnsignedLongLongMask(op1); \
    op2value = PyLong_AsUnsignedLongLongMask(op2);

/*
 * Addition and subtraction.
 */
template<typename T>
PyObject* cinc_integer<T>::add(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value);
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value + op2value);
}

template<typename T>
PyObject* cinc_integer<T>::subtract(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value)
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value - op2value);
}

/*
 * Multiply, divide, remainder and divmod.
 */
template<typename T>
PyObject* cinc_integer<T>::multiply(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value);
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value * op2value);
}

template<typename T>
PyObject* cinc_integer<T>::divide(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value)
    if (op2value == 0)
    {
        PyErr_SetString(PyExc_ZeroDivisionError, "division by zero");
        return NULL;
    }
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value / op2value);
}

template<typename T>
PyObject* cinc_integer<T>::remainder(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value);
    if (op2value == 0)
    {
        PyErr_SetString(PyExc_ZeroDivisionError,
            "integer division or modulo by zero");
        return NULL;
    }
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value % op2value);
}

template<typename T>
PyObject* cinc_integer<T>::divmod(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value);
    if (op2value == 0)
    {
        PyErr_SetString(PyExc_ZeroDivisionError,
            "integer division or modulo by zero");
        return NULL;
    }

    // The compiler can optimize this into a divmod instruction.
    T quot = op1value / op2value;
    T remain = op1value % op2value;

    PyObject* pyquot = cinc_integer<T>::create_object(Py_TYPE(op1), quot);
    if (pyquot == NULL)
        return NULL;
    PyObject* pyremain = cinc_integer<T>::create_object(Py_TYPE(op1), remain);
    if (pyremain == NULL)
    {
        Py_DECREF(pyquot);
        return NULL;
    }

    PyObject* result = PyTuple_New(2);
    if (result == NULL)
    {
        Py_DECREF(pyquot);
        Py_DECREF(pyremain);
    }
    PyTuple_SET_ITEM(result, 0, pyquot);
    PyTuple_SET_ITEM(result, 1, pyremain);
    return result;
}


/*
 * power
 */
template<typename T>
PyObject* cinc_integer<T>::power(PyObject* op1, PyObject* op2, PyObject* mod)
{
    T op1value, op2value, modvalue = 0;
    GET_OPARGS(op1, op1value, op2, op2value)
    if (mod != Py_None)
    {
        if (!PyLong_Check(mod))
            Py_RETURN_NOTIMPLEMENTED;

        if (op2value < 0)
        {
            PyErr_SetString(PyExc_ValueError,
                "pow() 2nd argument cannot be negative when 3rd argument specified");
            return NULL;
        }

        modvalue = PyLong_AsUnsignedLongLongMask(mod);
        if (modvalue == 0)
        {
            PyErr_SetString(PyExc_ValueError,
                "pow() 3rd argument cannot be 0");
            return NULL;
        }
    }

    T result = 1;
    for (T i = 0; i < op2value; ++i)
        result *= op1value;
    if (mod != Py_None)
        result %= modvalue;
    return cinc_integer<T>::create_object(Py_TYPE(op1), result);
}


/*
 * negative, positive and abs.
 */
template<typename T>
PyObject* cinc_integer<T>::negative(cinc_integer<T>* self)
{
    T value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    if (value == (T)-value)
    {
        Py_INCREF(self);
        return (PyObject*)self;
    }
    else
        return cinc_integer<T>::create_object(Py_TYPE(self), -value);
}

template<typename T>
PyObject* cinc_integer<T>::positive(cinc_integer<T>* self)
{
    Py_INCREF(self);
    return (PyObject*)self;
}

template<typename T>
PyObject* cinc_integer<T>::abs(cinc_integer<T>* self)
{
    T value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    if (value < 0)
        return cinc_integer<T>::create_object(Py_TYPE(self), -value);
    else
    {
        Py_INCREF(self);
        return (PyObject*)self;
    }
}


/*
 * invert
 */
template<typename T>
PyObject* cinc_integer<T>::invert(cinc_integer<T>* self)
{
    T value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    return cinc_integer<T>::create_object(Py_TYPE(self), ~value);
}


/*
 * left and right shift.
 */
template<typename T>
PyObject* cinc_integer<T>::lshift(PyObject* op1, PyObject* op2)
{
    T op1value;
    unsigned char shift;
    GET_OPARGS(op1, op1value, op2, shift);
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value << shift);
}

template<typename T>
PyObject* cinc_integer<T>::rshift(PyObject* op1, PyObject* op2)
{
    T op1value;
    unsigned char shift;
    GET_OPARGS(op1, op1value, op2, shift);
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value >> shift);
}


/*
 * bitwise and, or and xor.
 */
template<typename T>
PyObject* cinc_integer<T>::bitwise_and(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value);
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value & op2value);
}

template<typename T>
PyObject* cinc_integer<T>::bitwise_or(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value);
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value | op2value);
}

template<typename T>
PyObject* cinc_integer<T>::bitwise_xor(PyObject* op1, PyObject* op2)
{
    T op1value, op2value;
    GET_OPARGS(op1, op1value, op2, op2value);
    return cinc_integer<T>::create_object(Py_TYPE(op1),
                                          op1value ^ op2value);
}


/*
 * math functions.
 *   All of them return self, so only one function is needed.
 */

template<typename T>
PyObject* cinc_integer<T>::mathfunc(PyObject* self, PyObject*)
{
    Py_INCREF(self);
    return self;
}


/*
 * int methods.
 */

template<typename T>
PyObject* cinc_integer<T>::bit_length(PyObject*, PyObject*)
{
    return PyLong_FromLong(sizeof(T) * 8);
}

static const char* const from_bytes_keywords[] = {"bytes", "byteorder", NULL};
template<typename T>
PyObject* cinc_integer<T>::from_bytes(PyTypeObject* type, PyObject* args, PyObject* kw)
{
    PyObject *bytes, *byteorder;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "OU",
            const_cast<char**>(from_bytes_keywords),
            &bytes, &byteorder))
        return NULL;

    bytes = PyObject_Bytes(bytes);
    if (bytes == NULL)
        return NULL;

    if (PyBytes_GET_SIZE(bytes) > (Py_ssize_t)sizeof(T))
    {
        Py_DECREF(bytes);
        PyErr_Format(PyExc_OverflowError,
            "bytes object must have a length of %d or less",
            PyBytes_GET_SIZE(bytes));
        return NULL;
    }

    // Get the from_bytes function
    PyObject* int_dict = PyObject_GetAttrString((PyObject*)&PyLong_Type, "__dict__");

    PyObject* func = PyMapping_GetItemString(int_dict, "from_bytes");
    Py_DECREF(int_dict);

    // Create args tuple
    PyObject* newargs = Py_BuildValue("ONO", type, bytes, byteorder);
    if (newargs == NULL)
    {
        Py_DECREF(func);
        Py_DECREF(bytes);
        return NULL;
    }

    // Create kw dict
    PyObject* signedobj = (std::is_unsigned<T>::value) ? Py_False : Py_True;

    PyObject* newkw = Py_BuildValue("{sO}", "signed", signedobj);
    if (newkw == NULL)
    {
        Py_DECREF(newargs);
        Py_DECREF(func);
        return NULL;
    }

    PyObject* result = PyObject_Call(func, newargs, newkw);
    Py_DECREF(newkw);
    Py_DECREF(newargs);
    Py_DECREF(func);

    return result;
}


/*
 * extract(pos, size)
 */
static const char* extract_keywords[] = {"pos", "size", NULL};
template<typename T>
PyObject* cinc_integer<T>::extract(cinc_integer<T>* self, PyObject* args, PyObject* kw)
{
    unsigned char pos, size;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "BB",
            const_cast<char**>(extract_keywords), &pos, &size))
        return NULL;

    const uint64_t mask = (1 << size) -1;
    T value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    return cinc_integer<T>::create_object(Py_TYPE(self),
                                          (value >> pos) & mask);
}

/*
 * insert(value, pos, size)
 */
static const char* insert_keywords[] = {"value", "pos", "size", NULL};
template<typename T>
PyObject* cinc_integer<T>::insert(cinc_integer<T>* self, PyObject* args, PyObject* kw)
{
    unsigned PY_LONG_LONG othervalue;
    unsigned char pos, size;
    if (!PyArg_ParseTupleAndKeywords(args, kw, "KBB",
            const_cast<char**>(insert_keywords),
            &othervalue, &pos, &size))
        return NULL;

    T value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    const uint64_t mask = ((1 << size) -1) << pos;

    T otherbits = othervalue << pos;
    T result = value ^ ((value ^ otherbits) & mask);
    return cinc_integer<T>::create_object(Py_TYPE(self), result);
}

/*
 * rotate methods
 */
template<typename T>
PyObject* cinc_integer<T>::lrotate(cinc_integer<T>* self, PyObject* object)
{
    if (!PyLong_Check(object))
    {
        PyErr_Format(PyExc_TypeError,
            "lrotate() argument must be an int, not '%s'",
            Py_TYPE(object)->tp_name);
        return NULL;
    }
    typedef typename std::make_unsigned<T>::type valuetype;
    valuetype value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    uint64_t shift = PyLong_AsUnsignedLongLongMask(object);

    const unsigned char bits = sizeof(T) * CHAR_BIT;
    return cinc_integer<T>::create_object(Py_TYPE(self),
        (value << shift) | (value >> (bits - shift)));
}

template<typename T>
PyObject* cinc_integer<T>::rrotate(cinc_integer<T>* self, PyObject* object)
{
    if (!PyLong_Check(object))
    {
        PyErr_Format(PyExc_TypeError,
            "rrotate() argument must be an int, not '%s'",
            Py_TYPE(object)->tp_name);
        return NULL;
    }
    typedef typename std::make_unsigned<T>::type valuetype;
    valuetype value = PyLong_AsUnsignedLongLongMask((PyObject*)self);
    uint64_t shift = PyLong_AsUnsignedLongLongMask(object);

    const unsigned char bits = sizeof(T) * CHAR_BIT;
    return cinc_integer<T>::create_object(Py_TYPE(self),
        (value >> shift) | (value << (bits - shift)));
}


#define DECLARE_TYPE(type) _DECLARE_TYPE(type, cinc_integer<type ## _t>)
#define _DECLARE_TYPE(type, integer) \
PyNumberMethods type ## _number_methods = { \
    integer::add, /* add */ \
    integer::subtract, /* subtract */ \
    integer::multiply, /* multiply */ \
    integer::remainder, /* remainder */ \
    integer::divmod, /* divmod */ \
    integer::power, /* power */ \
    (unaryfunc)integer::negative, /* negate */ \
    (unaryfunc)integer::positive, /* positive */ \
    (unaryfunc)integer::abs, /* absolute */ \
    0, /* bool */ \
    (unaryfunc)integer::invert, /* invert */ \
    integer::lshift, /* left shift */ \
    integer::rshift, /* right shift */ \
    integer::bitwise_and, /* and */ \
    integer::bitwise_xor, /* xor */ \
    integer::bitwise_or, /* or */ \
    0, /* int */ \
    0, /* reserved */ \
    0, /* float */ \
    0, /* in place add */ \
    0, /* in place subtract */ \
    0, /* in place multiply */ \
    0, /* in place remainder */ \
    0, /* in place power */ \
    0, /* in place left shift */ \
    0, /* in place right shift */ \
    0, /* in place and */ \
    0, /* in place xor */ \
    0, /* in place or */ \
    integer::divide, /* floor divide */ \
    0, /* true divide */ \
}; \
static PyMethodDef type ## _methods[] = { \
    {"__round__", \
        integer::mathfunc, \
        METH_NOARGS}, \
    {"__trunc__", \
        integer::mathfunc, \
        METH_NOARGS}, \
    {"__floor__", \
        integer::mathfunc, \
        METH_NOARGS}, \
    {"__ceil__", \
        integer::mathfunc, \
        METH_NOARGS}, \
    {"conjugate", \
        integer::mathfunc, \
        METH_NOARGS}, \
\
    {"bit_length", \
        integer::bit_length, \
        METH_NOARGS}, \
\
    {"from_bytes", \
        (PyCFunction)integer::from_bytes, \
        METH_VARARGS | METH_KEYWORDS | METH_CLASS}, \
\
    {"extract", \
        (PyCFunction)integer::extract, \
        METH_VARARGS | METH_KEYWORDS, \
        "extract($self, /, pos, size)\n--\n\n" \
        "Extracts size bits starting from pos.\n" \
        ">>> x = " #type "(0b10010).extract(1, 4)\n" \
        ">>> bin(int(x))\n" \
        "'0b1001'"}, \
\
    {"insert", \
        (PyCFunction)integer::insert, \
        METH_VARARGS | METH_KEYWORDS, \
        "insert($self, /, value, pos, size)\n--\n\n" \
        "Returns a " #type " with the right most size bits from value inserted at pos.\n" \
        ">>> x = " #type "(0b0101)\n" \
        ">>> y = " #type "(0b110100).insert(x, 1, 4)\n" \
        ">>> bin(int(y))\n" \
        "'0b101010'"}, \
\
    {"lrotate", \
        (PyCFunction)integer::lrotate, \
        METH_O, \
        "lrotate($self, value, /)\n--\n\n" \
        "Return self left-rotate value."}, \
\
    {"rrotate", \
        (PyCFunction)integer::rrotate, \
        METH_O, \
        "rrotate($self, value, /)\n--\n\n" \
        "Return self right-rotate value.\n" \
        "self is always treated as an unsigned type."}, \
\
    {NULL} \
}; \
template<> PyTypeObject integer::typeobj = { \
    PyVarObject_HEAD_INIT(NULL, 0) \
    "cinc." #type, /* type name */ \
    sizeof(integer), /* basic size */ \
    0, /* item size */ \
    0, /* deallocator */ \
    0, /* print */ \
    0, /* getattr (deprecated) */ \
    0, /* setattr (deprecated) */ \
    0, /* async methods */ \
    (reprfunc)integer::repr, /* repr */ \
    &type ## _number_methods, /* number methods */ \
    0, /* sequence methods */ \
    0, /* mapping methods */ \
    0, /* Inherited from python int type */ /* hash */ \
    0, /* call */ \
    0, /* str */ \
    0, /* getattro */ \
    0, /* setattro */ \
    0, /* buffer methods */ \
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_LONG_SUBCLASS, /* flags */ \
    #type "(x=0)\n\n" \
    "cinc type for the " #type "_t C type.", /* doc */ \
    0, /* traverse */ \
    0, /* clear */ \
    (richcmpfunc)integer::compare, /* rich compare */ \
    0, /* weak list offset */ \
    0, /* iter */ \
    0, /* iter next */ \
    type ## _methods, /* methods */ \
    0, /* members */ \
    0, /* get set */ \
    &PyLong_Type, /* base type */ \
    0, /* dict */ \
    0, /* descriptor get */ \
    0, /* descriptor set */ \
    0, /* dict offset */ \
    0, /* init */ \
    0, /* alloc */ \
    integer::new_object /* new */ \
};
DECLARE_TYPE(int8)
DECLARE_TYPE(uint8)
DECLARE_TYPE(int16)
DECLARE_TYPE(uint16)
DECLARE_TYPE(int32)
DECLARE_TYPE(uint32)
DECLARE_TYPE(int64)
DECLARE_TYPE(uint64)


static PyModuleDef cincmodule = {
    PyModuleDef_HEAD_INIT,
    "cinc", /* name */
    "Fast fixed-sized C-like integer types.\n"
    "\n"
    "Signed types are named \"intN\" and unsigned types are named \"uintN\", where \"N\"\n"
    "is the number of bits. Types for 8, 16, 32 and 64 bits are provided.\n"
    "\n"
    "cinc integers can be constructed from a Python ints or cast from another cinc\ntype.\n"
    "\n"
    "They support all arithmetic operators and also have methods for bit rotate \n"
    "operations as well as bit extraction and insertion.",
    -1, /* size */
    NULL, /* methods */
    NULL, /* reload */
    NULL, /* traverse */
    NULL, /* clear */
    NULL /* free */
};

#define INIT_TYPE(type) \
    cinc_integer<type ## _t>::typeobj.tp_hash = PyLong_Type.tp_hash; \
    if (PyType_Ready(&cinc_integer<type ## _t>::typeobj) < 0) \
        return NULL;
#define ADD_TYPE(type) \
    Py_INCREF(&cinc_integer<type ## _t>::typeobj); \
    PyModule_AddObject(module, #type, \
        reinterpret_cast<PyObject*>(&cinc_integer<type ## _t>::typeobj));

PyMODINIT_FUNC PyInit_cinc()
{
    INIT_TYPE(int8)
    INIT_TYPE(uint8)
    INIT_TYPE(int16)
    INIT_TYPE(uint16)
    INIT_TYPE(int32)
    INIT_TYPE(uint32)
    INIT_TYPE(int64)
    INIT_TYPE(uint64)

    PyObject* module = PyModule_Create(&cincmodule);
    if (module == NULL)
        return NULL;

    ADD_TYPE(int8)
    ADD_TYPE(uint8)
    ADD_TYPE(int16)
    ADD_TYPE(uint16)
    ADD_TYPE(int32)
    ADD_TYPE(uint32)
    ADD_TYPE(int64)
    ADD_TYPE(uint64)

    return module;
}
