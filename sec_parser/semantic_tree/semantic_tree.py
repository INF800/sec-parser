from __future__ import annotations

from typing import TYPE_CHECKING

from sec_parser.semantic_elements.semantic_elements import IrrelevantElement

if TYPE_CHECKING:  # pragma: no cover
    from sec_parser.semantic_elements.abstract_semantic_element import (
        AbstractSemanticElement,
    )
    from sec_parser.semantic_tree.tree_node import TreeNode

DEFAULT_MAX_LINE_LENGTH = 50


class SemanticTree:
    def __init__(self, root_nodes: list[TreeNode]) -> None:
        self.root_nodes = root_nodes

    def render(
        self,
        *,
        pretty: bool | None = True,
        ignored_types: tuple[type[AbstractSemanticElement], ...] | None = None,
        max_line_length: int | None = None,
        _nodes: list[TreeNode] | None = None,
        _level: int = 0,
        _prefix: str = "",
        _is_root: bool = True,
    ) -> str:
        """
        render function is used to visualize the structure of the semantic tree.
        It is primarily used for debugging purposes.
        """
        pretty = pretty if pretty is not None else True
        ignored_types = ignored_types or (IrrelevantElement,)
        max_line_length = (
            max_line_length
            if max_line_length and max_line_length > 0
            else DEFAULT_MAX_LINE_LENGTH
        )

        tree_strings = []
        _nodes = _nodes if _nodes is not None else self.root_nodes

        for i, node in enumerate(_nodes):
            element = node.semantic_element
            if isinstance(element, ignored_types):
                continue

            is_last = i == len(_nodes) - 1

            indent = "├── " if not is_last else "└── "
            new_prefix = "│   " if not is_last else "    "

            level = ""
            lvl = getattr(node.semantic_element, "level", "")
            if lvl:
                level = f"[L{lvl}]"
                if pretty:
                    level = f"\033[1;92m{level}\033[0m"
            class_name = f"{element.__class__.__name__}{level}"
            contents = element.html_tag.get_text().strip()
            if len(contents) > max_line_length:
                contents = f"{contents[:max_line_length]}..."
            if pretty:
                class_name = f"\033[1;34m{class_name}\033[0m"

            # Fix the alignment for root elements
            line = f"{_prefix}{indent}{class_name}" if not _is_root else f"{class_name}"
            if contents:
                line = f"{line}: {contents}"
            tree_strings.append(line)

            # Recursive call: Always set _is_root to False for non-root elements
            tree_strings.append(
                self.render(
                    _nodes=node.children,
                    _level=_level + 1,
                    _prefix=_prefix + (_prefix if _is_root else new_prefix),
                    pretty=pretty,
                    _is_root=False,
                ),
            )

        return "\n".join(filter(None, tree_strings))
