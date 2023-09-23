![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/5f46bb84-30ae-4007-aa32-acc84742cee6)Step by step

1. Read the email thoroughly the assignment is to "come up with a specific use case prompt to fine-tune the LLM on" as mentioned in https://github.com/mshumer/gpt-llm-trainer

It seemed like a simple task however I tried to run the code snippets but it gave errors. So I decided to run it locally.

2 Install Python and other related libraries:

![Screenshot 2023-09-23 065006](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/bce31cb3-bef8-4eae-99b2-2967cd661bfb)

3 creating a new account to get the API key (since I use chat GPT heavily there was no quota left).

https://stackoverflow.com/questions/71873182/no-module-named-openai

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=1000,
    )

![Screenshot 2023-09-23 065755](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/e098fec5-44d8-40be-aee1-e20030a7a88c)

Encountered a "RateLimitError"

temperature = .4
number_of_examples = 2

![Screenshot 2023-09-23 071200](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/576434ab-ac57-4228-b86e-93b786bb91c3)
