# -*- coding: utf-8 -*

# Copyright (C) 2018 Kin Foundation

import stellar_base.builder
from stellar_base.memo import NoneMemo

from .horizon import HORIZON_LIVE, HORIZON_TEST
from .horizon import Horizon
from .utils import validate_address, validate_seed


class Builder(stellar_base.builder.Builder):
    """
    This class overrides :class:`~stellar_base.builder` to provide additional functionality.
    """
    def __init__(self, secret=None, address=None, horizon=None, horizon_uri=None, network=None, sequence=None):
        if secret:
            validate_seed(secret)
        elif address:
            validate_address(address)
        else:
            raise Exception('either secret or address must be provided')

        # run baseclass constructor to init baseclass variables
        super(Builder, self).__init__(secret=secret, address=address, sequence=1)

        # custom overrides

        self.network = network.upper() if network else 'PUBLIC'

        if horizon:
            self.horizon = horizon
        elif horizon_uri:
            self.horizon = Horizon(horizon_uri)
        else:
            self.horizon = Horizon(HORIZON_LIVE) if self.network == 'PUBLIC' else Horizon(HORIZON_TEST)

        self.sequence = sequence if sequence else self.get_sequence()

    def clear(self):
        """"Clears the builder so it can be reused."""
        self.ops = []
        self.time_bounds = []
        self.memo = NoneMemo()
        self.fee = None
        self.tx = None
        self.te = None

    def next(self):
        """
        Alternative implementation that does not create a new builder but clears the current one and increments
        the account sequence number.
        """
        self.clear()
        self.sequence = str(int(self.sequence) + 1)

    def sign(self, secret=None):
        """
        Alternative implementation that does not use the self-managed sequence, but always fetches it from Horizon.
        """
        self.sequence = self.get_sequence()
        super(Builder, self).sign(secret)