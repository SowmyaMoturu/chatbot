import json
from app.chatbot.dispatch_function_call import dispatch_function_call

class BaseConversationManager:

    def handle_tool_call(self, fn_name, fn_args, messages, llm_client=None, followup=True):
        """
        Executes the tool call and optionally generates a user-friendly response using the LLM.
        """
        tool_result = dispatch_function_call(fn_name, fn_args)
        messages.append({
            "role": "user",
            "content": f"Tool output for '{fn_name}': {json.dumps(tool_result, default=str)}"
        })
       
        if followup and llm_client:
            followup_prompt = [
                {
                    "role": "system",
                    "content": """
                    Generate a user-friendly explanation based on the tool output provided. 
                    In case of slot checking, if not available, confirm with user if they want to search for next slot
                    Never suggest users visit the hospital or contact the clinic directly.
                    """
                },
                {
                    "role": "user",
                    "content": f"Tool output for '{fn_name}': {json.dumps(tool_result, default=str)}"
                }
            ]

            # Pass tool result to LLM for generating user-friendly output
            response = llm_client.chat.completions.create(
                model="gpt-4o",
                messages=followup_prompt,
                max_tokens=300,
                temperature=0,
            )
            message = response.choices[0].message
            if hasattr(message, "content") and message.content:
                print(f"Bot: {message.content}")
            messages.append({"role": "assistant", "content": message.content})
        return tool_result

    def extract_tool_call_from_response(self, llm_response_content):
        """
        Extracts the tool call from the LLM response content.
        """
        try:
            json_str = self.extract_json(llm_response_content)
            parsed_response = json.loads(json_str)
            if isinstance(parsed_response, dict) and \
               "tool_call" in parsed_response and \
               isinstance(parsed_response["tool_call"], dict) and \
               "name" in parsed_response["tool_call"] and \
               "args" in parsed_response["tool_call"]:
                return parsed_response["tool_call"]
        except Exception:
            pass
        return None

    def extract_json(self, text):
        """
        Extracts JSON content from text, handling markdown formatting.
        """
        text = text.strip()
        if text.startswith("```"):
            text = text.lstrip("`")
            if text.lower().startswith("json"):
                text = text[4:]
            text = text.strip("` \n")
        if text.lower().startswith("json"):
            text = text[4:].strip()
        return text.strip()

    def chat_loop(self, get_llm_response):
        """
        Main chat loop for interacting with the user.
        """
        print("Welcome to the Doctor's Assistant ChatBot! (type 'exit' to quit)\n")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Bot: Goodbye!")
                break
            self.messages.append({"role": "user", "content": user_input})

            message = get_llm_response(self.messages)
            if not isinstance(message, dict):
                message = message.to_dict()
            llm_response_content = message.get("content", "")
            self.messages.append({"role": "assistant", "content": llm_response_content or ""})

            # Support both function_call and default mode
            tool_call_data = None
            if message.get("function_call"):
                fn_name = message["function_call"]["name"]
                fn_args = json.loads(message["function_call"]["arguments"])
                tool_call_data = {"name": fn_name, "args": fn_args}
            else:
                tool_call_data = self.extract_tool_call_from_response(llm_response_content)

            if not tool_call_data:
                print(f"Bot: {llm_response_content}")
                continue

            fn_name = tool_call_data["name"]
            fn_args = tool_call_data["args"]

            # All tool calls now use followup=True
            self.handle_tool_call(fn_name, fn_args, self.messages, self.llm_client, followup=True)