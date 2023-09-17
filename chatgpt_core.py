from openai.error import InvalidRequestError

import json
import openai
import pandas as pd

##-------------------start-of-GPTCore---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class GPTCore:

    ##-------------------start-of-init()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, instructions="You are a helpful assistant.", model="gpt-3.5-turbo", filename:str | None=None, inserts=None):

        """
        
        Initializes the GPTCore object.\n

        Parameters:\n
        instructions (str) : The instructions given to chatgpt when the conversation starts.\n
        model (str) : The GPT model to use. Defaults to "gpt-3.5-turbo".\n
        filename (str) : The filename to save the conversation history to. Defaults to None.\n
        inserts (dict) : A dictionary of keywords and their corresponding inserts. Defaults to None.\n

        Returns:\n
        GPTCore object.\n

        """

        self.model = model
        self.instructions = instructions
        self.filename = filename
        self.inserts = inserts if inserts else {}
        self.messages = pd.DataFrame(columns=["actor", "message", "sendable"])
        
        if(filename):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.messages = pd.DataFrame(data.get('messages', []))
                    self.model = data.get('model', model)
                    self.instructions = data.get('instructions', instructions)

            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"File {filename} was not found. This file will be generated to store conversation data.")

    ##-------------------start-of-add_message()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def add_message(self, message, actor="user"):

        """

        Adds a message to the conversation history.\n

        Parameters:\n
        self (object - GPTCore) : The GPTCore object.\n
        message (str) : The message to add to the conversation history.\n

        Returns:\n
        None.\n

        """

        ## Modify the user's message if it contains a keyword from the inserts

        if(message):
            for keyword, insert_text in self.inserts.items():
                if keyword in message:
                    message = f"{message}\n\n{insert_text}"

        ## For non-background messages, use concat to add to the dataframe
        new_entry = pd.DataFrame([{"actor": actor, "message": message, "sendable": True}])
        self.messages = pd.concat([self.messages, new_entry], ignore_index=True)

    ##-------------------start-of-generate_response()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def generate_response(self, message=None, store_message=True, retries=3):

        """

        Generates a response from the GPT model.\n

        Parameters:\n
        self (object - GPTCore) : The GPTCore object.\n
        message (str) : The message to generate a response to. Defaults to None.\n
        store_message (bool) : Whether to store the message in the conversation history. Defaults to True.\n
        retries (int) : The number of times to retry if the message is too long. Defaults to 3.\n

        Returns:\n
        assistant_message (str) : The response from the GPT model.\n

        """

        ## Compile the messages for GPT
        outbound_messages = [{"role": "system", "content": self.instructions}]
        for index, row in self.messages.iterrows():
            if(row['sendable']):
                actor_role = "user" if row['actor'] != "assistant" else "assistant"
                outbound_messages.append({
                    "role": actor_role,
                    "content": row['message']
                })

        ## Only append the user message if it's not None
        if(message is not None):
            outbound_messages.append({"role": "user", "content": message})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=outbound_messages
            )
            if not hasattr(response, 'choices'):
                raise AttributeError("The response object does not contain a 'choices' attribute.")
             
            assistant_message = response['choices'][0]['message']['content'] ## type: ignore (Seems to be a common issue with the openai library)

            ## If store_message is True, store the user and AI's messages to the history
            if(store_message and message is not None):
                self.add_message(message)

            if(store_message):
                self.add_message(assistant_message, actor="assistant")
            
            if(self.filename):
                self.save_chat()

            return assistant_message

        except InvalidRequestError as e:  ## Adjust this to the specific error class you expect
            ## Check if the error is due to too many tokens and if we have retries left
            if("Please reduce the length of the messages" in str(e) and retries > 0):
                ## Mark the oldest non-background sendable message as unsendable
                for index, row in self.messages.iterrows():
                    if row['sendable'] and row['actor'] != "background":
                        self.messages.at[index, 'sendable'] = False
                        break

                ## Recursive call with decremented retries
                return self.generate_response(message, store_message, retries-1)
            else:
                raise e

##-------------------start-of-save_chat()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def save_chat(self):

        """
        
        Saves the conversation history to a JSON file.\n

        Parameters:\n
        self (object - GPTCore) : The GPTCore object.\n

        Returns:\n
        None.\n

        """

        ## Convert the DataFrame to a list of dictionaries
        messages = self.messages.to_dict('records')

        chat_data = {
            "instructions": self.instructions,
            "messages": messages,
            "model": self.model
        }

        with open(self.filename, 'w') as f: ## type: ignore (filename is not None)
            json.dump(chat_data, f, indent=4)

##-------------------start-of-main()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Load API key from the text file

try:
    with open('chatgpt_api_key.txt', 'r') as file:
        openai.api_key = file.read().strip()

except FileNotFoundError:
    raise FileNotFoundError("API key file 'chatgpt_api_key.txt' not found in the directory where chat_gpt_core.py is stored. Please create this file, the contents of which should be your api key (and nothing else).")
