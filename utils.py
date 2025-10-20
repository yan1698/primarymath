def format_fraction(fraction):
    """格式化分数输出"""
    if fraction.denominator == 1:
        return str(fraction.numerator)
    elif fraction.numerator > fraction.denominator:
        whole = fraction.numerator // fraction.denominator
        remainder = fraction.numerator % fraction.denominator
        return f"{whole}'{remainder}/{fraction.denominator}"
    else:
        return f"{fraction.numerator}/{fraction.denominator}"

def is_proper_fraction(fraction):
    """检查是否为真分数"""
    return fraction.numerator < fraction.denominator