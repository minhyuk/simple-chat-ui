import openai
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich import box
from rich.console import Group
import random
import re

# Rich 콘솔 초기화
console = Console()

# 다양한 색상 설정
USER_COLORS = ["cyan", "blue", "green", "magenta"]
AI_COLORS = ["yellow", "red", "purple", "orange1"]

# OpenAI API 설정
client = openai.OpenAI(
    base_url="http://10.10.10.200:8000/v1",
    api_key="not-needed"
)

def display_welcome_message():
    welcome_text = Text("AI 채팅을 시작합니다. 종료하려면 'quit'를 입력하세요.", style="bold white")
    console.print(Panel(welcome_text, box=box.DOUBLE_EDGE, border_style="bright_blue"))

def process_markdown_and_code(text):
    """마크다운과 코드 블록을 처리하는 함수"""
    # 코드 블록 패턴 (```language\ncode\n```)
    code_pattern = r"```(\w+)?\n(.*?)\n```"
    
    # 텍스트를 처리하기 위한 조각들을 저장
    segments = []
    last_end = 0
    
    # 코드 블록 찾기
    for match in re.finditer(code_pattern, text, re.DOTALL):
        # 코드 블록 이전의 텍스트를 마크다운으로 처리
        if match.start() > last_end:
            md_text = text[last_end:match.start()]
            if md_text.strip():
                segments.append(Markdown(md_text))
        
        # 코드 블록 처리
        language = match.group(1) or "text"
        code = match.group(2)
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        segments.append(Panel(syntax, border_style="bright_blue"))
        
        last_end = match.end()
    
    # 마지막 남은 텍스트 처리
    if last_end < len(text):
        md_text = text[last_end:]
        if md_text.strip():
            segments.append(Markdown(md_text))
    
    return Group(*segments)

def chat_with_ai():
    conversation_history = []
    display_welcome_message()
    
    while True:
        # 사용자 입력을 패널로 표시
        user_input = console.input("\n[bold green]사용자: ")
        
        if user_input.lower() == 'quit':
            farewell_text = Text("채팅을 종료합니다.", style="bold red")
            console.print(Panel(farewell_text, box=box.DOUBLE_EDGE, border_style="red"))
            break
            
        try:
            # 사용자 입력을 패널로 표시
            user_color = random.choice(USER_COLORS)
            console.print(Panel(
                user_input,
                border_style=user_color,
                box=box.ROUNDED,
                title="사용자",
                title_align="left"
            ))
            
            # AI 응답 시작
            ai_color = random.choice(AI_COLORS)
            console.print("\n[bold]AI 응답 중...[/]\n")
            
            response = client.chat.completions.create(
                model="meta/llama3-8b-instruct",
                messages=[
                    *conversation_history,
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )
            
            full_response = ""
            
            # Live 디스플레이로 스트리밍 응답 표시
            with Live(auto_refresh=False) as live:
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        # 마크다운과 코드 블록 처리
                        rendered_content = process_markdown_and_code(full_response)
                        
                        # 패널 내용 업데이트
                        panel = Panel(
                            rendered_content,
                            border_style=ai_color,
                            box=box.ROUNDED,
                            title="AI 응답",
                            title_align="right"
                        )
                        live.update(panel, refresh=True)
            
            # 대화 기록 업데이트
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_text = Text(f"오류가 발생했습니다: {str(e)}", style="bold red")
            console.print(Panel(error_text, border_style="red"))

if __name__ == "__main__":
    chat_with_ai()
