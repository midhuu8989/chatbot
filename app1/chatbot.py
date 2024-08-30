import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from .models import Ticket

def load_data():
    # Load data from the Django model
    tickets = Ticket.objects.all().values('hw_type', 'apps_sw', 'report_type', 'report_desc', 'act_taken')
    df = pd.DataFrame.from_records(tickets)
    return df

def preprocess_data(df):
    # Preprocess data
    for col in ['hw_type', 'apps_sw', 'report_type', 'report_desc', 'act_taken']:
        df[col] = df[col].str.lower().fillna('')
    df['combined'] = df['hw_type'] + ' ' + df['apps_sw'] + ' ' + df['report_type'] + ' ' + df['report_desc']
    return df

def train_model(df):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['combined'], df['act_taken'], test_size=0.2, random_state=42)
    # Create and train a model pipeline
    model = make_pipeline(TfidfVectorizer(), RandomForestClassifier())
    model.fit(X_train, y_train)
    return model

# Load, preprocess data, and train the model once when the module is loaded
df = preprocess_data(load_data())
model = train_model(df)

# Function to recommend action based on user input
'''def recommend_action(hw_type, apps_sw, report_type, report_desc):
    combined_input = hw_type + ' ' + apps_sw + ' ' + report_type + ' ' + report_desc
    action = model.predict([combined_input])[0]
    return action'''
def recommend_action(hw_type, apps_sw, report_type, report_desc):
    # Ensure all fields are strings
    
    
    # Combine fields into a single string
    combined_input = hw_type + ' ' + apps_sw + ' ' + report_type + ' ' + report_desc
    
    # Predict the action
    action = model.predict([combined_input])[0]
    return action

# Function to handle user messages
def respond(hw_type, apps_sw, report_type, report_desc, chat_history):
    action = recommend_action(hw_type, apps_sw, report_type, report_desc)
    bot_message = f"Recommended Action: {action}"
    chat_history.append((f"Hardware Type: {hw_type}\nSoftware/Application: {apps_sw}\nReport Type: {report_type}\nProblem Description: {report_desc}", bot_message))
    return hw_type, apps_sw, report_desc, chat_history
