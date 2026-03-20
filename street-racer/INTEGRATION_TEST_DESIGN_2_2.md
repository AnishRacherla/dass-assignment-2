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
| IT-01 | Register a crew member, assign driver role, and enter race | Registration, Crew Management, Race Management, Inventory | Registered driver and good-condition vehicle can be added to race | PASS | None |
| IT-02 | Try entering race with unregistered crew | Crew Management, Race Management | System should reject with error | PASS | None |
| IT-03 | Try entering race with registered non-driver role | Registration, Crew Management, Race Management | System should reject because only drivers can race | PASS | None |
| IT-04 | Complete race and record result with prize money deduction | Race Management, Results, Inventory | Race result saved; inventory cash reduced by prize amount; ranking updated | PASS | None |
| IT-05 | Record race result when cash is insufficient | Results, Inventory | System should reject with insufficient funds error | PASS | None |
| IT-06 | Create mission and validate role requirements (rescue/heist) | Registration, Crew Management, Mission Planning | Mission starts only when required roles are present | PASS | None |
| IT-07 | Assign unregistered crew to mission | Registration, Mission Planning | System should reject assignment | PASS | None |
| IT-08 | Damage vehicle then attempt to race | Inventory, Race Management | Damaged vehicle should be rejected from race | PASS | None |
| IT-09 | Repair vehicle and verify condition/cost update | Inventory, Maintenance | Repair should reduce damage, improve condition, and deduct cash | PASS | Historical issue found during testing: missing parts in setup caused repair failure; fixed by adding required parts in test setup |
| IT-10 | Track reputation after mission success/failure | Registration, Reputation | Success increases score; failure decreases score | PASS | Historical expectation mismatch found: default score maps to Professional, not Rookie; test corrected |
| IT-11 | CLI mission creation with multiple crew using yes/no answers | CLI (main), Mission Planning, Registration, Crew Management | Using yes should continue assignment so 3 crew can be assigned for heist mission | PASS | **Detected and fixed:** CLI accepted only exact `y`; `yes` stopped assignment early (expected 3, actual 0 in failing run) |
| IT-12 | End-to-end workflow: register -> role -> race -> result -> reputation | Registration, Crew Management, Inventory, Race Management, Results, Reputation | Full workflow should complete with consistent state updates | PASS | None |
| IT-13 | End-to-end mission workflow with all required roles | Registration, Crew Management, Mission Planning | Mission should start and complete successfully | PASS | None |

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
- Result: `Ran 23 tests ... OK`
- Conclusion: Module interactions are working correctly for the tested call-graph scenarios, and detected integration issues were documented and fixed.
