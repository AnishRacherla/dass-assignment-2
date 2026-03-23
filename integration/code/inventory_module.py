"""Inventory module for StreetRace Manager.

Tracks vehicles, parts, tools, and cash balance.
"""


class InventoryModule:
    """Manages inventory including vehicles, parts, tools, and cash."""

    def __init__(self, initial_cash=10000):
        """
        Initialize inventory with starting cash.
        
        Args:
            initial_cash (int): Initial cash balance.
        """
        self.cash = initial_cash
        self.vehicles = {}  # {vehicle_id: {'model': str, 'condition': str, ...}}
        self.parts = {}  # {part_name: quantity}
        self.tools = {}  # {tool_name: quantity}
        self.next_vehicle_id = 1

    def add_cash(self, amount):
        """Add cash to balance."""
        if amount < 0:
            raise ValueError("Cannot add negative amount")
        self.cash += amount

    def deduct_cash(self, amount):
        """
        Deduct cash from balance.
        
        Raises:
            ValueError: If insufficient funds.
        """
        if amount < 0:
            raise ValueError("Cannot deduct negative amount")
        if self.cash < amount:
            raise ValueError(
                f"Insufficient funds. Balance: ${self.cash}, Need: ${amount}"
            )
        self.cash -= amount

    def get_balance(self):
        """Get current cash balance."""
        return self.cash

    def add_vehicle(self, model, condition="good"):
        """
        Add a vehicle to inventory.
        
        Args:
            model (str): Vehicle model name.
            condition (str): Vehicle condition ('good', 'damaged', 'critical').
        
        Returns:
            int: Vehicle ID.
        """
        vehicle_id = self.next_vehicle_id
        self.vehicles[vehicle_id] = {
            "model": model,
            "condition": condition,
            "damage_level": 0,
        }
        self.next_vehicle_id += 1
        return vehicle_id

    def get_vehicle(self, vehicle_id):
        """Get vehicle details."""
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle {vehicle_id} not found")
        return self.vehicles[vehicle_id].copy()

    def list_vehicles(self):
        """List all vehicles."""
        return [
            {**self.vehicles[vid], "id": vid}
            for vid in sorted(self.vehicles.keys())
        ]

    def damage_vehicle(self, vehicle_id, damage_amount):
        """Increase damage level of a vehicle."""
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle {vehicle_id} not found")
        self.vehicles[vehicle_id]["damage_level"] += damage_amount
        if self.vehicles[vehicle_id]["damage_level"] > 50:
            self.vehicles[vehicle_id]["condition"] = "critical"
        elif self.vehicles[vehicle_id]["damage_level"] > 20:
            self.vehicles[vehicle_id]["condition"] = "damaged"

    def get_vehicle_condition(self, vehicle_id):
        """Get vehicle condition status."""
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle {vehicle_id} not found")
        return self.vehicles[vehicle_id]["condition"]

    def add_part(self, part_name, quantity=1):
        """Add spare parts to inventory."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.parts[part_name] = self.parts.get(part_name, 0) + quantity

    def remove_part(self, part_name, quantity=1):
        """Remove spare parts from inventory."""
        if part_name not in self.parts or self.parts[part_name] < quantity:
            raise ValueError(f"Not enough {part_name} in inventory")
        self.parts[part_name] -= quantity
        if self.parts[part_name] == 0:
            del self.parts[part_name]

    def get_part_quantity(self, part_name):
        """Get quantity of a spare part."""
        return self.parts.get(part_name, 0)

    def add_tool(self, tool_name, quantity=1):
        """Add tools to inventory."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.tools[tool_name] = self.tools.get(tool_name, 0) + quantity

    def get_tool_quantity(self, tool_name):
        """Get quantity of a tool."""
        return self.tools.get(tool_name, 0)

    def list_inventory(self):
        """Get full inventory summary."""
        return {
            "cash": self.cash,
            "vehicles": self.list_vehicles(),
            "parts": self.parts.copy(),
            "tools": self.tools.copy(),
        }
