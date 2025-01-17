from tensorflow.keras.models import load_model # type: ignore
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
import numpy as np # type: ignore

model = load_model('../models/intent_lstm_model.keras')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

with open('../models/tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)
with open('../models/label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)

# Each intent requires its own entites
intents_entities = {
    "change_first_name": ["matriculation_number", "first_name"],
    "change_last_name": ["matriculation_number", "last_name"],
    "change_address": ["matriculation_number", "address", "city", "post_code"],
    "register_exam": ["matriculation_number", "course_name"],
    "deregister_exam": ["matriculation_number", "course_name"],
    "query_exam_status": ["matriculation_number", "course_name"],
    "query_exam_grade": ["matriculation_number", "course_name"],
    "query_student_profile": ["matriculation_number"],
}

# Intent Classifier model
def lstm_classification_intent(text):
    text = text.lower()
    
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=model.input_shape[1], padding='post')
    
    prediction = model.predict(padded_sequence)
    
    predicted_index = np.argmax(prediction, axis=1)[0]
    classified_intent = label_encoder.inverse_transform([predicted_index])[0]
    confidence = np.max(prediction)
    
    return classified_intent, confidence
