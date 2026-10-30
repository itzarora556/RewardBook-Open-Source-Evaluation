# challenges.md - COMPULSORY submission

## 1. Dealing with weird data types in refund `amount_paise`
The biggest issue I ran into was in `test_invalid_or_excess_refund_does_not_change_account` inside `test_acceptance_matrix.py`. At first, I just added a simple condition to check if the refund was valid:
`if refund <= 0 or txn['refunded_paise'] + refund > txn['amount_paise']: return out`

When I ran pytest, it still failed on several test cases! Looking at the error log, the test was passing values like `None`, `"100"`, `[]`, `{}`, and `True` as `amount_paise`.
- For `None` and `"100"`, Python threw a `TypeError` when comparing them with `<= 0`.
- Even weirder, when `amount_paise` was `True`, it didn't throw an error at all—it actually treated `True` as `1` and added `1` paise to `refunded_paise`! I learned that in Python `bool` is a subtype of `int`, so `True == 1`.

**How I fixed it:** I added `type(refund) is not int` right at the start of the `if` statement before doing any math comparisons. That way, only real integers are allowed through, and `True`, `False`, `None`, floats, and strings get rejected immediately.

## 2. The `cap_points = 0` bug
Another small thing that tripped me up briefly was `test_cap_zero_is_respected`. The starter code had `if cap_points: points = min(points, cap_points)`. At first glance that looked fine, until I realized that passing `cap_points=0` makes `if cap_points:` evaluate to `False` in Python, so it skipped the `min()` line completely. Changing it to `if cap_points is not None:` fixed it right away.