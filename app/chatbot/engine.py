import os
import sys
import openai
from datetime import date
from app.db.doctor_service import DoctorService
from app.chatbot.conversation_manager import ConversationManager
from app.chatbot.function_call_conversation_manager import FunctionCallConversationManager
from app.chatbot.functions import functions

openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai

def format_prompt_template(template):
    available_specializations = DoctorService.get_list_of_specializations()
    today = date.today().isoformat()
    return template.format(
        available_specializations=available_specializations,
        today=today
    )

def main(mode="default"):
    if mode == "function_call":
        prompt_path = os.path.join(os.path.dirname(__file__), "prompt_template_function.md")
        with open(prompt_path, "r") as f:
            system_prompt = format_prompt_template(f.read())
        manager = FunctionCallConversationManager(
            llm_client=client,
            functions=functions,
            system_prompt=system_prompt
        )
    else:
        prompt_path = os.path.join(os.path.dirname(__file__), "prompt_template.md")
        with open(prompt_path, "r") as f:
            system_prompt = format_prompt_template(f.read())
        manager = ConversationManager(
            llm_client=client,
            system_prompt=system_prompt
        )
    manager.run()

if __name__ == "__main__":
    # Usage: python -m app.chatbot.run_chatbot [function_call|default]
    mode = sys.argv[1] if len(sys.argv) > 1 else "default"
    main(mode)