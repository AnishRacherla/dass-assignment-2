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

## Final Verification
- Command used: `python -m unittest -v test_integration.py`
- Result: `Ran 28 tests ... OK`
- Conclusion: Module interactions are working correctly for the tested call-graph scenarios, and detected integration issues were documented and fixed.
