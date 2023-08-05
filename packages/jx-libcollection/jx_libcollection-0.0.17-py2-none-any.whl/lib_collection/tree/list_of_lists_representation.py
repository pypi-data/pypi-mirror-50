def get_binary_tree(r):
    return [r, [], []]


def insert_left(root, subtree):
    left_node = root.pop(1)
    if len(left_node) > 1:
        root.insert(1, [subtree, left_node, []])
    else:
        root.insert(1, [subtree, [], []])
    return root


def insert_right(root, subtree):
    right_node = root.pop(2)
    if len(right_node) > 1:
        root.insert(2, [subtree, [], right_node])
    else:
        root.insert(2, [subtree, [], []])
    return root


def get_root_value(root):
    return root[0]


def set_root_value(root, value):
    root[0] = value


def get_left_child(root):
    return root[1]


def get_right_child(root):
    return root[2]

r = get_binary_tree(3)
insert_left(r, 4)
insert_left(r, 5)
insert_right(r, 6)
insert_right(r, 7)


left = get_left_child(r)
print left

set_root_value(left, 9)
print r

insert_left(left, 11)
print r

print get_right_child(get_right_child(r))


class Tree(object):
    def __init__(self, v):
        self.lst = [v, [], []]

    def __len__(self):
        return 1 + len(self.lst[1]) + len(self.lst[2])

    def insert_left(self, v):
        t = Tree(v)
        if len(self.lst[1]) == 0:
            self.lst[1] = t
            return
        t.insert_left(self.lst[1])
        self.lst[1] = t

    def insert_right(self, v):
        t = Tree(v)
        if len(self.lst[2]) == 0:
            self.lst[2] = t
            return
        t.insert_right(self.lst[2])
        self.lst[2] = t

    @property
    def root_value(self):
        return self.lst[0]

    @root_value.setter
    def root_value(self, v):
        self.lst[0] = v

    @property
    def left_tree(self):
        return self.lst[1] if self.lst[1] else None

    @property
    def right_tree(self):
        return self.lst[2] if self.lst[2] else None

    def __repr__(self):
        return 'Tree({}, {}, {})'.format(self.root_value, self.left_tree, self.right_tree)


r = Tree(3)
r.insert_left(4)
r.insert_left(5)
r.insert_right(6)
r.insert_right(7)
print r.left_tree
r.left_tree.root_value = 9
print r
r.left_tree.insert_left(11)
print r
print r.right_tree.right_tree
