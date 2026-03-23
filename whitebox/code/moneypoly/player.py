"""Player model and player-state operations for MoneyPoly."""

from dataclasses import dataclass, field

from moneypoly.config import STARTING_BALANCE, BOARD_SIZE, GO_SALARY, JAIL_POSITION


@dataclass
class _PlayerState:
    """Mutable gameplay state for a single player."""

    balance: int
    position: int = 0
    properties: list = field(default_factory=list)
    in_jail: bool = False
    jail_turns: int = 0
    get_out_of_jail_cards: int = 0
    is_eliminated: bool = False


class Player:
    """Represents a single player in a MoneyPoly game."""

    def __init__(self, name, balance=STARTING_BALANCE):
        self.name = name
        self._state = _PlayerState(balance=balance)

    @property
    def balance(self):
        """Current cash balance for this player."""
        return self._state.balance

    @balance.setter
    def balance(self, value):
        self._state.balance = value

    @property
    def position(self):
        """Current board position for this player."""
        return self._state.position

    @position.setter
    def position(self, value):
        self._state.position = value

    @property
    def properties(self):
        """Properties currently owned by this player."""
        return self._state.properties

    @properties.setter
    def properties(self, value):
        self._state.properties = value

    @property
    def in_jail(self):
        """Whether the player is currently in jail."""
        return self._state.in_jail

    @in_jail.setter
    def in_jail(self, value):
        self._state.in_jail = value

    @property
    def jail_turns(self):
        """How many turns the player has served in jail."""
        return self._state.jail_turns

    @jail_turns.setter
    def jail_turns(self, value):
        self._state.jail_turns = value

    @property
    def get_out_of_jail_cards(self):
        """Number of Get Out of Jail Free cards held."""
        return self._state.get_out_of_jail_cards

    @get_out_of_jail_cards.setter
    def get_out_of_jail_cards(self, value):
        self._state.get_out_of_jail_cards = value

    @property
    def is_eliminated(self):
        """Whether the player has been eliminated from the game."""
        return self._state.is_eliminated

    @is_eliminated.setter
    def is_eliminated(self, value):
        self._state.is_eliminated = value


    def add_money(self, amount):
        """Add funds to this player's balance. Amount must be non-negative."""
        if amount < 0:
            raise ValueError(f"Cannot add a negative amount: {amount}")
        self.balance += amount

    def deduct_money(self, amount):
        """Deduct funds from this player's balance. Amount must be non-negative."""
        if amount < 0:
            raise ValueError(f"Cannot deduct a negative amount: {amount}")
        self.balance -= amount

    def is_bankrupt(self):
        # bankruptcy should be determined by the player's net worth not just
        # the balance because a player might have no cash but still have
        # valuable properties that can be sold to pay off debts
        """Return True if this player has no money remaining."""
        return self.balance <= 0

    def net_worth(self):
        # total net wroth should include the value of properties owned by the
        # player as well not just the balance
        """Calculate and return this player's total net worth."""
        return self.balance + sum(prop.price for prop in self.properties)

    def move(self, steps):
        # move should also check if the player passes go and award the salary
        # accordingly.
        """
        Move this player forward by `steps` squares, wrapping around the board.
        Awards the Go salary if the player passes or lands on Go.
        Returns the new board position.
        """
        old_position = self.position
        self.position = (self.position + steps) % BOARD_SIZE

        if old_position + steps >= BOARD_SIZE:
            self.add_money(GO_SALARY)
            print(f"  {self.name} passed Go and collected ${GO_SALARY}.")

        return self.position

    def go_to_jail(self):
        """Send this player directly to the Jail square."""
        self.position = JAIL_POSITION
        self.in_jail = True
        self.jail_turns = 0


    def add_property(self, prop):
        """Add a property tile to this player's holdings."""
        if prop not in self.properties:
            self.properties.append(prop)

    def remove_property(self, prop):
        """Remove a property tile from this player's holdings."""
        if prop in self.properties:
            self.properties.remove(prop)

    def count_properties(self):
        """Return the number of properties this player currently owns."""
        return len(self.properties)


    def status_line(self):
        # what is the purpose of this function ??(not used anywhere)
        """Return a concise one-line status string for this player."""
        jail_tag = " [JAILED]" if self.in_jail else ""
        return (
            f"{self.name}: ${self.balance}  "
            f"pos={self.position}  "
            f"props={len(self.properties)}"
            f"{jail_tag}"
        )

    def __repr__(self):
        return f"Player({self.name!r}, balance={self.balance}, pos={self.position})"
