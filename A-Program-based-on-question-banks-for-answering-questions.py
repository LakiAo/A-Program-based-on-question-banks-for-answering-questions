import pandas as pd
import tkinter as tk
from tkinter import messagebox

class EnhancedQuestionBank:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.questions = self._prepare_questions()

    def _prepare_questions(self):
        needed_columns = ['题型', '题干', '正确答案', '答案解析', 'A', 'B', 'C', 'D']
        questions = self.dataframe[needed_columns].dropna(subset=['题干', '正确答案'])
        return questions

    def get_random_question(self):
        question = self.questions.sample().iloc[0]
        return question

    def check_answer(self, question, user_answer):
        correct_answer = question['正确答案']
        if question['题型'] == '多选题':
            return ''.join(sorted(user_answer.upper())) == ''.join(sorted(correct_answer.upper()))
        else:
            return user_answer.strip().upper() == correct_answer.strip().upper()

# 加载题库数据
all_data = pd.concat(pd.read_excel("D:/Users/LakiAo/Downloads/普通生物学客观题.xlsx", sheet_name=None), ignore_index=True)
question_bank = EnhancedQuestionBank(all_data)

# 创建窗口
root = tk.Tk()
root.title("题目测试")

current_question = None
answer_vars = []

# 定义用于显示题目和选项的函数
def display_question():
    global current_question, answer_vars
    current_question = question_bank.get_random_question()
    question_type = current_question['题型']
    question_text = current_question['题干']

    # 清除旧的题目和选项
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=question_text, wraplength=400).pack()

    # 创建答案选项
    answer_vars = []
    if question_type in ['单选题', '多选题']:
        options = ['A', 'B', 'C', 'D']
    else:  # 判断题
        options = ['对', '错']

    for option in options:
        answer_var = tk.StringVar(value='')
        answer_vars.append(answer_var)
        if question_type == '单选题':
            tk.Radiobutton(root, text=current_question.get(option, option), variable=answer_vars[0], value=option).pack()
        elif question_type == '多选题':
            tk.Checkbutton(root, text=current_question[option], variable=answer_var).pack()
        else:  # 判断题
            tk.Radiobutton(root, text=option, variable=answer_vars[0], value=option).pack()

    # 提交按钮
    submit_button = tk.Button(root, text="提交答案", command=submit_answer)
    submit_button.pack()

    # 下一题按钮
    next_button = tk.Button(root, text="下一题", command=display_question)
    next_button.pack()

# 提交答案的函数
def submit_answer():
    selected_answers = [answer_var.get() for answer_var in answer_vars if answer_var.get()]
    is_correct = question_bank.check_answer(current_question, ''.join(selected_answers))
    result_text = "答案正确!" if is_correct else "答案错误"
    explanation_text = f"正确答案: {current_question['正确答案']}\n解析: {current_question['答案解析']}"
    messagebox.showinfo("结果", result_text + "\n\n" + explanation_text)

# 初始加载题目
display_question()

# 启动事件循环
root.mainloop()