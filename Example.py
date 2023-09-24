#--------------------------------------------------------------------------
# Hello world application + to test the import openai
#--------------------------------------------------------------------------
'''

import openai

openai.api_key = "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"

prompt = "Say this is a test"

response = openai.Completion.create(
    engine="text-davinci-001", prompt=prompt, max_tokens=6
)

print(response)

'''

#--------------------------------------------------------------------------
# data generation 
#--------------------------------------------------------------------------



import os
import openai
import random
from tenacity import retry, stop_after_attempt, wait_exponential



openai.api_key = "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"

prompt = "A model that takes in a puzzle-like reasoning-heavy question in English, and responds with a well-reasoned, step-by-step thought out response in Spanish."
temperature = .4
### DEFAULT VALUE WAS 100, CHANGED AS I GOT AN ERROR
number_of_examples = 1

N_RETRIES = 3

@retry(stop=stop_after_attempt(N_RETRIES), wait=wait_exponential(multiplier=1, min=4, max=70))
def generate_example(prompt, prev_examples, temperature=.5):
    messages=[
        {
            "role": "system",
            "content": f"You are generating data which will be used to train a machine learning model.\n\nYou will be given a high-level description of the model we want to train, and from that, you will generate data samples, each with a prompt/response pair.\n\nYou will do so in this format:\n```\nprompt\n-----------\n$prompt_goes_here\n-----------\n\nresponse\n-----------\n$response_goes_here\n-----------\n```\n\nOnly one prompt/response pair should be generated per turn.\n\nFor each turn, make the example slightly more complex than the last, while ensuring diversity.\n\nMake sure your samples are unique and diverse, yet high-quality and complex enough to train a well-performing model.\n\nHere is the type of model we want to train:\n`{prompt}`"
        }
    ]

    if len(prev_examples) > 0:
        if len(prev_examples) > 8:
            prev_examples = random.sample(prev_examples, 8)
        for example in prev_examples:
            messages.append({
                "role": "assistant",
                "content": example
            })

    response = openai.ChatCompletion.create(
        ### CHANGED TO GPT-3.5
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=200,
    )

    return response.choices[0].message['content']

# Generate examples
prev_examples = []
for i in range(number_of_examples):
    print(f'Generating example {i}')
    example = generate_example(prompt, prev_examples, temperature)
    prev_examples.append(example)

print(prev_examples)

#--------------------------------------------------------------------------
# generate a system message.
#--------------------------------------------------------------------------

def generate_system_message(prompt):

    response = openai.ChatCompletion.create(
        ### CHANGED GPT-4 AS I ENCOUNTERED AN ERROR
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": "You will be given a high-level description of the model we are training, and from that, you will generate a simple system prompt for that model to use. Remember, you are not generating the system message for data generation -- you are generating the system message to use for inference. A good format to follow is `Given $INPUT_DATA, you will $WHAT_THE_MODEL_SHOULD_DO.`.\n\nMake it as concise as possible. Include nothing but the system prompt in your response.\n\nFor example, never write: `\"$SYSTEM_PROMPT_HERE\"`.\n\nIt should be like: `$SYSTEM_PROMPT_HERE`."
          },
          {
              "role": "user",
              "content": prompt.strip(),
          }
        ],
        temperature=temperature,
        max_tokens=500,
    )

    return response.choices[0].message['content']

system_message = generate_system_message(prompt)

print(f'The system message is: `{system_message}`. Feel free to re-run this cell if you want a better result.')

#--------------------------------------------------------------------------
# put the example into a dataframe and turn them into a final pair of dataset
#--------------------------------------------------------------------------

import json
import pandas as pd

# Initialize lists to store prompts and responses
prompts = []
responses = []

# Parse out prompts and responses from examples
for example in prev_examples:
  try:
    split_example = example.split('-----------')
    prompts.append(split_example[1].strip())
    responses.append(split_example[3].strip())
  except:
    pass

# Create a DataFrame
df = pd.DataFrame({
    'prompt': prompts,
    'response': responses
})

# Remove duplicates
df = df.drop_duplicates()

print('There are ' + str(len(df)) + ' successfully-generated examples.')

# Initialize list to store training examples
training_examples = []

# Create training examples in the format required for GPT-3.5 fine-tuning
for index, row in df.iterrows():
    training_example = {
        "messages": [
            {"role": "system", "content": system_message.strip()},
            {"role": "user", "content": row['prompt']},
            {"role": "assistant", "content": row['response']}
        ]
    }
    training_examples.append(training_example)

# Save training examples to a .jsonl file
with open('training_examples.jsonl', 'w') as f:
    for example in training_examples:
        f.write(json.dumps(example) + '\n')

#--------------------------------------------------------------------------
# Upload the file to OpenAI
#--------------------------------------------------------------------------

print('Uploading file to OpenAI...')

file_id = openai.File.create(
  file=open("C:/Users/anuja/Documents/training_examples.jsonl", "rb"),
  purpose='fine-tune'
).id

print('File Upload Successful')

#--------------------------------------------------------------------------
# Train the model! You may need to wait a few minutes before running the 
# next cell to allow for the file to process on OpenAI's servers.
#--------------------------------------------------------------------------

job = openai.FineTuningJob.create(training_file=file_id, model="gpt-3.5-turbo")

job_id = job.id

#--------------------------------------------------------------------------
# Now, just wait until the fine-tuning run is done, and you'll have a ready-to-use model!
# Run this cell every 20 minutes or so -- eventually, you'll see a message "New fine-tuned model created: ft:gpt-3.5-turbo-0613:xxxxxxxxxxxx"
# Once you see that message, you can go to the OpenAI Playground (or keep going to the next cells and use the API) to try the model!
#--------------------------------------------------------------------------

openai.FineTuningJob.list_events(id=job_id, limit=10)

#--------------------------------------------------------------------------
# Once your model is trained, run the next cell to grab the fine-tuned model name.
#--------------------------------------------------------------------------

model_name_pre_object = openai.FineTuningJob.retrieve(job_id)
model_name = model_name_pre_object.fine_tuned_model
print(model_name)

#--------------------------------------------------------------------------
# Let's try it out!
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# 
#--------------------------------------------------------------------------