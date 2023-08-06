from tests.core.common import *


class AggregationMethodsTests(LinqTestBase):


    def test_count(self):
        self.assertEqual(3,Query.args(1,2,3).count())

    def test_sum(self):
        self.assertEqual(6,Query.args(1,2,3).sum())

    def test_sum_on_empty(self):
        self.assertRaises(ValueError,lambda: Query.args().sum())

    def test_min(self):
        self.assertEqual(1,Query.args(1,2,3).min())

    def test_min_on_empty(self):
        self.assertRaises(ValueError,lambda: Query.args().min())

    def test_max(self):
        self.assertEqual(3,Query.args(1,2,3).max())

    def test_max_on_empty(self):
        self.assertRaises(ValueError,lambda: Query.args().max())

    def test_mean(self):
        self.assertEqual(2.0,Query.args(1,2,3).mean())

    def test_mean_on_empty(self):
        self.assertRaises(ValueError,lambda: Query.args().mean())

    def test_all_1(self):
        self.assertEqual(True, Query.args(1, 2, 3).all(lambda z: z > 0))

    def test_all_2(self):
        self.assertEqual(False, Query.args(1, 2, 3).all(lambda z: z > 1))

    def test_all_3(self):
        self.assertEqual(True, Query.args(dict()).all())

    def test_all_4(self):
        self.assertEqual(True, Query.args().all())


    def test_any_1(self):
        self.assertEqual(True, Query.args(1, 2, 3).any(lambda z: z > 1))

    def test_any_2(self):
        self.assertEqual(False, Query.args(1, 2, 3).any(lambda z: z < 1))

    def test_any_3(self):
        self.assertEqual(True, Query.args(dict()).any())

    def test_any_4(self):
        self.assertEqual(False, Query.args().any())


    def test_complex_aggregator(self):
        self.assertDictEqual({'sum':6,'count':3,'mean':2.0},Query.args(1,2,3).aggregate_with(agg.Sum(),agg.Count(),agg.Mean()))