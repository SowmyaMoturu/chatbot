# filepath: /Users/sowmyamoturu/Downloads/doctor_assistant_chatbot/app/chatbot/conversation_manager.py
from app.chatbot.base_conversation_manager import BaseConversationManager

class ConversationManager(BaseConversationManager):
    def __init__(self, llm_client, system_prompt):
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]
        self.specialization = None
        self.patient_name = None
        self.patient_phone = None

    def run(self):
        def get_llm_response(messages):
            response = self.llm_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=300,
                temperature=0,
            )
            return response.choices[0].message
        self.chat_loop(get_llm_response)