import json

answers = ""

with open("ml_training_data.json", "r") as f:
    data = json.load(f)

for i,v in enumerate(data):
    print(f"{i}: {v}")
    answers += "<question_start>" + v["question"] + "<question_end> <answer_start>" + v["answer"] + "<answer_end>\n"

with open("context.txt", "w") as f:
    f.write(answers)