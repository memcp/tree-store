class TreeStore:
    def __init__(self, items):
        self.items = items
        self.root = items[0]
        self.root_id = self.root.get("id")
        self.tree = self.as_tree()

    def get_all(self):
        return self.items

    def get_item(self, id):
        return self.items[id - 1]

    def get_children(self, id):
        children = []
        self.traversal_for_children(self.tree, self.root_id, id, children)
        return children

    def get_all_parents(self, id):
        parents = [self.root]
        try:
            self.traversal_for_parents(self.tree, self.root_id, id, parents)
        except StopIteration:
            pass

        return list(reversed(parents))

    def traversal_for_children(self, tree, parent_id, target_id, res):
        children = tree.get(parent_id).get("children")

        if not children:
            return

        for node_id, node in children.items():
            node_value = node.get("value")
            if node_value.get("parent") == target_id:
                res.append(node_value)
            self.traversal_for_children(children, node_id, target_id, res)

    def traversal_for_parents(self, tree, parent_id, target_id, res):
        children = tree.get(parent_id).get("children")

        if not children:
            res.pop()
            return

        for node_id, node in children.items():
            node_value = node.get("value")

            if node_id == target_id:
                raise StopIteration

            res.append(node_value)
            self.traversal_for_parents(children, node_id, target_id, res)

        res.pop()

    def build_tree(self, tree, parent_id, nodes):
        children = [n for n in nodes if n["parent"] == parent_id]

        for child in children:
            tree[parent_id]["children"][child["id"]] = {"value": child, "children": {}}
            self.build_tree(tree[parent_id].get("children"), child["id"], nodes)

    def as_tree(self):
        tree = {self.root.get("id"): {"value": self.root, "children": {}}}
        self.build_tree(tree, self.root_id, self.items[self.root_id :])
        return tree
