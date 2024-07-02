from typing import List
import argparse
import src.elevator as elevator
import unittest

class TestElevator(unittest.TestCase):

    def test_provided_example(self):
        test_run =  elevator.operate_elevator(start_floor=12, floors=[2,9,1,32])
        self.assertEqual(test_run, (560, [12,2,9,1,32]))

    def test_optimized_example(self):
        test_run =  elevator.operate_elevator(start_floor=12, floors=[2,9,1,32], optimize=True)
        self.assertEqual(test_run, (420, [12,1,2,9,32]))

    def test_top_floor_exception(self):
        self.assertRaises(ValueError, elevator.operate_elevator, start_floor=12, floors=[2,9,1,32], top_floor=10)

    def test_bad_floor(self):
        test_run =  elevator.list_int(values="2,9,1,32,badinput,-12,0.5")
        self.assertEqual(test_run, [2,9,1,32,-12])

    def test_positve_float(self):
        test_run = elevator.positive_float('32.7')
        self.assertEqual(test_run, 32.7)

    def test_negative_float(self):
        self.assertRaises(argparse.ArgumentTypeError, elevator.positive_float, -12.0)

    def test_floor_out_of_range(self):
        test_run =  elevator.operate_elevator(start_floor=12, floors=[2,9,1,-2,-4,32], top_floor=14, bottom_floor=-3)
        self.assertEqual(test_run, (280, [12,2,9,1,-2]))
    
    def test_travel_time_up(self):
        test_run = elevator.calc_travel_time(2,12,10)
        self.assertEqual(test_run, 100)
    
    def test_travel_time_down(self):
        test_run = elevator.calc_travel_time(12,2,10)
        self.assertEqual(test_run, 100)

    def test_time_at_floor(self):
        test_run =  elevator.calc_time_at_floor(floors=[12,2,9,1,32], time_at_floor=2)
        self.assertEqual(test_run, 10)


if __name__ == "__main__":
    unittest.main()
