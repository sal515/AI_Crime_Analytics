class vertices:

    def __init__(self, node_a, node_b) -> None:
        self.node_a = node_a
        self.node_b = node_b

    def __eq__(self, other):
        return (self.node_b == other.node_b) and (self.node_a == other.node_a)
