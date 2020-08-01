"""
implementinglazy_deletion_using_multiple_inheritance.py

Created by Jas Lau on 8/3/19.
Copyright © 2019 Jas Lau. All rights reserved.

"""
import copy


# ========================== Client As Main Functions ========================


def main():
    """ test the TheSdTree  class """
    # instantiate a "data" tree of strings
    database_tree = TheSdDataTree(str)

    # print("Starting tree empty? " + str(database_tree.empty()))

    database_tree.add_child_to_cur("ABC bank")
    database_tree.find("ABC bank")
    database_tree.add_child_to_cur("employees")
    database_tree.add_child_to_cur("departments")
    database_tree.find_in_cur_subtree("employees")
    database_tree.add_child_to_cur("profile")
    database_tree.find_in_cur_subtree("profile")
    database_tree.add_child_to_cur("employee id")
    database_tree.add_child_to_cur("employee name")
    database_tree.find_in_cur_subtree("employee name")
    database_tree.add_child_to_cur("first name")
    database_tree.add_child_to_cur("last name")
    database_tree.find_in_cur_subtree("first name")
    database_tree.add_child_to_cur("Farrell")
    database_tree.find("employee name")
    database_tree.find_in_cur_subtree("last name")
    database_tree.add_child_to_cur("Andy")
    database_tree.find("employee id")
    database_tree.add_child_to_cur("1028")
    # add children in department
    database_tree.find("departments")
    database_tree.add_child_to_cur("department name")
    database_tree.add_child_to_cur("jobs")
    database_tree.add_child_to_cur("location")

    database_tree.find_in_cur_subtree("department name")
    database_tree.add_child_to_cur("GMD")
    # add children to jobs
    database_tree.find("jobs")
    database_tree.add_child_to_cur("job title")
    # job title
    database_tree.find_in_cur_subtree("job title")
    database_tree.add_child_to_cur("associate")

    # add children to location
    database_tree.find("location")
    database_tree.add_child_to_cur("US")
    database_tree.add_child_to_cur("Latin America")
    database_tree.add_child_to_cur("Asia")
    database_tree.add_child_to_cur("Europe")

    database_tree.find_in_cur_subtree("US")
    database_tree.add_child_to_cur("California")
    database_tree.find_in_cur_subtree("California")
    database_tree.add_child_to_cur("Los Angeles")

    print("\n------------ Original Tree --------------- \n", database_tree)

    # test of deep copy and soft deletion
    my_copy = copy.deepcopy(database_tree)

    # remove some parts from original
    database_tree.remove("employee id")
    database_tree.remove("Los Angeles")
    database_tree.remove("Europe")

    print("\n----------- Virtual Tree ------------ \n", database_tree)
    print("\n----------- Physical Tree ------------ \n",
          database_tree.str_physical())

    print("\n------- Testing Sizes (compare with above) ------ \n")
    print("\nvirtual size:", database_tree.size())
    print("\nphysical size:", database_tree.size_physical())

    print("\n------------ Collecting Garbage ------------ \n")
    print("found soft-deleted nodes?", database_tree.collect_garbage())
    print("immediate collect again?", database_tree.collect_garbage())
    print("-------- Hard Display after Garbage Collection ----------\n",
          database_tree.str_physical())


# ======================= End Of Client As Main Functions ====================

# =========================== Begin TheTreeNode Class ========================


class TheTreeNode:
    """ TheTreeNode class for a TheTree - not designed for
       general clients, so no accessors or exception raising """

    # constructor
    def __init__(self, sib=None, first_child=None, prev=None, root=None):
        # instance attributes
        self.sib, self.first_child, self.prev, self.my_root = sib, \
                                                              first_child, \
                                                              prev, root

    # stringizer
    def __str__(self):
        return "(generic tree node)"


# =========================== End Of TheTreeNode Class =======================

# ============================= Begin TheTree Class ==========================


class TheTree:
    """ TheTree is our base class for a data-filled general trees """

    # static constant helpers for stringizer
    BLANK_STRING = "                                    "
    BLANK_STR_LEN = len(BLANK_STRING)

    # constructor
    def __init__(self):
        self.clear()

    # accessors
    def empty(self):
        """Check if it is empty()."""
        return self.size() == 0

    def size(self):
        """Get the size."""
        return self.m_size

    # current pointer mutators
    def reset_cur(self):
        """Reset current pointer."""
        self.current = self.m_root

    def set_cur(self, tree_node):
        """Set current.
        Args:
            tree_node: Node to be set

        Returns:
            True for valid type and in tree. False otherwise.
        """
        if not self.valid_node_in_tree(tree_node):
            self.current = None
            return False
        # else
        self.current = tree_node
        return True

    # tree mutators
    def clear(self):
        self.m_root = None
        self.m_size = 0
        self.reset_cur()

    def remove_node_rec(self, node_to_delete):
        """Node_to_delete points to node in tree to be removed (along
        w/entire  subtree). Deletes children recursively
          errors handled by caller (remove_at_cur()).
        Args:
            node_to_delete: Node to be deleted
        """

        ntd = node_to_delete  # alias for shorter lines
        # remove all the children of this node (need loop unfortunately)
        while ntd.first_child:
            self.remove_node_rec(ntd.first_child)

        # we have a non-null prev pointer
        # either it has a left sib ...
        if ntd.prev.sib == node_to_delete:
            ntd.prev.sib = node_to_delete.sib
        # ... or it's the first_child of some parent
        else:
            ntd.prev.first_child = ntd.sib

        # deal with a possible right sib
        if ntd.sib is not None:
            ntd.sib.prev = ntd.prev

        # node is now out of the tree (Python will g.c. if appropriate)
        # wipe the fields to prevent client from doing harm
        ntd.first_child, ntd.prev, ntd.sib, ntd.my_root = None, None, None, None

        # finally, update tree size
        self.m_size -= 1

    def remove_at_cur(self):
        """Calls remove_node() passing cur, and resets cur handles all
        errors here to avoid repetition in rec call.

        Returns:
            True for successfully removed. False otherwise.

        """

        ntd = self.current  # saves cur so we can reset early
        self.reset_cur()  # no matter what, we'll return fresh cur

        # bad current or empty tree
        if not self.valid_node_in_tree(ntd) or self.size() == 0:
            return False

        # deleting root?
        if ntd.prev is None:
            self.clear()
            return True

        # since we know this node is in tree, call will succeed
        self.remove_node_rec(ntd)
        return True

    def add_child_node_to_cur(self, to_add=None):
        """Push node_to_add as new first child of parent.

        Args:
            to_add: Node to be added

        Returns:
            Return None (error) or ref to newly created node expect parent
            == None IFF tree is empty.
        """

        if not self.valid_node_to_add(to_add):
            return False

        # empty tree
        if self.m_size == 0:
            self.m_root = to_add
            self.m_root.my_root = self.m_root
            self.m_size = 1
            self.reset_cur()  # for empty tree we ignore what cur *was*
            return True

        if not self.valid_node_in_tree(self.current):
            return False

        # "push" new_node as the head of the sibling list; adjust all ptrs
        # notice "None": any "subtree: hanging off to_add, is trimmed

        cur = self.current  # for brevity...
        ta = to_add  # ... of next block

        ta.sib, ta.first_child, ta.prev, ta.my_root = cur.first_child, None,\
                                                      cur, self.m_root
        cur.first_child = ta
        if ta.sib is not None:
            ta.sib.prev = ta
        self.m_size += 1
        return True

    # stringizers
    def __str__(self):
        ret_str = "Tree: \n" + self.str_recurse(
            self.m_root, 0) + "- End of Tree -\n"

        return ret_str

    def str_recurse(self, tree_node, level=0):
        """Recursive tree stringizer (with indentation) for subtree with
        root tree_node in this instance's tree

        Args:
            tree_node: Tree
            level: Level of tree

        Returns:
            String of an entire Tree.

        """

        ret_str = ""

        # multi-purpose termination:  error, None or not-in-self
        if not self.valid_node_in_tree(tree_node):
            return ret_str

        # stop runaway indentation, otherwise set indent for this level
        if level > self.BLANK_STR_LEN - 1:
            return self.BLANK_STRING + " ...... "

        # this call's node
        indent = self.BLANK_STRING[0:level]
        ret_str += (indent * 3 + "-" + str(tree_node) + "\n")

        # recurse over children
        ret_str += self.str_recurse(tree_node.first_child, level + 1)

        # recurse over siblings
        if level > 0:
            ret_str += self.str_recurse(tree_node.sib, level)

        return ret_str

    # helpers
    def valid_node_to_add(self, am_i_valid):
        """ insists that node is an TheTreeNode """
        return isinstance(am_i_valid, TheTreeNode)

    def valid_node_in_tree(self, am_i_valid):
        """Insists that node is an TheTreeNode AND in this tree
        Args:
            am_i_valid: node to be examined

        Returns:

        """
        return isinstance(am_i_valid, TheTreeNode) and (
                    am_i_valid.my_root is self.m_root)


# ============================= End Of TheTree Class =========================


# ========================= Begin TheDataTreeNode Class ======================


class TheDataTreeNode(TheTreeNode):
    """ TheDataTreeNode subclass of TheTreeNode. It is the node class for a
    data tree.
   Requires data item, x, be vetted by client (TheDataTree) """

    # constructor
    def __init__(self, x, sib=None, first_child=None, prev=None, root=None):
        # first chain to base class
        super().__init__(sib, first_child, prev, root)

        # added attribute
        self.data = x

    # stringizer(s)
    # ultimate client, main(), can provide data stringizer if needed
    def __str__(self):
        return str(self.data)


# ========================= End Of TheDataTreeNode Class =====================


# =========================== Begin TheDataTree Class ========================


class TheDataTree(TheTree):
    """ TheDataTree subclass of TheTree """
    # default type is string
    DEFAULT_TYPE = type("")

    # constructor
    def __init__(self, tree_type=None):
        super().__init__()
        self.set_tree_type(tree_type)

    # current pointer mutators
    def find(self, x):
        """Looks for x in entire tree.

        Args:
            x:

        Returns:
            If found and valid, current will point to it and return T,
            else current None and return F (all done by find_rec())
        """

        self.reset_cur()
        return self.find_in_cur_subtree(x)

    def find_in_cur_subtree(self, x):
        """Looks for x in subtree rooted at self.current.

        Args:
            x: Node

        Returns:
            If x valid and found, current will point to it and return T,
            else current None and return F
        """

        if not self.current or not self.valid_data(x):
            return False

        return self.find_rec(x, self.current) is not None

    def find_rec(self, x, root):
        """Recursively search for x in subtree rooted at root.
         x and current vetted by non-recursive originator
        Args:
            x: Node
            root: Tree

        Returns:
            If found, current set to node and returned, else current/return
            = None.
        """
        # default current if all recursive calls fail
        self.current = None

        # not found (in this sub-search)
        if not root:
            return None

        # found (current will survive all higher-level calls)
        if root.data == x:
            self.current = root
            return root

        # recurse children
        child = root.first_child
        while child:
            test_result = self.find_rec(x, child)
            if test_result:
                return test_result
            child = child.sib

        return None

    # tree mutators
    def set_tree_type(self, the_type):
        # make sure it's a subclass of type
        if isinstance(the_type, type):
            self.tree_type = the_type
        else:
            self.tree_type = self.DEFAULT_TYPE

    def remove(self, x):
        """Looks for x in entire tree.

        Args:
            x: Node to be removed

        Returns:
            If the node is valid and is found, remove node, return T (cur
            reset by base call, remove_at_cur()). else curr = None and return F

        """

        self.current = None  # prepare for not found or error return
        if self.size() == 0 or (not self.valid_data(x)):
            return False

        found_node = self.find_rec(x, self.m_root)
        if not found_node:
            return False

        # found x
        self.current = found_node
        self.remove_at_cur()  # not overriden, so base call
        return True

    def add_child_to_cur(self, x):
        """Calls base add_child_node_to_cur(). no change to cur
        Args:
            x: Current node

        Returns:
            Return super().add_child_node_to_cur if valid. False for otherwise.

        """
        if not self.valid_data(x):
            return False

        new_node = TheDataTreeNode(x)
        return super().add_child_node_to_cur(new_node)

    # helpers
    def valid_data(self, am_i_valid):
        """Validate the type of tree.
        Args:
            am_i_valid: Current tree

        Returns:
            True for valid. False otherwise.

        """
        return isinstance(am_i_valid, self.tree_type)


# ========================== End Of TheDataTree Class ========================


# ========================== Begin TheSdTreeNode Class ========================


class TheSdTreeNode(TheTreeNode):
    """ TheSdTreeNode class for a TheSdTree - adds dltd flag """

    # initializer ("constructor") method ------------------------
    def __init__(self, sib=None, first_child=None, prev=None, root=None,
                 dltd=False):
        super().__init__(sib, first_child, prev, root)
        # subclass instance attributes
        self.dltd = dltd


# ========================= End Of TheSdTreeNode Class =======================


# ============================ Begin TheSdTree Class =========================


class TheSdTree(TheTree):
    """ TheSdTree, derived from TheTree, is our base class for lazy deletion
      general trees """

    # constructor
    # inherited
    # accessors
    def empty(self):
        """Overridden method to call new size() since m_size is physical.
        Returns: True if size is 0. False otherwise.

        """
        return self.size() == 0

    def size_physical(self):
        """New name for base class size() method.

        Returns:
            Size of all nodes, included deleted node.

        """
        return super().size()

    def size(self):
        """Overridden method to compute the size.

        Returns:
            Size of tree

        """
        return self.size_rec(self.m_root)

    def size_rec(self, tree_node, level=0):
        """Recursively computes size of subtree with root tree_node.

        Args:
            tree_node: Tree
            level: Level of tree

        Returns:
            Size of tree

        """
        if not self.m_root or not tree_node:
            return 0

        sib_size, count_this, children_size = 0, 0, 0
        # count siblings
        if level > 0:
            sib_size = self.size_rec(tree_node.sib, level)

        # a deleted node cuts off its entire subtree
        if not tree_node.dltd:
            children_size = self.size_rec(tree_node.first_child, level + 1)
            count_this = 1

        return children_size + sib_size + count_this

    # current pointer mutators
    # reset_cur() inherited

    def set_cur(self, tree_node):
        """Overridden method to test for soft deleted node.

        Args:
            tree_node: Current node

        Returns:
            True for valid node in tree or soft deleted. False for otherwise.

        """
        if not self.valid_node_in_tree(tree_node) or tree_node.dltd:
            self.current = None
            return False
        # else
        self.current = tree_node
        return True

    # tree mutators
    # clear() inherited

    def collect_garbage(self):
        """Physically deletes all marked nodes in tree.
          True if anything removed, False if not."""
        return self.collect_garbage_rec(self.m_root)

    def collect_garbage_rec(self, tree_node):
        """Recursively deletes all marked nodes in subtree tree_node.

        Args:
            tree_node: Soft deleted tree node

        Returns:
            True for successfully deleted. False for otherwise.

        """
        if not self.m_root or not tree_node:
            return False

        sib_result, this_result, children_result = False, False, False

        # collect sib garbage (must do before root removed)
        sib_result = self.collect_garbage_rec(tree_node.sib)
        if tree_node.dltd:
            self.remove_node_rec(tree_node)  # will remove all children
            this_result = True
        else:
            # if root not deleted, must remove children manually
            children_result = self.collect_garbage_rec(tree_node.first_child)

        # if anything was deleted, return True
        return sib_result or children_result or this_result;

    # remove_node_rec() inherited

    def remove_at_cur(self):
        """Overridden method to mark self.current's del flag and chk current
        dltd
        but if this is the root node, we can do a physical clear()

        Returns:
            True for successfully deleted. False otherwise.

        """

        ntd = self.current  # saves cur so we can reset early
        self.reset_cur()  # no matter what, we'll return fresh cur

        # bad current, empty tree or already soft deleted
        if not self.valid_node_in_tree(ntd) or (self.size() == 0) or ntd.dltd:
            return False

        # deleting root?  we will do total gc and start fresh
        if ntd.prev is None:
            self.clear()
            return True

        # don't need recursive helper in this method - just soft delete
        ntd.dltd = True
        return True

    def add_child_node_to_cur(self, to_add=None):
        """Overridden method to make sure to_add goes in non-deleted.
        Args:
            to_add: Node to be added

        Returns:
            If the node to be added is valid, return super(). Return False
            otherwise.

        """

        # be sure  to_add is lazy-delection type
        if not self.valid_node_to_add(to_add):
            return False

        to_add.dltd = False  # just in case del flag was True
        return super().add_child_node_to_cur(to_add)

    # stringizers
    # __str__() inherited

    def str_recurse(self, tree_node, level=0):
        """Overridden method to skip soft deleted nodes and their children.
        Args:
            tree_node: Node to be added
            level: Level of tree

        Returns:
            String of an entire tree without printing soft deleted node.

        """
        ret_str = ""

        # multi-purpose termination:  error, None or not-in-self
        if not self.valid_node_in_tree(tree_node):
            return ret_str

        # stop runaway indentation, otherwise set indent for this level
        if level > self.BLANK_STR_LEN - 1:
            return self.BLANK_STRING + " ... "

        # this call's node
        if not tree_node.dltd:
            indent = self.BLANK_STRING[0:level]
            ret_str += (indent * 3 + "-" + str(tree_node) + "\n")

            # recurse over children
            ret_str += self.str_recurse(tree_node.first_child, level + 1)

        # recurse over siblings
        if level > 0:
            ret_str += self.str_recurse(tree_node.sib, level)

        return ret_str

    def str_physical(self):
        """
        Client version of new stringizer showing dltd nodes.

        Returns:
            String of an entire tree included soft deleted node.

        """
        ret_str = "Physical Tree (including soft-deleted nodes):\n" + \
                  self.str_recurse_phys(
                      self.m_root, 0) + "---------- End of Tree --------\n"

        return ret_str

    def str_recurse_phys(self, tree_node, level=0):
        """Like old str_recurse, but with (D) tag added

        Args:
            tree_node: Node to be added
            level: Level of tree

        Returns:
            String of an entire tree included soft deleted node.

        """
        ret_str = ""

        # multi-purpose termination:  error, None or not-in-self
        if not self.valid_node_in_tree(tree_node):
            return ret_str

        # stop runaway indentation, otherwise set indent for this level
        if level > self.BLANK_STR_LEN - 1:
            return self.BLANK_STRING + " ... "
        indent = self.BLANK_STRING[0:level]

        # this call's node
        if not tree_node.dltd:
            ret_str += (indent * 3 + "-" + str(tree_node) + "\n")
        else:
            ret_str += (indent * 3 + "-" + str(tree_node) + " (D)\n")

        # recurse over children
        ret_str += self.str_recurse_phys(tree_node.first_child, level + 1)

        # recurse over siblings
        if level > 0:
            ret_str += self.str_recurse_phys(tree_node.sib, level)

        return ret_str

    # helpers
    def valid_node_to_add(self, am_i_valid):
        """Check if the type of node is valid.

        Args:
            am_i_valid: Current node

        Returns:
            True for type is valid. False for otherwise.

        """
        return isinstance(am_i_valid, TheSdTreeNode)

    def valid_node_in_tree(self, am_i_valid):
        """Check if the node is a valid in tree.

        Args:
            am_i_valid: Current node

        Returns:
            True for type is valid and is in tree. False for otherwise.

        """
        return isinstance(am_i_valid, TheSdTreeNode) and (
                am_i_valid.my_root is self.m_root)


# ============================ Enf Of TheSdTree Class ========================

# ======================== Begin TheDataTreeNode Class =======================


class TheSdDataTreeNode(TheDataTreeNode, TheSdTreeNode):
    """TheDataTreeNode subclass of TheTreeNode.
    It is the node class for a data tree.
    Requires data item, x, be vetted by client (TheDataTree)
    """

    # constructor
    def __init__(self, x, sib=None, first_child=None, prev=None, root=None,
                 dltd=False):
        # first chain to base class
        TheDataTreeNode.__init__(self, x, sib, first_child, prev, root)
        TheSdTreeNode.__init__(self, dltd=dltd)

    # stringizer(s)
    # ultimate client, main(), can provide data stringizer if needed
    def __str__(self):
        return str(self.data)


# ======================== End of TheDataTreeNode Class ======================

# ========================= Begin TheSdDataTree Class ========================


class TheSdDataTree(TheSdTree, TheDataTree):
    """ TheDataTree subclass of TheTree """
    # default type is string
    DEFAULT_TYPE = type("")

    # constructor
    def __init__(self, tree_type=None):
        TheSdTree.__init__(self)
        TheDataTree.__init__(self, tree_type)

    def find_in_cur_subtree(self, x):
        """Look for x in subtree rooted at self.current.
        Args:
            x:
            Search key

        Returns:
            If x valid and found, current will point to it and return T,
           otherwise current None and return F
        """
        if not self.current or not self.valid_data(x):
            return False

        return self.find_rec(x, self.current) is not None

    def find_rec(self, x, root):
        """Recursively search for x in subtree rooted at root.
        x and current vetted by non-recursive originator.

        Args:
            x: Search key
            root: Tree

        Returns:
            If found, current set to node and returned. Return None otherwise.
        """
        # default current if all recursive calls fail
        self.current = None

        # not found (in this sub-search)
        if not root:
            return None

        # found (current will survive all higher-level calls)
        # if node has not been soft delete, visit the child, else, don't visit
        if root.dltd is False:
            if root.data == x:
                self.current = root
                return root

            # recurse children
            child = root.first_child
            while child:
                test_result = self.find_rec(x, child)
                if test_result:
                    return test_result
                child = child.sib
        return None

    def add_child_to_cur(self, x):
        """Calls base add_child_node_to_cur(). no change to cur

        Args:
            x: Child to be added

        Returns:
            self.add_child_node_to_cur(new_node) if x is valid. False
            otherwise.

        """
        if not self.valid_data(x):
            return False

        new_node = TheSdDataTreeNode(x)
        return self.add_child_node_to_cur(new_node)


# ========================= End of TheSdDataTree Class ========================

# ============================== Main Program ================================


if __name__ == "__main__":
    main()
