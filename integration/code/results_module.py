"""Results module for StreetRace Manager.

Records race outcomes, updates rankings, and handles prize money distribution.
"""


class ResultsModule:
    """Manages race results and rankings."""

    def __init__(self, inventory):
        """
        Initialize with reference to inventory module.
        
        Args:
            inventory: InventoryModule instance for cash updates.
        """
        self.inventory = inventory
        self.race_results = {}  # {race_id: {'winner': crew_id, 'prize_awarded': amount, ...}}
        self.crew_rankings = {}  # {crew_id: {'wins': int, 'total_prizes': int}}

    def record_result(self, race_id, winner_crew_id, prize_amount):
        """
        Record race result and award prize to winner.
        
        Args:
            race_id (int): Race ID.
            winner_crew_id (int): Winning crew member ID.
            prize_amount (int): Prize money to award.
        
        Raises:
            ValueError: If insufficient funds in inventory.
        """
        if prize_amount < 0:
            raise ValueError("Prize amount cannot be negative")

        # Deduct from inventory cash
        self.inventory.deduct_cash(prize_amount)

        # Record result
        self.race_results[race_id] = {
            "winner": winner_crew_id,
            "prize_awarded": prize_amount,
        }

        # Update rankings
        if winner_crew_id not in self.crew_rankings:
            self.crew_rankings[winner_crew_id] = {"wins": 0, "total_prizes": 0}

        self.crew_rankings[winner_crew_id]["wins"] += 1
        self.crew_rankings[winner_crew_id]["total_prizes"] += prize_amount

    def get_race_result(self, race_id):
        """Get result of a completed race."""
        if race_id not in self.race_results:
            raise ValueError(f"No result recorded for race {race_id}")
        return self.race_results[race_id].copy()

    def get_crew_ranking(self, crew_id):
        """Get ranking stats for a crew member."""
        if crew_id not in self.crew_rankings:
            return {"wins": 0, "total_prizes": 0}
        return self.crew_rankings[crew_id].copy()

    def get_leaderboard(self):
        """
        Get leaderboard sorted by wins.
        
        Returns:
            list: List of crew members with their rankings, sorted by wins.
        """
        return sorted(
            [
                {**self.crew_rankings[cid], "crew_id": cid}
                for cid in self.crew_rankings.keys()
            ],
            key=lambda x: x["wins"],
            reverse=True,
        )

    def list_results(self):
        """List all recorded race results."""
        return [
            {**self.race_results[rid], "race_id": rid}
            for rid in sorted(self.race_results.keys())
        ]
