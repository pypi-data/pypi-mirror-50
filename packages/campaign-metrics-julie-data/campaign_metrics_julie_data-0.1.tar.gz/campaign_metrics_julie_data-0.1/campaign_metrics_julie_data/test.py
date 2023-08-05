# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest

from campaign_metrics_julie_data import Email
from campaign_metrics_julie_data import Website

class TestEmailClass(unittest.TestCase):
    def setUp(self):
        self.email = Email('super campaign', '2019-07-01', '2019-07-15', 1000, .2, 700, 120, 20)
        
    def test_initialization(self):
        self.assertEqual(self.email.eligible_customers, 1000, 'incorrect number of eligible customers')
        self.assertEqual(self.email.control_proportion, .2, 'incorrect control proportion')
        self.assertEqual(self.email.opened, 700, 'incorrect number of customers who have opened')
        
    def test_calculate_length(self):
        length = self.email.calculate_length()        
        self.assertEqual(length, 14, 'incorrect length')
        
    def test_calculate_treatment_size(self):
        treat_size = self.email.calculate_treatment_size()        
        self.assertEqual(treat_size, 800, 'incorrect treatment size')
        
    def test_calculate_control_size(self):
        control_size = self.email.calculate_control_size()        
        self.assertEqual(control_size, 200, 'incorrect control size')
        
    def test_calculate_adjusted_population(self):
        adjusted_population, adjusted_treatment, adjusted_control = self.email.calculate_adjusted_population(0.05)        
        self.assertEqual(adjusted_population, 950, 'incorrect adjusted population')
        self.assertEqual(adjusted_treatment, 760, 'incorrect adjusted population')
        self.assertEqual(adjusted_control, 190, 'incorrect adjusted population')
        
    def test_calculate_open_rate(self):
        treat_open_rate, diff_with_benchmark = self.email.calculate_open_rate(0.05, 0.5)
        self.assertEqual(treat_open_rate, 0.92105263157894735, 'incorrect open rate')
        self.assertEqual(diff_with_benchmark, 0.42105263157894735, 'incorrect difference with benchmark')
        
    def test_calculate_purchase_performance(self):
        purchase_rate_treatment, purchase_rate_control, performed_group, lift = self.email.calculate_purchase_performance(0.05)
        self.assertEqual(purchase_rate_treatment, 0.15789473684210525, 'incorrect treatment purchase rate')
        self.assertEqual(purchase_rate_control, 0.10526315789473684, 'incorrect control purchase rate')
        self.assertEqual(performed_group, 'treatment', 'incorrect performed group')
        self.assertEqual(lift, 0.05263157894736842, 'incorrect lift')
        
class TestEmailClass(unittest.TestCase):
    def setUp(self):
        self.website = Website('super campaign', '2019-01-01', '2019-01-31', 2000, .3, 1100, 300, 24)
        
    def test_initialization(self):
        self.assertEqual(self.website.eligible_customers, 2000, 'incorrect number of eligible customers')
        self.assertEqual(self.website.control_proportion, .3, 'incorrect control proportion')
        self.assertEqual(self.website.clicked, 1100, 'incorrect number of customers who have clicked')
        
    def test_calculate_length(self):
        length = self.website.calculate_length()        
        self.assertEqual(length, 30, 'incorrect length')
        
    def test_calculate_treatment_size(self):
        treat_size = self.website.calculate_treatment_size()        
        self.assertEqual(treat_size, 1400, 'incorrect treatment size')
        
    def test_calculate_control_size(self):
        control_size = self.website.calculate_control_size()        
        self.assertEqual(control_size, 600, 'incorrect control size')
        
    def test_calculate_adjusted_population(self):
        adjusted_population, adjusted_treatment, adjusted_control = self.website.calculate_adjusted_population(0.05)        
        self.assertEqual(adjusted_population, 1900, 'incorrect adjusted population')
        self.assertEqual(adjusted_treatment, 1330, 'incorrect adjusted population')
        self.assertEqual(adjusted_control, 570, 'incorrect adjusted population')
        
    def test_calculate_click_rate(self):
        treat_open_rate, diff_with_benchmark = self.website.calculate_click_rate(0.05, 0.3)
        self.assertEqual(treat_open_rate, 0.82706766917293233, 'incorrect click rate')
        self.assertEqual(diff_with_benchmark, 0.52706766917293233, 'incorrect difference with benchmark')
        
    def test_calculate_purchase_performance(self):
        purchase_rate_treatment, purchase_rate_control, performed_group, lift = self.website.calculate_purchase_performance(0.05)
        self.assertEqual(purchase_rate_treatment, 0.22556390977443609022, 'incorrect treatment purchase rate')
        self.assertEqual(purchase_rate_control, 0.04210526315789473684, 'incorrect control purchase rate')
        self.assertEqual(performed_group, 'treatment', 'incorrect performed group')
        self.assertEqual(lift, 0.18345864661654135338, 'incorrect lift')
        
        
if __name__ == '__main__':
    unittest.main()