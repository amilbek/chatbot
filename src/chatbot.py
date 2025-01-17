from db_connection import actions
from intent_classifier import intents_entities
from ner import chatbot_classification_with_entity_validation, entity_validation, is_complex_request
from rule_based_chat import match_rule_based_intent, generate_rule_based_response

# accoring to database operation type, it is decided if the request needs confirmation or not
READING_DATABASE = ["query_exam_status", "query_exam_grade", "query_student_profile"]
WRITING_DATABASE = ["change_first_name", "change_last_name", "change_address",  "register_exam", "deregister_exam"]

# Implementation of chatbot memory
USER_CONTEXT_TEMPLATE = {
    "classified_intent": None,
    "detected_entities": {},
    "missed_entities": [],
    "matriculation_number": None,
    "course_name": None,
    "first_name": None,
    "last_name": None,
    "address": None,
    "city": None,
    "post_code": None,
}

# Implementation of chatbot memory
CONFIRMATION_CONTEXT_TEMPLATE = {
    "summary": None,
    "classified_intent": None,
    "detected_entities": {}
}

# Converting variable names to human readable text
HUMAN_READABLE_ENTITY = {
    'matriculation_number': "matriculation number",
    'course_name': 'course name',
    'address': 'address',
    'city': 'city',
    'post_code': 'post code',
    'first_name': 'first name',
    'last_name': 'last name'
}

user_context = USER_CONTEXT_TEMPLATE.copy()
confirmation_context = CONFIRMATION_CONTEXT_TEMPLATE.copy()

def chatbot_response(user_input):
    global user_context, confirmation_context

    # check if meta text or question
    rule_based_intent = match_rule_based_intent(user_input)
    
    # check if it is reset command to refresh memory
    if rule_based_intent == "reset_command":
        # clean user and confirmation context
        return clear_all_contexts()

    # check complexity of user input
    complex_request = is_complex_request(user_input)
    if not complex_request and rule_based_intent:
        # generate response according to rule-based intent
        return generate_rule_based_response(rule_based_intent)

    # check if the chatbot is waiting for confirmation
    if confirmation_context["summary"]:
        return handle_confirmation(user_input)

    # check if the chatbot is waiting for missed entities
    if user_context["missed_entities"]:
        return handle_missing_entities(user_input)

    # classify intent, retrive confidenece, detect entities and check if there are missed entities
    classified_intent, confidence, detected_entities, missed_entities = chatbot_classification_with_entity_validation(user_input)

    log_classification(classified_intent, confidence, detected_entities, missed_entities)

    # classified intent's confidence should higher 0.9
    if confidence >= 0.9:
        update_user_context(classified_intent, detected_entities, missed_entities)
        store_entities_in_memory(detected_entities)
    else:
        return "Sorry, I couldn't identify the correct action to take."

    # check if user missed entities
    if missed_entities:
        return request_missing_information(missed_entities)

    return summarize_and_confirm_request(classified_intent, detected_entities)

# Cleaning chatbot memory
def clear_all_contexts():
    global user_context, confirmation_context
    user_context = USER_CONTEXT_TEMPLATE.copy()
    confirmation_context = CONFIRMATION_CONTEXT_TEMPLATE.copy()
    print(f"LOG: clear_all_contexts: clean memory: user_context {user_context}, confirmation_context {confirmation_context}")
    return "All your details have been removed. How can I assist you now?"

# Handle user confirmation to perform further actions
def handle_confirmation(user_input):
    global confirmation_context
    if user_input.lower() in ["yes", "y", "correct", "+", "good"]:
        # retrive database method by classified intent from dictionary of database methods
        action = get_action_by_intent(confirmation_context["classified_intent"])
        response = process_user_request(action, confirmation_context["detected_entities"])
        # clean confirmation context
        confirmation_context["summary"] = None  
        return response
    elif user_input.lower() in ["no", "n", "wrong", "incorrect", "-"]:
        # clean confirmation context
        confirmation_context["summary"] = None  
        return "Request canceled. How else can I assist you?"
    else:
        return f"Please confirm: {confirmation_context['summary']}"

# handle user input for missed entities
def handle_missing_entities(user_input):
    global user_context

    # NER model to recognize entities
    detected_entities = entity_validation(user_input)

    # store new entities in user context
    store_entities_in_memory(detected_entities)
    user_context["detected_entities"].update(detected_entities)

    # update missed_entities if there are entity, that is not in detected_entities and user context
    user_context["missed_entities"] = [
        entity for entity in user_context["missed_entities"] if entity not in detected_entities and not user_context.get(entity)
    ]

    # check if there are still missing entities
    if user_context["missed_entities"]:
        next_missing_entity = user_context["missed_entities"][0]
        return f"Please provide the {HUMAN_READABLE_ENTITY[next_missing_entity]}"

    return process_request_with_context()

def log_classification(classified_intent, confidence, detected_entities, missed_entities):
    print(f"LOG: Classified Intent: {classified_intent}, Confidence: {confidence:.3f}")
    print(f"LOG: Detected Entities: {detected_entities}")
    print(f"LOG: Missed Entities: {missed_entities}")

def update_user_context(classified_intent, detected_entities, missed_entities):
    global user_context
    user_context["classified_intent"] = classified_intent
    user_context["detected_entities"].update(detected_entities)
    user_context["missed_entities"] = missed_entities

def request_missing_information(missed_entities):
    global user_context
    detected_entities = user_context["detected_entities"]
    remaining_missed_entities = []

    required_entities = [
        "matriculation_number", "course_name", "first_name", "last_name", "address", "city", "post_code"
    ]

    # check if missing entity exists in user context
    for missing_entity in missed_entities:
        if missing_entity in required_entities and user_context.get(missing_entity):
            detected_entities[missing_entity] = user_context[missing_entity]
        else:
            remaining_missed_entities.append(missing_entity)

     # check there are still missing entities, that are not in user context
    if not remaining_missed_entities:
        return process_request_with_context()

    return f"Please provide the {HUMAN_READABLE_ENTITY[remaining_missed_entities[0]]}"


def get_action_by_intent(classified_intent):
    print(f'LOG: get_action_by_intent: {classified_intent}')
    action = actions.get(classified_intent)
    if not action:
        return "Sorry, I couldn't identify the correct action to take."
    return action

def process_user_request(action, detected_entities):
    print(f'LOG: process_user_request: action {action}, detected_entities {detected_entities}')
    try:
        # taking necessary entities for current method
        required_entities = intents_entities.get(action.__name__, [])
        action_arguments = {key: value for key, value in detected_entities.items() if key in required_entities}
        return action(**action_arguments)
    except Exception as e:
        return f"An error occurred while performing the operation: {str(e)}"

# Perform user's request
def process_request_with_context():
    global user_context
    classified_intent = user_context["classified_intent"]
    detected_entities = user_context["detected_entities"].copy()
    required_entities = intents_entities.get(classified_intent, [])
    for entity in required_entities:
        if entity not in detected_entities and user_context.get(entity):
            detected_entities[entity] = user_context[entity]

    # perform database operation or generation confirmation text
    response = summarize_and_confirm_request(classified_intent, detected_entities)

    # clean user context except for user fields
    reset_user_context_except_memory()
    return response

# store detected entities in user context
def store_entities_in_memory(detected_entities):
    for key in USER_CONTEXT_TEMPLATE:
        if key in detected_entities:
            user_context[key] = detected_entities[key]
    print(f"LOG: store_entities_in_memory: {user_context}")

# clean user context except for user fields
def reset_user_context_except_memory():
    global user_context
    memory_fields = ["matriculation_number", "course_name", "first_name", "last_name", "address", "city", "post_code"]
    user_context = {key: user_context[key] for key in memory_fields}
    user_context.update({"classified_intent": None, "detected_entities": {}, "missed_entities": []})

# perform database operation or generation confirmation text
def summarize_and_confirm_request(intent, detected_entities):
    global confirmation_context

    required_entities = intents_entities.get(intent, [])
    
    relevant_entities = {key: value for key, value in detected_entities.items() if key in required_entities}

    entity_summary = ", ".join(f"{HUMAN_READABLE_ENTITY[key]} - {value}" for key, value in relevant_entities.items())

    # if this operation is query data from database, perform operation, otherwise ask confirmation    
    if intent in READING_DATABASE:
        action = get_action_by_intent(intent)
        return process_user_request(action, relevant_entities)
    elif intent in WRITING_DATABASE:
        summary = f"You want to {intent.replace('_', ' ')} with the following details: {entity_summary}. Is this correct?"
        confirmation_context.update({
            "summary": summary,
            "classified_intent": intent,
            "detected_entities": relevant_entities
        })
        return summary
    
    return "Sorry, I couldn't identify the correct operation type."
