import re
from calculator import ExpressionCalculator

class AnswerValidator:
    def __init__(self):
        self.calculator = ExpressionCalculator()
    
    def parse_exercise_file(self, file_path):
        """解析题目文件"""
        exercises = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d+)\.\s*(.+)\s*=', line.strip())
                if match:
                    exercises.append(match.group(2))
        return exercises
    
    def parse_answer_file(self, file_path):
        """解析答案文件"""
        answers = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d+)\.\s*(.+)', line.strip())
                if match:
                    answers.append(match.group(2))
        return answers
    
    def normalize_fraction(self, fraction_str):
        """标准化分数表示"""
        if "'" in fraction_str:
            return fraction_str
        elif '/' in fraction_str:
            parts = fraction_str.split('/')
            num, den = int(parts[0]), int(parts[1])
            if num < den:
                return fraction_str
            else:
                whole = num // den
                remainder = num % den
                return f"{whole}'{remainder}/{den}"
        else:
            return fraction_str
    
    def validate(self, exercise_file, answer_file):
        """验证答案"""
        exercises = self.parse_exercise_file(exercise_file)
        student_answers = self.parse_answer_file(answer_file)
        
        correct = []
        wrong = []
        
        for i, (exercise, student_answer) in enumerate(zip(exercises, student_answers), 1):
            correct_answer = self.calculator.calculate_expression(exercise)
            if correct_answer is None:
                wrong.append(i)
                continue
            
            # 标准化正确答案
            if correct_answer.denominator == 1:
                correct_str = str(correct_answer.numerator)
            elif correct_answer.numerator > correct_answer.denominator:
                whole = correct_answer.numerator // correct_answer.denominator
                remainder = correct_answer.numerator % correct_answer.denominator
                correct_str = f"{whole}'{remainder}/{correct_answer.denominator}"
            else:
                correct_str = f"{correct_answer.numerator}/{correct_answer.denominator}"
            
            # 标准化学生答案
            normalized_student = self.normalize_fraction(student_answer)
            
            if normalized_student == correct_str:
                correct.append(i)
            else:
                wrong.append(i)
        
        return {"correct": correct, "wrong": wrong}