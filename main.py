import argparse
from generator import ExerciseGenerator
from validator import AnswerValidator

def main():
    parser = argparse.ArgumentParser(description='小学四则运算题目生成器')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', type=int, help='生成题目的数量')
    group.add_argument('-e', type=str, help='题目文件路径')
    
    parser.add_argument('-r', type=int, help='数值范围（生成题目时必需）')
    parser.add_argument('-a', type=str, help='答案文件路径（批改题目时必需）')
    
    args = parser.parse_args()
    
    # 生成题目模式
    if args.n:
        if not args.r:
            print("错误：生成题目时必须使用 -r 参数指定数值范围")
            parser.print_help()
            return
            
        generator = ExerciseGenerator(args.r)
        exercises, answers = generator.generate_exercises(args.n)
        
        # 保存题目和答案
        with open('Exercises.txt', 'w', encoding='utf-8') as f:
            for i, exercise in enumerate(exercises, 1):
                f.write(f"{i}. {exercise} =\n")
        
        with open('Answers.txt', 'w', encoding='utf-8') as f:
            for i, answer in enumerate(answers, 1):
                f.write(f"{i}. {answer}\n")
                
        print(f"已生成 {args.n} 道题目到 Exercises.txt 和 Answers.txt")
        
    # 批改模式
    elif args.e:
        if not args.a:
            print("错误：批改题目时必须使用 -a 参数指定答案文件路径")
            parser.print_help()
            return
            
        validator = AnswerValidator()
        result = validator.validate(args.e, args.a)
        
        with open('Grade.txt', 'w', encoding='utf-8') as f:
            f.write(f"Correct: {len(result['correct'])} {tuple(result['correct'])}\n")
            f.write(f"Wrong: {len(result['wrong'])} {tuple(result['wrong'])}\n")
        
        print("批改完成，结果已保存到 Grade.txt")

if __name__ == "__main__":
    main()