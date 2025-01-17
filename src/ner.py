from intent_classifier import intents_entities, lstm_classification_intent
import spacy # type: ignore
import string

def find_missed_entities(classified_intent, detected_entities):
    print(f'LOG find_missed_entities: classified_intent {classified_intent}, detected_entities {detected_entities}')
    required_entities = intents_entities.get(classified_intent, [])
    missed_entities = [entity for entity in required_entities if entity not in detected_entities]
    return missed_entities

# NER model usage
def chatbot_classification_with_entity_validation(user_input):
    print(f'LOG chatbot_classification_with_entity_validation: user_input {user_input}')
    classified_intent, confidence = lstm_classification_intent(user_input)

    nlp = spacy.load("../models/custom_ner_model")

    doc = nlp(user_input)
    detected_entities = {}
    for ent in doc.ents:
        clean_text = ent.text.strip(string.punctuation)
        detected_entities[ent.label_] = clean_text

    missed_entities = find_missed_entities(classified_intent, detected_entities)

    return classified_intent, confidence, detected_entities, missed_entities

# NER model for detection of missed entities
def entity_validation(user_input):
    print(f'LOG entity_validation: user_input {user_input}')
    nlp = spacy.load("../models/custom_ner_model")

    doc = nlp(user_input)
    detected_entities = {}
    for ent in doc.ents:
        clean_text = ent.text.strip(string.punctuation)
        detected_entities[ent.label_] = clean_text

    return detected_entities

nlp = spacy.load("de_core_news_lg")

# Checking the complexity of user input
def is_complex_request(user_input):
    doc = nlp(user_input)
    
    content_words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    
    verbs = [token for token in doc if token.pos_ == "VERB"]
    distinct_nouns = set(token.lemma_ for token in doc if token.pos_ == "NOUN")
    
    if len(verbs) > 1:
        return True
    if len(distinct_nouns) > 2:
        return True
    if len(content_words) > 5:
        return True
    
    return False
