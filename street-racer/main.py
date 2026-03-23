"""Command-line interface for StreetRace Manager."""

from registration_module import RegistrationModule
from crew_management_module import CrewManagementModule
from inventory_module import InventoryModule
from race_management_module import RaceManagementModule
from results_module import ResultsModule
from mission_planning_module import MissionPlanningModule
from reputation_module import ReputationModule
from maintenance_module import MaintenanceModule


class StreetRaceManagerCLI:
    """Simple CLI facade across all StreetRace modules."""

    def __init__(self):
        self.registration = RegistrationModule()
        self.crew_mgmt = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=50000)
        self.races = RaceManagementModule(self.crew_mgmt, self.inventory)
        self.results = ResultsModule(self.inventory)
        self.missions = MissionPlanningModule(self.registration, self.crew_mgmt)
        self.reputation = ReputationModule(self.registration)
        self.maintenance = MaintenanceModule(self.inventory)

    @staticmethod
    def _is_yes(value):
        """Return True for affirmative answers."""
        return value.strip().lower() in {"y", "yes"}

    @staticmethod
    def _is_no(value):
        """Return True for negative answers."""
        return value.strip().lower() in {"n", "no"}

    def show_menu(self):
        """Print CLI menu."""
        print("\n=== StreetRace Manager ===")
        print("1. Register Crew Member")
        print("2. Assign Crew Role")
        print("3. Add Vehicle")
        print("4. Create Race")
        print("5. Add Driver To Race")
        print("6. Record Race Result")
        print("7. Create Mission")
        print("8. Show Dashboard")
        print("9. Maintenance & Repairs")
        print("10. Crew Skills & Reputation")
        print("11. Race Control")
        print("12. Mission Control")
        print("13. Exit")

    def register_crew(self):
        """Register a new crew member via CLI input."""
        name = input("Enter crew name: ").strip()
        crew_id = self.registration.register_crew(name)
        self.reputation.initialize_crew(crew_id)
        print(f"Registered {name} with Crew ID {crew_id}")

    def assign_role(self):
        """Assign role to an existing crew member."""
        crew_id = int(input("Enter crew ID: ").strip())
        role = input("Enter role (driver/mechanic/strategist/engineer/spotter): ").strip()
        self.crew_mgmt.assign_role(crew_id, role)
        print(f"Assigned role '{role}' to crew {crew_id}")

    def add_vehicle(self):
        """Add a vehicle to inventory."""
        model = input("Enter vehicle model: ").strip()
        vehicle_id = self.inventory.add_vehicle(model)
        print(f"Added vehicle '{model}' with ID {vehicle_id}")

    def create_race(self):
        """Create a new race."""
        name = input("Enter race name: ").strip()
        prize = int(input("Enter prize money: ").strip())
        race_id = self.races.create_race(name, prize)
        print(f"Created race '{name}' with ID {race_id}")

    def add_driver_to_race(self):
        """Add a driver and vehicle to a race."""
        race_id = int(input("Enter race ID: ").strip())
        crew_id = int(input("Enter crew ID (driver): ").strip())
        vehicle_id = int(input("Enter vehicle ID: ").strip())
        self.races.add_driver(race_id, crew_id)
        self.races.add_vehicle(race_id, vehicle_id)
        print(f"Added crew {crew_id} and vehicle {vehicle_id} to race {race_id}")

    def record_result(self):
        """Record race winner and award prize."""
        race_id = int(input("Enter race ID: ").strip())
        winner_id = int(input("Enter winner crew ID: ").strip())
        prize_amount = self.races.get_race_prize(race_id)
        self.results.record_result(race_id, winner_id, prize_amount)
        self.reputation.record_race_win(winner_id)
        print(f"Recorded result for race {race_id}; winner crew {winner_id}")

    def create_mission(self):
        """Create a mission and optionally assign crew members."""
        mission_type = input(
            "Enter mission type (delivery/rescue/heist/parts_run/surveillance): "
        ).strip()
        target = input("Enter mission target description: ").strip()
        mission_id = self.missions.create_mission(mission_type, target)

        # Surface required roles so MissionPlanningModule.get_required_roles is
        # used in the main flow and players see the expectations.
        try:
            required_roles = self.missions.get_required_roles(mission_type)
            if required_roles:
                print(
                    "Required roles for this mission:",
                    ", ".join(required_roles),
                )
        except ValueError:
            # Invalid types are already rejected inside create_mission; this is
            # just a defensive guard.
            pass

        add_crew = input("Assign crew now? (y/n): ").strip()
        while True:
            if self._is_yes(add_crew):
                crew_id = int(input("Enter crew ID to assign: ").strip())
                self.missions.assign_crew_to_mission(mission_id, crew_id)
                add_crew = input("Assign another crew? (y/n): ").strip()
                continue
            if self._is_no(add_crew):
                break
            print("Please enter y/yes or n/no.")
            add_crew = input("Assign crew now? (y/n): ").strip()

        print(f"Created mission ID {mission_id}")

    def show_dashboard(self):
        """Show current system overview."""
        print("\n--- Dashboard ---")
        print(f"Crew count: {len(self.registration.list_crew())}")
        print(f"Race count: {len(self.races.list_races())}")
        print(f"Mission count: {len(self.missions.list_missions())}")

        # Use list_inventory to summarise vehicles, parts, and tools.
        inventory_snapshot = self.inventory.list_inventory()
        print(f"Vehicle count: {len(inventory_snapshot['vehicles'])}")
        print(f"Known part types: {len(inventory_snapshot['parts'])}")
        print(f"Known tool types: {len(inventory_snapshot['tools'])}")
        print(f"Cash balance: ${inventory_snapshot['cash']}")

        # Use ResultsModule.list_results to show how many races have results.
        results = self.results.list_results()
        print(f"Recorded race results: {len(results)}")

        # Show top leaderboard entries based on reputation-aware results.
        print("Top leaderboard entries:")
        leaderboard = self.results.get_leaderboard()
        for entry in leaderboard[:5]:
            print(
                f"  Crew {entry['crew_id']} | Wins: {entry['wins']}"
                f" | Prize: ${entry['total_prizes']}"
            )

        # Also surface reputation ordering so list_crew_by_reputation is used.
        rep_listing = self.reputation.list_crew_by_reputation()
        if rep_listing:
            print("Reputation ranking (top 5):")
            for row in rep_listing[:5]:
                print(
                    f"  Crew {row['crew_id']} | Score: {row['score']}"
                    f" | Races won: {row['races_won']}"
                )

    def maintenance_menu(self):
        """Interactive maintenance menu using MaintenanceModule helpers."""
        print("\n--- Maintenance & Repairs ---")
        if not self.inventory.list_vehicles():
            print("No vehicles in inventory. Add a vehicle first.")
            return

        while True:
            print("\nMaintenance options:")
            print("1. Perform standard maintenance (oil change)")
            print("2. Repair vehicle damage")
            print("3. Show maintenance history and total cost")
            print("4. Manage tools (add/check quantity)")
            print("5. Back to main menu")
            choice = input("Choose an option: ").strip()

            if choice == "5":
                break

            vehicle_id = int(input("Enter vehicle ID: ").strip())

            if choice == "1":
                self.maintenance.perform_standard_maintenance(vehicle_id)
                print("Standard maintenance logged.")
            elif choice == "2":
                # Only repair if vehicle currently needs maintenance.
                if not self.maintenance.needs_maintenance(vehicle_id):
                    print("Vehicle does not currently need maintenance.")
                else:
                    damage = self.inventory.get_vehicle(vehicle_id)["damage_level"]
                    print(f"Current damage level: {damage}")
                    amount_str = input(
                        "Damage points to repair (blank for full repair): "
                    ).strip()
                    if amount_str:
                        amount = int(amount_str)
                    else:
                        amount = None
                    cost = self.maintenance.repair_vehicle(vehicle_id, amount)
                    print(f"Repair completed. Cost: ${cost}")
            elif choice == "3":
                history = self.maintenance.get_maintenance_history(vehicle_id)
                total = self.maintenance.get_total_maintenance_cost(vehicle_id)
                print(f"Total maintenance cost: ${total}")
                if not history:
                    print("No maintenance history for this vehicle.")
                else:
                    for entry in history:
                        print(
                            f"  {entry['type']} | Cost: ${entry['cost']}"
                            f" | Parts: {entry['parts_used']}"
                        )
            elif choice == "4":
                tool = input("Tool name: ").strip()
                qty_str = input("Quantity to add (0 to skip adding): ").strip()
                qty = int(qty_str or "0")
                if qty > 0:
                    self.inventory.add_tool(tool, qty)
                current_qty = self.inventory.get_tool_quantity(tool)
                print(f"Current quantity of '{tool}': {current_qty}")
            else:
                print("Invalid choice.")

    def crew_skills_menu(self):
        """Interactive menu for crew skills and reputation helpers."""
        print("\n--- Crew Skills & Reputation ---")
        crew_list = self.registration.list_crew()
        if not crew_list:
            print("No crew registered yet.")
            return

        print("Available crew:")
        for crew in crew_list:
            print(f"  ID {crew['id']}: {crew['name']}")

        crew_id = int(input("Enter crew ID to manage: ").strip())

        while True:
            print("\nCrew options:")
            print("1. Set skill level")
            print("2. Show skills")
            print("3. Show reputation and score")
            print("4. Show race ranking for this crew")
            print("5. Back to main menu")
            choice = input("Choose an option: ").strip()

            if choice == "5":
                break

            if choice == "1":
                skill = input("Skill name: ").strip()
                level = int(input("Skill level (1-10): ").strip())
                self.crew_mgmt.set_skill_level(crew_id, skill, level)
                print("Skill level set.")
            elif choice == "2":
                skills = self.crew_mgmt.get_crew_skills(crew_id)
                if not skills:
                    print("No skills recorded.")
                else:
                    for name, level in skills.items():
                        print(f"  {name}: {level}")
            elif choice == "3":
                rep = self.reputation.get_crew_reputation(crew_id)
                level = self.reputation.get_reputation_level(crew_id)
                score = self.reputation.get_score(crew_id)
                print(
                    f"Reputation level: {level} (score {score}) | "
                    f"Missions: {rep['missions_completed']} | "
                    f"Races won: {rep['races_won']} | Failures: {rep['failures']}"
                )
            elif choice == "4":
                ranking = self.results.get_crew_ranking(crew_id)
                print(
                    f"Race record for crew {crew_id}: "
                    f"wins={ranking['wins']}, total prizes=${ranking['total_prizes']}"
                )
            else:
                print("Invalid choice.")

    def race_menu(self):
        """Interactive menu for race control helpers."""
        print("\n--- Race Control ---")
        races = self.races.list_races()
        if not races:
            print("No races created yet.")
            return

        print("Available races:")
        for race in races:
            print(
                f"  ID {race['id']}: {race['name']} "
                f"(status={race['status']}, prize=${race['prize']})"
            )

        race_id = int(input("Enter race ID to manage: ").strip())

        while True:
            print("\nRace options:")
            print("1. Show race details (drivers/vehicles/prize)")
            print("2. Check if race is ready")
            print("3. Start race")
            print("4. Back to main menu")
            choice = input("Choose an option: ").strip()

            if choice == "4":
                break

            if choice == "1":
                try:
                    details = self.races.get_race(race_id)
                    drivers = self.races.get_race_drivers(race_id)
                    vehicles = self.races.get_race_vehicles(race_id)
                    prize = self.races.get_race_prize(race_id)
                except ValueError as error:
                    print(error)
                    continue
                print(f"Race '{details['name']}' (status={details['status']})")
                print(f"Prize: ${prize}")
                print(f"Drivers: {drivers if drivers else 'None'}")
                print(f"Vehicles: {vehicles if vehicles else 'None'}")
            elif choice == "2":
                ready = self.races.is_race_ready(race_id)
                print("Race is ready." if ready else "Race is NOT ready.")
            elif choice == "3":
                try:
                    self.races.start_race(race_id)
                    print("Race started.")
                except ValueError as error:
                    print(f"Cannot start race: {error}")
            else:
                print("Invalid choice.")

    def mission_menu(self):
        """Interactive menu for mission lifecycle helpers."""
        print("\n--- Mission Control ---")
        missions = self.missions.list_missions()
        if not missions:
            print("No missions created yet.")
            return

        print("Available missions:")
        for mission in missions:
            print(
                f"  ID {mission['id']}: {mission['type']} -> {mission['target']} "
                f"(status={mission['status']})"
            )

        mission_id = int(input("Enter mission ID to manage: ").strip())

        while True:
            print("\nMission options:")
            print("1. Show mission details")
            print("2. Check if mission can start")
            print("3. Start mission")
            print("4. Complete mission and update reputation")
            print("5. Back to main menu")
            choice = input("Choose an option: ").strip()

            if choice == "5":
                break

            if choice == "1":
                try:
                    mission = self.missions.get_mission(mission_id)
                except ValueError as error:
                    print(error)
                    continue
                required_roles = self.missions.get_required_roles(mission["type"])
                print(
                    f"Mission {mission_id}: {mission['type']} -> {mission['target']} "
                    f"(status={mission['status']})"
                )
                print(f"Assigned crew: {mission['assigned_crew'] or 'None'}")
                print(f"Required roles: {', '.join(required_roles)}")
            elif choice == "2":
                can_start = self.missions.can_start_mission(mission_id)
                print(
                    "Mission can start." if can_start else "Mission CANNOT start yet."
                )
            elif choice == "3":
                try:
                    self.missions.start_mission(mission_id)
                    print("Mission started.")
                except ValueError as error:
                    print(f"Cannot start mission: {error}")
            elif choice == "4":
                try:
                    mission = self.missions.get_mission(mission_id)
                except ValueError as error:
                    print(error)
                    continue
                success_input = input(
                    "Was the mission successful? (y/n): "
                ).strip()
                successful = self._is_yes(success_input)
                self.missions.complete_mission(mission_id)
                # Update reputation for all assigned crew members.
                for crew_id in mission["assigned_crew"]:
                    self.reputation.record_mission_completion(crew_id, successful)
                print("Mission marked completed and reputation updated.")
            else:
                print("Invalid choice.")

    def run(self):
        """Run CLI loop."""
        while True:
            try:
                self.show_menu()
                choice = input("Choose an option: ").strip()

                if choice == "1":
                    self.register_crew()
                elif choice == "2":
                    self.assign_role()
                elif choice == "3":
                    self.add_vehicle()
                elif choice == "4":
                    self.create_race()
                elif choice == "5":
                    self.add_driver_to_race()
                elif choice == "6":
                    self.record_result()
                elif choice == "7":
                    self.create_mission()
                elif choice == "8":
                    self.show_dashboard()
                elif choice == "9":
                    self.maintenance_menu()
                elif choice == "10":
                    self.crew_skills_menu()
                elif choice == "11":
                    self.race_menu()
                elif choice == "12":
                    self.mission_menu()
                elif choice == "13":
                    print("Exiting StreetRace Manager.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError as error:
                print(f"Input error: {error}")
            except Exception as error:  # broad fallback for CLI resilience
                print(f"Operation failed: {error}")


if __name__ == "__main__":
    StreetRaceManagerCLI().run()
