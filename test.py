from __future__ import annotations

import csv
from typing import Any, Optional

from python_ta.contracts import check_contracts


# @check_contracts - We are commenting this out, so it doesn't slow down the code for Part 2.2
class Tree:
    """A recursive tree data structure.
    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.
        If root is None, the tree is empty.
        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all('ex2_part2.py', config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'random'],
        'allowed-io': ['build_decision_tree', 'get_user_input', 'run_animal_guesser']
    })