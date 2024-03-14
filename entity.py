from dataclasses import dataclass, field


@dataclass
class Node:
    level: int
    name: str
    is_child: bool
    has_child: bool = field(default=False)


@dataclass
class Tree:
    nodes: list[Node] = field(default_factory=list)
    level_settings: dict[int:int] = field(default_factory=dict)
