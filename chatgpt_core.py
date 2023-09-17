# Note that this file was not purpose-made for the reddit history thing, I use it for other conversation scripts I've made and have removed a bunch of functions that aren't relevant.

import os
import json
import openai
import pandas as pd

# Load API key from the text file
try:
    with open('chatgpt_api_key.txt', 'r') as file:
        openai.api_key = file.read().strip()
except FileNotFoundError:
    raise FileNotFoundError("API key file 'chatgpt_api_key.txt' not found in the directory where chat_gpt_core.py is stored. Please create this file, the contents of which should be your api key (and nothing else).")

class ChatGptCore:
    def __init__(self, instructions="You are a helpful assistant.", model="gpt-3.5-turbo", filename=None, inserts=None):
        self.model = model
        self.instructions = instructions
        self.filename = filename
        self.inserts = inserts if inserts else {}
        self.messages = pd.DataFrame(columns=["actor", "message", "sendable"])
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.messages = pd.DataFrame(data.get('messages', []))
                    self.model = data.get('model', model)
                    self.instructions = data.get('instructions', instructions)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"File {filename} was not found. This file will be generated to store conversation data.")

    def add_message(self, message, actor="user"):
        """
        Adds a message to the conversation history.
        """
        # Modify the user's message if it contains a keyword from the inserts
        if message:
            for keyword, insert_text in self.inserts.items():
                if keyword in message:
                    message = f"{message}\n\n{insert_text}"

        # For non-background messages, use concat to add to the dataframe
        new_entry = pd.DataFrame([{"actor": actor, "message": message, "sendable": True}])
        self.messages = pd.concat([self.messages, new_entry], ignore_index=True)
        #print(self.messages)

    def generate_response(self, message=None, store_message=True, retries=5):
        # Compile the messages for GPT
        outbound_messages = [{"role": "system", "content": self.instructions}]
        for index, row in self.messages.iterrows():
            if row['sendable']:
                actor_role = "user" if row['actor'] != "assistant" else "assistant"
                outbound_messages.append({
                    "role": actor_role,
                    "content": row['message']
                })

        # Only append the user message if it's not None
        if message is not None:
            outbound_messages.append({"role": "user", "content": message})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=outbound_messages
            )
        except openai.error.RateLimitError:
            if retries > 0:
                time.sleep(20)  # Wait for 20 seconds before retrying
                return self.generate_response(message, store_message, retries, retries-1)
            else:
                raise  # Re-raise the exception if no retries left
        except openai.error.InvalidRequestError as e:  # Adjust this to the specific error class you expect
            # Check if the error is due to too many tokens and if we have retries left
            if "Please reduce the length of the messages" in str(e) and retries > 0:
                # Mark the oldest non-background sendable message as unsendable
                for index, row in self.messages.iterrows():
                    if row['sendable'] and row['actor'] != "background":
                        self.messages.at[index, 'sendable'] = False
                        break

                # Recursive call with decremented retries
                return self.generate_response(message, store_message, retries-1)
            else:
                raise e

        # If store_message is True, store the user and AI's messages to the history
        if store_message and message is not None:
            self.add_message(message)
        assistant_message = response.choices[0].message['content']
        if store_message:
            self.add_message(assistant_message, actor="assistant")
        
        if self.filename:
            self.save_chat()

        return assistant_message

    def save_chat(self):
        # Convert the DataFrame to a list of dictionaries
        messages = self.messages.to_dict('records')

        chat_data = {
            "instructions": self.instructions,
            "messages": messages,
            "model": self.model
        }

        with open(self.filename, 'w') as f:
            json.dump(chat_data, f, indent=4)
