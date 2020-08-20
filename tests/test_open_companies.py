from unittest import TestCase
from vrbr18xx.company import Corporations


class TestOpenCompanies(TestCase):

    def test_init(self):
        open_companies = Corporations()
        self.assertDictEqual(open_companies.corporations, {})

    def test_par(self):
        open_companies = Corporations()
        open_companies.par('PRR', 100)
        self.assertTrue('PRR' in open_companies)
        self.assertEqual(open_companies['PRR'], 100)

    def test_par_company_a_second_time(self):
        open_companies = Corporations()
        open_companies.par('PRR', 100)
        with self.assertRaises(ValueError):
            open_companies.par('PRR', 100)

    def test_par_company_with_negative_price(self):
        open_companies = Corporations()
        with self.assertRaises(ValueError):
            open_companies.par('C&O', -1)

    def test_set_price(self):
        open_companies = Corporations()
        open_companies.par('NYC', 100)
        self.assertEqual(open_companies.NYC, 100)
        open_companies.set_price('NYC', 50)
        self.assertEqual(open_companies.NYC, 50)

    def test_set_price_not_opened_company(self):
        open_companies = Corporations()
        with self.assertRaises(ValueError):
            open_companies.set_price('B&O', 80)

    def test_set_negative_price(self):
        open_companies = Corporations()
        with self.assertRaises(ValueError):
            open_companies.set_price('NYC', -1)


