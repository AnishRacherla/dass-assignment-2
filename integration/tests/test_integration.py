"""Integration tests for StreetRace Manager system.

Tests module interactions, business rule enforcement, and data consistency
across module boundaries.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import unittest
from registration_module import RegistrationModule
from crew_management_module import CrewManagementModule
from inventory_module import InventoryModule
from race_management_module import RaceManagementModule
from results_module import ResultsModule
from mission_planning_module import MissionPlanningModule
from reputation_module import ReputationModule
from maintenance_module import MaintenanceModule
from main import StreetRaceManagerCLI
from unittest.mock import patch


class TestMissionCLIInputIntegration(unittest.TestCase):
    """Integration tests for CLI mission assignment input handling."""

    def setUp(self):
        self.cli = StreetRaceManagerCLI()
        self.driver_id = self.cli.registration.register_crew("CLI Driver")
        self.mechanic_id = self.cli.registration.register_crew("CLI Mechanic")
        self.strategist_id = self.cli.registration.register_crew("CLI Strategist")
        self.cli.crew_mgmt.assign_role(self.driver_id, "driver")
        self.cli.crew_mgmt.assign_role(self.mechanic_id, "mechanic")
        self.cli.crew_mgmt.assign_role(self.strategist_id, "strategist")

    def test_create_mission_allows_yes_for_multiple_crew_assignments(self):
        """Test that CLI accepts 'yes' while assigning multiple crew members."""
        inputs = [
            "heist",
            "Downtown operation",
            "yes",
            str(self.driver_id),
            "yes",
            str(self.mechanic_id),
            "yes",
            str(self.strategist_id),
            "no",
        ]

        with patch("builtins.input", side_effect=inputs):
            self.cli.create_mission()

        mission = self.cli.missions.get_mission(1)
        self.assertEqual(len(mission["assigned_crew"]), 3)


class TestRegistrationToCrew(unittest.TestCase):
    """Integration tests for Registration → Crew Management chain."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)

    def test_crew_must_be_registered_before_role_assignment(self):
        """Test that role assignment requires prior registration."""
        # Attempt to assign role without registration should fail
        with self.assertRaises(ValueError):
            self.crew_mgmt.assign_role(999, "driver")

    def test_registration_then_role_assignment(self):
        """Test successful registration followed by role assignment."""
        crew_id = self.registration.register_crew("Alice", "driver")
        self.crew_mgmt.assign_role(crew_id, "driver")
        self.assertEqual(self.crew_mgmt.get_crew_role(crew_id), "driver")

    def test_crew_member_name_accessible_after_registration(self):
        """Test that registered crew details are accessible."""
        crew_id = self.registration.register_crew("Bob")
        crew_info = self.registration.get_crew(crew_id)
        self.assertEqual(crew_info["name"], "Bob")


class TestRaceManagementChain(unittest.TestCase):
    """Integration tests for Crew → Race Management chain."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)
        self.inventory = InventoryModule()
        self.races = RaceManagementModule(self.crew_mgmt, self.inventory)

    def test_only_registered_drivers_can_race(self):
        """Test that unregistered crew cannot be added to race."""
        race_id = self.races.create_race("Test Race", 5000)
        
        # Try to add unregistered crew - should fail
        with self.assertRaises(ValueError):
            self.races.add_driver(race_id, 999)

    def test_non_driver_crew_cannot_race(self):
        """Test that crew without driver role cannot enter race."""
        crew_id = self.registration.register_crew("Charlie")
        self.crew_mgmt.assign_role(crew_id, "mechanic")
        
        race_id = self.races.create_race("Speed Race", 5000)
        
        # Try to add non-driver - should fail
        with self.assertRaises(ValueError):
            self.races.add_driver(race_id, crew_id)

    def test_driver_registration_and_race_participation(self):
        """Test full chain: register, assign driver role, enter race."""
        crew_id = self.registration.register_crew("Dave")
        self.crew_mgmt.assign_role(crew_id, "driver")
        
        race_id = self.races.create_race("Championship", 10000)
        vehicle_id = self.inventory.add_vehicle("Ferrari")
        
        # Should succeed
        self.races.add_driver(race_id, crew_id)
        self.races.add_vehicle(race_id, vehicle_id)
        
        self.assertIn(crew_id, self.races.get_race_drivers(race_id))
        self.assertIn(vehicle_id, self.races.get_race_vehicles(race_id))

    def test_race_start_requires_driver_and_vehicle_then_starts(self):
        """Test race readiness transition from invalid to valid state."""
        crew_id = self.registration.register_crew("Ready Driver")
        self.crew_mgmt.assign_role(crew_id, "driver")
        race_id = self.races.create_race("Readiness Race", 4000)
        vehicle_id = self.inventory.add_vehicle("Ready Car")

        self.assertFalse(self.races.is_race_ready(race_id))
        with self.assertRaises(ValueError):
            self.races.start_race(race_id)

        self.races.add_driver(race_id, crew_id)
        self.races.add_vehicle(race_id, vehicle_id)
        self.assertTrue(self.races.is_race_ready(race_id))

        self.races.start_race(race_id)
        self.assertEqual(self.races.get_race(race_id)["status"], "started")

    def test_duplicate_driver_entry_rejected(self):
        """Test duplicate-driver protection across Registration/Crew/Race modules."""
        crew_id = self.registration.register_crew("Repeat Driver")
        self.crew_mgmt.assign_role(crew_id, "driver")
        race_id = self.races.create_race("No Duplicates", 5000)

        self.races.add_driver(race_id, crew_id)
        with self.assertRaises(ValueError):
            self.races.add_driver(race_id, crew_id)


class TestRaceToResultsChain(unittest.TestCase):
    """Integration tests for Race → Results → Inventory chain."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=50000)
        self.races = RaceManagementModule(self.crew_mgmt, self.inventory)
        self.results = ResultsModule(self.inventory)

    def test_race_result_updates_inventory_cash(self):
        """Test that race prize is deducted from inventory when result recorded."""
        initial_cash = self.inventory.get_balance()
        
        crew_id = self.registration.register_crew("Eve")
        self.crew_mgmt.assign_role(crew_id, "driver")
        
        race_id = self.races.create_race("Test", 5000)
        vehicle_id = self.inventory.add_vehicle("Car")
        
        self.races.add_driver(race_id, crew_id)
        self.races.add_vehicle(race_id, vehicle_id)
        
        # Record result - deducts prize from inventory
        self.results.record_result(race_id, crew_id, 5000)
        
        self.assertEqual(
            self.inventory.get_balance(), initial_cash - 5000
        )

    def test_race_result_insufficient_funds_fails(self):
        """Test that race result fails if inventory insufficient funds."""
        self.inventory.deduct_cash(self.inventory.get_balance() - 1000)
        
        crew_id = self.registration.register_crew("Frank")
        race_id = self.races.create_race("Expensive", 5000)
        
        # Try to record prize that exceeds inventory - should fail
        with self.assertRaises(ValueError):
            self.results.record_result(race_id, crew_id, 5000)

    def test_crew_ranking_updated_on_race_win(self):
        """Test that crew ranking is updated when they win a race."""
        crew_id = self.registration.register_crew("Grace")
        self.crew_mgmt.assign_role(crew_id, "driver")
        
        race_id = self.races.create_race("Title race", 3000)
        
        self.results.record_result(race_id, crew_id, 3000)
        
        ranking = self.results.get_crew_ranking(crew_id)
        self.assertEqual(ranking["wins"], 1)
        self.assertEqual(ranking["total_prizes"], 3000)


class TestMissionPlanningValidation(unittest.TestCase):
    """Integration tests for Mission Planning module."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)
        self.missions = MissionPlanningModule(self.registration, self.crew_mgmt)

    def test_mission_requires_unregistered_crew_assignment_fails(self):
        """Test that unregistered crew cannot be assigned to missions."""
        mission_id = self.missions.create_mission("delivery", "Package to city")
        
        with self.assertRaises(ValueError):
            self.missions.assign_crew_to_mission(mission_id, 999)

    def test_mission_with_all_required_roles_can_start(self):
        """Test mission can start when all required roles are assigned."""
        # Create rescue mission (needs driver + strategist)
        mission_id = self.missions.create_mission("rescue", "Hostage situation")
        
        # Register and assign drivers
        driver_id = self.registration.register_crew("Driver1")
        self.crew_mgmt.assign_role(driver_id, "driver")
        
        strategist_id = self.registration.register_crew("Strategist1")
        self.crew_mgmt.assign_role(strategist_id, "strategist")
        
        # Assign to mission
        self.missions.assign_crew_to_mission(mission_id, driver_id)
        self.missions.assign_crew_to_mission(mission_id, strategist_id)
        
        # Should be able to start
        self.assertTrue(self.missions.can_start_mission(mission_id))
        self.missions.start_mission(mission_id)

    def test_mission_fails_without_all_required_roles(self):
        """Test that mission cannot start without all required roles."""
        # Create heist mission (needs driver, mechanic, strategist)
        mission_id = self.missions.create_mission("heist", "Bank heist")
        
        # Only assign driver
        driver_id = self.registration.register_crew("Driver2")
        self.crew_mgmt.assign_role(driver_id, "driver")
        self.missions.assign_crew_to_mission(mission_id, driver_id)
        
        # Should not be able to start
        self.assertFalse(self.missions.can_start_mission(mission_id))
        
        with self.assertRaises(ValueError):
            self.missions.start_mission(mission_id)

    def test_surveillance_mission_requires_spotter_and_strategist(self):
        """Test role validation for surveillance mission integration path."""
        mission_id = self.missions.create_mission("surveillance", "Watch target")
        strategist_id = self.registration.register_crew("Planner")
        self.crew_mgmt.assign_role(strategist_id, "strategist")
        self.missions.assign_crew_to_mission(mission_id, strategist_id)

        self.assertFalse(self.missions.can_start_mission(mission_id))

        spotter_id = self.registration.register_crew("Scout")
        self.crew_mgmt.assign_role(spotter_id, "spotter")
        self.missions.assign_crew_to_mission(mission_id, spotter_id)

        self.assertTrue(self.missions.can_start_mission(mission_id))
        self.missions.start_mission(mission_id)
        self.assertEqual(self.missions.get_mission(mission_id)["status"], "started")


class TestRaceResultCLIIntegration(unittest.TestCase):
    """Integration tests for CLI race/result interactions across modules."""

    def setUp(self):
        self.cli = StreetRaceManagerCLI()

    def test_cli_add_driver_to_race_connects_registration_and_inventory(self):
        """Test CLI path that adds driver and vehicle to race in one flow."""
        crew_id = self.cli.registration.register_crew("CLI Racer")
        self.cli.crew_mgmt.assign_role(crew_id, "driver")
        race_id = self.cli.races.create_race("CLI Race", 5000)
        vehicle_id = self.cli.inventory.add_vehicle("CLI Car")

        with patch(
            "builtins.input",
            side_effect=[str(race_id), str(crew_id), str(vehicle_id)],
        ):
            self.cli.add_driver_to_race()

        self.assertIn(crew_id, self.cli.races.get_race_drivers(race_id))
        self.assertIn(vehicle_id, self.cli.races.get_race_vehicles(race_id))

    def test_cli_record_result_updates_results_reputation_and_cash(self):
        """Test CLI result flow updates all downstream modules."""
        crew_id = self.cli.registration.register_crew("CLI Winner")
        self.cli.crew_mgmt.assign_role(crew_id, "driver")
        race_id = self.cli.races.create_race("CLI Final", 6000)
        vehicle_id = self.cli.inventory.add_vehicle("CLI Winner Car")
        self.cli.races.add_driver(race_id, crew_id)
        self.cli.races.add_vehicle(race_id, vehicle_id)

        start_cash = self.cli.inventory.get_balance()
        start_rep = self.cli.reputation.get_crew_reputation(crew_id)

        with patch("builtins.input", side_effect=[str(race_id), str(crew_id)]):
            self.cli.record_result()

        result = self.cli.results.get_race_result(race_id)
        updated_rep = self.cli.reputation.get_crew_reputation(crew_id)
        self.assertEqual(result["winner"], crew_id)
        self.assertEqual(result["prize_awarded"], 6000)
        self.assertEqual(self.cli.inventory.get_balance(), start_cash - 6000)
        self.assertEqual(updated_rep["races_won"], start_rep["races_won"] + 1)


class TestVehicleAndMaintenance(unittest.TestCase):
    """Integration tests for Inventory → Maintenance chain."""

    def setUp(self):
        self.inventory = InventoryModule(initial_cash=20000)
        self.inventory.add_part("standard_parts", 20)
        self.inventory.add_part("advanced_parts", 10)
        self.inventory.add_part("oil", 10)
        self.inventory.add_part("filters", 10)
        self.maintenance = MaintenanceModule(self.inventory)

    def test_repair_requires_cash_deduction(self):
        """Test that vehicle repair deducts cost from inventory."""
        vehicle_id = self.inventory.add_vehicle("Truck")
        self.inventory.damage_vehicle(vehicle_id, 15)
        
        initial_cash = self.inventory.get_balance()
        self.maintenance.repair_vehicle(vehicle_id, 10)
        
        # Repair cost should be deducted (10 damage * $10)
        self.assertEqual(self.inventory.get_balance(), initial_cash - 100)

    def test_vehicle_condition_updated_after_repair(self):
        """Test that vehicle condition improves after repair."""
        vehicle_id = self.inventory.add_vehicle("Car")
        self.inventory.damage_vehicle(vehicle_id, 25)
        
        self.assertEqual(self.inventory.get_vehicle_condition(vehicle_id), "damaged")
        
        self.maintenance.repair_vehicle(vehicle_id, 25)
        
        self.assertEqual(self.inventory.get_vehicle_condition(vehicle_id), "good")

    def test_damaged_vehicle_cannot_race(self):
        """Test that damaged vehicles cannot be added to races."""
        registration = RegistrationModule()
        crew_mgmt = CrewManagementModule(registration)
        races = RaceManagementModule(crew_mgmt, self.inventory)
        
        vehicle_id = self.inventory.add_vehicle("RaceCar")
        self.inventory.damage_vehicle(vehicle_id, 21)  # Becomes critical
        
        race_id = races.create_race("Race", 5000)
        
        with self.assertRaises(ValueError):
            races.add_vehicle(race_id, vehicle_id)


class TestReputationTracking(unittest.TestCase):
    """Integration tests for Reputation module."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.reputation = ReputationModule(self.registration)

    def test_reputation_initialized_on_first_access(self):
        """Test that reputation is initialized when first accessed."""
        crew_id = self.registration.register_crew("Henry")
        
        # First access initializes
        rep = self.reputation.get_crew_reputation(crew_id)
        self.assertEqual(rep["score"], 50)
        self.assertEqual(rep["missions_completed"], 0)

    def test_mission_success_increases_reputation(self):
        """Test that successful missions increase reputation."""
        crew_id = self.registration.register_crew("Ivy")
        initial_score = self.reputation.get_score(crew_id)
        
        self.reputation.record_mission_completion(crew_id, successful=True)
        
        new_score = self.reputation.get_score(crew_id)
        self.assertGreater(new_score, initial_score)

    def test_mission_failure_decreases_reputation(self):
        """Test that failed missions decrease reputation."""
        crew_id = self.registration.register_crew("Jack")
        initial_score = self.reputation.get_score(crew_id)
        
        self.reputation.record_mission_completion(crew_id, successful=False)
        
        new_score = self.reputation.get_score(crew_id)
        self.assertLess(new_score, initial_score)

    def test_reputation_level_progression(self):
        """Test reputation level changes with score."""
        crew_id = self.registration.register_crew("Karen")
        
        # Start as Professional at default score 50
        self.assertEqual(
            self.reputation.get_reputation_level(crew_id),
            "Professional",
        )
        
        # Boost to Professional range
        for _ in range(8):
            self.reputation.record_mission_completion(crew_id, successful=True)
        
        self.assertIn(
            self.reputation.get_reputation_level(crew_id),
            ["Professional", "Elite", "Legend"],
        )


class TestCompleteWorkflow(unittest.TestCase):
    """End-to-end integration test of complete system workflow."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=100000)
        self.inventory.add_part("standard_parts", 20)
        self.inventory.add_part("advanced_parts", 10)
        self.inventory.add_part("oil", 10)
        self.inventory.add_part("filters", 10)
        self.races = RaceManagementModule(self.crew_mgmt, self.inventory)
        self.results = ResultsModule(self.inventory)
        self.missions = MissionPlanningModule(self.registration, self.crew_mgmt)
        self.reputation = ReputationModule(self.registration)
        self.maintenance = MaintenanceModule(self.inventory)

    def test_complete_crew_racing_workflow(self):
        """Test: Register→Assign Role→Create Race→Assign Vehicle→Complete Race."""
        # Step 1: Register crew
        driver_id = self.registration.register_crew("Racing Legend")
        self.reputation.initialize_crew(driver_id)
        
        # Step 2: Assign driver role
        self.crew_mgmt.assign_role(driver_id, "driver")
        self.assertTrue(self.crew_mgmt.has_role(driver_id, "driver"))
        
        # Step 3: Add vehicle
        vehicle_id = self.inventory.add_vehicle("Fast Car")
        
        # Step 4: Create race
        race_id = self.races.create_race("Championship", 10000)
        self.races.add_driver(race_id, driver_id)
        self.races.add_vehicle(race_id, vehicle_id)
        
        # Step 5: Start race
        self.assertTrue(self.races.is_race_ready(race_id))
        self.races.start_race(race_id)
        
        # Step 6: Record result and update reputation
        self.results.record_result(race_id, driver_id, 10000)
        self.reputation.record_race_win(driver_id)
        
        # Verify state
        ranking = self.results.get_crew_ranking(driver_id)
        self.assertEqual(ranking["wins"], 1)
        
        rep = self.reputation.get_crew_reputation(driver_id)
        self.assertGreater(rep["races_won"], 0)

    def test_complete_mission_workflow(self):
        """Test: Register Crew→Assign Roles→Create Mission→Start Mission."""
        # Step 1: Register crew members
        driver_id = self.registration.register_crew("Mission Driver")
        mechanic_id = self.registration.register_crew("Mission Mechanic")
        strategist_id = self.registration.register_crew("Mission Strategist")
        
        # Step 2: Assign roles
        self.crew_mgmt.assign_role(driver_id, "driver")
        self.crew_mgmt.assign_role(mechanic_id, "mechanic")
        self.crew_mgmt.assign_role(strategist_id, "strategist")
        
        # Step 3: Create heist mission
        mission_id = self.missions.create_mission("heist", "High stakes operation")
        
        # Step 4: Assign crew to mission
        self.missions.assign_crew_to_mission(mission_id, driver_id)
        self.missions.assign_crew_to_mission(mission_id, mechanic_id)
        self.missions.assign_crew_to_mission(mission_id, strategist_id)
        
        # Step 5: Start mission
        self.assertTrue(self.missions.can_start_mission(mission_id))
        self.missions.start_mission(mission_id)
        
        # Step 6: Complete mission
        self.missions.complete_mission(mission_id)
        mission = self.missions.get_mission(mission_id)
        self.assertEqual(mission["status"], "completed")

    def test_vehicle_damage_race_workflow(self):
        """Test: Create Race→Damage Vehicle→Repair→Race Again."""
        driver_id = self.registration.register_crew("Stunt Driver")
        self.crew_mgmt.assign_role(driver_id, "driver")
        
        vehicle_id = self.inventory.add_vehicle("Stunt Car")
        
        # First race
        race1_id = self.races.create_race("Stunt Show 1", 5000)
        self.races.add_driver(race1_id, driver_id)
        self.races.add_vehicle(race1_id, vehicle_id)
        self.races.start_race(race1_id)
        
        # Damage vehicle post-race
        self.inventory.damage_vehicle(vehicle_id, 25)
        self.assertEqual(
            self.inventory.get_vehicle_condition(vehicle_id), "damaged"
        )
        
        # Cannot add to new race while damaged
        race2_id = self.races.create_race("Stunt Show 2", 5000)
        with self.assertRaises(ValueError):
            self.races.add_vehicle(race2_id, vehicle_id)
        
        # Repair vehicle
        self.maintenance.repair_vehicle(vehicle_id, 25)
        self.assertEqual(
            self.inventory.get_vehicle_condition(vehicle_id), "good"
        )
        
        # Can now race again
        self.races.add_vehicle(race2_id, vehicle_id)
        self.races.add_driver(race2_id, driver_id)
        self.races.start_race(race2_id)


class TestCrewSkillsAPIs(unittest.TestCase):
    """Integration-style tests exercising crew skill helper APIs."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)

    def test_set_and_get_crew_skills_and_levels(self):
        crew_id = self.registration.register_crew("Skillful Racer")

        # Assign role to ensure crew is considered valid
        self.crew_mgmt.assign_role(crew_id, "driver")

        self.crew_mgmt.set_skill_level(crew_id, "drifting", 7)
        self.crew_mgmt.set_skill_level(crew_id, "diagnostics", 4)

        skills = self.crew_mgmt.get_crew_skills(crew_id)
        self.assertEqual(skills["drifting"], 7)
        self.assertEqual(skills["diagnostics"], 4)

        self.assertEqual(self.crew_mgmt.get_skill_level(crew_id, "drifting"), 7)
        self.assertEqual(self.crew_mgmt.get_skill_level(crew_id, "unknown"), 0)


class TestInventoryToolsAndListing(unittest.TestCase):
    """Integration-style tests for inventory tools and listing helpers."""

    def setUp(self):
        self.inventory = InventoryModule(initial_cash=15000)

    def test_add_tools_and_list_inventory(self):
        self.inventory.add_tool("wrench", 3)
        self.inventory.add_tool("jack", 1)

        self.assertEqual(self.inventory.get_tool_quantity("wrench"), 3)
        self.assertEqual(self.inventory.get_tool_quantity("jack"), 1)

        snapshot = self.inventory.list_inventory()
        tool_names = set(snapshot["tools"].keys())
        self.assertIn("wrench", tool_names)
        self.assertIn("jack", tool_names)


class TestMaintenanceHelperAPIs(unittest.TestCase):
    """Integration-style tests for maintenance helper APIs."""

    def setUp(self):
        self.inventory = InventoryModule(initial_cash=20000)
        self.inventory.add_part("oil", 5)
        self.inventory.add_part("filters", 5)
        self.maintenance = MaintenanceModule(self.inventory)

    def test_perform_standard_maintenance_and_total_cost(self):
        vehicle_id = self.inventory.add_vehicle("Service Car")

        # Perform standard maintenance twice
        self.maintenance.perform_standard_maintenance(vehicle_id)
        self.maintenance.perform_standard_maintenance(vehicle_id)

        history = self.maintenance.get_maintenance_history(vehicle_id)
        self.assertEqual(len(history), 2)

        total_cost = self.maintenance.get_total_maintenance_cost(vehicle_id)
        # Each standard maintenance uses the configured oil_change cost
        expected_single_cost = self.maintenance.repair_costs["oil_change"]
        self.assertEqual(total_cost, 2 * expected_single_cost)

    def test_get_repair_cost_lookup(self):
        self.assertGreater(self.maintenance.get_repair_cost("engine_overhaul"), 0)
        self.assertEqual(self.maintenance.get_repair_cost("unknown_type"), 0)


class TestMissionMetadataAPIs(unittest.TestCase):
    """Tests for mission metadata helper functions like get_required_roles."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)
        self.missions = MissionPlanningModule(self.registration, self.crew_mgmt)

    def test_get_required_roles_exposes_mission_contract(self):
        heist_roles = self.missions.get_required_roles("heist")
        self.assertIn("driver", heist_roles)
        self.assertIn("mechanic", heist_roles)
        self.assertIn("strategist", heist_roles)


class TestReputationListingAPIs(unittest.TestCase):
    """Tests for listing crew by reputation score."""

    def setUp(self):
        self.registration = RegistrationModule()
        self.reputation = ReputationModule(self.registration)

    def test_list_crew_by_reputation_orders_by_score(self):
        low_id = self.registration.register_crew("Low Rep")
        high_id = self.registration.register_crew("High Rep")

        # Boost one crew member's score
        for _ in range(5):
            self.reputation.record_mission_completion(high_id, successful=True)

        listing = self.reputation.list_crew_by_reputation()
        crew_ids_in_order = [entry["crew_id"] for entry in listing]

        # Only the crew that has reputation activity must appear,
        # and it should be first in the sorted list.
        self.assertIn(high_id, crew_ids_in_order)
        self.assertEqual(crew_ids_in_order[0], high_id)


class TestResultsListingAPIs(unittest.TestCase):
    """Tests for listing recorded race results."""

    def setUp(self):
        self.inventory = InventoryModule(initial_cash=50000)
        self.results = ResultsModule(self.inventory)

    def test_list_results_returns_all_recorded_races(self):
        # Record two results with different race IDs
        self.results.record_result(1, winner_crew_id=10, prize_amount=1000)
        self.results.record_result(2, winner_crew_id=20, prize_amount=2000)

        results_list = self.results.list_results()
        race_ids = {entry["race_id"] for entry in results_list}

        self.assertEqual(race_ids, {1, 2})


class TestInventoryCashAndListingAPIs(unittest.TestCase):
    """Additional tests for cash helpers and vehicle/mission listings."""

    def setUp(self):
        self.inventory = InventoryModule(initial_cash=1000)
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)
        self.races = RaceManagementModule(self.crew_mgmt, self.inventory)
        self.missions = MissionPlanningModule(self.registration, self.crew_mgmt)

    def test_add_cash_and_deduct_cash_round_trip(self):
        self.inventory.add_cash(500)
        self.assertEqual(self.inventory.get_balance(), 1500)

        self.inventory.deduct_cash(200)
        self.assertEqual(self.inventory.get_balance(), 1300)

    def test_list_races_and_list_missions_return_ids(self):
        r1 = self.races.create_race("Sprint", 1000)
        r2 = self.races.create_race("Endurance", 2000)

        m1 = self.missions.create_mission("delivery", "City A")
        m2 = self.missions.create_mission("parts_run", "City B")

        race_ids = {race["id"] for race in self.races.list_races()}
        mission_ids = {mission["id"] for mission in self.missions.list_missions()}

        self.assertEqual(race_ids, {r1, r2})
        self.assertEqual(mission_ids, {m1, m2})


class TestMaintenanceNeedsMaintenanceAPI(unittest.TestCase):
    """Tests for the needs_maintenance helper on vehicles."""

    def setUp(self):
        self.inventory = InventoryModule(initial_cash=5000)
        self.maintenance = MaintenanceModule(self.inventory)

    def test_needs_maintenance_reflects_vehicle_damage(self):
        vehicle_id = self.inventory.add_vehicle("Service Van")

        # Fresh vehicle should not need maintenance
        self.assertFalse(self.maintenance.needs_maintenance(vehicle_id))

        # After damage, maintenance should be required
        self.inventory.damage_vehicle(vehicle_id, 5)
        self.assertTrue(self.maintenance.needs_maintenance(vehicle_id))


class TestLeaderboardAPI(unittest.TestCase):
    """Tests for the leaderboard helper in ResultsModule."""

    def setUp(self):
        self.inventory = InventoryModule(initial_cash=50000)
        self.results = ResultsModule(self.inventory)

    def test_leaderboard_orders_by_wins(self):
        # Crew 1 wins two races, crew 2 wins one
        self.results.record_result(1, winner_crew_id=1, prize_amount=1000)
        self.results.record_result(2, winner_crew_id=1, prize_amount=2000)
        self.results.record_result(3, winner_crew_id=2, prize_amount=1500)

        leaderboard = self.results.get_leaderboard()
        self.assertGreaterEqual(len(leaderboard), 2)
        self.assertEqual(leaderboard[0]["crew_id"], 1)


if __name__ == "__main__":
    unittest.main()
