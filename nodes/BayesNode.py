# Most of the code in this file comes from PBNT by Elliot Cohen. See
# separate file in this project with PBNT license.

import itertools as it

from nodes.DirectedNode import *
import Utilities as ut


class BayesNode(DirectedNode):
    """
    A BayesNode is a DirectedNode wih additional information such as a
    Potential. A Potential is either a PD in the CBnet case, or a PAD in the
    QBnet case. abbreviations in MyConstants.py. value of node = state of node.


    Attributes
    ----------
    __active_states : list[int]
        When all states are active, use range(self.size)
    clique : Clique
        In a JoinTree, the family of any node belongs
        to exactly one clique, stored here. The family of a node
        is the node and its parents. The nodes on which a
        node's potential depends are its family.
    potential : Potential
    size : int
        number of values = number of states of node =
        size of node
    state_names : list[str]

    children : set[Node]
    neighbors : set[Node]
    parents : set[Node]
    id_num : int
    topo_index : int
    name : str
    visited : bool
    """

    def __init__(self, id_num, name="blank", size=2):
        """
        Constructor.

        Parameters
        ----------
        id_num : int
            This should be a different int for each node.
        name : str
            The name of the node. Optional.

        Returns
        -------

        """

        DirectedNode.__init__(self, id_num, name)
        self.size = size
        self.state_names = ["state" + str(k) for k in range(size)]
        self.clique = None
        self.potential = None
        self.__active_states = range(size)  # underscore to use @property

    def set_potential(self, pot):
        """

        Parameters
        ----------
        pot : Potential

        Returns
        -------
        None

        """
        self.potential = pot
        assert(pot.nd_sizes[-1] == self.size)

    def resize(self, size):
        """
        Add or remove nodes taking care to change everything that depends on
        number of nodes.

        Parameters
        ----------
        size : int

        Returns
        -------
        None

        """
        if size < self.size:
            self.state_names = self.state_names[:size]
            self.potential = None
        elif size == self.size:
            pass
        else:
            self.state_names += [
                "state" + str(k) for k in range(self.size, size)]
            self.potential = None
        self.size = size
        self.forget_all_evidence()

    def set_state_name(self, position, name):
        """
        Changes name of state of node.

        Parameters
        ----------
        position : int
        name : str

        Returns
        -------
        None

        """
        assert(0 <= position < self.size)
        self.state_names[position] = name

    def st_name_index(self, st_name):
        """
        returns index in state_names list given name

        Parameters
        ----------
        st_name : str

        Returns
        -------
        int

        """
        return self.state_names.index(st_name)

    def forget_all_evidence(self):
        """
        Expand list of self's active states to include all possible states from
        0 to size-1.

        Returns
        -------
        None

        """
        self.active_states = range(self.size)

    def get_active_states(self):
        """
        Getter for active state list.

        Returns
        -------
        list[int]

        """
        return self.__active_states

    def set_active_states(self, states):
        """
        Setter for active state list.

        Parameters
        ----------
        states : list[int]

        Returns
        -------
        None

        """
        assert(max(states) < self.size and min(states) >= 0)
        assert(len(states) >= 1)
        self.__active_states = states

    active_states = property(get_active_states, set_active_states)

    def set_state_names_to_product(self, list_of_iters, repeat=1, trim=False):
        """
        Sets state names to a sequence of tuples generate by it.product().
        trim option to remove punctuation marks.

        Parameters
        ----------
        list_of_iters : list[str] | list[list[int]]
            list of iterables like a list of one or more strings, or a list of
            one or more lists of ints
        repeat : int
            In case list_of_iters is list of single string or list of single
            list of ints, repeat them
        trim : bool
            Whether to keep punctuation or not. True removes white spaces,
            commas and parentheses
        Returns
        -------
        None

        """
        if not trim:
            bad = ''
        else:
            bad = '(,) '
        self.state_names = [ut.fix(str(t).replace("'", ''), bad, '')
            for t in it.product(*list_of_iters, repeat=repeat)]
        self.size == len(self.state_names)

# These imports are here after the class definition
# to avoid import loops.
# The idea is to define the class before these imports occur.
from potentials.Potential import *
from potentials.DiscreteCondPot import *
if __name__ == "__main__":

    a = BayesNode(0, "alice")

    def speak(k):
        print('test' + str(k) + ":", a.state_names, "\n")

    speak(1)

    a.resize(4)
    speak(2)

    a.resize(3)
    speak(3)

    a.set_state_name(2, "horse")
    speak(4)

    a.set_state_names_to_product([range(3)])
    speak(5)

    a.set_state_names_to_product([range(3)], trim=True)
    speak(5.1)

    a.set_state_names_to_product([range(3)], repeat=3)
    speak(6)

    a.set_state_names_to_product([range(3), range(2)]),
    speak(7)

    a.set_state_names_to_product(['abc'])
    speak(8)

    a.set_state_names_to_product(['abc'], trim=True)
    speak(8.1)

    a.set_state_names_to_product(['abc'], repeat=3)
    speak(9)

    a.set_state_names_to_product(['abc', 'xyz'])
    speak(10)

    a.set_state_names_to_product(['abc', 'xyz'], trim=True)
    speak(10.1)

    a.set_state_names_to_product(['01'], repeat=3, trim=True)
    speak(11)


