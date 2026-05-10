from ollama import Client


client = Client(
    host="http://host.docker.internal:11434"
)


class OllamaClient:

    @staticmethod
    async def generate_response(
        prompt: str
    ):

        response = client.chat(
            model="llama3:8b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response[
            "message"
        ][
            "content"
        ]