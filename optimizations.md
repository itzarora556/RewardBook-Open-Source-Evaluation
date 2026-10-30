# optimizations.md - Required submission

## What I Improved
1. **Early return checks:**
   In both `calculate_points` and `apply_reward_event`, I put the validation checks right at the top of the functions. If an `event_id` was already processed or if the numbers are `<= 0`, the function returns immediately instead of doing extra calculations or modifying the dictionary.
2. **Using `//` instead of `round(a / b)`:**
   Using integer floor division (`amount_paise // 10000`) is not only required for the business rule, it also avoids converting integers into floats first, which is faster and avoids floating-point rounding bugs.

## Trade-offs I Thought About
1. **Keeping `processed_event_ids` as a `list` instead of a `set`:**
   I thought about changing `processed_event_ids` to a `set` because checking `event_id in out['processed_event_ids']` is $O(1)$ in a set and $O(n)$ in a list. However, the existing tests check `assert twice["processed_event_ids"] == [event_id]` and JSON data doesn't support sets directly. Since the number of events per single account in these tests is small, keeping it as a list keeps all tests passing without breaking the account format.
2. **Keeping `deepcopy(account)`:**
   `deepcopy` copies the whole account dictionary every time `apply_reward_event` is called, which takes a bit more memory, but the test `test_event_processing_does_not_mutate_input_account` requires the original dictionary to stay untouched. So keeping `deepcopy` is the safest choice to avoid accidentally modifying the original input.

## Future Improvements
If this service had to handle thousands of events per user in a real app, we could store processed event IDs in a database index or keep a separate set in memory for fast lookups while still saving the ordered list for the history.