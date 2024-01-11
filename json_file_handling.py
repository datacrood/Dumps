# Brute-Force approach
import json
with open('/Users/deveshsharma/Downloads/example2.json', 'r') as example:
    data = json.load(example)
    topic, question, answer=[],[],[]
    for key1, value1 in data.items(): #Ignore
        for key2, value2 in value1.items(): #Subject/Topic
            topic.append(key2)
            for key3, value3 in value2.items(): #Ignore question number
                for key4, value4 in value3.items(): # Get questions
                    # Going further prints type of value as str and list rather than dict. Hence last layer
                    if key4=="question":
                        question.append(value4)
                    elif key4=="answer":
                        answer.append(value4)
print(topic, question, answer)

#------
import pandas as pd
data1 = {"Topic": topic+['math'], "Question": question, "Answer": answer}
table = pd.DataFrame(data1)
table
