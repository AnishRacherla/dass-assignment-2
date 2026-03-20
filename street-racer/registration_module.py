"""Registration module for StreetRace Manager.

Handles registration of new crew members with name and role assignment.
"""


class RegistrationModule:
    """Manages crew member registration."""

    def __init__(self):
        self.crew_members = {}  # {crew_id: {'name': str, 'role': str}}
        self.next_id = 1

    def register_crew(self, name, role=None):
        """
        Register a new crew member.
        
        Args:
            name (str): Crew member name.
            role (str): Initial role (optional, can be assigned later).
        
        Returns:
            int: Unique crew ID.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        crew_id = self.next_id
        self.crew_members[crew_id] = {"name": name, "role": role}
        self.next_id += 1
        return crew_id

    def get_crew(self, crew_id):
        """Get crew member details by ID."""
        if crew_id not in self.crew_members:
            raise ValueError(f"Crew member {crew_id} not found")
        return self.crew_members[crew_id]

    def list_crew(self):
        """Return list of all registered crew members."""
        return [
            {**self.crew_members[cid], "id": cid}
            for cid in sorted(self.crew_members.keys())
        ]

    def crew_exists(self, crew_id):
        """Check if crew member is registered."""
        return crew_id in self.crew_members
