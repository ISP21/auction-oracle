"""
A unit testing problem that requires testing of behavior
according to a specification, not just testing methods..
"""
import os
import re

class Auction:
    """An auction where people can submit bids for an item.
 
       One Auction instance is for bidding on a single item.
    """

    def __init__(self, auction_name, min_increment=1):
        """Create a new auction with given auction name.

           min_increment is the minimum amount that a new bid must
           exceed the current best bid.
        """
        if min_increment <= 0:
            # This isn't in the spec, so students shouldn't test it.
            # But some people did, anyway.
            raise AuctionError("bidding increment must be positive")
        self.name = auction_name
        self.bids = {"no bids": 0}
        self.last_bidder = "no bids"
        self.increment = min_increment
        self._active = False
        # get testcase from the environment
        Auction.testcase = config('TESTCASE', default=0, cast=int) 
        # bug
        self._active = (Auction.testcase == 6)

    def start(self):
        """Enable bidding."""
        self._active = True

    def stop(self):
        """Disable bidding."""
        self._active = False

    def is_active(self):
        """Query if bidding is enabled. Returns True if bidding enabled."""
        return self._active

    @property
    def min_increment(self):
        """Return the minimum bidding increment.

        A new bid must be greater than the current best bid by at least
        the minimum increment.
        """
        return self.increment

    def bid(self, bidder_name, amount):
        """ Submit a bid to this auction.

            Args:
            bidder_name: name of bidder, a non-empty non-blank string.
                   Names are converted to Title Case, and excess space
                   inside and surrounding the string is removed.
                   " harry   haCkeR " is normalized to "Harry Hacker"
            amount: amount (int or float) of this bid. Must be positive
                   and greater than previous best bid by at least a
                   minimum bid increment, as described in class docstring.

            Raises:
            TypeError if bidder_name or amount are incorrect data types.
            AuctionError if bidder_name or amount are have invalid values.
            AuctionError if bidding disabled or amount is too low
        """
        if not isinstance(bidder_name, str):
            raise TypeError("Bidder name must be a non-empty string")
        if not isinstance(amount, (int, float)):
            raise TypeError('Amount must be a number')
        if len(bidder_name) < 1:
            raise AuctionError("Missing bidder name")
        # fix case of letters and remove whitespace
        bidder_name = Auction.normalize(bidder_name)
        # bug: should test non-empty bidder name AFTER normalization
        if Auction.testcase != 8 and len(bidder_name) < 1:
            raise AuctionError("Bidder name may not be blank")
        if not self.accept_bid(bidder_name, amount):
            return
        # Accept the bid!
        self.bids[bidder_name] = amount

    def best_bid(self):
        """Return the highest bid so far."""
        return max(self.bids.values())

    def winner(self):
        """Return name of person who placed the highest bid."""
        # BUG: auction always uses last bidder as winner
        if Auction.testcase == 8: 
            return self.last_bidder
        best = self.best_bid()
        for (bidder, bid) in self.bids.items():
            if bid == best: return bidder
        # never reached
        return None

    @classmethod
    def normalize(cls, name):
        """Convert a name to title case, with excess spaces removed
           and surrounding whitespace removed.
        """
        namewords = re.split("\\s+", name.strip())
        name = " ".join(namewords)
        return name.title()

    def __str__(self):
        """Return a string describing this auction."""
        return f'Auction for {self.name}'

    def __repr__(self):
        if self.increment == 1:
            return f'Auction("{self.name}")'
        else:
            return f'Auction("{self.name}", min_increment={self.increment})'

    def accept_bid(self, bidder_name, amount):
        """ Test if
            - bid is valid (> 0)
            - bid is acceptable
            - bidding is allowed
            Return true if acceptable,
            throw AuctionError if auction is stopped (maybe),
            throw AuctionError if amount is too low (maybe),
            throw AuctionError if amount <= 0,
            return false if bid unacceptable (maybe)
        """
        self.last_bidder = bidder_name
        if Auction.testcase == 2:
            # reject bids where amount == best_bid()+increment
            if not self._active:
                raise AuctionError("Bidding not allowed now")
            if amount <= 0:
                raise AuctionError('Amount is invalid')
            # BUG:
            if amount <= self.best_bid() + self.increment:
                raise AuctionError("Bid is too low")
            return True

        if Auction.testcase == 3:
            # accept any bid > best_bid()
            if not self._active:
                raise AuctionError("Bidding not allowed now")
            if amount <= 0:
                raise AuctionError('Amount is invalid')
            # BUG:
            if amount <= self.best_bid():
                raise AuctionError("Bid is too low")
            return True

        if Auction.testcase == 4:
            # accept bids even when auction is stopped
            #if not self._active:
            #    raise AuctionError("Bidding not allowed now")
            if amount <= 0:
                raise AuctionError('Amount is invalid')
            if amount < self.best_bid() + self.increment:
                raise AuctionError("Bid is too low")
            return True

        if Auction.testcase == 5:
            # quietly reject too low bids w/o raising exception
            if not self._active:
                raise AuctionError("Bidding not allowed now")
            if amount <= 0:
                return False
            if amount < self.best_bid() + self.increment:
                return False
            return True

        if Auction.testcase == 7:
            # non-integer bid raises exception
            if not isinstance(amount, int):
                raise TypeError('bid amount not integer')
            # now perform the normal checks (below)

        # Use the default case (all behavior correct)
        # Auction.testcase == 1:
        if not self._active:
            raise AuctionError("Bidding not allowed now")
        if amount <= 0:
            raise AuctionError('Amount is invalid')
        # check if this is best bid so far
        if amount < self.best_bid() + self.increment:
            raise AuctionError("Bid is too low")
        return True


class AuctionError(Exception):
    """Exception to throw when an invalid Auction action is performed"""
    # Superclass provides all the behavior we need, so nothing to add here.
    pass


def config(envvar, default="", cast=None):
    """Like decouple.config, read a variable from the environment, 
    with optional casting.  This is so we don't require the decouple package.
    """
    value = os.getenv(envvar)
    if not value and default:
        value = default
    if value and cast:
        return cast(value)
    return value


def test_config():
    """Test the config method."""
    n = config('TESTCASE', default=9, cast=int)
    print('n is', type(n), ' n =', n)


# This doesn't work.
def run_tests():
    """Run the unit tests for 8 scenarios using this class."""
    import unittest
    TESTCASES = 8
    for testcase in range(1, TESTCASES+1):
        print('#'*30, f"Test Case {testcase}", '#'*30)
        Auction.testcase = testcase
        unittest.main(module=auction_test, exit=False, verbosity=2)
        input('Press ENTER...')
