---------------------------------------------------------------------------------------------------------------------------------------------------
**Table of Contents**
- [Quick Start ](#quick-start-)
- [Setting Up ](#setting-up-)
- [Dependencies ](#dependencies-)
- [Usage ](#usage-)
- [Security Note ](#security-note-)
- [Troubleshooting ](#troubleshooting-)
- [Contact ](#contact-)

---------------------------------------------------------------------------------------------------------------------------------------------------
## Quick Start <a name="quick-start"></a>
1. Acquire an API key for ChatGPT from your OpenAI account website.
2. Clone this repository to your local machine.
3. In the repository directory, create a file named "chatgpt_api_key.txt" and paste your API key into it.
4. Visit https://redditcommentsearch.com/, search for comments from the target profile, save the results as `{username}.html` and place it in the directory.
5. Run the script using the command "python main.py yourusername".


---------------------------------------------------------------------------------------------------------------------------------------------------
## Setting Up <a name="setting-up"></a>
Ensure you have Python installed. If not, [download](https://www.python.org/downloads/) and install any version of Python. Set up your environment variables for command line usage. 

---------------------------------------------------------------------------------------------------------------------------------------------------
## Dependencies <a name="dependencies"></a>
Install the following Python packages:

pip install openai
pip install pandas
pip install beautifulsoup4


---------------------------------------------------------------------------------------------------------------------------------------------------
## Usage <a name="usage"></a>
Once you have all the necessary files in your directory:
- `main.py`
- `chatgpt_core.py`
- `chatgpt_api_key.txt`
- `yourusername.html`

Run the script by opening a command line in the directory and executing: 

```python main.py yourusername```

The final analysis will be saved as "yourusername_synthesized_profile.txt" in the directory.

---------------------------------------------------------------------------------------------------------------------------------------------------
## Security Note <a name="security-note"></a>
Always ensure you're using trusted scripts. Review the content of the scripts to ensure that no malicious actions, like sending your API keys elsewhere, are taking place. 

---------------------------------------------------------------------------------------------------------------------------------------------------
## Troubleshooting <a name="troubleshooting"></a>
If you encounter any errors during the execution, ChatGPT is a reliable tool to diagnose and solve issues. Paste the error messages to ChatGPT for guidance.

---------------------------------------------------------------------------------------------------------------------------------------------------
## Contact <a name="contact"></a>
For questions, concerns, or suggestions, reach out on reddit at /u/Grays42.
