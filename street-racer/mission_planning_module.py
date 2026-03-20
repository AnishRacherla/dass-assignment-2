"""Mission Planning module for StreetRace Manager.

Assigns missions and enforces preconditions on required crew roles.
"""


class MissionPlanningModule:
    """Manages mission assignment and verification."""

    MISSION_TYPES = {
        "delivery": {"required_roles": ["driver"]},
        "rescue": {"required_roles": ["driver", "strategist"]},
        "heist": {"required_roles": ["driver", "mechanic", "strategist"]},
        "parts_run": {"required_roles": ["driver"]},
        "surveillance": {"required_roles": ["strategist", "spotter"]},
    }

    def __init__(self, registration, crew_management):
        """
        Initialize with references to registration and crew management modules.
        
        Args:
            registration: RegistrationModule instance.
            crew_management: CrewManagementModule instance.
        """
        self.registration = registration
        self.crew_mgmt = crew_management
        self.missions = {}  # {mission_id: {'type': str, 'assigned_crew': [], ...}}
        self.next_mission_id = 1

    def create_mission(self, mission_type, target_description):
        """
        Create a new mission.
        
        Args:
            mission_type (str): One of MISSION_TYPES keys.
            target_description (str): Describe the mission target.
        
        Returns:
            int: Mission ID.
        
        Raises:
            ValueError: If invalid mission type.
        """
        if mission_type not in self.MISSION_TYPES:
            raise ValueError(
                f"Invalid mission type. Valid types: {list(self.MISSION_TYPES.keys())}"
            )

        mission_id = self.next_mission_id
        self.missions[mission_id] = {
            "type": mission_type,
            "target": target_description,
            "assigned_crew": [],
            "status": "pending",
        }
        self.next_mission_id += 1
        return mission_id

    def assign_crew_to_mission(self, mission_id, crew_id):
        """
        Assign crew member to a mission.
        
        Args:
            mission_id (int): Mission ID.
            crew_id (int): Crew member ID.
        
        Raises:
            ValueError: If crew not registered or already assigned.
        """
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")

        if not self.registration.crew_exists(crew_id):
            raise ValueError(f"Crew {crew_id} not registered")

        if crew_id in self.missions[mission_id]["assigned_crew"]:
            raise ValueError(f"Crew {crew_id} already assigned to this mission")

        self.missions[mission_id]["assigned_crew"].append(crew_id)

    def can_start_mission(self, mission_id):
        """
        Check if mission has all required roles assigned.
        
        Returns:
            bool: True if all role requirements met.
        """
        if mission_id not in self.missions:
            return False

        mission = self.missions[mission_id]
        required_roles = self.MISSION_TYPES[mission["type"]]["required_roles"]
        assigned_roles = [
            self.crew_mgmt.get_crew_role(cid) for cid in mission["assigned_crew"]
        ]

        # Check if all required roles are covered
        for required in required_roles:
            if required not in assigned_roles:
                return False
        return True

    def start_mission(self, mission_id):
        """
        Start a mission if all roles are available.
        
        Raises:
            ValueError: If required roles missing.
        """
        if not self.can_start_mission(mission_id):
            mission = self.missions[mission_id]
            required = self.MISSION_TYPES[mission["type"]]["required_roles"]
            assigned_roles = [
                self.crew_mgmt.get_crew_role(cid)
                for cid in mission["assigned_crew"]
            ]
            raise ValueError(
                f"Missing required roles: {set(required) - set(assigned_roles)}"
            )
        self.missions[mission_id]["status"] = "started"

    def complete_mission(self, mission_id):
        """Mark mission as completed."""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        self.missions[mission_id]["status"] = "completed"

    def get_mission(self, mission_id):
        """Get mission details."""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        return self.missions[mission_id].copy()

    def list_missions(self):
        """List all missions."""
        return [
            {**self.missions[mid], "id": mid}
            for mid in sorted(self.missions.keys())
        ]

    def get_required_roles(self, mission_type):
        """Get required roles for a mission type."""
        if mission_type not in self.MISSION_TYPES:
            raise ValueError(f"Unknown mission type: {mission_type}")
        return self.MISSION_TYPES[mission_type]["required_roles"].copy()
