import random
from fractions import Fraction
import re

class ExerciseGenerator:
    def __init__(self, range_num):
        self.range_num = range_num  # 数值范围
        self.generated_expressions = set()  # 用于去重的标准化表达式集合

    def generate_number(self):
        """生成自然数或真分数（含带分数）"""
        is_fraction = random.random() < 0.3
        if is_fraction:
            # 生成真分数（分子 < 分母）
            denominator = random.randint(2, self.range_num)
            numerator = random.randint(1, denominator - 1)
            # 30%概率生成带分数（整数部分+真分数）
            if random.random() < 0.3 and numerator + denominator < self.range_num:
                whole = random.randint(1, self.range_num - denominator - 1)
                return f"{whole}'{numerator}/{denominator}", Fraction(whole) + Fraction(numerator, denominator)
            return f"{numerator}/{denominator}", Fraction(numerator, denominator)
        else:
            # 生成自然数
            num = random.randint(0, self.range_num - 1)
            return str(num), Fraction(num)

    def generate_operator(self):
        operators = ['+', '-', '×', '÷']
        weights = [0.3, 0.2, 0.3, 0.2]
        return random.choices(operators, weights=weights)[0]

    # 核心修改1：完善去重逻辑（处理+、×的交换律和结合律）
    def normalize_expression(self, expr):
        """标准化表达式，解决重复问题"""
        expr = expr.replace(' ', '')
        
        # 递归处理嵌套的+和×（按结合律和交换律标准化）
        def normalize(s):
            # 处理括号（如果存在）
            if s.startswith('(') and s.endswith(')'):
                s = s[1:-1]
            
            # 先处理×（优先级高）
            mul_parts = self.split_by_operator(s, '×')
            if len(mul_parts) > 1:
                # 对×的操作数排序（交换律）
                sorted_parts = sorted([normalize(part) for part in mul_parts])
                return '×'.join(sorted_parts)
            
            # 再处理+
            add_parts = self.split_by_operator(s, '+')
            if len(add_parts) > 1:
                # 对+的操作数排序（交换律）
                sorted_parts = sorted([normalize(part) for part in add_parts])
                return '+'.join(sorted_parts)
            
            return s
        
        return normalize(expr)

    def split_by_operator(self, s, op):
        """按运算符分割表达式（忽略括号内的运算符）"""
        parts = []
        current = []
        paren_count = 0
        for c in s:
            if c == '(':
                paren_count += 1
                current.append(c)
            elif c == ')':
                paren_count -= 1
                current.append(c)
            elif paren_count == 0 and c == op:
                parts.append(''.join(current))
                current = []
            else:
                current.append(c)
        if current:
            parts.append(''.join(current))
        return parts

    # 核心修改2：限制运算符数量≤3
    def count_operators(self, expr):
        """统计表达式中运算符数量"""
        return sum(1 for c in expr if c in ['+', '-', '×', '÷'])

    def generate_expression(self, depth=0):
        # 控制递归深度，间接控制运算符数量
        if depth >= 3 or (depth > 0 and random.random() < 0.6):
            return self.generate_number()
        
        left_expr, left_val = self.generate_expression(depth + 1)
        op = self.generate_operator()
        right_expr, right_val = self.generate_expression(depth + 1)

        # 减法验证：e1 ≥ e2
        if op == '-':
            if left_val < right_val:
                return self.generate_expression(depth)
            result = left_val - right_val
        # 除法验证：结果为真分数
        elif op == '÷':
            if right_val == 0 or (left_val / right_val).numerator >= (left_val / right_val).denominator:
                return self.generate_expression(depth)
            result = left_val / right_val
        elif op == '+':
            result = left_val + right_val
        else:  # ×
            result = left_val * right_val

        # 结果范围验证
        if result < 0 or result >= self.range_num:
            return self.generate_expression(depth)

        # 拼接表达式（无括号）
        expr = f"{left_expr} {op} {right_expr}"

        # 核心修改3：验证运算符数量≤3
        if self.count_operators(expr) > 3:
            return self.generate_expression(depth)

        return expr, result

    def generate_exercises(self, count):
        exercises = []
        answers = []
        while len(exercises) < count:
            expr, result = self.generate_expression()
            # 用标准化后的表达式去重
            normalized = self.normalize_expression(expr)
            if normalized not in self.generated_expressions:
                self.generated_expressions.add(normalized)
                exercises.append(expr)
                # 格式化答案
                if result.denominator == 1:
                    answers.append(str(result.numerator))
                else:
                    if result.numerator > result.denominator:
                        whole = result.numerator // result.denominator
                        remainder = result.numerator % result.denominator
                        answers.append(f"{whole}'{remainder}/{result.denominator}")
                    else:
                        answers.append(f"{result.numerator}/{result.denominator}")
        return exercises, answers