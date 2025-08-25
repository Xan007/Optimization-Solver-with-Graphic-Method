import base64
from typing import Optional, Union, List
from groq import Groq

class IAClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

        self.messages: List[dict] = []
        self.promptSystem: Optional[str] = None

    def append_message(self, role: str, content: Union[str, List[dict]]):
        self.messages.append({"role": role, "content": content})

    def set_system_prompt(self, prompt: str):
        self.promptSystem = prompt
        self.append_message("system", self.promptSystem)

    def clear_history(self):
        self.messages = []

        if self.promptSystem:
            self.append_message("system", self.promptSystem)

    def _encode_image(self, image_path: str) -> str:
        """Encode a local image file to base64 for API request"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def new_message(
        self,
        userPrompt: str,
        promptSystem: Optional[str] = None,
        image_paths: Optional[List[str]] = None,  # local file paths
        image_urls: Optional[List[str]] = None    # direct URLs
    ) -> str:
        content = []

        if promptSystem:
            self.messages.append({"role": "system", "content": promptSystem})

        if userPrompt:
            content.append({"type": "text", "text": userPrompt})

        model = "openai/gpt-oss-20b"
        if image_paths or image_urls:
            model = "meta-llama/llama-4-scout-17b-16e-instruct"


        if image_paths:
            for path in image_paths:
                base64_img = self._encode_image(path)
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_img}"}
                })

        if image_urls:
            for url in image_urls:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": url}
                })

        self.messages.append({"role": "user", "content": content})

        try:
            chat_completion = self.client.chat.completions.create(
                messages=self.messages,
                model=model,
            )
            
            return chat_completion.choices[0].message.content
        except Exception as e:
            print("Error during API call:", e)
            return None
