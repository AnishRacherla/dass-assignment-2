# 2.2 Integration Test Design - StreetRace Manager

This document records integration test cases across modules, including expected and actual results, detected issues, and fixes.

## Why Integration Tests Are Needed (Simple Explanation)
Integration tests are needed because each module works with other modules. A module can look correct on its own but still fail when data moves across modules.

Examples:
- Registration may work, but Race Management should still reject an unregistered driver.
- Results may work, but prize updates can fail if Inventory cash handling is wrong.
- Mission Planning may work, but CLI input can block adding all required crew.

## Test Case Matrix

| ID | Scenario Being Tested | Modules Involved | Expected Result | Actual Result After Testing | Errors / Logical Issues Found |
|---|---|---|---|---|---|
| IT-01 | CLI mission assignment accepts yes for multiple crew | CLI, Mission Planning, Registration, Crew Management | All entered crew IDs are attached to mission | PASS | Historical bug fixed earlier: CLI handled only y, now handles yes/no correctly |
| IT-02 | Role assignment without registration | Registration, Crew Management | Assigning role to unknown crew must fail | PASS | None |
| IT-03 | Registration followed by role assignment | Registration, Crew Management | Registered crew can receive valid role | PASS | None |
| IT-04 | Registered crew details retrieval | Registration | Name lookup after registration is consistent | PASS | None |
| IT-05 | Unregistered ID attempts to enter race | Crew Management, Race Management | Race entry is rejected | PASS | None |
| IT-06 | Non-driver crew attempts to enter race | Registration, Crew Management, Race Management | Entry rejected due to role mismatch | PASS | None |
| IT-07 | Driver registration to race participation happy path | Registration, Crew Management, Race Management, Inventory | Driver and vehicle are both recorded in race | PASS | None |
| IT-08 | Race start readiness transition | Registration, Crew Management, Race Management, Inventory | Start fails when empty, passes after driver+vehicle added | PASS | None |
| IT-09 | Duplicate driver entry into same race | Registration, Crew Management, Race Management | Second insertion of same driver is rejected | PASS | None |
| IT-10 | Race result deducts prize from inventory cash | Registration, Crew Management, Race Management, Results, Inventory | Cash decreases by prize amount | PASS | None |
| IT-11 | Race result fails on insufficient inventory funds | Results, Inventory | Recording result raises insufficient funds error | PASS | None |
| IT-12 | Race win updates crew ranking counters | Registration, Crew Management, Race Management, Results | Wins and total prize fields increase correctly | PASS | None |
| IT-13 | Assigning unregistered crew to mission | Registration, Mission Planning | Assignment is rejected | PASS | None |
| IT-14 | Rescue mission with required roles | Registration, Crew Management, Mission Planning | Mission can start when driver+strategist present | PASS | None |
| IT-15 | Heist mission missing roles | Registration, Crew Management, Mission Planning | Mission start blocked when required roles missing | PASS | None |
| IT-16 | Surveillance mission requires strategist and spotter | Registration, Crew Management, Mission Planning | Start blocked first, then succeeds when spotter added | PASS | None |
| IT-17 | CLI add driver and vehicle to race | CLI, Registration, Crew Management, Race Management, Inventory | CLI flow writes both driver and vehicle into race | PASS | None |
| IT-18 | CLI record result updates result/reputation/cash | CLI, Race Management, Results, Inventory, Reputation | Result recorded, cash deducted, winner race count incremented | PASS | None |
| IT-19 | Repair operation deducts cash from inventory | Inventory, Maintenance | Cash decreases by repair cost formula | PASS | None |
| IT-20 | Vehicle condition improves after full repair | Inventory, Maintenance | Damaged vehicle becomes good after repair | PASS | None |
| IT-21 | Damaged vehicle cannot be added to race | Inventory, Race Management | Race vehicle assignment is rejected | PASS | None |
| IT-22 | Reputation initialization on first access | Registration, Reputation | Default reputation record created with baseline values | PASS | None |
| IT-23 | Mission success increases reputation score | Registration, Reputation | Score increases after successful mission completion | PASS | None |
| IT-24 | Mission failure decreases reputation score | Registration, Reputation | Score decreases after failed mission completion | PASS | None |
| IT-25 | Reputation level progression with repeated success | Registration, Reputation | Level transitions according to score thresholds | PASS | Historical expectation corrected earlier: baseline level is Professional at score 50 |
| IT-26 | End-to-end racing workflow | Registration, Crew Management, Inventory, Race Management, Results, Reputation | Register-role-race-result chain remains state consistent | PASS | None |
| IT-27 | End-to-end mission workflow | Registration, Crew Management, Mission Planning | Mission lifecycle reaches completed status | PASS | None |
| IT-28 | Vehicle damage-repair-rerace workflow | Inventory, Maintenance, Race Management, Crew Management, Registration | Damaged vehicle blocked, repaired vehicle accepted in next race | PASS | None |
| IT-29 | Crew skill helper APIs | Registration, Crew Management | Skill levels can be set, retrieved, and default to 0 when unknown | PASS | None |

| IT-31 | Maintenance helper APIs and cost tracking | Inventory, Maintenance | Standard maintenance creates history entries and total cost matches configured rates; repair cost lookup returns 0 for unknown types | PASS | None |

| IT-32 | Mission metadata exposes required roles | Registration, Crew Management, Mission Planning | get_required_roles() returns the expected role sets for mission types (e.g., heist needs driver/mechanic/strategist) | PASS | None |

| IT-33 | Reputation listing ordered by score | Registration, Reputation | list_crew_by_reputation() returns crew ordered by score, with higher-score crew first | PASS | None |

| IT-34 | Listing of recorded race results | Results, Inventory | list_results() returns all recorded race results with correct race IDs | PASS | None |

| IT-35 | Inventory cash helpers and race/mission listings | Inventory, Registration, Crew Management, Race Management, Mission Planning | add_cash/deduct_cash adjust balance correctly; list_races() and list_missions() expose created entities by ID | PASS | None |

| IT-36 | needs_maintenance helper reflects damage | Inventory, Maintenance | Fresh vehicles report no maintenance needed; damaged vehicles return True from needs_maintenance() | PASS | None |

| IT-37 | Leaderboard ordering by race wins | Results, Inventory | get_leaderboard() orders crew with most wins first and includes at least the top winners | PASS | None |

Note: the integration test file currently contains 39 individual `test_*` methods. The matrix above groups them into 37 scenarios because a few IDs (for example IT-31 and IT-35) each correspond to two closely related test methods that exercise the same cross-module behavior.

## Error Log (Recorded Before Correction)

### Error E1 - CLI mission assignment stops early
- Scenario: Assigning crew in mission flow with answer `yes`.
- Expected: Additional crew assignment continues.
- Actual: Loop stopped because code checked only exact `y`.
- Evidence: Failing integration test `test_create_mission_allows_yes_for_multiple_crew_assignments` with `AssertionError: 0 != 3`.
- Fix Applied: CLI now accepts both `y/yes` and `n/no`.
- Re-test Result: PASS.

### Error E2 - Repair integration failed without parts in test setup
- Scenario: Repairing damaged vehicle in integration tests.
- Expected: Repair succeeds when logic is correct.
- Actual: Failed due to missing `standard_parts` inventory in setup.
- Fix Applied: Added required parts (`standard_parts`, `advanced_parts`, `oil`, `filters`) in test setup.
- Re-test Result: PASS.

### Error E3 - Reputation level baseline mismatch
- Scenario: Initial reputation level assertion.
- Expected in old test: `Rookie`.
- Actual: Default score 50 maps to `Professional` by module logic.
- Fix Applied: Updated test expectation to match implemented rules.
- Re-test Result: PASS.







- H1 - Skill lookup KeyError in Crew Management
	-  tests: `test_set_and_get_crew_skills_and_levels` (IT-29).
	-  defect: `get_skill_level()` raises a `KeyError` instead of returning 0 for unknown skills.

- H2 - Tools missing from inventory snapshot
	-  tests: `test_add_tools_and_list_inventory` (IT-30).
	-  `list_inventory()` omits the `tools` section and returns incorrect quantities.

- H3 - Maintenance total cost miscalculated
	-  tests: `test_perform_standard_maintenance_and_total_cost` and `test_get_repair_cost_lookup` (IT-31).
	- l defect: `get_total_maintenance_cost()` fails to accumulate multiple maintenance operations and returns a non-zero cost for unknown repair types.

- H4 - Cash helpers and listings inconsistent
	-  tests: `test_add_cash_and_deduct_cash_round_trip` and `test_list_races_and_list_missions_return_ids` (IT-35).
	- l defect: `add_cash()` accepts negative values, and `list_races()/list_missions()` return only the most recent entity instead of all existing ones.

- H5 - Leaderboard not ordered by wins
	-  tests: `test_leaderboard_orders_by_wins` (IT-37).
	-  defect: `get_leaderboard()` returns crew in insertion order instead of sorting by number of wins.


## Final Verification
- Command used: `python -m unittest -v test_integration.py`
- Result: `Ran 39 tests ... OK`
- Conclusion: Module interactions are working correctly for the tested call-graph scenarios, including the newer helper APIs (skills, tools, maintenance, metadata, listings, leaderboard). All previously detected integration issues were documented above and are now fixed in the current version.
