# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 22:07:30 2023

@author: sihu2
"""

import os
import openai
import json
import matplotlib.pyplot as plt
import io
import sys

openai.api_key = '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'
plt.rc('font', family='NanumGothic')


#adhd 관점
query = """
너는 adhd 진단이 의심되는 아이를 보조하는 간호/교사의 역할로서, 해당 adhd환자인 아이가 푼 수학문제와 이에 대한 모범 풀이과정을 인풋받고, 이 정보들을 바탕으로 학생의 풀이과정에 대한 해설을 내놓아서 adhd 진단과 연관시킨다
"""

#학생 풀이 해설 관점
{"role": "system", "content": "너는 대한민국 수능 과정에 입각한 수학 교사의 역할로서, 수학문제와 이에 대한 모범 풀이과정을 인풋받고, 이 정보들을 바탕으로 학생의 풀이과정에 대한 해설을 내놓는다 "},


query = """
"학생의 풀이를 모범풀이와 비교하여 line별로 해설하라 - 풀이과정 한 줄에 해설 한 줄이 필요하다, 각 line에는 학생이 사용한 수식도 표기해주라, 각 line별로 사용된 핵심개념을 []bracket 안에 표기하라, 학생풀이에서 잘못된 개념을 사용했을 경우, 이도 표기하라"
"""

#adhd
query =  """
학생의 풀이를 모범풀이와 비교하여 line별로 해설하라 - 풀이과정 한 줄에 해설 한 줄이 필요하다, 각 line에는 학생이 사용한 수식도 표기해주라, 각 line별로 사용된 핵심개념을 []bracket 안에 표기하라, 학생풀이에서 잘못된 개념을 사용했을 경우, 이도 표기하며, 각 line별로 adhd 증상과 연관이 있어 보이면 그에 대한 정보도 기술하라
"""

question = """
함수 \( f(x)=\sin \left(x+\frac{\pi}{2}\right)-\cos ^{2}(x+\pi) \) 의 최댓값은? [3점]
(1) \( \frac{1}{4} \)
(2) \( \frac{1}{2} \)
(3) \( \frac{3}{4} \)
(4) 1
(5) \( \frac{5}{4} \)'
"""

model_solution = """
\( \begin{array}{l}\text { 秱接 } \quad f(x)=-\left(\cos ^{2} x-\cos x+\frac{f}{4}\right)+\frac{f}{4} \\ =-\left(\cos x-\frac{1}{2}\right)^{2}+\frac{1}{4} \\ \cos x=t \\ f(x)=-\left(t-\frac{1}{2}\right)^{2}+\frac{f}{4}, \prod_{\frac{1}{2}}^{\frac{1}{4}} \\\end{array} \)
"""


student_solution = """
\( \begin{array} { l } f ( x ) = \cos x - \cos ^ { 2 } x \\ - 1 \leq \cos x \leq 1,0 \leq \cos ^ { 2 } x \leq 1 \text { or } 0 \text { s } \\ \quad \cos x = 1 , \cos ^ { 2 } x = 0 \text { of } x a x \\ f ( x ) = 1 - 0 = 1 \end{array} \)
"""


MODEL = "gpt-3.5-turbo"
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "너는 대한민국 수능 과정에 입각한 수학 교사의 역할로서, 수학문제와 이에 대한 모범 풀이과정을 인풋받고, 이 정보들을 바탕으로 학생의 풀이과정에 대한 해설을 내놓는다 "},
        {"role": "user", "content": f"문제는 {question}이다"},
        {"role": "user", "content": f"이에 대한 모범 풀이는 {model_solution}이다"},
        {"role": "user", "content": f"이에 대한 학생의 풀이는 {student_solution}이다"},
        {"role": "user", "content": f"학생의 풀이를 모범풀이와 한줄 한줄 비교하여 해설하라 - 풀이과정 한 줄에 해설 하나씩 필요하다, 각 line에는 학생이 사용한 수식도 표기해주라,각 line별로 사용된 핵심개념을 []bracket 안에 표기하라, 학생풀이에서 오답 개념을 사용했을 경우, 이도 명확히 표기하라"}
        ],
    temperature=1,
)
response_str = str(response)
data = json.loads(response_str)
content = data["choices"][0]["message"]["content"]






example = """

"""

MODEL = "gpt-3.5-turbo"
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "너는 대한민국 수능 과정에 입각한 수학 교사의 역할로서, 수학문제와 이에 대한 모범 풀이과정을 인풋받고, 이 정보들을 바탕으로 학생의 풀이과정에 대한 해설을 내놓는다 "},
        {"role": "user", "content": f"문제는 {question}이다"},
        {"role": "user", "content": f"이에 대한 모범 풀이는 {model_solution}이다"},
        {"role": "user", "content": f"이에 대한 학생의 풀이는 {student_solution}이다"},
        {"role": "user", "content": f"각각의 풀이를 line별로 해설하라 - 풀이과정 한 줄에 해설 한 줄이 필요하다, 각 line별로 사용된 핵심개념을 []bracket 안에 표기하라, 학생풀이에서 잘못된 개념을 사용했을 경우, 이도 표기하라"},
        {"role": "assistant", "content": content},
        {"role": "user", "content": "encode each step as [head, relationship, tail]"}
    ],
    temperature=0,
)
response_str = str(response)
data = json.loads(response_str)
motion = data["choices"][0]["message"]["content"]





MODEL = "gpt-3.5-turbo"
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "너는 대한민국 수능 과정에 입각한 수학 교사의 역할로서, 수학문제와 이에 대한 모범 풀이과정을 인풋받고, 이 정보들을 바탕으로 학생의 풀이과정에 대한 해설을 내놓는다 "},
        {"role": "user", "content": f"문제는 {question}이다"},
        {"role": "user", "content": f"이에 대한 모범 풀이는 {model_solution}이다"},
        {"role": "user", "content": f"이에 대한 학생의 풀이는 {student_solution}이다"},
        {"role": "user", "content": f"각각의 풀이를 line별로 해설하라 - 풀이과정 한 줄에 해설 한 줄이 필요하다, 각 line별로 사용된 핵심개념을 []bracket 안에 표기하라, 학생풀이에서 잘못된 개념을 사용했을 경우, 이도 표기하라"},
        {"role": "assistant", "content": content},
        {"role": "user", "content": "어느 학생의 유형을 아래와 같이 두 분류로 나눈다.암기해서 문제유형/풀이방식을 외우는 체화형, 개념을 올바르게 이해하고 응용/적용하는 탐구형. 학생의 체화형/탐구형인지 구분부터 하고, 해당 프레임워크로 학생의 학습성향을 심층적으로 분석하라"}
    ],
    temperature=0,
)
response_str = str(response)
data = json.loads(response_str)
content = data["choices"][0]["message"]["content"]














fig, ax = plt.subplots(figsize=(6, 4))
ax.axis('off')
ax.text(0, 0, content, va='top', fontsize=12)

# Save the rendered image to a buffer
buffer = io.BytesIO()
plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
buffer.seek(0)

# Print the rendered image
img = plt.imread(buffer)
plt.imshow(img)
plt.show()
