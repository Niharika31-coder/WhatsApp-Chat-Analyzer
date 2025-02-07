import re
import pandas as pd

def preprocess(data):
    # Regex for your WhatsApp chat format
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s?[ap]m'

    # Print raw data for debugging
    print("Raw data preview:")
    print(data[:500])  # Print the first 500 characters

    # Split the data and extract dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Debugging: Print counts
    print(f"Number of messages: {len(messages)}")
    print(f"Number of dates: {len(dates)}")

    if len(messages) != len(dates):
        print("Warning: Number of messages and dates don't match!")

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_data': dates})

    # Parse date-time strings into pandas datetime
    try:
        df['message_date'] = pd.to_datetime(df['message_data'], format='%d/%m/%y, %I:%M %p', errors='coerce')
    except Exception as e:
        print(f"Error in date parsing: {str(e)}")
        return pd.DataFrame()

    # Extract user and message content
    users = []
    message_text = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 1:
            users.append(entry[1])
            message_text.append(entry[2])
        else:
            users.append('group_notifications')
            message_text.append(entry[0])

    df['user'] = users
    df['message'] = message_text
    df.drop(columns=['user_message', 'message_data'], inplace=True)

    # Extract additional info
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    return df

