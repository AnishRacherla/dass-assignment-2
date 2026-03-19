# 1.3 White-Box Test Cases Report

## Scope
These tests were designed from internal code paths (branch logic, state transitions, and edge cases) in:
- `Bank`
- `PropertyGroup`
- `Player`
- `Game`

Run command:

```bash
python -m unittest tests.test_white_box -v
```

## Test Cases, Why Needed, and Issues Found

1. **`test_collect_ignores_negative_amount`**  
   Why needed: `Bank.collect` has a decision path for input amount; negative values are an edge case that can corrupt bank balance.  
   Issue found: Negative amount reduced bank funds even though method description says to ignore negatives.  
   Fix: Return early when `amount < 0`.

2. **`test_give_loan_reduces_bank_balance`**  
   Why needed: Loan flow changes two key states (`player.balance`, `bank._funds`); both must stay consistent.  
   Issue found: Borrower got money but bank balance did not decrease.  
   Fix: Disburse through `pay_out(amount)` and then credit player.

3. **`test_all_owned_by_requires_full_set`**  
   Why needed: Monopoly rent rules depend on full color-group ownership branch.  
   Issue found: `any(...)` was used, so owning only one property incorrectly counted as full ownership.  
   Fix: Use `all(...)` and require non-empty group.

4. **`test_move_awards_salary_when_passing_go`**  
   Why needed: Player movement has branch where crossing board boundary should award Go salary.  
   Issue found: Salary only awarded when landing exactly on position 0.  
   Fix: Track old position and award salary when `old_position + steps >= BOARD_SIZE`.

5. **`test_net_worth_includes_property_values`**  
   Why needed: Winner calculation depends on `net_worth`; variable state must include assets.  
   Issue found: Net worth returned cash only and ignored property value.  
   Fix: Return `balance + sum(property.price)`.

6. **`test_buy_property_allows_exact_balance`**  
   Why needed: Affordability branch has edge case where `balance == price`.  
   Issue found: Exact balance could not buy because condition used `<=`.  
   Fix: Change check to `<`.

7. **`test_pay_rent_transfers_to_owner`**  
   Why needed: Rent payment updates two players and must preserve money transfer correctness.  
   Issue found: Tenant was charged, owner was not credited.  
   Fix: Add `prop.owner.add_money(rent)`.

8. **`test_trade_transfers_property_and_cash`**  
   Why needed: Trade branch mutates ownership list, owner pointer, and both balances.  
   Issue found: Buyer paid cash but property ownership and seller credit were not updated.  
   Fix: Credit seller, move property between player lists, and set `prop.owner = buyer`.

9. **`test_jail_fine_branch_deducts_player_balance`**  
   Why needed: Jail release decision path changes jail state and money state; fine branch is critical.  
   Issue found: Bank collected jail fine but player balance was not deducted.  
   Fix: Add `player.deduct_money(JAIL_FINE)` in voluntary fine branch.

10. **`test_find_winner_uses_highest_net_worth`**  
    Why needed: Winner branch is a core game result path.  
    Issue found: Winner selected with `min(...)` instead of `max(...)`.  
    Fix: Use `max(self.players, key=lambda p: p.net_worth())`.

## Result Summary
- Initial run: **10 failures** (all above issues reproduced).
- Final run: **10/10 tests passed**.
- These tests cover branch decisions, key variable-state transitions, and edge conditions such as negative values, exact balances, pass-Go boundary crossing, and trade/jail action paths.
