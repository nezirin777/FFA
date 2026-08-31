"""転職前提と経験済み職への再転職判定の回帰テスト。"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cgi_py import tensyoku


class TensyokuReentryTests(unittest.TestCase):
    def setUp(self):
        self.target_data = {
            "req_str": 100,
            "req_int": 100,
            "req_mnd": 100,
            "req_vit": 100,
            "req_dex": 100,
            "req_agi": 100,
            "req_cha": 100,
            "req_karma": 100,
            "job_reqs": [60] + [0] * 30,
        }
        self.low_chara = {
            "str": 10, "int": 10, "mnd": 10, "vit": 10,
            "dex": 10, "agi": 10, "cha": 10, "karma": 10,
        }

    def test_experienced_job_ignores_all_prerequisites(self):
        history = [0] * 31
        history[5] = 1

        self.assertTrue(tensyoku.can_change_to_job(
            self.low_chara, history, 5, self.target_data,
        ))

    def test_unexperienced_job_still_requires_stats_and_mastery(self):
        self.assertFalse(tensyoku.can_change_to_job(
            self.low_chara, [0] * 31, 5, self.target_data,
        ))

    def test_unexperienced_job_is_available_when_all_prerequisites_are_met(self):
        history = [0] * 31
        history[0] = 60
        ready_chara = {key: 100 for key in self.low_chara}

        self.assertTrue(tensyoku.can_change_to_job(
            ready_chara, history, 5, self.target_data,
        ))


if __name__ == "__main__":
    unittest.main()
