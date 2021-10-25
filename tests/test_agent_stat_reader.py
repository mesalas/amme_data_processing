import unittest
from adp.make_agent_stat import make_agent_stat
from adp.make_agent_stat_daily import make_agent_stat_daily


class TestCase(unittest.TestCase):
    def test_read_stats_write_resampled_stats(self):
        for symbol in ["ABC","DEF", "GHI"]:
            test_args = ["tests/test_data/"+symbol +"_NYSE@0_Matching-Agents.csv.gz",
                         "5T",
                         "Pos",
                         "tests/test_data/"+symbol +"_NYSE@0_Agent_Pos.csv.gz"]
            make_agent_stat(test_args)
    
    def test_read_stats_write_daily_stats(self):
        for symbol in ["ABC","DEF", "GHI"]:
            test_args = ["tests/test_data/"+symbol +"_NYSE@0_Matching-Agents.csv.gz",
                         "PL",
                         "tests/test_data/"+symbol +"_NYSE@0_Agent_daily_pnl.csv.gz"]
            make_agent_stat_daily(test_args)


if __name__ == '__main__':
    unittest.main()