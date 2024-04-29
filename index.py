import json
from difflib import get_close_matches

def citirea_json(file_path: str)-> dict:
    with open(file_path,'r') as file:
        data: dict = json.load(file)
    return data


def save_response(file_path: str, data: dict)-> dict:
    with open(file_path,'w') as file:
        json.dump(data,file, indent=2)

def find_best_match(user_question: str, questions: list[str])-> str | None:
    matches: list = get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

def get_answer(question:str, knowledge_base:dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] ==question:
            return q["answer"]
        
def chat_bot():
    knowledge_base : dict = citirea_json("train.json")

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break
    
        best_match: str = find_best_match(user_input,[q['question'] for q in knowledge_base['questions']])

        if best_match:
            answer: str = get_answer(best_match,knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: Nu inteleg aceasta intrebare. Poti sa ma inveti ?')
            new_answer: str = input('Scrie raspunsul sau scrie quit pentru a iesi: ')

            if new_answer.lower() != 'skip':
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                save_response('train.json', knowledge_base)
                print('Bot: Multumesc ! Am invatat ceva nou!')

if __name__ == '__main__':
    chat_bot()
 

