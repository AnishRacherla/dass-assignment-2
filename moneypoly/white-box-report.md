# 1.3 White-Box Test Cases Report

## Scope
This report is for branch-focused white-box testing of MoneyPoly.

Modules tested:
- `Player`
- `Property` and `PropertyGroup`
- `Game`

Run command:

```bash
python -m unittest tests.test_white_box -v
```

## Branch Coverage Design

The test suite is designed from code structure (if/elif/else and early-return paths), not only from input/output behavior.

### A) Player Branches

1. `move` pass-Go branch: salary is awarded when board wraps.
2. `move` non-wrap branch: no salary awarded.
3. `add_money` negative branch: raises `ValueError`.
4. `net_worth` state branch: includes property prices.

### B) Property and Group Branches

1. `get_rent` full-group ownership branch: doubled rent.
2. `get_rent` mortgaged branch: zero rent.

### C) Game Turn Flow Branches

1. `play_turn` jailed-player path.
2. `play_turn` three-doubles path (go to jail).
3. `play_turn` doubles path (extra turn behavior).
4. `play_turn` normal path (advance turn).

### D) Property Interaction Branches

1. `_handle_property_tile` unowned + buy branch.
2. `_handle_property_tile` unowned + auction branch.
3. `_handle_property_tile` unowned + skip branch.
4. `_handle_property_tile` already-owned-by-self branch.
5. `_handle_property_tile` owned-by-other branch (rent path).

### E) Money and Trade Branches

1. `buy_property` insufficient-funds branch.
2. `buy_property` exact-balance edge branch.
3. `pay_rent` mortgaged-property early-return branch.
4. `pay_rent` no-owner early-return branch.
5. `pay_rent` normal transfer branch.
6. `trade` seller-not-owner failure branch.
7. `trade` buyer-cannot-afford failure branch.
8. `trade` successful branch (owner/list/balance updates).

### F) Mortgage/Unmortgage Branches

1. `mortgage_property` not-owner failure branch.
2. `mortgage_property` already-mortgaged failure branch.
3. `mortgage_property` success branch.
4. `unmortgage_property` not-owner failure branch.
5. `unmortgage_property` not-mortgaged failure branch.
6. `unmortgage_property` insufficient-funds failure branch.
7. `unmortgage_property` success branch.

### G) Auction Branches

1. `auction_property` no-valid-bids branch.
2. `auction_property` winner branch.
3. Also exercises low-bid and over-budget sub-branches.

### H) Jail Branches

1. `_handle_jail_turn` uses Get Out of Jail card branch.
2. `_handle_jail_turn` voluntary fine payment branch.
3. `_handle_jail_turn` no-action branch (stay jailed).
4. `_handle_jail_turn` mandatory release on third turn branch.

### I) Tile Resolution Branches

1. `_move_and_resolve` income-tax branch.
2. `_move_and_resolve` luxury-tax branch.
3. `_move_and_resolve` go-to-jail branch.
4. `_move_and_resolve` free-parking branch.
5. `_move_and_resolve` chance branch.
6. `_move_and_resolve` community-chest branch.
7. `_move_and_resolve` railroad branch with no property object.
8. `_move_and_resolve` normal property branch.

### J) Card Action Branches

1. `_apply_card` `None` card branch.
2. `_apply_card` `collect` branch.
3. `_apply_card` `pay` branch.
4. `_apply_card` `jail` branch.
5. `_apply_card` `jail_free` branch.
6. `_apply_card` `move_to` pass-Go + property handling branch.
7. `_apply_card` `move_to` non-property branch.
8. `_apply_card` `birthday` branch (only players with enough balance pay).
9. `_apply_card` `collect_from_all` branch.

### K) Endgame Branches

1. `_check_bankruptcy` non-bankrupt branch.
2. `_check_bankruptcy` bankrupt elimination branch.
3. `find_winner` no-players branch.

## Why These Tests Are Needed (Simple Explanation)

- Branch testing ensures each decision path is executed at least once.
- Monopoly-style games are state-heavy, so we must check balance, ownership, jail flags, and turn index after each branch.
- Edge cases (exact balance, zero/low money, pass-Go boundary, forced jail release, invalid bids) can break logic even when normal cases pass.

## Errors or Logical Issues Found

- In this branch-focused run, no failing logic was observed in the covered branches.
- All branch tests passed on the current code.

## Result Summary

- Total test cases executed: **56**
- Test result: **PASS**
- Command output summary: `Ran 56 tests ... OK`
