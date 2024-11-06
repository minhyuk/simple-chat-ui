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
import time

# Rich 콘솔 초기화
console = Console()

# 다양한 색상 설정
USER_COLORS = ["cyan", "blue", "green", "magenta"]
AI_COLORS = ["yellow", "red", "purple", "orange1"]

# OpenAI API 설정
client_8b = openai.OpenAI(
    base_url="http://10.10.10.200:8000/v1",
    api_key="not-needed"
)

client_70b = openai.OpenAI(
    base_url="http://10.10.10.200:8001/v1",
    api_key="not-needed"
)

# 전역 변수로 현재 선택된 클라이언트와 모델 설정
current_client = None
current_model = None

def select_model():
    """사용자가 모델을 선택하는 함수"""
    global current_client, current_model
    
    console.print(Panel(
        Text("사용할 모델을 선택하세요:", style="bold white"),
        box=box.DOUBLE_EDGE,
        border_style="bright_blue"
    ))
    console.print("[1] LLaMA 8B\n[2] LLaMA 70B")
    
    while True:
        choice = console.input("\n선택 (1 또는 2): ")
        if choice == "1":
            current_client = client_8b
            current_model = "meta/llama3-8b-instruct"
            break
        elif choice == "2":
            current_client = client_70b
            current_model = "meta/llama3-70b-instruct"
            break
        else:
            console.print("[red]잘못된 선택입니다. 1 또는 2를 입력하세요.[/]")
    
    console.print(f"\n[green]선택된 모델: {current_model}[/]")

def display_welcome_message():
    welcome_text = Text("AI 채팅을 시작합니다. 종료하려면 'quit'를 입력하세요.", style="bold white")
    console.print(Panel(welcome_text, box=box.DOUBLE_EDGE, border_style="bright_blue"))

def chat_with_ai():
    conversation_history = []
    display_welcome_message()
    select_model()  # 채팅 시작 전 모델 선택
    
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
            
            response = current_client.chat.completions.create(
                model=current_model,
                messages=[
                    *conversation_history,
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )
            
            full_response = ""
            buffer = ""
            console.print("\n[bold]AI 응답 중...[/]\n")
            
            panel = Panel(
                Group(),
                border_style=ai_color,
                box=box.ROUNDED,
                title="AI 응답",
                title_align="right",
                padding=(0, 1),
                expand=True
            )
            
            last_update = time.time()
            min_update_interval = 0.2  # 최소 업데이트 간격을 0.2초로 설정
            
            with Live(
                panel,
                auto_refresh=False,
                vertical_overflow="visible",
                refresh_per_second=2,  # 리프레시 속도를 낮춤
            ) as live:
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        buffer += content
                        
                        current_time = time.time()
                        # 최소 업데이트 간격이 지났거나 버퍼가 충분히 쌓였을 때만 업데이트
                        if (current_time - last_update >= min_update_interval and 
                            (len(buffer) >= 100 or '\n' in buffer)):
                            rendered_content = process_markdown_and_code(full_response)
                            panel.renderable = rendered_content
                            live.refresh()
                            buffer = ""
                            last_update = current_time
            
                # 스트리밍 완료 후 최종 업데이트
                if buffer:
                    rendered_content = process_markdown_and_code(full_response)
                    panel.renderable = rendered_content
                    live.refresh()
            
            # 대화 기록 업데이트
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_text = Text(f"오류가 발생했습니다: {str(e)}", style="bold red")
            console.print(Panel(error_text, border_style="red"))

def process_markdown_and_code(text: str) -> Group:
    """마크다운과 코드 블록을 처리하는 함수"""
    code_pattern = r"```(\w+)?\n(.*?)\n```"
    segments = []
    last_end = 0
    
    for match in re.finditer(code_pattern, text, re.DOTALL):
        # 코드 블록 이전 텍스트 처리
        if match.start() > last_end:
            md_text = text[last_end:match.start()].strip()
            if md_text:
                segments.append(Markdown(md_text, style="white"))
        
        # 코드 블록 처리
        language = match.group(1) or "text"
        code = match.group(2)
        segments.append(Panel(
            Syntax(code, language, theme="monokai", line_numbers=True),
            border_style="bright_blue",
            expand=True
        ))
        
        last_end = match.end()
    
    # 남은 텍스트 처리
    if last_end < len(text):
        md_text = text[last_end:].strip()
        if md_text:
            segments.append(Markdown(md_text, style="white"))
    
    return Group(*segments)

if __name__ == "__main__":
    chat_with_ai()
