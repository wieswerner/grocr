import openai

class OpenAiApi:
    def ask_open_ai(input, openai_org, openai_api_key):
        print(f"Asking AI {input}")

        openai.organization = openai_org
        openai.api_key = openai_api_key

        completion = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=4096-len(input),
            prompt=input,
            temperature=0
        )

        print(f"AI Response: {completion.choices[0].text}")
        return completion.choices[0].text
