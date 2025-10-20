import random
from fractions import Fraction
from calculator import ExpressionCalculator

class ExerciseGenerator:
    def __init__(self, range_num):
        self.range_num = range_num
        self.calculator = ExpressionCalculator()
        self.generated_expressions = set()
    
    def generate_number(self):
        """生成数字（自然数或真分数）- 表达式内部不使用带分数"""
        if random.random() < 0.3:  # 30%概率生成分数
            denominator = random.randint(2, self.range_num - 1)
            numerator = random.randint(1, denominator - 1)
            # 在表达式内部，只使用真分数，不使用带分数
            return f"{numerator}/{denominator}", Fraction(numerator, denominator)
        else:
            number = random.randint(1, self.range_num - 1)  # 从1开始，避免0
            return str(number), Fraction(number)
    
    def generate_operator(self):
        """随机生成运算符"""
        return random.choice(['+', '-', '×', '÷'])
    
    def get_operator_priority(self, operator):
        """获取运算符优先级"""
        if operator in ['×', '÷']:
            return 2
        elif operator in ['+', '-']:
            return 1
        return 0
    
    def generate_expression(self, depth=0, parent_operator=None, parent_priority=0):
        """生成表达式，只在真正必要时添加括号"""
        if depth >= 2 or (depth > 0 and random.random() < 0.6):
            num_str, num_value = self.generate_number()
            return num_str, num_value
        
        # 生成左表达式
        left_expr, left_value = self.generate_expression(depth + 1)
        operator = self.generate_operator()
        current_priority = self.get_operator_priority(operator)
        
        # 生成右表达式
        right_expr, right_value = self.generate_expression(depth + 1, operator, current_priority)
        
        # 避免无意义的运算
        if right_value == 0:
            if operator == '-' or operator == '+' or operator == '×':
                # +0, -0, ×0 都是无意义的
                return self.generate_expression(depth, parent_operator, parent_priority)
            elif operator == '÷':
                # 除以0不允许
                return self.generate_expression(depth, parent_operator, parent_priority)
        
        if left_value == 0 and operator in ['+', '-']:
            # 0+ 或 0- 也是无意义的
            return self.generate_expression(depth, parent_operator, parent_priority)
        
        # 验证表达式合法性
        if operator == '-':
            if left_value <= right_value:  # 确保被减数大于减数
                return self.generate_expression(depth, parent_operator, parent_priority)
            result = left_value - right_value
        elif operator == '÷':
            if right_value == 0:
                return self.generate_expression(depth, parent_operator, parent_priority)
            result = left_value / right_value
            # 确保结果是真分数
            if result.numerator >= result.denominator:
                return self.generate_expression(depth, parent_operator, parent_priority)
        elif operator == '+':
            result = left_value + right_value
        else:  # '×'
            result = left_value * right_value
        
        # 检查结果是否在范围内
        if result < 0 or result >= self.range_num:
            return self.generate_expression(depth, parent_operator, parent_priority)
        
        # 只在真正必要时添加括号（极少数情况）
        needs_parentheses = False
        
        # 唯一需要括号的情况：当前是减法或除法，且右表达式包含更低优先级的运算
        # 例如：a - (b + c) 或 a ÷ (b + c)
        if operator in ['-', '÷'] and '(' in right_expr and any(op in right_expr for op in ['+', '-']):
            if random.random() < 0.3:  # 即使这种情况，也只有30%概率加括号
                needs_parentheses = True
        
        # 根节点几乎不需要括号
        elif depth == 0 and random.random() < 0.05:  # 只有5%的概率在根节点加括号
            needs_parentheses = True
        
        if needs_parentheses:
            expression = f"({left_expr} {operator} {right_expr})"
        else:
            expression = f"{left_expr} {operator} {right_expr}"
        
        return expression, result
    
    def normalize_expression(self, expression):
        """标准化表达式用于去重"""
        # 移除空格
        expr = expression.replace(' ', '')
        
        # 对于加法和乘法，排序操作数（简单的去重策略）
        parts = []
        current_part = ""
        paren_count = 0
        
        for char in expr:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            
            if paren_count == 0 and char in ['+', '×']:
                parts.append(current_part)
                parts.append(char)
                current_part = ""
            else:
                current_part += char
        
        if current_part:
            parts.append(current_part)
        
        # 对可交换的运算排序
        if len(parts) == 3 and parts[1] in ['+', '×']:
            if parts[0] > parts[2]:
                parts[0], parts[2] = parts[2], parts[0]
        
        return ''.join(parts)
    
    def format_answer(self, fraction):
        """格式化答案，在输出时可以使用带分数"""
        if fraction.denominator == 1:
            return str(fraction.numerator)
        elif fraction.numerator > fraction.denominator:
            whole = fraction.numerator // fraction.denominator
            remainder = fraction.numerator % fraction.denominator
            return f"{whole}'{remainder}/{fraction.denominator}"
        else:
            return f"{fraction.numerator}/{fraction.denominator}"
    
    def count_operators(self, expression):
        """计算表达式中的运算符数量"""
        count = 0
        for char in expression:
            if char in ['+', '-', '×', '÷']:
                count += 1
        return count
    
    def is_too_simple(self, expression, operator_count):
        """检查表达式是否过于简单"""
        # 单个运算符的表达式不应该有括号
        if operator_count == 1 and '(' in expression:
            return True
        
        # 检查是否包含不必要的括号
        if expression.startswith('(') and expression.endswith(')'):
            inner = expression[1:-1]
            # 如果括号内的表达式已经很简单，就不需要括号
            inner_operator_count = self.count_operators(inner)
            if inner_operator_count <= 1:
                return True
        
        return False
    
    def generate_exercises(self, count):
        """生成指定数量的题目"""
        exercises = []
        answers = []
        
        attempts = 0
        max_attempts = count * 10  # 防止无限循环
        
        while len(exercises) < count and attempts < max_attempts:
            attempts += 1
            expression, result = self.generate_expression()
            
            # 检查运算符数量
            operator_count = self.count_operators(expression)
            if operator_count > 3 or operator_count == 0:
                continue
            
            # 检查表达式是否过于简单或不合理
            if self.is_too_simple(expression, operator_count):
                continue
            
            normalized = self.normalize_expression(expression)
            
            # 检查是否重复
            if normalized in self.generated_expressions:
                continue
            
            self.generated_expressions.add(normalized)
            exercises.append(expression)
            answers.append(self.format_answer(result))
        
        if len(exercises) < count:
            print(f"警告：只生成了 {len(exercises)} 道题目，未能达到要求的 {count} 道")
        
        return exercises, answers