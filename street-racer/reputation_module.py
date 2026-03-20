"""Reputation System module for StreetRace Manager.

Tracks crew member reputation and performance metrics.
Reputation affects mission eligibility and prestige.
"""


class ReputationModule:
    """Manages crew reputation and performance tracking."""

    def __init__(self, registration):
        """
        Initialize with reference to registration module.
        
        Args:
            registration: RegistrationModule instance.
        """
        self.registration = registration
        self.reputation = {}  # {crew_id: {'score': int, 'missions_completed': int, ...}}

    def initialize_crew(self, crew_id):
        """Initialize reputation for a newly registered crew member."""
        if not self.registration.crew_exists(crew_id):
            raise ValueError(f"Crew {crew_id} not registered")

        if crew_id not in self.reputation:
            self.reputation[crew_id] = {
                "score": 50,  # Starting score out of 100
                "missions_completed": 0,
                "races_won": 0,
                "failures": 0,
            }

    def add_reputation(self, crew_id, amount):
        """
        Add reputation points to a crew member.
        
        Args:
            crew_id (int): Crew member ID.
            amount (int): Points to add (can be negative).
        
        Raises:
            ValueError: If crew not registered or score out of bounds.
        """
        if crew_id not in self.reputation:
            self.initialize_crew(crew_id)

        self.reputation[crew_id]["score"] += amount
        # Clamp score between 0 and 100
        self.reputation[crew_id]["score"] = max(
            0, min(100, self.reputation[crew_id]["score"])
        )

    def record_mission_completion(self, crew_id, successful=True):
        """Record mission completion and update reputation."""
        if crew_id not in self.reputation:
            self.initialize_crew(crew_id)

        self.reputation[crew_id]["missions_completed"] += 1
        if successful:
            self.add_reputation(crew_id, 5)
        else:
            self.reputation[crew_id]["failures"] += 1
            self.add_reputation(crew_id, -10)

    def record_race_win(self, crew_id):
        """Record race win and boost reputation."""
        if crew_id not in self.reputation:
            self.initialize_crew(crew_id)

        self.reputation[crew_id]["races_won"] += 1
        self.add_reputation(crew_id, 10)

    def get_reputation_level(self, crew_id):
        """
        Get reputation level based on score.
        
        Returns:
            str: Level ('Rookie', 'Professional', 'Elite', 'Legend').
        """
        if crew_id not in self.reputation:
            self.initialize_crew(crew_id)

        score = self.reputation[crew_id]["score"]
        if score >= 80:
            return "Legend"
        elif score >= 60:
            return "Elite"
        elif score >= 40:
            return "Professional"
        else:
            return "Rookie"

    def get_crew_reputation(self, crew_id):
        """Get full reputation stats for a crew member."""
        if crew_id not in self.reputation:
            self.initialize_crew(crew_id)
        return self.reputation[crew_id].copy()

    def get_score(self, crew_id):
        """Get reputation score (0-100)."""
        if crew_id not in self.reputation:
            self.initialize_crew(crew_id)
        return self.reputation[crew_id]["score"]

    def list_crew_by_reputation(self):
        """List all crew members sorted by reputation score."""
        return sorted(
            [
                {**self.reputation[cid], "crew_id": cid}
                for cid in self.reputation.keys()
            ],
            key=lambda x: x["score"],
            reverse=True,
        )
