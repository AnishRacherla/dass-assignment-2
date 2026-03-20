"""Crew Management module for StreetRace Manager.

Manages crew roles and skill levels. Requires crew to be registered first.
"""


class CrewManagementModule:
    """Manages crew roles and skill levels."""

    VALID_ROLES = ["driver", "mechanic", "strategist", "engineer", "spotter"]

    def __init__(self, registration_module):
        """
        Initialize with reference to registration module.
        
        Args:
            registration_module: RegistrationModule instance for validation.
        """
        self.registration = registration_module
        self.crew_roles = {}  # {crew_id: {'primary_role': str, 'skills': {}}}

    def assign_role(self, crew_id, role):
        """
        Assign or update a crew member's primary role.
        
        Precondition: Crew must be registered.
        
        Args:
            crew_id (int): Crew member ID.
            role (str): Role name.
        
        Raises:
            ValueError: If crew not registered or invalid role.
        """
        if not self.registration.crew_exists(crew_id):
            raise ValueError(f"Crew member {crew_id} must be registered first")

        if role not in self.VALID_ROLES:
            raise ValueError(
                f"Invalid role '{role}'. Valid roles: {self.VALID_ROLES}"
            )

        if crew_id not in self.crew_roles:
            self.crew_roles[crew_id] = {"primary_role": role, "skills": {}}
        else:
            self.crew_roles[crew_id]["primary_role"] = role

    def set_skill_level(self, crew_id, skill_name, level):
        """
        Set a specific skill level for a crew member.
        
        Args:
            crew_id (int): Crew member ID.
            skill_name (str): Skill name (e.g., 'drifting', 'diagnostics').
            level (int): Skill level (1-10).
        
        Raises:
            ValueError: If crew not registered or skill invalid.
        """
        if not self.registration.crew_exists(crew_id):
            raise ValueError(f"Crew member {crew_id} not registered")

        if not (1 <= level <= 10):
            raise ValueError("Skill level must be between 1 and 10")

        if crew_id not in self.crew_roles:
            self.crew_roles[crew_id] = {"primary_role": None, "skills": {}}

        self.crew_roles[crew_id]["skills"][skill_name] = level

    def get_crew_role(self, crew_id):
        """Get primary role of a crew member."""
        if crew_id not in self.crew_roles:
            return None
        return self.crew_roles[crew_id]["primary_role"]

    def get_crew_skills(self, crew_id):
        """Get all skills and levels for a crew member."""
        if crew_id not in self.crew_roles:
            return {}
        return self.crew_roles[crew_id]["skills"].copy()

    def has_role(self, crew_id, role):
        """Check if crew member has a specific role."""
        return self.get_crew_role(crew_id) == role

    def get_skill_level(self, crew_id, skill_name):
        """Get skill level for a crew member, or 0 if not set."""
        if crew_id not in self.crew_roles:
            return 0
        return self.crew_roles[crew_id]["skills"].get(skill_name, 0)
