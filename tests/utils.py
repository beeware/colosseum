from colosseum.layout import CSSNode


class TestNode(object):
    def __init__(self, style=None, children=None):
        self.parent = None
        self._children = []
        if children:
            for child in children:
                self.add(child)

        if style:
            self._style = style.apply(self)
        else:
            self._style = CSSNode(self)

    @property
    def style(self):
        return self._style

    @property
    def children(self):
        return self._children

    def add(self, child):
        self._children.append(child)
        child.parent = self.parent
        if self.parent:
            self.parent.dirty = True
