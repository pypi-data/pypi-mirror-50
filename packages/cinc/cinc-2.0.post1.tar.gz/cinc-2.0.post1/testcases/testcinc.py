import unittest
import unittest.mock
import math
import pickle

from dualtest import *


def classes():
    """
    Return all the cinc types.

    This function is necessary because the classes aren't available until
    they're loaded by dualtest.
    """
    return (
           int8,  uint8,
           int16, uint16,
           int32, uint32,
           int64, uint64,
           )

def classes_size():
    """Return cinc types grouped by bit size."""
    return (
           (8,  (int8,  uint8)),
           (16, (int16, uint16)),
           (32, (int32, uint32)),
           (64, (int64, uint64)),
           )


class CincTestCase(DualTestCase):
    import_from_names = [
        ('cinc', ['*']),
        ]

    def test_default_construction(self):
        """Test if cinc types are default contructed to 0"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = cint()
                self.assertEqual(value, cint(0))

    def test_bit_truncate(self):
        """Test if cinc types truncate ints to their fixed size"""
        for size, classlist in classes_size():
            for cint in classlist:
                with self.subTest(cint=cint):
                    intvalue = 0xFF << size
                    value = cint(intvalue)
                    self.assertEqual(value, 0)

    def test_casting(self):
        """Test casting between signed and unsigned cinc types"""
        for size, (cint, cuint) in classes_size():
            with self.subTest(size=size):
                maxvalue = (1 << size) - 1
                value = cuint(maxvalue)
                self.assertEqual(cint(value), -1)

                value = cint(-1)
                self.assertEqual(cuint(value), maxvalue)

    def test_str(self):
        """Test converting to str"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = cint(1)
                self.assertEqual(str(value), '1')

    def test_repr(self):
        """Test repr conversion"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = cint(1)
                expected = 'cinc.{}(1)'.format(cint.__name__)
                self.assertEqual(repr(value), expected)

    def test_hash(self):
        """Test hash function"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = cint(0x7F)
                self.assertEqual(hash(value), hash(0x7F))

                value = cint(-1)
                self.assertNotEqual(hash(value), -1)

    def test_bool(self):
        """Test boolean conversion"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = cint(1)
                self.assertTrue(value)
                value = cint(0)
                self.assertFalse(value)

    def test_pickle(self):
        """Test if cinc types can be pickled"""
        for cint in classes():
            with self.subTest(cint=cint):
                data = pickle.dumps(cint(1))
                value = pickle.loads(data)
                self.assertEqual(value, cint(1))
                self.assertIsInstance(value, cint)


class CincOperatorTestCase(DualTestCase):
    import_from_names = [
        ('cinc', ['*']),
        ]

    def test_equals(self):
        """Test if equals operator works"""
        for cint in classes():
            with self.subTest(cint=cint):
                self.assertEqual(cint(1), cint(1))

    def test_int_equals(self):
        """Test if equals operator with python ints work"""
        for cint in classes():
            with self.subTest(cint=cint):
                self.assertEqual(cint(1), 1)
                self.assertEqual(1, cint(1))

    def test_equals_truncate(self):
        """Test if equals operator truncates ints"""
        largevalue = 0x10000000000000001
        for cint in classes():
            with self.subTest(cint=cint):
                self.assertEqual(cint(1), largevalue)
                self.assertEqual(largevalue, cint(1))

    def test_not_equals_truncate(self):
        """Test if not equals operator truncates ints"""
        largevalue = 0x10000000000000001
        for cint in classes():
            with self.subTest(cint=cint):
                self.assertFalse(cint(1) != largevalue)
                self.assertFalse(largevalue != cint(1))

    def test_sign_comparison(self):
        """Test comparison between signed and unsigned cinc types"""
        largevalue = 0xFFFFFFFFFFFFFFFF

        for size, (cint, cuint) in classes_size():
            with self.subTest(size=size):
                value = cint(-1)
                uvalue = cuint(largevalue)
                self.assertEqual(value, uvalue)
                self.assertEqual(uvalue, value)

    def test_ordering(self):
        """Test if ordering operators work"""
        for cint in classes():
            with self.subTest(cint=cint):
                self.assertLess(cint(1), cint(2))
                self.assertLessEqual(cint(1), cint(2))
                self.assertLessEqual(cint(1), cint(1))
                self.assertGreater(cint(2), cint(1))
                self.assertGreaterEqual(cint(2), cint(1))
                self.assertGreaterEqual(cint(1), cint(1))

    def test_sign_ordering(self):
        """Test ordering between signed and unsigned cinc types"""
        for size, (cint, cuint) in classes_size():
            with self.subTest(size=size):
                value = cint(-1)
                uvalue = cuint(0)
                self.assertLess(value, uvalue)
                self.assertLessEqual(value, uvalue)

                self.assertLess(uvalue, value)
                self.assertLessEqual(uvalue, value)

    def test_int_ordering(self):
        """Test if ordering operators with python ints work"""
        largevalue = 0xFFFFFFFFFFFFFFFF

        classlist = (uint8, uint16, uint32, uint64)
        for cint in classlist:
            with self.subTest(cint=cint):
                value = cint(largevalue)
                self.assertGreater(value, 0)
                self.assertGreaterEqual(value, 0)

                value = cint(0)
                self.assertLess(value, largevalue)
                self.assertLessEqual(value, largevalue)

        classlist = (int8, int16, int32, int64)
        for cint in classlist:
            with self.subTest(cint=cint):
                value = cint(largevalue)
                self.assertLess(value, 0)
                self.assertLessEqual(value, 0)

                value = cint(0)
                self.assertGreater(value, largevalue)
                self.assertGreaterEqual(value, largevalue)

    def test_arithmetic(self):
        """Test if arithmetic operators work"""
        for cint in classes():
            with self.subTest(cint=cint):
                # Addition
                value = cint(1) + cint(2)
                self.assertEqual(value, cint(3))
                self.assertIsInstance(value, cint)

                # Subtraction
                value = cint(3) - cint(2)
                self.assertEqual(value, cint(1))
                self.assertIsInstance(value, cint)

                # Multiplication
                value = cint(2) * cint(3)
                self.assertEqual(value, cint(6))
                self.assertIsInstance(value, cint)

                # Division
                value = cint(6) // cint(2)
                self.assertEqual(value, cint(3))
                self.assertIsInstance(value, cint)

                # Modulo
                value = cint(8) % cint(3)
                self.assertEqual(value, cint(2))
                self.assertIsInstance(value, cint)

                # divmod
                div, mod = divmod(cint(10), cint(3))
                self.assertEqual(div, cint(3))
                self.assertIsInstance(div, cint)

                self.assertEqual(mod, cint(1))
                self.assertIsInstance(mod, cint)

                # Power
                value = cint(2) ** cint(3)
                self.assertEqual(value, cint(8))
                self.assertIsInstance(value, cint)

    def test_arithmetic_casting(self):
        """Test if arithmetic with different types returns the right type"""
        for size, (cint, cuint) in classes_size():
            with self.subTest(size=size):
                # Addition
                value = cint(1) + cuint(2)
                self.assertEqual(value, cint(3))
                self.assertIsInstance(value, cint)

                value = cuint(1) + cint(2)
                self.assertEqual(value, cuint(3))
                self.assertIsInstance(value, cuint)

                # Subtraction
                value = cint(3) - cuint(2)
                self.assertEqual(value, cint(1))
                self.assertIsInstance(value, cint)

                value = cuint(3) - cint(2)
                self.assertEqual(value, cuint(1))
                self.assertIsInstance(value, cuint)

                # Multiplication
                value = cint(2) * cuint(3)
                self.assertEqual(value, cint(6))
                self.assertIsInstance(value, cint)

                value = cuint(2) * cint(3)
                self.assertEqual(value, cuint(6))
                self.assertIsInstance(value, cuint)

                # Division
                value = cint(6) // cuint(2)
                self.assertEqual(value, cint(3))
                self.assertIsInstance(value, cint)

                value = cuint(6) // cint(2)
                self.assertEqual(value, cuint(3))
                self.assertIsInstance(value, cuint)

                # Modulo
                value = cint(8) % cuint(3)
                self.assertEqual(value, cint(2))
                self.assertIsInstance(value, cint)

                value = cuint(8) % cint(3)
                self.assertEqual(value, cuint(2))
                self.assertIsInstance(value, cuint)

                # divmod
                div, mod = divmod(cint(10), cuint(3))
                self.assertEqual(div, cint(3))
                self.assertIsInstance(div, cint)

                self.assertEqual(mod, cint(1))
                self.assertIsInstance(mod, cint)

                div, mod = divmod(cuint(10), cint(3))
                self.assertEqual(div, cuint(3))
                self.assertIsInstance(div, cuint)

                self.assertEqual(mod, cuint(1))
                self.assertIsInstance(mod, cuint)

                # Power
                value = cint(2) ** cuint(3)
                self.assertEqual(value, cint(8))
                self.assertIsInstance(value, cint)

                value = cuint(2) ** cint(3)
                self.assertEqual(value, cuint(8))
                self.assertIsInstance(value, cuint)

    def test_int_arithmetic(self):
        """Test if arithmetic with python ints work"""
        for cint in classes():
            with self.subTest(cint=cint):
                # Addition
                value = cint(1) + 2
                self.assertEqual(value, cint(3))
                self.assertIsInstance(value, cint)

                # Subtraction
                value = cint(3) - 2
                self.assertEqual(value, cint(1))
                self.assertIsInstance(value, cint)

                # Multiplication
                value = cint(2) * 3
                self.assertEqual(value, cint(6))
                self.assertIsInstance(value, cint)

                # Division
                value = cint(6) // 2
                self.assertEqual(value, cint(3))
                self.assertIsInstance(value, cint)

                # Modulo
                value = cint(8) % 3
                self.assertEqual(value, cint(2))
                self.assertIsInstance(value, cint)

                # divmod
                div, mod = divmod(cint(10), 3)
                self.assertEqual(div, cint(3))
                self.assertIsInstance(div, cint)

                self.assertEqual(mod, cint(1))
                self.assertIsInstance(mod, cint)

                # Power
                value = cint(2) ** 3
                self.assertEqual(value, cint(8))
                self.assertIsInstance(value, cint)

    def test_int_arithmetic_right(self):
        """Test if arithmetic on the right side of python ints work"""
        for cint in classes():
            with self.subTest(cint=cint):
                # Addition
                value = 1 + cint(2)
                self.assertEqual(value, 3)
                self.assertIs(type(value), int)

                # Subtraction
                value = 3 - cint(2)
                self.assertEqual(value, 1)
                self.assertIs(type(value), int)

                # Multiplication
                value = 2 * cint(3)
                self.assertEqual(value, 6)
                self.assertIs(type(value), int)

                # Division
                value = 6 // cint(2)
                self.assertEqual(value, 3)
                self.assertIs(type(value), int)

                # Modulo
                value = 8 % cint(3)
                self.assertEqual(value, 2)
                self.assertIs(type(value), int)

                # divmod
                div, mod = divmod(10, cint(3))
                self.assertEqual(div, 3)
                self.assertIs(type(div), int)

                self.assertEqual(mod, 1)
                self.assertIs(type(mod), int)

                # Power
                value = 2 ** cint(3)
                self.assertEqual(value, 8)
                self.assertIs(type(value), int)

    def test_int_arithmetic_right_overflow(self):
        """Test if large python ints on the left aren't being truncated"""
        largevalue = 0xFFFFFFFFFFFFFFFF0

        for cint in classes():
            with self.subTest(cint=cint):
                # Addition
                value = largevalue + cint(1)
                self.assertEqual(value, largevalue + 1)
                self.assertIs(type(value), int)

                # Subtraction
                value = largevalue - cint(1)
                self.assertEqual(value, largevalue - 1)
                self.assertIs(type(value), int)

                # Multiplication
                value = largevalue * cint(2)
                self.assertEqual(value, largevalue * 2)
                self.assertIs(type(value), int)

                # Division
                value = largevalue // cint(2)
                self.assertEqual(value, largevalue // 2)
                self.assertIs(type(value), int)

    def test_true_division_overflow(self):
        """Test if large python ints aren't being truncated in division"""
        largevalue = 0x20000000000000000

        for cint in classes():
            with self.subTest(cint=cint):
                value = largevalue / cint(2)
                self.assertEqual(value, largevalue / 2)
                self.assertIsInstance(value, float)

    def test_bitwise(self):
        """Test if bitwise operators work"""
        for cint in classes():
            with self.subTest(cint=cint):
                # Left shift
                value = cint(0b1) << cint(2)
                self.assertEqual(value, cint(0b100))
                self.assertIsInstance(value, cint)

                # Right shift
                value = cint(0b100) >> cint(2)
                self.assertEqual(value, cint(0b1))
                self.assertIsInstance(value, cint)

                # And
                value = cint(0xFF) & cint(0x0F)
                self.assertEqual(value, cint(0x0F))
                self.assertIsInstance(value, cint)

                # Or
                value = cint(0xF0) | cint(0x0F)
                self.assertEqual(value, cint(0xFF))
                self.assertIsInstance(value, cint)

                # Xor
                value = cint(0x0F) ^ cint(0xFF)
                self.assertEqual(value, cint(0xF0))
                self.assertIsInstance(value, cint)

    def test_bitwise_casting(self):
        """Test if bitwise operators with different types returns the right type"""
        for size, (cint, cuint) in classes_size():
            with self.subTest(size=size):
                # Left shift
                value = cint(0b1) << cuint(2)
                self.assertEqual(value, cint(0b100))
                self.assertIsInstance(value, cint)

                value = cuint(0b1) << cint(2)
                self.assertEqual(value, cuint(0b100))
                self.assertIsInstance(value, cuint)

                # Right shift
                value = cint(0b100) >> cuint(2)
                self.assertEqual(value, cint(0b1))
                self.assertIsInstance(value, cint)

                value = cuint(0b100) >> cint(2)
                self.assertEqual(value, cuint(0b1))
                self.assertIsInstance(value, cuint)

                # And
                value = cint(0xFF) & cuint(0x0F)
                self.assertEqual(value, cint(0x0F))
                self.assertIsInstance(value, cint)

                value = cuint(0xFF) & cint(0x0F)
                self.assertEqual(value, cuint(0x0F))
                self.assertIsInstance(value, cuint)

                # Or
                value = cint(0xF0) | cuint(0x0F)
                self.assertEqual(value, cint(0xFF))
                self.assertIsInstance(value, cint)

                value = cuint(0xF0) | cint(0x0F)
                self.assertEqual(value, cuint(0xFF))
                self.assertIsInstance(value, cuint)

                # Xor
                value = cint(0x0F) ^ cuint(0xFF)
                self.assertEqual(value, cint(0xF0))
                self.assertIsInstance(value, cint)

                value = cuint(0x0F) ^ cint(0xFF)
                self.assertEqual(value, cuint(0xF0))
                self.assertIsInstance(value, cuint)

    def test_int_bitwise(self):
        """Test if bitwise operators with python ints work"""
        for cint in classes():
            with self.subTest(cint=cint):
                # Left shift
                value = cint(0b1) << 2
                self.assertEqual(value, cint(0b100))
                self.assertIsInstance(value, cint)

                # Right shift
                value = cint(0b100) >> 2
                self.assertEqual(value, cint(0b1))
                self.assertIsInstance(value, cint)

                # And
                value = cint(0xFF) & 0x0F
                self.assertEqual(value, cint(0x0F))
                self.assertIsInstance(value, cint)

                # Or
                value = cint(0xF0) | 0x0F
                self.assertEqual(value, cint(0xFF))
                self.assertIsInstance(value, cint)

                # Xor
                value = cint(0x0F) ^ 0xFF
                self.assertEqual(value, cint(0xF0))
                self.assertIsInstance(value, cint)

    def test_int_bitwise_right(self):
        """Test if bitwise operators on the right side of python ints work"""
        for cint in classes():
            with self.subTest(cint=cint):
                # Left shift
                value = 0b1 << cint(2)
                self.assertEqual(value, 0b100)
                self.assertIs(type(value), int)

                # Right shift
                value = 0b100 >> cint(2)
                self.assertEqual(value, 0b1)
                self.assertIs(type(value), int)

                # And
                value = 0xFF & cint(0x0F)
                self.assertEqual(value, 0x0F)
                self.assertIs(type(value), int)

                # Or
                value = 0xF0 | cint(0x0F)
                self.assertEqual(value, 0xFF)
                self.assertIs(type(value), int)

                # Xor
                value = 0x0F ^ cint(0x7F)
                self.assertEqual(value, 0x70)
                self.assertIs(type(value), int)

    def test_negate(self):
        """Test if negation works"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = -cint(1)
                self.assertEqual(value, cint(-1))
                self.assertIsInstance(value, cint)

    def test_pos(self):
        """Test if positive operator works"""
        for cint in classes():
            with self.subTest(cint=cint):
                orig = cint(1)
                new = +orig
                self.assertIsInstance(new, cint)
                self.assertIs(new, orig)

    def test_invert(self):
        """Test if bit invert works"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = ~cint(0)
                self.assertEqual(value, cint(-1))
                self.assertIsInstance(value, cint)

    def test_abs(self):
        """Test if abs works"""
        for size, (cint, cuint) in classes_size():
            with self.subTest(size=size):
                value = abs(cint(-1))
                self.assertEqual(value, cint(1))
                self.assertIsInstance(value, cint)

                # Unsigned abs does nothing
                value = abs(cuint(-1))
                self.assertEqual(value, cuint(-1))
                self.assertIsInstance(value, cuint)

    def test_round(self):
        """Test if round works"""
        for cint in classes():
            with self.subTest(cint=cint):
                orig = cint(1)
                new = round(orig)
                self.assertIsInstance(new, cint)
                self.assertIs(new, orig)

    def test_trunc(self):
        """Test if trunc works"""
        for cint in classes():
            with self.subTest(cint=cint):
                orig = cint(1)
                new = math.trunc(orig)
                self.assertIsInstance(new, cint)
                self.assertIs(new, orig)

    def test_floor(self):
        """Test if floor works"""
        for cint in classes():
            with self.subTest(cint=cint):
                orig = cint(1)
                new = math.floor(orig)
                self.assertIsInstance(new, cint)
                self.assertIs(new, orig)

    def test_ceil(self):
        """Test if ceil works"""
        for cint in classes():
            with self.subTest(cint=cint):
                orig = cint(1)
                new = math.ceil(orig)
                self.assertIsInstance(new, cint)
                self.assertIs(new, orig)

    def test_zero_division(self):
        """Test if division by zero raises ZeroDivisionError"""
        for cint in classes():
            with self.subTest(cint=cint):
                with self.assertRaises(ZeroDivisionError):
                    cint(1) // cint(0)

    def test_zero_modulo(self):
        """Test if modulo by zero raises ZeroDivisionError"""
        for cint in classes():
            with self.subTest(cint=cint):
                with self.assertRaises(ZeroDivisionError):
                    cint(1) % cint(0)

    def test_zero_divmod(self):
        """Test if divmod by zero raises ZeroDivisionError"""
        for cint in classes():
            with self.subTest(cint=cint):
                with self.assertRaises(ZeroDivisionError):
                    divmod(uint32(1), uint32(0))

    def test_power(self):
        """Test if power operator works"""
        self.assertEqual(pow(int32(0), int32(0)), int32(1))
        self.assertEqual(pow(int32(0), int32(1)), int32(0))
        self.assertEqual(pow(int32(1), int32(0)), int32(1))
        self.assertEqual(pow(int32(1), int32(1)), int32(1))

        self.assertEqual(pow(int32(2), int32(0)), int32(1))
        self.assertEqual(pow(int32(2), int32(10)), int32(1024))
        self.assertEqual(pow(int32(2), int32(20)), int32(1024 * 1024))
        self.assertEqual(pow(int32(2), int32(30)), int32(1024 * 1024 * 1024))

        self.assertEqual(pow(int32(-2), int32(0)), int32(1))
        self.assertEqual(pow(int32(-2), int32(1)), int32(-2))
        self.assertEqual(pow(int32(-2), int32(2)), int32(4))
        self.assertEqual(pow(int32(-2), int32(3)), int32(-8))

        self.assertEqual(pow(int32(2), int32(10), int32(1000)), int32(24))

        self.assertRaises(ValueError, pow, int32(-1), int32(-2), int32(3))
        self.assertRaises(ValueError, pow, int32(1), int32(2), int32(0))


class CincMethodTestCase(DualTestCase):
    import_from_names = [
        ('cinc', ['*']),
        ]

    def test_conjugate(self):
        """Test if conjugate method works"""
        for cint in classes():
            with self.subTest(cint=cint):
                orig = cint(1)
                new = orig.conjugate()
                self.assertIsInstance(new, cint)
                self.assertIs(new, orig)

    def test_bit_length(self):
        """Test if the bit_length method returns a constant"""
        for size, classes in classes_size():
            for cint in classes:
                with self.subTest(cint=cint):
                    self.assertEqual(cint().bit_length(), size)

    def test_from_bytes(self):
        """Test if from_bytes method works"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = cint.from_bytes(b'\1', 'little')
                self.assertEqual(value, cint(1))
                self.assertIsInstance(value, cint)

    def test_from_bytes_max_length(self):
        """Test if from_bytes raises an error when too many bytes are given"""
        for size, classlist in classes_size():
            for cint in classlist:
                with self.subTest(cint=cint):
                    data = b'\0' * (size+1)
                    self.assertRaises(OverflowError,
                                      cint.from_bytes, data, 'little')

    def test_extract(self):
        """Test if extract method works"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = cint(0xF0)
                new = value.extract(4, 4)
                self.assertEqual(new, 0xF)
                self.assertIsInstance(new, cint)

    def test_insert(self):
        """Test if insert method works"""
        for cint in classes():
            with self.subTest(cint=cint):
                value = cint(0)
                new = value.insert(0xF, 4, 4)
                self.assertEqual(new, 0xF0)
                self.assertIsInstance(new, cint)

    def test_lrotate(self):
        """Test if lrotate method works"""
        for size, classlist in classes_size():
            for cint in classlist:
                with self.subTest(cint=cint):
                    value = cint(0b11 << (size-2) | 0b11)
                    new = value.lrotate(2)
                    self.assertEqual(new, 0b1111)
                    self.assertIsInstance(new, cint)

    def test_lrotate_overflow(self):
        """Test if lrotate laps around"""
        for size, classlist in classes_size():
            for cint in classlist:
                with self.subTest(cint=cint):
                    value = cint(1)
                    new = value.lrotate(size+1)
                    self.assertEqual(new, 2)

    def test_rrotate(self):
        """Test if rrotate method works"""
        for size, classlist in classes_size():
            for cint in classlist:
                with self.subTest(cint=cint):
                    value = cint(0b11 << (size-2) | 0b11)
                    new = value.rrotate(2)
                    expected = 0b1111 << (size-4)
                    self.assertEqual(new, expected)
                    self.assertIsInstance(new, cint)

    def test_rrotate_overflow(self):
        """Test if rrotate laps around"""
        for size, classlist in classes_size():
            for cint in classlist:
                with self.subTest(cint=cint):
                    value = cint(2)
                    new = value.rrotate(size+1)
                    self.assertEqual(new, 1)

    def test_signed_lrotate(self):
        """Test if signed lrotate works"""
        for size, (cint, _) in classes_size():
            with self.subTest(cint=cint):
                value = cint(1 << (size-1))
                new = value.lrotate(1)
                self.assertEqual(new, 1)

    def test_signed_rrotate(self):
        """Test if signed rrotate works"""
        for size, (cint, _) in classes_size():
            with self.subTest(cint=cint):
                value = cint(1 << (size-1))
                new = value.rrotate(size-1)
                self.assertEqual(new, 1)
