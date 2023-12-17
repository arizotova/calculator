import operator
from typing import Callable, List, Union

SPECIAL_SYMBOLS = {'-', '+', '*', '/', '(', ')'}
UNARY_MINUS_OPERATOR_TOKEN = '±'

OPERATOR_TO_PRIORITY = {
    UNARY_MINUS_OPERATOR_TOKEN: 1,
    '+': 2,
    '-': 2,
    '*': 1,
    '/': 1
}

OPERATOR_TO_FUNCTION = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False


def is_operator(token: str) -> bool:
    return token in OPERATOR_TO_PRIORITY


def get_operator_priority(token: str) -> int:
    return OPERATOR_TO_PRIORITY[token]


def str_to_number(token: str) -> Union[int, float]:
    return float(token)


def str_to_operator(token: str) -> Callable:
    return OPERATOR_TO_FUNCTION[token]


class Calculator:
    def evaluate(self, expression: str) -> Union[int, float]:
        tokens = self._parse_expression(expression)
        rpn = self._transform_to_reverse_polish_notation(tokens)
        answer = self._evaluate_reverse_polish_notation(rpn)
        return answer

    def _parse_expression(self, expression: str) -> List[str]:
        expression = expression.replace(' ', '')
        start = None
        tokens = []
        for i in range(len(expression)):
            symbol = expression[i]
            if symbol in SPECIAL_SYMBOLS:
                if not self._is_special_symbol_position_valid(expression, symbol, i):
                    raise RuntimeError('Invalid symbol sequence encountered.')
                if start is not None:
                    numeric_token = expression[start:i]
                    if not is_number(numeric_token):
                        raise RuntimeError(f'Invalid symbol sequence encountered.')
                    tokens.append(numeric_token)
                if self._is_symbol_unary_minus(expression, symbol, i):
                    symbol = UNARY_MINUS_OPERATOR_TOKEN
                tokens.append(symbol)
                start = None
            else:
                if start is None:
                    start = i
        if start is not None:
            numeric_token = expression[start:]
            if not is_number(numeric_token):
                raise RuntimeError(f'Invalid symbol sequence encountered.')
            tokens.append(numeric_token)
        return tokens

    def _transform_to_reverse_polish_notation(self, tokens: List[str]):
        output = []
        operator_stack = []
        for token in tokens:
            if is_number(token):
                output.append(token)
            elif is_operator(token):
                while (
                        operator_stack and
                        operator_stack[-1] != '(' and
                        get_operator_priority(operator_stack[-1]) <= get_operator_priority(token)
                ):
                    op_token = operator_stack.pop()
                    output.append(op_token)
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append('(')
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    op_token = operator_stack.pop()
                    output.append(op_token)
                if not operator_stack:
                    raise RuntimeError('Invalid parenthesis sequence encountered.')
                operator_stack.pop()  # remove '(' from stack

        while operator_stack:
            if operator_stack[-1] == '(':
                raise RuntimeError('Invalid parenthesis sequence encountered.')
            output.append(operator_stack.pop())

        return output

    def _evaluate_reverse_polish_notation(self, tokens: List[str]):
        operand_stack = []
        for token in tokens:
            if is_number(token):
                operand_stack.append(token)
            elif is_operator(token):
                if token == UNARY_MINUS_OPERATOR_TOKEN:
                    right_token = operand_stack.pop()
                    right = str_to_number(right_token)
                    result = -1 * right
                else:
                    right_token = operand_stack.pop()
                    left_token = operand_stack.pop()
                    left, right = str_to_number(left_token), str_to_number(right_token)
                    op = str_to_operator(token)
                    result = op(left, right)
                operand_stack.append(result)

        answer = operand_stack.pop()
        return answer

    def _is_special_symbol_position_valid(self, expression: str, symbol: str, pos: int):
        if symbol == '(':
            if pos > 0:
                cond_1 = expression[pos - 1] in '(+-*/'
            else:
                cond_1 = True
            if pos < len(expression) - 1:
                cond_2 = expression[pos + 1] not in ')+*/'
            else:
                cond_2 = False
        elif symbol == ')':
            if pos > 0:
                cond_1 = expression[pos - 1] not in '(+-*/'
            else:
                cond_1 = False
            if pos < len(expression) - 1:
                cond_2 = expression[pos + 1] in ')+-*/'
            else:
                cond_2 = True
        else:
            if pos > 0:
                cond_1 = symbol == '-' or expression[pos - 1] not in '(+-*/'
            else:
                cond_1 = symbol == '-'
            if pos < len(expression) - 1:
                cond_2 = expression[pos + 1] not in ')+*/'
            else:
                cond_2 = False

        return cond_1 and cond_2

    def _is_symbol_unary_minus(self, expression: str, symbol: str, pos: int):
        if symbol == '-' and (pos == 0 or (pos > 0 and expression[pos - 1] in SPECIAL_SYMBOLS and expression[pos - 1] != ')')):
            return True
        return False

    def _operator_stack_is_not_empty(self, stack: List[str]):
        return len(stack) > 1 or (len(stack) == 1 and stack[0] != '(')




if __name__ == '__main__':
    calculator = Calculator()
    expression = '-4 * ((17 - -5 * 1 + 3) / 2.5) / 4'
    answer = calculator.evaluate(expression)
    assert answer == eval(expression)
