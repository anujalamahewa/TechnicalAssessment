<h3> This document contains detailed step-by-step guide on how i approached the given scenario </h3>
 
1 Read the email thoroughly the assignment is to "come up with a specific use case prompt to fine-tune the LLM on" as mentioned in https://github.com/mshumer/gpt-llm-trainer


It seemed like a simple task however I tried to run the code snippets but it gave errors. So I decided to run it locally.
The idea behind this was to check out what this code actually does when it comes to execution, plus I'm curious as to see how this is done: code-wise.

#---------------------------------
2 Install Python and other related libraries:


![Screenshot 2023-09-23 065006](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/bce31cb3-bef8-4eae-99b2-2967cd661bfb)

<b> The rest of this file is about errors I encountered and how i solved them: </b>




#---------------------------------
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

With that, moved the next part of the code



#---------------------------------
4 Error "The model `gpt-4` does not exist or you do not have access to it."

![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/14707035-851c-415c-857d-ccae8bbee4eb)

fix

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",


        
#---------------------------------
5 module panda not found


![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/aaab2a9d-cc42-43b1-ab3d-51c232bd140a)

https://saturncloud.io/blog/how-to-fix-no-module-named-pandas-error-in-visual-studio-code-for-windows/#:~:text=In%20conclusion%2C%20the%20%E2%80%9CNo%20module,and%20checking%20the%20Python%20path.

create a virtual environment, open the terminal in Visual Studio Code and type the following command: python -m venv myenv. This will create a virtual environment named “myenv”. To activate the virtual environment, type the following command: .\myenv\Scripts\activate. Once the virtual environment is activated, you can install Pandas using the pip install pandas command.



#---------------------------------
6 Now let's put our examples into a dataframe and turn them into a final pair of datasets.



![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/60d18b4b-5d3b-4358-abc0-4ab17e63b192)

![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/d9ecb02c-083f-493e-9c70-e6100e5df651)



#---------------------------------
7 Upload the file to OpenAI


![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/6e83b480-132a-4a90-a27b-e623a8039c57)

  file=open("/training_examples.jsonl", "rb"),

![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/f7978730-dc23-4b1a-ac3a-fe3eedaa839c)


It seems that we have generated questions and responses:


![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/6e94f069-e0d5-4933-8f4b-51b1aec38bce)


![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/ba2a75a8-f29b-4874-99b8-405b0796e555)





#---------------------------------
8 Train the model! You may need to wait a few minutes before running the next cell to allow for the file to process on OpenAI's servers.


![image](https://github.com/anujalamahewa/TechnicalAssessment/assets/12027102/73982742-6308-4c18-a8a2-184dd1d399a9)


