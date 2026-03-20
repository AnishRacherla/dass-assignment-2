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
        print("9. Exit")

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
        print(f"Vehicle count: {len(self.inventory.list_vehicles())}")
        print(f"Race count: {len(self.races.list_races())}")
        print(f"Mission count: {len(self.missions.list_missions())}")
        print(f"Cash balance: ${self.inventory.get_balance()}")
        print("Top leaderboard entries:")
        leaderboard = self.results.get_leaderboard()
        for entry in leaderboard[:5]:
            print(
                f"  Crew {entry['crew_id']} | Wins: {entry['wins']}"
                f" | Prize: ${entry['total_prizes']}"
            )

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
