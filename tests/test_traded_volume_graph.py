import unittest
from adp.make_full_traded_volume_graph import make_full_traded_volume_graph
from adp.readers.trades_reader import TradesData
import pandas as pd


class TestCase(unittest.TestCase):
    def test_traded_volume_graph(self):
        matched_orders_file_path = "tests/test_data/ABC_NYSE@0_Matching-MatchedOrders.csv.gz"
        make_full_traded_volume_graph(matched_orders_file_path,
                          "tests/test_data/full_traded_volume_graph.gefx")
        

if __name__ == '__main__':
    unittest.main()