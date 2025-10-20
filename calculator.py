import fractions
from fractions import Fraction
import re

class ExpressionCalculator:
    def __init__(self):
        pass
    
    def parse_fraction(self, num_str):
        """解析分数格式"""
        if "'" in num_str:
            parts = num_str.split("'")
            whole = int(parts[0])
            fraction_parts = parts[1].split('/')
            numerator = int(fraction_parts[0])
            denominator = int(fraction_parts[1])
            return Fraction(whole) + Fraction(numerator, denominator)
        elif '/' in num_str:
            parts = num_str.split('/')
            return Fraction(int(parts[0]), int(parts[1]))
        else:
            return Fraction(int(num_str))
    
    def safe_eval(self, expr):
        """安全地计算表达式，返回 Fraction 对象"""
        # 替换运算符
        expr = expr.replace('×', '*').replace('÷', '/')
        
        # 使用 Fraction 和安全的 eval
        # 创建安全的环境
        safe_dict = {
            'Fraction': Fraction,
            '__builtins__': {}
        }
        
        # 将数字转换为 Fraction
        def convert_numbers(match):
            num_str = match.group(0)
            if '/' in num_str:
                return f"Fraction('{num_str}')"
            else:
                return f"Fraction({num_str})"
        
        # 将表达式中的所有数字替换为 Fraction
        expr_fraction = re.sub(r'\d+/\d+|\d+', convert_numbers, expr)
        
        try:
            result = eval(expr_fraction, safe_dict)
            return result
        except:
            return None
    
    def calculate_expression(self, expression):
        """计算表达式结果，返回 Fraction 对象"""
        try:
            return self.safe_eval(expression)
        except:
            return None