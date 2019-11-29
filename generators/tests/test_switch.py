import unittest
from generators import G, switch

class TestGeneratorsSwitch(unittest.TestCase):
    def test_switch_basic_usage_1(self):
        self.assertEqual(
            G(
                range(10)
            ).switch(
                lambda i: i%3,
                {
                    0: lambda i: [i],
                    2: lambda i: float(i)
                }
            ).to(list),
            [
                [0],
                1,
                2.0,
                [3],
                4,
                5.0,
                [6],
                7,
                8.0,
                [9]
            ]
        )

    def test_switch_basic_usage_2(self):
        self.assertEqual(
            G(
                range(10)
            ).switch(
                lambda i: i%5,
                {
                    0: lambda i: i+1,
                    4: lambda i: float(i)
                }
            ).to(list),
            [
                1,
                1,
                2,
                3,
                4.0,
                6,
                6,
                7,
                8,
                9.0
            ]
        )
    
    def test_switch_basic_usage_3(self):
        self.assertEqual(
            G(
                'hello world or something'.split(' ')
            ).switch(
                lambda i: i[:2],
                {
                    'wo': lambda i: i+i,
                    'or': lambda i: i[0],
                    'he': lambda i: i.upper()
                }
            ).to(list),
            ['HELLO', 'worldworld', 'o', 'something']
        )
        
    def test_switch_with_default_1(self):
        self.assertEqual(
            G(
                range(10)
            ).switch(
                lambda i: i%5,
                {
                    0: lambda i: i+1,
                    4: lambda i: float(i)
                },
                lambda i: None
            ).to(list),
            [
                1,
                None,
                None,
                None,
                4.0,
                6,
                None,
                None,
                None,
                9.0
            ]
        )
    
    def test_switch_with_default_2(self):
        self.assertEqual(
            G(
                range(10)
            ).switch(
                lambda i: i%5,
                {
                    0: lambda i: i+1,
                    4: lambda i: float(i)
                },
                range
            ).to(list),
            [
                1,
                range(0, 1),
                range(0, 2),
                range(0, 3),
                4.0,
                6,
                range(0, 6),
                range(0, 7),
                range(0, 8),
                9.0
            ]
        )
        
    def test_switch_benchmark(self):
        '''ensure switch can process 1,000,000 items a second minimum'''
        from itertools import count
        speed = self.assertGreater(
            G(
                count()
            ).switch(
                lambda i: i%3,
                {
                    0: lambda i: [i],
                    2: lambda i: float(i)
                }
            ).benchmark(),
            1000000
        )
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
