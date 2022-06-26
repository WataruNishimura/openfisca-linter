
from typing import Optional


class Node:
    def __init__(
        self,
        path: Optional[str] = None,
        parent: Optional[Node] = None,
        obj_name: Optional[str] = None,
    ):
        self.children: list[Node] = []
        self.parent: Optional[Node] = parent
        self.path: Optional[str] = path
        # Graphviz で可視化する際のラベル
        self.obj_name: Optional[str] = obj_name
        # obj_name をルートノードから順にドットで連結したもの
        if parent is None:
            self.obj_name_full: Optional[str] = obj_name
        else:
            self.obj_name_full = (
                f"{parent.obj_name_full}.{obj_name}"
                if parent.obj_name_full is not None
                else obj_name
            )
