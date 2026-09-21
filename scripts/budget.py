"""Offline cash-budget calculator. No broker connection or order execution."""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_UP

CENT = Decimal('0.01')


def amount(value, name):
    if isinstance(value, bool):
        raise ValueError(f'{name} must be a nonnegative finite decimal')
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f'{name} must be a decimal') from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f'{name} must be a nonnegative finite decimal')
    return result


def budget(snapshot, policy):
    """Requires normalized available cash, net of broker holds; see STRATEGY.md."""
    names = ('equity', 'available_cash', 'buying_power',
             'unreserved_withdrawals', 'unreserved_order_costs', 'cycle_spent')
    s = {k: amount(snapshot[k], k) for k in names}
    p = {k: amount(policy[k], k) for k in
         ('reserve_fraction', 'max_cycle_fraction', 'minimum_order', 'fee_buffer')}
    if p['reserve_fraction'] > 1 or p['max_cycle_fraction'] > 1:
        raise ValueError('fractions must be between 0 and 1')
    if p['minimum_order'] <= 0:
        raise ValueError('minimum_order must be positive')
    reserve = (s['equity'] * p['reserve_fraction']).quantize(CENT, rounding=ROUND_UP)
    free = max(Decimal(0), min(s['available_cash'], s['buying_power'])
               - s['unreserved_withdrawals'] - s['unreserved_order_costs'] - reserve)
    cap = max(Decimal(0), s['equity'] * p['max_cycle_fraction'] - s['cycle_spent'])
    order = max(Decimal(0), min(free, cap) - p['fee_buffer']).quantize(CENT, rounding=ROUND_DOWN)
    if order < p['minimum_order']:
        order = Decimal(0)
    return {'cash_reserve': str(reserve), 'max_new_order_notional': f'{order:.2f}',
            'decision': 'HOLD' if order == 0 else 'BUDGET_AVAILABLE',
            'note': 'A cash ceiling, not a trade recommendation or authorization.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot')
    parser.add_argument('--policy', default='strategy-policy.json')
    args = parser.parse_args()
    try:
        with open(args.snapshot) as f:
            snapshot = json.load(f)
        with open(args.policy) as f:
            policy = json.load(f)
        print(json.dumps(budget(snapshot, policy['budget']), indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'No budget produced: {exc}\n')


if __name__ == '__main__':
    main()
