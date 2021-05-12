"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log
import random
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            tree = ""
            if node is not None:
                tree += recurse(node.right, level + 1)
                tree += "| " * level
                tree += str(node.data) + "\n"
                tree += recurse(node.left, level + 1)
            return tree

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root

        while node is not None:
            if item == node.data:
                return node.data

            if item < node.data:
                node = node.left
            else:
                node = node.right

        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        node = self._root
        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            while node is not None:
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break

                    node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right is None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(self._size + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        match_elements = []

        def find_match_elements(curr_node, low, high):
            if curr_node:
                find_match_elements(curr_node.left, low, high)

                if low <= curr_node.data <= high:
                    match_elements.append(curr_node.data)

                find_match_elements(curr_node.right, low, high)

        find_match_elements(self._root, low, high)
        return match_elements

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = []
        for node in self:
            nodes.append(node)

        self.clear()

        nodes.sort()

        def create_tree(nodes_list):
            if nodes_list:
                mid = len(nodes_list) // 2

                self.add(nodes_list[mid])
                create_tree(nodes_list[:mid])
                create_tree(nodes_list[mid + 1:])

        create_tree(nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def find_successor(curr_node, item, successor_value):
            if curr_node:
                if item < curr_node.data:
                    return find_successor(curr_node.left, item, curr_node.data)
                elif item > curr_node.data:
                    return find_successor(curr_node.right, item, successor_value)
                else:
                    if curr_node.right:
                        curr_node = curr_node.right
                        while curr_node:
                            successor_value = curr_node.data
                            curr_node = curr_node.left

                    return successor_value

            else:
                return successor_value

        return find_successor(self._root, item, None)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def find_predecessor(curr_node, item, predecessor_value):
            if curr_node:
                if item < curr_node.data:
                    return find_predecessor(curr_node.left, item, predecessor_value)
                elif item > curr_node.data:
                    return find_predecessor(curr_node.right, item, curr_node.data)
                else:
                    if curr_node.left:
                        curr_node = curr_node.left
                        while curr_node:
                            predecessor_value = curr_node.data
                            curr_node = curr_node.right

                    return predecessor_value

            else:
                return predecessor_value

        return find_predecessor(self._root, item, None)

    def demo_bst(self, path_to_file):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        # select 10000 random words
        total_number = 10000
        number_to_select = 1000
        words = []
        with open(path_to_file, 'r', encoding='utf-8') as file:
            for row in file:
                words.append(row[:-1])

        words = random.sample(words, total_number)
        random_words = random.sample(words, number_to_select)
        print('Calculating time for array search...')
        # 1st type of search
        array_time_start = time.time()
        for word in random_words:
            if word in words:
                continue
        array_time = time.time() - array_time_start
        print(array_time)

        print('Calculating time for binary search (sorted words)...')
        # 2st type of search
        for word in words:
            self.add(word)

        binary_sorted_time_start = time.time()
        for word in random_words:
            if word in self:
                continue
        binary_sorted_time = time.time() - binary_sorted_time_start
        print(binary_sorted_time)

        self.clear()

        print('Calculating time for binary search (random words)...')
        # 3st type of search
        mixed_words = random.sample(words, len(words))
        for word in mixed_words:
            self.add(word)
        binary_time_start = time.time()
        for word in random_words:
            if word in self:
                continue
        binary_time = time.time() - binary_time_start
        print(binary_time)
        self.clear()

        print('Calculating time for binary search (after rebalance)...')
        # 4st type of search
        for word in words:
            self.add(word)
        self.rebalance()

        binary_balance_time_start = time.time()
        for word in random_words:
            if word in self:
                continue
        binary_balance_time = time.time() - binary_balance_time_start
        print(binary_balance_time)


if __name__ == '__main__':
    bst = LinkedBST()
    bst.demo_bst('words.txt')
