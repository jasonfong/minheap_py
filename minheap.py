import math


class MinHeapError(Exception):
    pass


class MinHeap(object):
    """Implementation of a min-heap.

    You should probably use heapq if you want a min-heap.
    But here's what you could do if you wanted to do it yourself.

    Min-heap data is contained in a complete binary tree represented
    as an array. Organization of the array is from root level to leaf
    level, with each level's nodes listed left to right.

    Values stored are floats. Inputs are accepted as either a number or
    a string that can be parsed to a float.

    Navigating through the tree structure is done by calculating
    array indexes to find the parent or children nodes.

    Attributes:
        debug: A boolean indicating if debug output should be printed out.
    """

    def __init__(self, debug=False):
        """Creates an empty min-heap.

        Creates a new min-heap with an empty data array.
        Optionally enable a debug mode that will output details of operations.

        Args:
            debug: A boolean indicating if debug output should be printed out.

        Returns:
            A new empty min-heap.
        """
        self.debug = debug
        self.data = []

    def clear(self):
        """Clears the contents of the min-heap.

        Returns:
            None
        """
        self.data = []

    def push(self, value):
        """Adds a value or a list of values to the min-heap.

        Adds one or more values to the min-heap and maintains
        node organization properties of a min-heap. Values should be able
        to be converted to a float.

        Args:
            value: A single value or a list of values.

        Returns:
            None

        Raises:
            ValueError: Pushed value could not be converted to a float.
        """
        if isinstance(value, list):
            for item in value:
                self.push(item)
        else:
            insert_val = float(value)
            if self.debug:
                print "pushing value: %s" % insert_val

            self.data.append(insert_val)
            self._bubble_up(len(self.data) - 1)

    def pop(self):
        """Removes and returns the minimum value from the min-heap.

        Removes and returns the minimum value from the min-heap. If multiple
        copies of the minimum value exists in the min-heap, only one will be
        removed. Maintains node organization properties of a min-heap.

        Returns:
            The minimum value in the min-heap.
        """
        size = len(self.data)

        if size == 0:
            raise MinHeapError("Heap is empty")

        if size == 1:
            return self.data.pop()

        last_idx = size - 1
        self._swap(0, last_idx)
        value = self.data.pop()

        self._bubble_down(0)

        return value

    def _get_parent_idx(self, idx):
        if idx == 0:
            raise MinHeapError("Root node has no parent")

        return (idx - 1) // 2

    def _get_left_idx(self, idx):
        return (2 * idx) + 1

    def _get_right_idx(self, idx):
        return (2 * idx) + 2

    def _get_value(self, idx):
        if len(self.data) - 1 < idx:
            return None

        return self.data[idx]

    def _set_value(self, idx, value):
        if len(self.data) - 1 < idx:
            raise MinHeapError("Node does not exist")

        self.data[idx] = value

    def _swap(self, idx1, idx2):
        temp = self._get_value(idx1)
        self._set_value(idx1, self._get_value(idx2))
        self._set_value(idx2, temp)

    def _bubble_up(self, idx):
        """Move a node up to its proper position in a min-heap.

        Swaps the node at index idx with its parent node if the value of the
        node at idx is less than the value of the parent node. If the nodes
        were swapped, repeat this on the parent node.

        Use this to maintain the min-heap property after a node is pushed
        into the min-heap and added to the bottom of the tree.

        Returns:
            None
        """
        if self.debug:
            print str(self)
            print "bubbling up index: %s" % idx

        if idx == 0:
            return

        parent_idx = self._get_parent_idx(idx)

        if self._get_value(idx) < self._get_value(parent_idx):
            self._swap(idx, parent_idx)
            self._bubble_up(parent_idx)

    def _bubble_down(self, idx):
        """Move a node down to its proper position in a min-heap.

        Swaps the node at index idx with its smaller child node if the value
        of the node at idx is greater than the value of the smaller child node.
        If the nodes were swapped, repeat this on the smaller child node.

        Use this to maintain the min-heap property after the root (minimum)
        value is popped and the last node is moved to the root.

        Returns:
            None
        """
        if self.debug:
            print str(self)
            print "bubbling down index: %s" % idx

        left_idx = self._get_left_idx(idx)
        right_idx = self._get_right_idx(idx)

        left_val = self._get_value(left_idx)
        right_val = self._get_value(right_idx)

        if left_val is None and right_val is None:
            return

        if right_val is None or left_val < right_val:
            smaller_idx = left_idx
            smaller_val = left_val
        else:
            smaller_idx = right_idx
            smaller_val = right_val

        value = self._get_value(idx)

        if value > smaller_val:
            self._swap(idx, smaller_idx)
            self._bubble_down(smaller_idx)

    def __str__(self):
        """Create a string representation of the min-heap.

        The string representation is in the form of left-aligned
        outputs of the values of nodes in each level of the tree.

        Returns:
            String representation of the min-heap.
        """
        if len(self.data) == 0:
            return ""

        size = len(self.data)
        height = int(math.log(size, 2))
        output_lines = []

        for layer in range(height + 1):
            start_idx = (2 ** layer) - 1
            end_idx = (2 ** (layer + 1)) - 1
            values = " ".join([str(x) for x in self.data[start_idx:end_idx]])
            output_lines.append(values)

        output_lines.insert(0, '-----')
        output_lines.append('-----')

        return "\n".join(output_lines)
