from langchain.prompts import PromptTemplate

outline_prompt = PromptTemplate.from_template(
    """
你是一位学术写作助手，请根据以下论文主题设计一篇论文大纲，并以JSON格式返回。
只返回符合 JSON 格式的数据，不要加入任何说明性文字、标点或 Markdown 代码块。
论文主题：{title}
请返回格式如下：
{{
    "title": "...",
    "sections": [
        {{
            "section_title": "一、引言",
            "section_summary": "简要介绍研究背景、目的和结构。"
        }},
        {{
            "section_title": "二、人工智能带来的机遇",
            "section_summary": "详细阐述AI在教学、科研、管理等方面的优势。"
        }},
        ...
    ]
}}
"""
)
paragraph_prompt = PromptTemplate.from_template(
    "请根据论文主题《{title}》和以下大纲部分《{section}`》，为该部分写出一段正式的中文论文内容，要求学术规范、语言通顺、信息充实，段落长度不少于150字。"
)
#要求输入的内容：title,section  
conclusion_prompt = PromptTemplate.from_template(
    "请你根据主题《{title}》与其内容，撰写一段论文的总结部分，简要概括全文要点，并得出适当的结论。"
)
#三部分：outline,paragraph,conclusion   

from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
import os
from dotenv import load_dotenv  
from langchain_core.output_parsers import JsonOutputParser

json_parser = JsonOutputParser()

load_dotenv()

# ✅ 从环境变量中读取 key 和 base
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")

# 模型
llm = ChatOpenAI(model_name="deepseek-chat", 
                 temperature=0.3,
                 openai_api_key=os.getenv("OPENAI_API_KEY"),
                 openai_api_base=os.getenv("OPENAI_API_BASE")
                 )

# 输出解析器
parser = StrOutputParser()

# 生成论文大纲链
generate_outline_chain = outline_prompt | llm | json_parser

# 单个段落内容生成链（待后续动态调用）
generate_paragraph_chain = paragraph_prompt | llm | parser

# 论文总结部分链
generate_conclusion_chain = conclusion_prompt | llm | parser

#用函数串联链
def generate_full_essay(title: str):
    # # 1. 生成论文大纲
    # outline = generate_outline_chain.invoke({"title": title})
    # print("🧱 大纲生成：\n", outline)
    import json

    outline_data = generate_outline_chain.invoke({"title": title})
    #outline_data = json.loads(outline_json)

    sections = outline_data["sections"]
 

    # 2. 按大纲生成段落
    # sections = outline.split("\n")
    print(sections,'\n')
    paragraphs = []
    for section in sections:
        para = generate_paragraph_chain.invoke({
            "title": outline_data["title"],
            "section": section["section_title"] + "：" + section["section_summary"]
        })
        paragraphs.append({
            "title": section["section_title"],
            "content": para
        })


    #full_essay = f"论文题目：{outline_data['title']}\n\n"
    #防止和tex模板中的题目重复
    for p in paragraphs:
        #full_essay += f"{p['title']}\n{p['content']}\n\n"
        full_essay += f"{p['content']}\n\n"#避免标题重复

    conclusion = generate_conclusion_chain.invoke({"title": outline_data["title"]})
    full_essay += f"结语\n{conclusion}"


    return full_essay
#此处更改主题
title = "人工智能对金融行业的影响"
essay = generate_full_essay(title)
#essay = generate_outline_chain.invoke({"title":"人工智能对高等教育的影响"}) 
print(essay)


from pylatex import Document, Section, Command, NoEscape
import   subprocess
import re

import os
import subprocess

def save_essay_to_pdf_from_template(essay_content: str, template_path: str, save_path: str, filename: str, title: str):
    # 读取 LaTeX 模板
    with open(template_path, 'r', encoding='utf-8') as f:
        tex_template = f.read()

    # 替换占位符（注意转义 \、% 等字符）
    safe_content = essay_content.replace('\\', r'\\').replace('%', r'\%') \
                                .replace('&', r'\&').replace('_', r'\_') \
                                .replace('#', r'\#').replace('{', r'\{') \
                                .replace('}', r'\}').replace('~', r'\textasciitilde{}') \
                                .replace('^', r'\^{}') \
                                .replace('\n\n', '\n\n\\par\n\n')  # 插入段落

    # 替换 LaTeX 模板中的占位符
    rendered_tex = tex_template.replace("{{ essay_content }}", safe_content)
    rendered_tex = rendered_tex.replace("{{ title }}", title)

    # 写入 .tex 文件
    tex_file = os.path.join(save_path, filename + ".tex")
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(rendered_tex)

    # 编译 PDF
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", filename + ".tex"],
            cwd=save_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"✅ PDF 已生成：{os.path.join(save_path, filename)}.pdf")
    except subprocess.CalledProcessError:
        print("❌ LaTeX 编译失败，请检查 .tex 格式是否有语法错误。")

save_path = r"E:\test01\环境设置"
template_path = r"E:\test01\py311\统一环境\essay_template.tex"
filename = "AI_HigherEdu_Essay"+title

# 生成后的论文内容，150字段落起，已准备好
essay_cleaned = essay.encode("utf-8", errors="ignore").decode("utf-8")

# 保存为 PDF
save_essay_to_pdf_from_template(essay_cleaned, template_path, save_path, filename, title)

