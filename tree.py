from pprint import pprint


class TreeStore:
    def __init__(self, items):
        self.items = items
        self.root = items[0]
        self.root_id = self.root.get("id")
        self.tree = self.as_tree()

    def get_all(self):
        """Список всех элементов"""
        return self.items

    def get_item(self, id):
        """Получение элементов из расчета изначальный список отсортирован и значения
        id элементов последовательны"""
        try:
            return self.items[id - 1]
        except IndexError:
            print(f"Index {id} is out of range")

    def get_children(self, id):
        """Возвращает список всех дочерних элементов, являющихся дочерними для элемента
        с указанным 'id', в случае если нет дочерних возвращает пустой список"""
        children = []
        self.traversal_for_children(self.tree, self.root_id, id, children)
        return children

    def get_all_parents(self, id):
        """Возвращает список, состоящий из цепочки родительских элементов для элемента
        с указанным 'id', последним элементом цепи будет корневой элемент дерева"""
        parents = [self.root]
        try:
            self.traversal_for_parents(self.tree, self.root_id, id, parents)
        except StopIteration:
            pass

        return list(reversed(parents))

    def traversal_for_children(self, tree, parent_id, target_id, res):
        """Рекурсивный обход дерева в глубину для поиска дочерних элементов

        Параметры

            tree - текущее поддерево
            parent_id - родитель элементов текущего уровня
            target_id - элемент у которого нужно найти дочерние, сравнивается с
                      родителем текущего уровня
            res - результирующий список с дочерними элементами
        """
        children = tree.get(parent_id).get("children")

        if not children:
            return

        for node_id, node in children.items():
            node_value = node.get("value")
            if node_value.get("parent") == target_id:
                res.append(node_value)
            self.traversal_for_children(children, node_id, target_id, res)

    def traversal_for_parents(self, tree, parent_id, target_id, res):
        """Рекурсивный обход дерева в глубину поиска цепочки родительских элементов

        Параметры
            tree - текущее поддерево
            parent_id - родитель элементов текущего уровня
            target_id - элемент у которого нужно найти дочерние, сравнивается с
                      родителем текущего уровня
            res - результирующий список с дочерними элементами
        """
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
        """Рекурсивно проходит по списку словарей и строит дерево

        Параметры

            tree - поддерево в которое будут записаны значения дочерних элементов
            parent_id - текущий id родительского элемента, служит ключом и является
                        узлом построенного дерева
            nodes - список всех элементов кроме корневого
        """
        children = [n for n in nodes if n["parent"] == parent_id]

        for child in children:
            tree[parent_id]["children"][child["id"]] = {"value": child, "children": {}}
            self.build_tree(tree[parent_id].get("children"), child["id"], nodes)

    def as_tree(self):
        """Преобразует список словарей в древовидную структуру следующего формата

        Из следующего списка:
        [
            {"id": 1, "parent": "root"},
            {"id": 2, "parent": 1, "type": "test"},
            {"id": 3, "parent": 1, "type": "test"},
        ]

        построиться дерево:
        {
            "1": {
                "value": {
                    "id": 1,
                    "parent": "root"
                },
                "children": {
                    "2": {
                        "value": {
                            "id": 2,
                            "parent": 1,
                            "type": "test"
                        },
                        "children": {}
                    },
                    "3": {
                        "value": {
                            "id": 3,
                            "parent": 1,
                            "type": "test"
                        },
                        "children": {}
                    }
                }
            }
        }
        """
        tree = {self.root.get("id"): {"value": self.root, "children": {}}}
        self.build_tree(tree, self.root_id, self.items[self.root_id :])
        return tree


def main():
    """Пример использования класса TreeStore"""

    def pprint_case(s, description):
        """Выводит случай использования функции в консоль, оборачивая названием"""
        print(f"{description}:\n")
        pprint(s)
        print("\n")

    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None},
    ]
    ts = TreeStore(items)

    pprint_case(ts.get_all(), "get_all()")
    pprint_case(ts.get_item(7), "get_item(7)")
    pprint_case(ts.get_children(4), "get_children(4)")
    pprint_case(ts.get_children(5), "get_children(5)")
    pprint_case(ts.get_all_parents(7), "get_children(5)")


main()
