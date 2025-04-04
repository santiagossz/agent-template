import os


class PromptGenerator:
    def __init__(self, prompt_name):
        self.prompt_name = prompt_name
        self.prompt = None

    def load_prompt(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(base_path, f"{self.prompt_name}.md")
        with open(prompt_path) as f:
            self.prompt = f.read()

    def gen_prompt(self, state, chat_history=False, **kwargs):
        self.load_prompt()
        kwargs["user_input"] = state["messages"][-1].content
        context = {**kwargs, **state}
        messages = [{"role": "system", "content": self.prompt.format(**context)}]
        if chat_history:
            messages += state["messages"]
        return messages

    @classmethod
    def general(cls, state, prompt_name):
        pg = cls(prompt_name)
        return pg.gen_prompt(state)

    @classmethod
    def router(cls, state, routes):
        pg = cls("router")
        kwargs = {
            "scope": "",
            "routes": routes,
        }
        return pg.gen_prompt(state, **kwargs)
