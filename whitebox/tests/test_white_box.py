"""White-box tests for branch, state, and edge-case coverage in MoneyPoly."""

import unittest
from unittest.mock import patch

from moneypoly.config import GO_SALARY, INCOME_TAX_AMOUNT, JAIL_FINE, LUXURY_TAX_AMOUNT
from moneypoly.bank import Bank
from moneypoly.board import Board
from moneypoly.cards import CardDeck
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


class BankWhiteBoxTests(unittest.TestCase):
    """Covers if/else and normal paths in Bank methods."""

    def test_collect_negative_amount_is_ignored(self):
        bank = Bank()
        start_balance = bank.get_balance()

        bank.collect(-100)

        self.assertEqual(bank.get_balance(), start_balance)

    def test_collect_positive_amount_is_added(self):
        bank = Bank()
        start_balance = bank.get_balance()

        bank.collect(200)

        self.assertEqual(bank.get_balance(), start_balance + 200)

    def test_pay_out_negative_amount_returns_zero(self):
        bank = Bank()
        start_balance = bank.get_balance()

        paid = bank.pay_out(-10)

        self.assertEqual(paid, 0)
        self.assertEqual(bank.get_balance(), start_balance)

    def test_pay_out_normal_amount_reduces_funds(self):
        bank = Bank()
        start_balance = bank.get_balance()

        paid = bank.pay_out(300)

        self.assertEqual(paid, 300)
        self.assertEqual(bank.get_balance(), start_balance - 300)

    def test_pay_out_raises_when_amount_exceeds_funds(self):
        bank = Bank()

        with self.assertRaises(ValueError):
            bank.pay_out(bank.get_balance() + 1)

    def test_give_loan_negative_amount_is_ignored(self):
        bank = Bank()
        player = Player("LoanEdge")
        start_bank = bank.get_balance()
        start_player = player.balance

        bank.give_loan(player, -50)

        self.assertEqual(bank.get_balance(), start_bank)
        self.assertEqual(player.balance, start_player)
        self.assertEqual(bank.loan_count(), 0)

    def test_give_loan_normal_amount_updates_player_and_bank(self):
        bank = Bank()
        player = Player("LoanNormal")
        start_bank = bank.get_balance()
        start_player = player.balance

        bank.give_loan(player, 400)

        self.assertEqual(bank.get_balance(), start_bank - 400)
        self.assertEqual(player.balance, start_player + 400)
        self.assertEqual(bank.loan_count(), 1)
        self.assertEqual(bank.total_loans_issued(), 400)


class PlayerWhiteBoxTests(unittest.TestCase):
    """Covers movement, arithmetic guards, and net-worth state transitions."""

    def test_move_awards_salary_when_passing_go(self):
        player = Player("Mover")
        player.position = 39
        start_balance = player.balance

        new_position = player.move(2)

        self.assertEqual(new_position, 1)
        self.assertEqual(player.balance, start_balance + GO_SALARY)

    def test_move_without_wrap_does_not_award_salary(self):
        player = Player("Walker")
        player.position = 5
        start_balance = player.balance

        player.move(3)

        self.assertEqual(player.position, 8)
        self.assertEqual(player.balance, start_balance)

    def test_add_money_rejects_negative_amount(self):
        player = Player("SafeAdder")

        with self.assertRaises(ValueError):
            player.add_money(-1)

    def test_net_worth_includes_property_values(self):
        player = Player("Investor")
        prop = Property("Boardwalk", 39, 400, 50)
        player.add_property(prop)

        self.assertEqual(player.net_worth(), player.balance + 400)


class PropertyWhiteBoxTests(unittest.TestCase):
    """Covers rent-branch and ownership-group branch behavior."""

    def test_full_group_ownership_doubles_rent(self):
        owner = Player("Owner")
        group = PropertyGroup("Brown", "brown")
        p1 = Property("Mediterranean Avenue", 1, 60, 2, group)
        p2 = Property("Baltic Avenue", 3, 60, 4, group)
        p1.owner = owner
        p2.owner = owner

        self.assertEqual(p1.get_rent(), 4)

    def test_partial_group_ownership_does_not_double_rent(self):
        owner = Player("Owner")
        group = PropertyGroup("Brown", "brown")
        p1 = Property("Mediterranean Avenue", 1, 60, 2, group)
        p2 = Property("Baltic Avenue", 3, 60, 4, group)
        p1.owner = owner

        # Only one property in the group is owned, so rent should not be doubled
        self.assertEqual(p1.get_rent(), 2)

    def test_mortgaged_property_has_zero_rent(self):
        prop = Property("Test Lane", 1, 100, 10)
        prop.is_mortgaged = True

        self.assertEqual(prop.get_rent(), 0)


class BoardWhiteBoxTests(unittest.TestCase):
    """Covers branch behavior in board tile and purchasable checks."""

    def setUp(self):
        self.board = Board()

    def test_get_property_at_returns_property_when_found(self):
        prop = self.board.get_property_at(1)

        self.assertIsNotNone(prop)
        self.assertEqual(prop.name, "Mediterranean Avenue")

    def test_get_property_at_returns_none_when_missing(self):
        prop = self.board.get_property_at(0)

        self.assertIsNone(prop)

    def test_get_tile_type_returns_special_for_special_tile(self):
        self.assertEqual(self.board.get_tile_type(0), "go")

    def test_get_tile_type_returns_property_for_property_tile(self):
        self.assertEqual(self.board.get_tile_type(1), "property")

    def test_get_tile_type_returns_blank_for_unknown_tile(self):
        self.assertEqual(self.board.get_tile_type(12), "blank")

    def test_is_purchasable_false_when_position_has_no_property(self):
        self.assertFalse(self.board.is_purchasable(0))

    def test_is_purchasable_false_when_property_is_mortgaged(self):
        prop = self.board.get_property_at(1)
        prop.is_mortgaged = True

        self.assertFalse(self.board.is_purchasable(1))

    def test_is_purchasable_false_when_property_is_owned(self):
        prop = self.board.get_property_at(1)
        prop.owner = Player("Owner")

        self.assertFalse(self.board.is_purchasable(1))

    def test_is_purchasable_true_when_unowned_and_not_mortgaged(self):
        prop = self.board.get_property_at(1)
        prop.owner = None
        prop.is_mortgaged = False

        self.assertTrue(self.board.is_purchasable(1))

    def test_is_special_tile_true_and_false_paths(self):
        self.assertTrue(self.board.is_special_tile(0))
        self.assertFalse(self.board.is_special_tile(1))


class CardDeckWhiteBoxTests(unittest.TestCase):
    """Covers draw/peek branch paths for empty and non-empty decks."""

    def test_draw_returns_none_when_deck_empty(self):
        deck = CardDeck([])

        self.assertIsNone(deck.draw())

    def test_draw_cycles_cards_in_order(self):
        cards = [
            {"description": "A", "action": "collect", "value": 10},
            {"description": "B", "action": "pay", "value": 5},
        ]
        deck = CardDeck(cards)

        first = deck.draw()
        second = deck.draw()
        third = deck.draw()

        self.assertEqual(first["description"], "A")
        self.assertEqual(second["description"], "B")
        self.assertEqual(third["description"], "A")

    def test_peek_returns_none_when_deck_empty(self):
        deck = CardDeck([])

        self.assertIsNone(deck.peek())

    def test_peek_does_not_advance_index(self):
        cards = [{"description": "Only", "action": "collect", "value": 10}]
        deck = CardDeck(cards)

        peeked = deck.peek()
        drawn = deck.draw()

        self.assertEqual(peeked["description"], "Only")
        self.assertEqual(drawn["description"], "Only")

    def test_cards_remaining_reports_expected_count_before_cycle(self):
        cards = [
            {"description": "A", "action": "collect", "value": 10},
            {"description": "B", "action": "pay", "value": 5},
            {"description": "C", "action": "collect", "value": 20},
        ]
        deck = CardDeck(cards)

        self.assertEqual(deck.cards_remaining(), 3)
        deck.draw()
        self.assertEqual(deck.cards_remaining(), 2)


class GameWhiteBoxTests(unittest.TestCase):
    """Covers decision-heavy game flow branches and state updates."""

    def setUp(self):
        self.game = Game(["A", "B", "C"])
        self.p1 = self.game.players[0]
        self.p2 = self.game.players[1]
        self.p3 = self.game.players[2]

    def test_buy_property_fails_when_insufficient_balance(self):
        prop = self.game.state.board.get_property_at(1)
        self.p1.balance = prop.price - 1

        bought = self.game.buy_property(self.p1, prop)

        self.assertFalse(bought)
        self.assertIsNone(prop.owner)

    def test_play_turn_jailed_player_path_advances_turn(self):
        self.p1.in_jail = True

        with patch.object(self.game, "_handle_jail_turn") as jail_turn:
            self.game.play_turn()

        jail_turn.assert_called_once_with(self.p1)
        self.assertEqual(self.game.current_index, 1)
        self.assertEqual(self.game.turn_number, 1)

    def test_play_turn_three_doubles_branch_sends_player_to_jail(self):
        self.game.state.dice.doubles_streak = 3

        with patch.object(self.game.state.dice, "roll", return_value=5), patch.object(
            self.game.state.dice, "describe", return_value="2 + 3 = 5"
        ), patch.object(self.game, "_move_and_resolve") as move_resolve:
            self.game.play_turn()

        self.assertTrue(self.p1.in_jail)
        move_resolve.assert_not_called()
        self.assertEqual(self.game.current_index, 1)

    def test_play_turn_doubles_branch_keeps_same_player(self):
        with patch.object(self.game.state.dice, "roll", return_value=6), patch.object(
            self.game.state.dice, "describe", return_value="3 + 3 = 6"
        ), patch.object(self.game.state.dice, "is_doubles", return_value=True), patch.object(
            self.game, "_move_and_resolve"
        ) as move_resolve:
            self.game.play_turn()

        move_resolve.assert_called_once_with(self.p1, 6)
        self.assertEqual(self.game.current_index, 0)

    def test_play_turn_normal_branch_advances_turn(self):
        with patch.object(self.game.state.dice, "roll", return_value=5), patch.object(
            self.game.state.dice, "describe", return_value="2 + 3 = 5"
        ), patch.object(self.game.state.dice, "is_doubles", return_value=False), patch.object(
            self.game, "_move_and_resolve"
        ) as move_resolve:
            self.game.play_turn()

        move_resolve.assert_called_once_with(self.p1, 5)
        self.assertEqual(self.game.current_index, 1)

    def test_buy_property_allows_exact_balance(self):
        prop = self.game.state.board.get_property_at(1)
        self.p1.balance = prop.price

        bought = self.game.buy_property(self.p1, prop)

        self.assertTrue(bought)
        self.assertEqual(prop.owner, self.p1)
        self.assertEqual(self.p1.balance, 0)

    def test_handle_property_tile_unowned_buy_branch(self):
        prop = self.game.state.board.get_property_at(1)

        with patch("builtins.input", return_value="b"), patch.object(
            self.game, "buy_property"
        ) as buy_property:
            self.game._handle_property_tile(self.p1, prop)

        buy_property.assert_called_once_with(self.p1, prop)

    def test_handle_property_tile_unowned_auction_branch(self):
        prop = self.game.state.board.get_property_at(1)

        with patch("builtins.input", return_value="a"), patch.object(
            self.game, "auction_property"
        ) as auction_property:
            self.game._handle_property_tile(self.p1, prop)

        auction_property.assert_called_once_with(prop)

    def test_handle_property_tile_unowned_skip_branch(self):
        prop = self.game.state.board.get_property_at(1)

        with patch("builtins.input", return_value="s"), patch.object(
            self.game, "buy_property"
        ) as buy_property, patch.object(self.game, "auction_property") as auction_property:
            self.game._handle_property_tile(self.p1, prop)

        buy_property.assert_not_called()
        auction_property.assert_not_called()

    def test_handle_property_tile_owned_by_self_branch(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p1

        with patch.object(self.game, "pay_rent") as pay_rent:
            self.game._handle_property_tile(self.p1, prop)

        pay_rent.assert_not_called()

    def test_handle_property_tile_owned_by_other_branch(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p2

        with patch.object(self.game, "pay_rent") as pay_rent:
            self.game._handle_property_tile(self.p1, prop)

        pay_rent.assert_called_once_with(self.p1, prop)

    def test_pay_rent_skips_mortgaged_property(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p2
        prop.is_mortgaged = True
        p1_start = self.p1.balance
        p2_start = self.p2.balance

        self.game.pay_rent(self.p1, prop)

        self.assertEqual(self.p1.balance, p1_start)
        self.assertEqual(self.p2.balance, p2_start)

    def test_pay_rent_transfers_money_to_owner(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p2
        rent = prop.get_rent()
        p1_start = self.p1.balance
        p2_start = self.p2.balance

        self.game.pay_rent(self.p1, prop)

        self.assertEqual(self.p1.balance, p1_start - rent)
        self.assertEqual(self.p2.balance, p2_start + rent)

    def test_pay_rent_returns_when_owner_is_none(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = None
        p1_start = self.p1.balance

        self.game.pay_rent(self.p1, prop)

        self.assertEqual(self.p1.balance, p1_start)

    def test_trade_fails_if_seller_is_not_owner(self):
        prop = self.game.state.board.get_property_at(1)

        ok = self.game.trade(self.p1, self.p2, prop, 100)

        self.assertFalse(ok)

    def test_trade_fails_if_buyer_cannot_afford_cash(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p1
        self.p1.add_property(prop)
        self.p2.balance = 20

        ok = self.game.trade(self.p1, self.p2, prop, 100)

        self.assertFalse(ok)
        self.assertEqual(prop.owner, self.p1)

    def test_trade_success_updates_owner_lists_and_balances(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p1
        self.p1.add_property(prop)
        p1_start = self.p1.balance
        p2_start = self.p2.balance

        ok = self.game.trade(self.p1, self.p2, prop, 100)

        self.assertTrue(ok)
        self.assertEqual(prop.owner, self.p2)
        self.assertNotIn(prop, self.p1.properties)
        self.assertIn(prop, self.p2.properties)
        self.assertEqual(self.p1.balance, p1_start + 100)
        self.assertEqual(self.p2.balance, p2_start - 100)

    def test_mortgage_property_fails_when_not_owner(self):
        prop = self.game.state.board.get_property_at(1)

        ok = self.game.mortgage_property(self.p1, prop)

        self.assertFalse(ok)

    def test_mortgage_property_fails_when_already_mortgaged(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p1
        prop.is_mortgaged = True

        ok = self.game.mortgage_property(self.p1, prop)

        self.assertFalse(ok)

    def test_mortgage_property_success_branch(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p1
        start_balance = self.p1.balance

        ok = self.game.mortgage_property(self.p1, prop)

        self.assertTrue(ok)
        self.assertTrue(prop.is_mortgaged)
        self.assertEqual(self.p1.balance, start_balance + prop.mortgage_value)

    def test_unmortgage_property_fails_when_not_owner(self):
        prop = self.game.state.board.get_property_at(1)

        ok = self.game.unmortgage_property(self.p1, prop)

        self.assertFalse(ok)

    def test_unmortgage_property_fails_when_not_mortgaged(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p1

        ok = self.game.unmortgage_property(self.p1, prop)

        self.assertFalse(ok)

    def test_unmortgage_property_fails_when_insufficient_balance(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p1
        prop.is_mortgaged = True
        self.p1.balance = 1

        ok = self.game.unmortgage_property(self.p1, prop)

        self.assertFalse(ok)

    def test_unmortgage_property_success_branch(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p1
        prop.is_mortgaged = True
        cost = int(prop.mortgage_value * 1.1)
        self.p1.balance = 1000
        start_balance = self.p1.balance

        ok = self.game.unmortgage_property(self.p1, prop)

        self.assertTrue(ok)
        self.assertFalse(prop.is_mortgaged)
        self.assertEqual(self.p1.balance, start_balance - cost)

    def test_auction_property_no_bids_branch(self):
        prop = self.game.state.board.get_property_at(1)

        with patch("moneypoly.game.ui.safe_int_input", side_effect=[0, 0, 0]):
            won = self.game.auction_property(prop)

        self.assertFalse(won)
        self.assertIsNone(prop.owner)

    def test_auction_property_negative_bids_are_treated_as_pass(self):
        prop = self.game.state.board.get_property_at(1)

        with patch("moneypoly.game.ui.safe_int_input", side_effect=[-10, -1, 0]):
            won = self.game.auction_property(prop)

        self.assertFalse(won)
        self.assertIsNone(prop.owner)

    def test_auction_property_returns_false_when_no_active_players(self):
        prop = self.game.state.board.get_property_at(1)
        self.game.players = []

        won = self.game.auction_property(prop)

        self.assertFalse(won)
        self.assertIsNone(prop.owner)

    def test_auction_property_with_winner_branch(self):
        prop = self.game.state.board.get_property_at(1)
        start_bank = self.game.state.bank.get_balance()

        with patch(
            "moneypoly.game.ui.safe_int_input",
            side_effect=[5, 100, self.p3.balance + 1000],
        ):
            won = self.game.auction_property(prop)

        self.assertTrue(won)
        self.assertEqual(prop.owner, self.p2)
        self.assertIn(prop, self.p2.properties)
        self.assertEqual(self.game.state.bank.get_balance(), start_bank + 100)

    def test_handle_jail_turn_uses_get_out_of_jail_card_branch(self):
        self.p1.in_jail = True
        self.p1.get_out_of_jail_cards = 1

        with patch("moneypoly.game.ui.confirm", return_value=True), patch.object(
            self.game.state.dice, "roll", return_value=6
        ), patch.object(self.game, "_move_and_resolve") as move_resolve:
            self.game._handle_jail_turn(self.p1)

        self.assertFalse(self.p1.in_jail)
        self.assertEqual(self.p1.get_out_of_jail_cards, 0)
        move_resolve.assert_called_once_with(self.p1, 6)

    def test_handle_jail_turn_pay_fine_branch(self):
        self.p1.in_jail = True
        self.p1.jail_turns = 0
        start_balance = self.p1.balance

        with patch("moneypoly.game.ui.confirm", return_value=True), patch.object(
            self.game.state.dice, "roll", return_value=4
        ), patch.object(self.game, "_move_and_resolve") as move_resolve:
            self.game._handle_jail_turn(self.p1)

        self.assertFalse(self.p1.in_jail)
        self.assertEqual(self.p1.balance, start_balance - JAIL_FINE)
        move_resolve.assert_called_once_with(self.p1, 4)

    def test_handle_jail_turn_mandatory_release_after_third_turn(self):
        self.p1.in_jail = True
        self.p1.jail_turns = 2
        start_balance = self.p1.balance

        with patch("moneypoly.game.ui.confirm", return_value=False), patch.object(
            self.game.state.dice, "roll", return_value=3
        ), patch.object(self.game, "_move_and_resolve") as move_resolve:
            self.game._handle_jail_turn(self.p1)

        self.assertFalse(self.p1.in_jail)
        self.assertEqual(self.p1.jail_turns, 0)
        self.assertEqual(self.p1.balance, start_balance - JAIL_FINE)
        move_resolve.assert_called_once_with(self.p1, 3)

    def test_handle_jail_turn_no_action_and_stays_jailed_before_third_turn(self):
        self.p1.in_jail = True
        self.p1.jail_turns = 0

        with patch("moneypoly.game.ui.confirm", return_value=False), patch.object(
            self.game, "_move_and_resolve"
        ) as move_resolve:
            self.game._handle_jail_turn(self.p1)

        self.assertTrue(self.p1.in_jail)
        self.assertEqual(self.p1.jail_turns, 1)
        move_resolve.assert_not_called()

    def test_move_and_resolve_income_tax_branch(self):
        self.p1.position = 3
        start_player_balance = self.p1.balance
        start_bank_balance = self.game.state.bank.get_balance()

        self.game._move_and_resolve(self.p1, 1)

        self.assertEqual(self.p1.position, 4)
        self.assertEqual(self.p1.balance, start_player_balance - INCOME_TAX_AMOUNT)
        self.assertEqual(
            self.game.state.bank.get_balance(),
            start_bank_balance + INCOME_TAX_AMOUNT,
        )

    def test_move_and_resolve_luxury_tax_branch(self):
        self.p1.position = 37
        start_player_balance = self.p1.balance
        start_bank_balance = self.game.state.bank.get_balance()

        self.game._move_and_resolve(self.p1, 1)

        self.assertEqual(self.p1.position, 38)
        self.assertEqual(self.p1.balance, start_player_balance - LUXURY_TAX_AMOUNT)
        self.assertEqual(self.game.state.bank.get_balance(), start_bank_balance + LUXURY_TAX_AMOUNT)

    def test_move_and_resolve_go_to_jail_branch(self):
        self.p1.position = 29

        self.game._move_and_resolve(self.p1, 1)

        self.assertTrue(self.p1.in_jail)
        self.assertEqual(self.p1.position, 10)

    def test_move_and_resolve_free_parking_branch(self):
        self.p1.position = 19
        start_balance = self.p1.balance

        self.game._move_and_resolve(self.p1, 1)

        self.assertEqual(self.p1.position, 20)
        self.assertEqual(self.p1.balance, start_balance)

    def test_move_and_resolve_chance_branch_draws_and_applies_card(self):
        self.p1.position = 6
        chance_card = {"description": "Test", "action": "collect", "value": 10}

        with patch.object(
            self.game.state.chance_deck, "draw", return_value=chance_card
        ) as draw_card, patch.object(self.game, "_apply_card") as apply_card:
            self.game._move_and_resolve(self.p1, 1)

        draw_card.assert_called_once()
        apply_card.assert_called_once_with(self.p1, chance_card)

    def test_move_and_resolve_community_chest_branch_draws_and_applies_card(self):
        self.p1.position = 16
        chest_card = {"description": "Test", "action": "pay", "value": 10}

        with patch.object(
            self.game.state.community_deck, "draw", return_value=chest_card
        ) as draw_card, patch.object(self.game, "_apply_card") as apply_card:
            self.game._move_and_resolve(self.p1, 1)

        draw_card.assert_called_once()
        apply_card.assert_called_once_with(self.p1, chest_card)

    def test_move_and_resolve_railroad_branch_with_no_property_object(self):
        self.p1.position = 4

        with patch.object(self.game, "_handle_property_tile") as handle_tile:
            self.game._move_and_resolve(self.p1, 1)

        handle_tile.assert_not_called()

    def test_move_and_resolve_property_branch_calls_property_handler(self):
        self.p1.position = 0

        with patch.object(self.game, "_handle_property_tile") as handle_tile:
            self.game._move_and_resolve(self.p1, 1)

        handle_tile.assert_called_once()

    def test_apply_card_move_to_pass_go_and_resolve_property(self):
        self.p1.position = 39
        start_balance = self.p1.balance
        card = {"description": "Move", "action": "move_to", "value": 1}

        with patch.object(self.game, "_handle_property_tile") as handle_tile:
            self.game._apply_card(self.p1, card)

        self.assertEqual(self.p1.position, 1)
        self.assertEqual(self.p1.balance, start_balance + GO_SALARY)
        handle_tile.assert_called_once()

    def test_apply_card_none_branch(self):
        start_balance = self.p1.balance

        self.game._apply_card(self.p1, None)

        self.assertEqual(self.p1.balance, start_balance)

    def test_apply_card_collect_branch(self):
        card = {"description": "Collect", "action": "collect", "value": 25}
        start_balance = self.p1.balance

        self.game._apply_card(self.p1, card)

        self.assertEqual(self.p1.balance, start_balance + 25)

    def test_apply_card_pay_branch(self):
        card = {"description": "Pay", "action": "pay", "value": 30}
        start_balance = self.p1.balance

        self.game._apply_card(self.p1, card)

        self.assertEqual(self.p1.balance, start_balance - 30)

    def test_apply_card_jail_branch(self):
        card = {"description": "Jail", "action": "jail", "value": 0}

        self.game._apply_card(self.p1, card)

        self.assertTrue(self.p1.in_jail)
        self.assertEqual(self.p1.position, 10)

    def test_apply_card_jail_free_branch(self):
        card = {"description": "JailFree", "action": "jail_free", "value": 0}
        start_cards = self.p1.get_out_of_jail_cards

        self.game._apply_card(self.p1, card)

        self.assertEqual(self.p1.get_out_of_jail_cards, start_cards + 1)

    def test_apply_card_move_to_non_property_branch(self):
        card = {"description": "Move", "action": "move_to", "value": 10}

        with patch.object(self.game, "_handle_property_tile") as handle_tile:
            self.game._apply_card(self.p1, card)

        self.assertEqual(self.p1.position, 10)
        handle_tile.assert_not_called()

    def test_apply_card_birthday_only_collects_from_players_with_enough_balance(self):
        self.p2.balance = 5
        self.p3.balance = 100
        start_p1 = self.p1.balance
        start_p2 = self.p2.balance
        start_p3 = self.p3.balance
        card = {"description": "Birthday", "action": "birthday", "value": 10}

        self.game._apply_card(self.p1, card)

        self.assertEqual(self.p2.balance, start_p2)
        self.assertEqual(self.p3.balance, start_p3 - 10)
        self.assertEqual(self.p1.balance, start_p1 + 10)

    def test_apply_card_collect_from_all_branch(self):
        self.p2.balance = 100
        self.p3.balance = 100
        start_p1 = self.p1.balance
        card = {
            "description": "CollectAll",
            "action": "collect_from_all",
            "value": 15,
        }

        self.game._apply_card(self.p1, card)

        self.assertEqual(self.p2.balance, 85)
        self.assertEqual(self.p3.balance, 85)
        self.assertEqual(self.p1.balance, start_p1 + 30)

    def test_check_bankruptcy_non_bankrupt_branch(self):
        players_before = list(self.game.players)

        self.game._check_bankruptcy(self.p1)

        self.assertEqual(self.game.players, players_before)

    def test_check_bankruptcy_eliminates_player_and_resets_index(self):
        prop = self.game.state.board.get_property_at(1)
        prop.owner = self.p3
        prop.is_mortgaged = True
        self.p3.add_property(prop)
        self.p3.balance = 0
        self.game.current_index = 2

        self.game._check_bankruptcy(self.p3)

        self.assertNotIn(self.p3, self.game.players)
        self.assertIsNone(prop.owner)
        self.assertFalse(prop.is_mortgaged)
        self.assertEqual(self.game.current_index, 0)

    def test_find_winner_returns_none_when_no_players(self):
        self.game.players.clear()

        winner = self.game.find_winner()

        self.assertIsNone(winner)

    def test_find_winner_returns_highest_net_worth_player(self):
        # Give p2 the highest net worth via balance
        self.p1.balance = 100
        self.p2.balance = 500
        self.p3.balance = 300

        winner = self.game.find_winner()

        self.assertEqual(winner, self.p2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
