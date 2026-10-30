# TESTING.md — Required submission

# TESTING.md

## Test Environment and Commands Run
- **Python version:** Python 3.11
- **Commands executed:**
  1. `python -m pip install -r requirements-dev.txt`
  2. `python -m pytest -q`
  3. `python -m main`

## Test Summary
- **Before fixing `service.py`:** `67 failed, 147 passed` (and `python -m main` printed `Points example: 28`).
- **After fixing `service.py` and adding 5 tests:** `214 passed` with 0 failures (and `python -m main` printed `Points example: 27`).

## 5 Edge Cases Tested

1. **Amount just under 200 rupees (`19999` paise)**
   - **Input:** `calculate_points(19999, 1)`
   - **Expected:** `1` point (because 199.99 rupees only has one full 100-rupee block).
   - **Actual:** `1`
   - **Test:** `test_points_use_floor` in `tests/test_contract.py`

2. **Zero cap value (`cap_points=0`)**
   - **Input:** `calculate_points(50000, 1, cap_points=0)`
   - **Expected:** `0` points because the cap is 0.
   - **Actual:** `0`
   - **Test:** `test_cap_zero_is_respected` in `tests/test_contract.py`

3. **Negative purchase amount (`-10000` paise)**
   - **Input:** `calculate_points(-10000, 1)`
   - **Expected:** `0` points (negative amounts shouldn't give points).
   - **Actual:** `0`
   - **Test:** `test_negative_amount_gives_zero` in `tests/test_contract.py`

4. **Two partial refunds where the second one exceeds the original purchase**
   - **Input:** Purchase of `100000` paise, first refund of `70000` paise, second refund of `40000` paise.
   - **Expected:** First refund works, second refund is ignored because `70000 + 40000 > 100000`.
   - **Actual:** `refunded_paise` remains `70000` and `points_balance` remains `3`.
   - **Test:** `test_two_partial_refunds_over_limit` in `tests/test_contract.py`

5. **Repeat transaction check with `threshold = 0`**
   - **Input:** 1 transaction for account `A1` with `threshold=0`.
   - **Expected:** `[]` (a single transaction is not a repeat).
   - **Actual:** `[]`
   - **Test:** `test_zero_threshold_in_repeats` in `tests/test_contract.py`
