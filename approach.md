# approach.md - Required submission

## Starting Test Result and Exploring the Code
When I first cloned the repo and ran `python -m pytest -q`, I got **67 failed, 147 passed**. I also ran `python -m main` which gave `Points example: 28` and `Repeat warnings: []`.

I checked all the files in the folder (`models.py`, `fixtures.py`, `main.py`, and `service.py`). I noticed that `models.py` just creates the empty account dictionary and `fixtures.py` has sample data, so all the actual logic and bugs were inside `service.py`.

## Finding the Root Causes
By looking at the failed tests in `test_contract.py` and `test_acceptance_matrix.py`, I found these issues in `service.py`:
1. In `calculate_points`, line 6 used `round(amount_paise / 10000)` instead of integer division `//`. That caused amounts like `19999` to round up to 2 instead of flooring to 1.
2. Also in `calculate_points`, `if cap_points:` didn't work when `cap_points` was `0` because `0` is treated as False in Python. Plus there was no check if `amount_paise <= 0`, `points_per_100_rupees <= 0`, or `bonus_percent < 0`.
3. In `apply_reward_event`, there was no check to see if `event_id` was already in `out['processed_event_ids']`, and `out['processed_event_ids'].append(event_id)` was at the very end of the function outside the `if/elif` blocks. Because of this, duplicate events were running again and even invalid/declined events were getting added to `processed_event_ids`.
4. In the `refund_processed` block, it directly added `refund` to `txn['refunded_paise']` without checking if the refund was negative, zero, a wrong data type (like `None`, `True`, or a string), or larger than the original purchase amount.
5. In `flag_repeat_transactions`, when a negative or zero threshold was passed in the tests, `len(ids) > threshold` matched groups of size 1, so I used `max(1, threshold)`.

## How I Validated the Fix
After making these changes in `service.py` and adding 5 regression tests in `tests/test_contract.py`, I ran `python -m pytest -q` again and all **214 tests passed**. Running `python -m main` also changed from `28` to `27`, which matches the floor calculation.