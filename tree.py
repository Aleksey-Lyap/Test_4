import re

from const import (
    ALLOW_TOKEN,
    DIGIT_WITH_SPACE,
    EXC_MSG,
    LEFT_BRACKET,
    RIGTH_BRACKET,
    WHITESPICE,
    WITHOUT_DIGIT,
    WITHOUT_LEFT_BRACKET,
)
from entity import Node, Tree
from errors import WrongFormatError

NODE_COUNT_PER_LEVEL = {}


def check_allow_prev_token(
    prev_token: str, cur_token: str, re_expr: re.Pattern
) -> None:
    if not re_expr.match(prev_token):
        raise Exception(EXC_MSG.format(cur_token=cur_token, prev_token=prev_token))


def build_tree(tokens: list[str]) -> Tree:
    prev_token = tokens[0]
    level = 1
    tree = Tree()

    if prev_token != LEFT_BRACKET:
        raise Exception('Первый токен должен быть "(". Текущий токен ' + tokens[0])

    for cur_token in tokens[1:]:
        if cur_token == LEFT_BRACKET:
            check_allow_prev_token(prev_token, cur_token, DIGIT_WITH_SPACE)
            level += 1

        elif cur_token == RIGTH_BRACKET:
            check_allow_prev_token(prev_token, cur_token, WITHOUT_LEFT_BRACKET)
            if level < 1:
                raise WrongFormatError("Неверный порядок скобок")
            level -= 1

        elif cur_token == WHITESPICE:
            prev_token = cur_token
            continue

        else:
            check_allow_prev_token(prev_token, cur_token, WITHOUT_DIGIT)

            is_child = False
            if tree.nodes:
                if tree.nodes[-1].level < level:
                    tree.nodes[-1].has_child = True
                if tree.level_settings.get(level - 1):
                    is_child = True

            tree.nodes.append(Node(level=level, name=cur_token, is_child=is_child))
            lvl_setting = tree.level_settings.get(level)

            if lvl_setting and len(cur_token) > lvl_setting:
                tree.level_settings[level] = len(cur_token)
            elif not lvl_setting:
                tree.level_settings[level] = len(cur_token)

            NODE_COUNT_PER_LEVEL[level] = NODE_COUNT_PER_LEVEL.get(level, 0) + 1

        prev_token = cur_token
    return tree


def print_tree(tree: Tree) -> None:
    prev_lvl = 1
    last_pos = 0
    prefix_dict = {}

    for index, node in enumerate(tree.nodes):
        level_postfix_ident = tree.level_settings[node.level]
        postfix = (
            "-" * (level_postfix_ident - len(node.name)) + "---+"
            if node.has_child
            else ""
        )

        if node.level in prefix_dict:
            prefix = prefix_dict[node.level]

        elif node.level > tree.nodes[index + 1].level + 1:
            prefix = prefix_dict[node.level - tree.nodes[index + 1].level]

        elif node.is_child and NODE_COUNT_PER_LEVEL[prev_lvl] >= 2:
            prefix = (
                prefix_dict[prev_lvl]
                + "|"
                + " " * (last_pos - len(prefix_dict[prev_lvl] + "|"))
            )
            prefix_dict[node.level] = prefix
        else:
            prefix = " " * last_pos
            prefix_dict[node.level] = prefix

        if node.has_child:
            last_pos = len(prefix + node.name + postfix) - 1

        prev_lvl = node.level

        print(prefix + node.name + postfix)


def main():
    input_string = "(1 (2 (4 5 6 (7) 108 (9)) 3))"
    # input_string = '(1 (2 (4        )      )       6)'
    # input_string = '(2 3 (4 5 (5 7) 6) 6 (5 6))'
    tokens = ALLOW_TOKEN.findall(input_string)
    if not tokens or len(tokens) < 3:
        raise WrongFormatError("Короткая строка")
    tree = build_tree(tokens)
    print_tree(tree)


if __name__ == "__main__":
    main()
