"""Race Management module for StreetRace Manager.

Creates races and selects drivers and vehicles. Enforces business rules
around driver role requirements and vehicle availability.
"""


class RaceManagementModule:
    """Manages race creation and participant selection."""

    def __init__(self, crew_management, inventory):
        """
        Initialize with references to crew and inventory modules.
        
        Args:
            crew_management: CrewManagementModule instance.
            inventory: InventoryModule instance.
        """
        self.crew_mgmt = crew_management
        self.inventory = inventory
        self.races = {}  # {race_id: {'name': str, 'drivers': [], 'vehicles': [], ...}}
        self.next_race_id = 1

    def create_race(self, name, prize=5000):
        """
        Create a new race.
        
        Args:
            name (str): Race name.
            prize (int): Prize money for winning.
        
        Returns:
            int: Race ID.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Race name must be a non-empty string")

        if prize < 0:
            raise ValueError("Prize must be non-negative")

        race_id = self.next_race_id
        self.races[race_id] = {
            "name": name,
            "status": "pending",
            "drivers": [],
            "vehicles": [],
            "prize": prize,
        }
        self.next_race_id += 1
        return race_id

    def add_driver(self, race_id, crew_id):
        """
        Add a driver to a race.
        
        Precondition: Crew member must have 'driver' role.
        
        Args:
            race_id (int): Race ID.
            crew_id (int): Crew member ID.
        
        Raises:
            ValueError: If not registered, not a driver, or already in race.
        """
        if race_id not in self.races:
            raise ValueError(f"Race {race_id} not found")

        if not self.crew_mgmt.has_role(crew_id, "driver"):
            raise ValueError(f"Crew {crew_id} must be a driver to enter races")

        if crew_id in self.races[race_id]["drivers"]:
            raise ValueError(f"Crew {crew_id} already in this race")

        self.races[race_id]["drivers"].append(crew_id)

    def add_vehicle(self, race_id, vehicle_id):
        """
        Add a vehicle to a race.
        
        Precondition: Vehicle must be in good condition.
        
        Args:
            race_id (int): Race ID.
            vehicle_id (int): Vehicle ID.
        
        Raises:
            ValueError: If vehicle damaged or already in race.
        """
        if race_id not in self.races:
            raise ValueError(f"Race {race_id} not found")

        condition = self.inventory.get_vehicle_condition(vehicle_id)
        if condition != "good":
            raise ValueError(
                f"Vehicle condition is '{condition}', must be 'good'"
            )

        if vehicle_id in self.races[race_id]["vehicles"]:
            raise ValueError(f"Vehicle {vehicle_id} already in this race")

        self.races[race_id]["vehicles"].append(vehicle_id)

    def get_race(self, race_id):
        """Get race details."""
        if race_id not in self.races:
            raise ValueError(f"Race {race_id} not found")
        return self.races[race_id].copy()

    def list_races(self):
        """List all races."""
        return [
            {**self.races[rid], "id": rid} for rid in sorted(self.races.keys())
        ]

    def is_race_ready(self, race_id):
        """Check if race has at least one driver and vehicle."""
        if race_id not in self.races:
            return False
        race = self.races[race_id]
        return len(race["drivers"]) > 0 and len(race["vehicles"]) > 0

    def start_race(self, race_id):
        """Start a race that has participants."""
        if not self.is_race_ready(race_id):
            raise ValueError("Race must have at least one driver and one vehicle")
        self.races[race_id]["status"] = "started"

    def get_race_drivers(self, race_id):
        """Get list of driver IDs for a race."""
        if race_id not in self.races:
            raise ValueError(f"Race {race_id} not found")
        return self.races[race_id]["drivers"].copy()

    def get_race_vehicles(self, race_id):
        """Get list of vehicle IDs for a race."""
        if race_id not in self.races:
            raise ValueError(f"Race {race_id} not found")
        return self.races[race_id]["vehicles"].copy()

    def get_race_prize(self, race_id):
        """Get prize amount for a race."""
        if race_id not in self.races:
            raise ValueError(f"Race {race_id} not found")
        return self.races[race_id]["prize"]
#there are drivers and vehicles is there any need to assign drivers to any vehicle .