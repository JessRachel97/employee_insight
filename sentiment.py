import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import var as v
import csv

# sending data to ChatGPT and saving results of analysis

load_dotenv()

filepath = "data/"

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

with open(filepath+"beliefs.json", 'r') as f:
    beliefs = json.load(f)

belief_str = ""
for b in beliefs:
    belief_str += str(b) + "\n"

with open(filepath+"employee_feedback.json", 'r') as f:
    feedback = json.load(f)


# NOTE: in production this would looop through employees, since there was only 5 I ran one at a time so I could
# watch what was happening
r = feedback["employees"][4]

emp_feedback = r["responses"]
feedback_str = ""
for f in emp_feedback:
    feedback_str += str(f) + "\n"

print(len(emp_feedback))

content = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": v.SYSTEM_PROMPT + "\n" + belief_str},
        {"role": "user", "content": feedback_str}
    ]
)

str_response_test = content.choices[0].message.content
filename = 'output/' + r["employee_id"] + '.csv'
with open(filename, "w") as f:
    f.write(r["name"] + '\n')
    f.write(r["employee_id"] + '\n')
    f.write(str_response_test)
