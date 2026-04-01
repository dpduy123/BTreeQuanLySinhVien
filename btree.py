class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = [] # list of dicts: {"key": k, "values": [v1, v2...]}
        self.children = [] # list of BTreeNode

    def to_dict(self):
        return {
            "keys": [k["key"] for k in self.keys],
            "values": [k["values"] for k in self.keys],
            "children": [child.to_dict() for child in self.children],
            "leaf": self.leaf
        }

class BTree:
    def __init__(self, order=3):
        self.root = BTreeNode(True)
        self.order = order

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]["key"]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]["key"]:
            return node.keys[i]["values"]
        elif node.leaf:
            return None
        else:
            return self._search(node.children[i], key)

    def insert(self, key, value):
        root = self.root
        
        # Check if key already exists, if so just append the value
        existing = self._search(root, key)
        if existing is not None:
            if value not in existing:
                existing.append(value)
            return

        if len(root.keys) == self.order - 1: # if full
            temp = BTreeNode(False)
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append({"key": None, "values": []})
            while i >= 0 and key < node.keys[i]["key"]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = {"key": key, "values": [value]}
        else:
            while i >= 0 and key < node.keys[i]["key"]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.order - 1:
                self._split_child(node, i)
                if key > node.keys[i]["key"]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, i):
        order = self.order
        child = parent.children[i]
        new_node = BTreeNode(child.leaf)
        
        # Mid index
        mid = (order - 1) // 2
        
        # Insert new key into parent
        parent.keys.insert(i, child.keys[mid])
        parent.children.insert(i + 1, new_node)
        
        # Split keys and children
        new_node.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]
        
        if not child.leaf:
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]

    def delete(self, key, value=None):
        # Value can be used to remove one specific item from the list of duplicates
        # If value is None, or it's the last value, we delete the key completely.
        node, i = self._find_node(self.root, key)
        if node is None:
            return # Key not found
        
        if value is not None:
            if value in node.keys[i]["values"]:
                node.keys[i]["values"].remove(value)
            if len(node.keys[i]["values"]) > 0:
                return # Still has values, don't delete key
                
        self._delete(self.root, key)
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]

    def _find_node(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]["key"]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]["key"]:
            return node, i
        elif node.leaf:
            return None, None
        else:
            return self._find_node(node.children[i], key)

    def _delete(self, node, key):
        t_min = (self.order + 1) // 2 - 1 # For order 3, t_min = 1 (wait, ceil(3/2)-1) = 2 - 1 = 1.
        # But root can have 0 keys if it delegates to children.
        # Max keys = 2.
        
        i = 0
        while i < len(node.keys) and key > node.keys[i]["key"]:
            i += 1

        if node.leaf:
            if i < len(node.keys) and node.keys[i]["key"] == key:
                node.keys.pop(i)
            return

        if i < len(node.keys) and node.keys[i]["key"] == key:
            return self._delete_internal_node(node, key, i)
        
        # key is not in node
        if len(node.children[i].keys) >= (self.order // 2): # At least 1 key if order=3
            self._delete(node.children[i], key)
        else:
            # fill child[i] which has 0 keys right now... 
            # Wait, order 3: minimum keys for internal node = ceil(3/2)-1 = 1.
            # So a node can have 1 or 2 keys. If it drops to 0, we must fill it.
            # But here `len >= self.order // 2` -> `3//2` = 1 > 0 ?
            pass
            self._fill(node, i)
            if i < len(node.keys) and key > node.keys[i]["key"]:
                self._delete(node.children[i+1], key)
            else:
                self._delete(node.children[i], key)

    def _delete_internal_node(self, node, key, i):
        if len(node.children[i].keys) >= self.order // 2 + 1: # > 1, so 2
            pred = self._get_pred(node, i)
            node.keys[i] = pred
            self._delete(node.children[i], pred["key"])
        elif len(node.children[i + 1].keys) >= self.order // 2 + 1:
            succ = self._get_succ(node, i)
            node.keys[i] = succ
            self._delete(node.children[i + 1], succ["key"])
        else:
            self._merge(node, i)
            self._delete(node.children[i], key)

    def _get_pred(self, node, i):
        curr = node.children[i]
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.keys[-1]

    def _get_succ(self, node, i):
        curr = node.children[i + 1]
        while not curr.leaf:
            curr = curr.children[0]
        return curr.keys[0]

    def _fill(self, node, i):
        if i != 0 and len(node.children[i - 1].keys) >= self.order // 2 + 1:
            self._borrow_from_prev(node, i)
        elif i != len(node.children) - 1 and len(node.children[i + 1].keys) >= self.order // 2 + 1:
            self._borrow_from_next(node, i)
        else:
            if i != len(node.children) - 1:
                self._merge(node, i)
            else:
                self._merge(node, i - 1)

    def _borrow_from_prev(self, node, i):
        child = node.children[i]
        sibling = node.children[i - 1]
        
        child.keys.insert(0, node.keys[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
            
        node.keys[i - 1] = sibling.keys.pop()

    def _borrow_from_next(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]
        
        child.keys.append(node.keys[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
            
        node.keys[i] = sibling.keys.pop(0)

    def _merge(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]
        
        child.keys.append(node.keys.pop(i))
        child.keys.extend(sibling.keys)
        
        if not child.leaf:
            child.children.extend(sibling.children)
            
        node.children.pop(i + 1)
        
    def to_dict(self):
        return self.root.to_dict()
