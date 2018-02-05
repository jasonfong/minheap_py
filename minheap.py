import math


class MinHeapError(Exception):
    pass


class MinHeap(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.data = []

    def clear(self):
        self.data = []

    def push(self, value):
        if isinstance(value, list):
            for item in value:
                self.push(item)
        else:
            if self.debug:
                print "pushing value: %s" % value

            self.data.append(value)
            self._bubble_up(len(self.data) - 1)

    def pop(self):
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
