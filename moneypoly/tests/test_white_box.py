"""White-box tests for core MoneyPoly game logic."""

import unittest
from unittest.mock import patch

from moneypoly.bank import Bank
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


class BankTests(unittest.TestCase):
    """Tests for bank state transitions and edge-case amounts."""

    def test_collect_ignores_negative_amount(self):
        bank = Bank()
        initial = bank.get_balance()

        bank.collect(-100)

        self.assertEqual(bank.get_balance(), initial)

    def test_give_loan_reduces_bank_balance(self):
        bank = Bank()
        borrower = Player("Borrower")
        initial = bank.get_balance()

        bank.give_loan(borrower, 250)

        self.assertEqual(borrower.balance, 1750)
        self.assertEqual(bank.get_balance(), initial - 250)


class PropertyGroupTests(unittest.TestCase):
    """Tests for ownership branch logic in property groups."""

    def test_all_owned_by_requires_full_set(self):
        owner = Player("Owner")
        other = Player("Other")
        group = PropertyGroup("Brown", "brown")
        p1 = Property("Mediterranean Avenue", 1, 60, 2, group)
        p2 = Property("Baltic Avenue", 3, 60, 4, group)
        p1.owner = owner
        p2.owner = other

        self.assertFalse(group.all_owned_by(owner))


class PlayerTests(unittest.TestCase):
    """Tests for movement and net-worth state calculations."""

    def test_move_awards_salary_when_passing_go(self):
        player = Player("Mover")
        player.position = 39
        start_balance = player.balance

        player.move(2)

        self.assertEqual(player.position, 1)
        self.assertEqual(player.balance, start_balance + 200)

    def test_net_worth_includes_property_values(self):
        player = Player("Investor")
        prop = Property("Boardwalk", 39, 400, 50)
        player.add_property(prop)

        self.assertEqual(player.net_worth(), player.balance + 400)


class GameTests(unittest.TestCase):
    """Tests for branch-heavy game rules and edge conditions."""

    def test_buy_property_allows_exact_balance(self):
        game = Game(["A", "B"])
        buyer = game.players[0]
        prop = game.board.get_property_at(1)
        buyer.balance = prop.price

        bought = game.buy_property(buyer, prop)

        self.assertTrue(bought)
        self.assertEqual(prop.owner, buyer)
        self.assertEqual(buyer.balance, 0)

    def test_pay_rent_transfers_to_owner(self):
        game = Game(["A", "B"])
        tenant = game.players[0]
        owner = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = owner
        owner.add_property(prop)
        tenant_start = tenant.balance
        owner_start = owner.balance
        rent = prop.get_rent()

        game.pay_rent(tenant, prop)

        self.assertEqual(tenant.balance, tenant_start - rent)
        self.assertEqual(owner.balance, owner_start + rent)

    def test_trade_transfers_property_and_cash(self):
        game = Game(["A", "B"])
        seller = game.players[0]
        buyer = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = seller
        seller.add_property(prop)
        seller_start = seller.balance
        buyer_start = buyer.balance

        ok = game.trade(seller, buyer, prop, 100)

        self.assertTrue(ok)
        self.assertEqual(prop.owner, buyer)
        self.assertNotIn(prop, seller.properties)
        self.assertIn(prop, buyer.properties)
        self.assertEqual(seller.balance, seller_start + 100)
        self.assertEqual(buyer.balance, buyer_start - 100)

    def test_jail_fine_branch_deducts_player_balance(self):
        game = Game(["A", "B"])
        player = game.players[0]
        player.in_jail = True
        player.jail_turns = 0
        start_balance = player.balance

        with patch("moneypoly.game.ui.confirm", return_value=True), patch(
            "moneypoly.game.Dice.roll", return_value=4
        ), patch.object(game, "_move_and_resolve"):
            game._handle_jail_turn(player)

        self.assertFalse(player.in_jail)
        self.assertEqual(player.balance, start_balance - 50)

    def test_find_winner_uses_highest_net_worth(self):
        game = Game(["A", "B"])
        game.players[0].balance = 1200
        game.players[1].balance = 2000

        winner = game.find_winner()

        self.assertEqual(winner.name, "B")


if __name__ == "__main__":
    unittest.main()
