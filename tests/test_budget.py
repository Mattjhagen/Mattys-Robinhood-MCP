import json
import unittest
from pathlib import Path
from scripts.budget import budget

ROOT = Path(__file__).resolve().parents[1]


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.s = json.loads((ROOT / 'examples/balance-20.json').read_text())
        self.p = json.loads((ROOT / 'strategy-policy.json').read_text())['budget']

    def test_twenty_dollars(self):
        self.assertEqual(budget(self.s, self.p)['max_new_order_notional'], '4.95')

    def test_deposit_resizes_only_when_available(self):
        self.s.update(equity='120', available_cash='20', buying_power='120')
        self.assertEqual(budget(self.s, self.p)['max_new_order_notional'], '7.95')
        self.s['available_cash'] = '120'
        self.assertEqual(budget(self.s, self.p)['max_new_order_notional'], '29.95')

    def test_pending_withdrawal_protected(self):
        self.s['unreserved_withdrawals'] = '17'
        self.assertEqual(budget(self.s, self.p)['decision'], 'HOLD')

    def test_existing_crypto_is_not_cash(self):
        self.s.update(equity='21.85', available_cash='0.19', buying_power='0.19')
        self.assertEqual(budget(self.s, self.p)['decision'], 'HOLD')

    def test_open_order_and_previous_spend(self):
        self.s.update(unreserved_order_costs='15', cycle_spent='3')
        self.assertEqual(budget(self.s, self.p)['max_new_order_notional'], '1.95')

    def test_zero_and_dust(self):
        for value in ('0', '0.99', '1'):
            self.s.update(equity=value, available_cash=value, buying_power=value)
            self.assertEqual(budget(self.s, self.p)['decision'], 'HOLD')

    def test_broker_buying_power_caps_cash(self):
        self.s['buying_power'] = '3.50'
        self.assertEqual(budget(self.s, self.p)['max_new_order_notional'], '1.45')

    def test_never_round_up_spend(self):
        self.s.update(equity='20.03')
        self.assertEqual(budget(self.s, self.p)['max_new_order_notional'], '4.95')

    def test_invalid_money_rejected(self):
        for value in ('NaN', 'Infinity', '-1', True, None, 'unknown'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                budget({**self.s, 'available_cash': value}, self.p)

    def test_missing_field_rejected(self):
        del self.s['unreserved_withdrawals']
        with self.assertRaises(KeyError):
            budget(self.s, self.p)

    def test_invalid_fraction_rejected(self):
        with self.assertRaises(ValueError):
            budget(self.s, {**self.p, 'max_cycle_fraction': '1.1'})

    def test_cash_invariant_across_balances(self):
        from decimal import Decimal
        for cents in range(0, 10000, 37):
            cash = Decimal(cents) / 100
            self.s.update(equity=str(cash), available_cash=str(cash), buying_power=str(cash))
            result = budget(self.s, self.p)
            spend = Decimal(result['max_new_order_notional'])
            self.assertLessEqual(spend, cash)
            self.assertLessEqual(spend, cash * Decimal(self.p['max_cycle_fraction']))
            if spend:
                self.assertLessEqual(spend + Decimal(result['cash_reserve']) + Decimal(self.p['fee_buffer']), cash)


if __name__ == '__main__':
    unittest.main()
