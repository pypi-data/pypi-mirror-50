from typing import Any, Callable, Generator
from loguru import logger

from pytezos.rpc.node import RpcError
from pytezos.rpc.query import RpcQuery
from pytezos.tools.docstring import get_attr_docstring
from pytezos.encoding import is_bh


def find_state_change_intervals(head: int, last: int, get: Callable, equals: Callable,
                                step=60) -> Generator:
    succ_value = get(head)

    for level in range(head - step, last, -step):
        value = get(level)
        logger.debug(f'{value} at level {level}')

        if not equals(value, succ_value):
            yield level + step, succ_value, level, value
            succ_value = value


def find_state_change(head: int, last: int, get: Callable, equals: Callable,
                      pred_value: Any) -> (int, Any):
    def bisect(start: int, end: int):
        if end == start + 1:
            return end, get(end)

        level = (end + start) // 2
        value = get(level)
        logger.debug(f'{value} at level {level}')

        if equals(value, pred_value):
            return bisect(level, end)
        else:
            return bisect(start, level)

    return bisect(last, head)


def walk_state_change_interval(head: int, last: int, get: Callable, equals: Callable,
                               head_value: Any, last_value: Any) -> Generator:
    level = last
    value = last_value
    while not equals(value, head_value):
        level, value = find_state_change(
            head, level, get, equals,
            pred_value=value)
        yield level, value


def find_state_changes(head: int, last: int, get: Callable, equals: Callable,
                       step=60) -> Generator:
    for int_head, int_head_value, int_tail, int_last_value in find_state_change_intervals(
            head, last, get, equals, step):
        for change in walk_state_change_interval(
                int_head, int_tail, get, equals,
                head_value=int_head_value,
                last_value=int_last_value):
            yield change


class BlockSliceQuery(RpcQuery):

    def __init__(self, start: int, stop=None, **kwargs):
        super(BlockSliceQuery, self).__init__(**kwargs)
        self._start = start
        self._stop = stop or 'head'

    def __repr__(self):
        res = [
            super(BlockSliceQuery, self).__repr__(),
            f'\nBlock range\n`{self._start}` — `{self._stop}`',
            f'\n(){get_attr_docstring(BlockSliceQuery, "__call__")}'
        ]
        return '\n'.join(res)

    def __call__(self) -> list:
        """
        Get block hashes (base58) for this interval
        """
        if is_bh(self._stop):
            head = self._stop
        else:
            head = self[self._stop].hash()

        if self._start < 0:
            length = abs(self._start)
        else:
            header = self[self._stop].header()
            length = header['level'] - self._start + 1

        return super(BlockSliceQuery, self).__call__(length=length, head=head)

    def get_range(self):
        """
        Get block level range.
        """
        if isinstance(self._start, int):
            last = self._start
        else:
            last = self[self._start].header()['level']

        if isinstance(self._stop, int):
            head = self._stop
        else:
            head = self[self._stop].header()['level']

        return last, head

    def find_proposal(self, proposal_id):
        """
        Find proposal injection.
        :param proposal_id: Proposal hash (base58)
        """
        last, head = self.get_range()
        level, _ = find_state_change(
            head=head,
            last=last,
            get=lambda x: self[x].votes.proposals[proposal_id](),
            equals=lambda x, y: x == y,
            pred_value=0
        )
        return self[level].operations.proposal(proposal_id)

    def find_ballots(self, proposal_id) -> Generator:
        """
        Find voting operations for the given proposal.
        :param proposal_id: Proposal hash (base58)
        :return: Generator (lazy)
        """
        last, head = self.get_range()
        for level, _ in find_state_changes(
                head=head,
                last=last,
                get=lambda x: self.blocks[x].votes.proposals[proposal_id],
                equals=lambda x, y: x == y):
            for ballot in self[level].operations.ballots(proposal_id):
                yield ballot

    def find_origination(self, contract_id):
        """
        Find contract origination
        :param contract_id: Contract ID (KT-address)
        """
        def get_counter(x):
            try:
                return self.blocks[x].context.contracts[contract_id].counter()
            except RpcError:
                return None

        level, _ = find_state_change(
            head=self.head.level(),
            last=0,
            get=get_counter,
            equals=lambda x, y: x == y,
            pred_value=None
        )
        return self[level].operations.origination(contract_id)

    def find_operation(self, operation_group_hash):
        """
        Find operation by hash
        :param operation_group_hash: base58
        :return: dict
        """
        last, head = self.get_range()
        for block_level in range(head, max(1, last - 1), -1):
            try:
                return self[block_level].operations[operation_group_hash]()
            except StopIteration:
                continue

        raise StopIteration(operation_group_hash)


class CyclesQuery(RpcQuery):

    def __call__(self, **params):
        """
        Get current cycle
        """
        return self.head.cycle()

    def __getitem__(self, item) -> BlockSliceQuery:
        """
        Get block range by cycle/cycle range.
        :param item: Cycle number or range (slice), range start/stop can be empty or negative
        :return: BlockSliceQuery
        """
        lvl = self.head.metadata()['level']
        blocks_per_cycle = int((lvl['level'] - lvl['cycle_position'] - 1) / lvl['cycle'])

        def get_range(cycle):
            if cycle > 0:
                start_lvl = (cycle - 1) * blocks_per_cycle + 1
                stop_lvl = start_lvl + blocks_per_cycle - 1
            elif cycle < 0:
                start_lvl = (lvl['cycle'] + cycle) * blocks_per_cycle + 1
                stop_lvl = None
            else:
                assert False
            return start_lvl, stop_lvl

        if isinstance(item, slice):
            start, _ = get_range(item.start or 1)
            _, stop = get_range(item.stop or -1)
        elif isinstance(item, int):
            start, stop = get_range(item)
        else:
            raise NotImplementedError(item)

        return BlockSliceQuery(
            start=start,
            stop=stop,
            node=self.node,
            path=self._path,
            params=self._params
        )
