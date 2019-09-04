import unittest 

from .RingBuffer import RingBuffer

class RingBufferUnitTests(unittest.TestCase): 
    def test_full(self):   
        size = 3      
        rb = RingBuffer(size)

        rb.add(0)
        self.assertFalse(rb.full())

        rb.add(0)
        self.assertFalse(rb.full())

        rb.add(0)
        self.assertTrue(rb.full())

    def test_get(self):
        size = 2
        rb = RingBuffer(size)

        rb.add('hi')
        self.assertEqual('hi', rb.get(0))
        self.assertRaises(AssertionError, rb.get, 1)
        self.assertRaises(AssertionError, rb.get, -1)

        rb.add(-1)
        self.assertEqual(-1, rb.get(1))
        self.assertRaises(AssertionError, rb.get, 2)
        self.assertRaises(AssertionError, rb.get, -1)

    def test_add(self):
        size = 10
        rb = RingBuffer(size)

        for i in range(100):
            rb.add(i)

        self.assertEqual(90, rb.get(0))