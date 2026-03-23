"""Vehicle Maintenance System module for StreetRace Manager.

Manages vehicle maintenance schedules, parts usage, and repair costs.
Maintains vehicle operational status across races.
"""


class MaintenanceModule:
    """Manages vehicle maintenance and repair."""

    def __init__(self, inventory):
        """
        Initialize with reference to inventory module.
        
        Args:
            inventory: InventoryModule instance.
        """
        self.inventory = inventory
        self.maintenance_log = {}  # {vehicle_id: [...maintenance events...]}
        self.repair_costs = {
            "oil_change": 50,
            "tire_replacement": 200,
            "brake_service": 150,
            "engine_overhaul": 1000,
            "suspension_repair": 300,
        }
        self.maintenance_requirements = {}  # {vehicle_id: {part_type: quantity_needed}}

    def log_maintenance(self, vehicle_id, maintenance_type, cost, parts_used=None):
        """
        Log a maintenance operation for a vehicle.
        
        Args:
            vehicle_id (int): Vehicle ID.
            maintenance_type (str): Type of maintenance performed.
            cost (int): Cost of maintenance.
            parts_used (dict): Parts consumed {'part_name': quantity}.
        
        Raises:
            ValueError: If insufficient parts in inventory.
        """
        if parts_used is None:
            parts_used = {}

        # Check parts availability
        for part, qty in parts_used.items():
            if self.inventory.get_part_quantity(part) < qty:
                raise ValueError(f"Not enough {part} in inventory (need {qty})")

        # Deduct parts from inventory
        for part, qty in parts_used.items():
            self.inventory.remove_part(part, qty)

        # Deduct cost from inventory cash
        self.inventory.deduct_cash(cost)

        # Log the maintenance
        if vehicle_id not in self.maintenance_log:
            self.maintenance_log[vehicle_id] = []

        self.maintenance_log[vehicle_id].append(
            {
                "type": maintenance_type,
                "cost": cost,
                "parts_used": parts_used.copy(),
            }
        )

    def repair_vehicle(self, vehicle_id, damage_level_repaired=None):
        """
        Repair damage to a vehicle.
        
        Args:
            vehicle_id (int): Vehicle ID.
            damage_level_repaired (int): Amount of damage to repair.
        
        Returns:
            int: Total repair cost.
        """
        vehicle = self.inventory.get_vehicle(vehicle_id)
        if damage_level_repaired is None:
            damage_level_repaired = vehicle["damage_level"]

        # Calculate repair cost (10 currency units per damage point)
        repair_cost = damage_level_repaired * 10

        # Repair requires specific parts based on damage severity
        parts_needed = {}
        if damage_level_repaired > 30:
            parts_needed["advanced_parts"] = 5
        if damage_level_repaired > 15:
            parts_needed["standard_parts"] = 3

        # Perform maintenance logging
        self.log_maintenance(
            vehicle_id,
            f"Damage repair ({damage_level_repaired} points)",
            repair_cost,
            parts_needed,
        )
        #if the damge is not repaired or there is anr error that is there are no parts then the damage level should stay like that only ??
        # Update vehicle damage level
        self.inventory.vehicles[vehicle_id]["damage_level"] -= damage_level_repaired
        self.inventory.vehicles[vehicle_id]["damage_level"] = max(
            0, self.inventory.vehicles[vehicle_id]["damage_level"]
        )#why all these things if it is repaired it is zero else it remains zero so we should just if there enough parts and if then update to zero or else no repai possible 

        # Update condition
        damage = self.inventory.vehicles[vehicle_id]["damage_level"]
        if damage == 0:
            self.inventory.vehicles[vehicle_id]["condition"] = "good"
        elif damage <= 20:
            self.inventory.vehicles[vehicle_id]["condition"] = "damaged"
        else:
            self.inventory.vehicles[vehicle_id]["condition"] = "critical"

        return repair_cost

    def perform_standard_maintenance(self, vehicle_id):
        """Perform standard maintenance (oil change, inspections)."""
        cost = self.repair_costs["oil_change"]
        self.log_maintenance(
            vehicle_id, "standard_maintenance", cost, {"oil": 1, "filters": 1}
        )

    def get_maintenance_history(self, vehicle_id):
        """Get maintenance history for a vehicle."""
        if vehicle_id not in self.maintenance_log:
            return []
        return self.maintenance_log[vehicle_id].copy()

    def get_total_maintenance_cost(self, vehicle_id):
        """Get total amount spent on maintenance for a vehicle."""
        if vehicle_id not in self.maintenance_log:
            return 0
        return sum(log["cost"] for log in self.maintenance_log[vehicle_id])

    def needs_maintenance(self, vehicle_id):
        """Check if vehicle needs maintenance based on usage."""
        # Simple heuristic: vehicles with damage need maintenance
        vehicle = self.inventory.get_vehicle(vehicle_id)
        return vehicle["damage_level"] > 0

    def get_repair_cost(self, maintenance_type):
        """Get cost for a specific repair type."""
        return self.repair_costs.get(maintenance_type, 0)#if there are mutliple such types 
