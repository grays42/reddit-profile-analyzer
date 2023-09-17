# Reddit Profile Analyzer

A ChatGPT-based Reddit profile analyzer. (Bring your own API key.)

## Instructions (For the Complete Newbie)

> Note: For each of these instructions, ask ChatGPT how to do it! It's super informative. Simply copy the instruction you're not sure about, paste it into ChatGPT, and ask "How do I do this?". It will provide you with detailed step-by-step instructions.

### 1. Get an API key for ChatGPT.

You'll need to do this from your OpenAI account website, see their site for details. You will be billed to use this script, but it will be on the order of like...$0.10 for an average profile with several hundred comments. It cost me a couple bucks to do two dozen profiles when I posted on reddit with the script and offered to do profiles for people.

### 2. Install Python.

Install any version of Python and make sure to set up your environment variables to use the command line commands.

### 3. Install Necessary Packages

Install the required packages using the following command line prompts:
```sh
pip install openai
pip install pandas
pip install beautifulsoup4
```

### 4. Clone this Repository

Check out this repo and save it to a local folder.

> You may want to check out the prompts in main.py, I put the instructions near the top so they're easier to edit. In particular, I had both the chunk analysis and the synthesis scripts structure their output into specific categories that came up on the two dozen samples I ran on reddit. You can tailor these instructions to your preference.

### 5. Create API Key File

In this folder, create the file "chatgpt_api_key.txt" and enter your API key as the file's content.

> Security Note for Newbies: This is a very dangerous thing to do for an unknown script, because I *could* be a malicious actor who is stealing API keys and sending them to myself so I can run up your bill. You need to make sure you open and review the two script files to make sure that's not what I'm doing! (You will notice that the only place the API key is actually loaded is in chat_gpt_core.py at the top of the script, where it is assigned to openai.api_key, which is necessary for the openai package to run.)

### 6. Search for all comments from the target profile

Visit https://redditcommentsearch.com/ and type the username you want to summarize (you're only doing this for your own profile, riiiiight?) and click 'Search'.

### 7. Save the HTML File

Once all the results have loaded, save the HTML file and rename it to `{username}.html` (e.g., "grays42.html"). You can delete the folder containing extra files after renaming. Place the html file inside your directory.

### 8. Check your files.

 You should now have four files in your directory:
- `main.py`
- `chatgpt_core.py`
- `chatgpt_api_key.txt`
- `yourusername.html`

### 9. Run the script!

Open a command line in this directory (if you're in Win10 or Win11, type "cmd" into the address bar and it will pull right up) and run the following command: "python main.py yourusername" (e.g. "python main.py grays42")

- As individual analyses are performed, they will output to the command line. Each will take about 30 seconds to run.
- When the final analysis outputs, it will be located in the folder as "yourusername_synthesized_profile.txt".

### Get an error?

Paste it to ChatGPT! ChatGPT is fantastic at figuring out where errors are coming from and telling you how to fix them. You *should* only encounter errors like missing packages and the like, but if something big breaks (like redditcommentsearch.com changes their format) reach out to me to fix it.

I don't use github hardly at all except to post a script occasionally, so if you really need to contact me just message me on reddit at /u/Grays42.

Enjoy!
