import random
import json

with open("../data/raw/rule_based_intents.json", "r") as file:
    rule_based_data = json.load(file)

def match_rule_based_intent(user_input):
    print(f'LOG match_rule_based_intent: user_input: {user_input}')
    for intent, data in rule_based_data.items():
        for pattern in data["patterns"]:
            if pattern in user_input.lower():
                return intent
    return None

def generate_rule_based_response(intent):
    print(f'LOG generate_rule_based_response: intent {intent}')
    responses = rule_based_data[intent]["responses"]
    return random.choice(responses)