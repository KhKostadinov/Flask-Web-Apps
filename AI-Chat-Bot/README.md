This is a minimalistic, as simple as possible customer service chat bot. It is programmed on Python 3.12 - Flask for the backend and ollama's llama3.2 powering the AI 
bot functionallity. I have used gpt-oss via Ollama UI directly installed on my PC. The project was built with uv and requirements are stored in pyproject.toml. In order
to run the project please follow the below steps (assuming you have Python installed already):

1. Install uv (if you don't have it already) - pip install uv
2. Create project folder
3. Open terminal and navigate to project folder, then run "uv init" which will create virtual environment in .venv folder
4. Paste all other files and folders (except .venv) in main project folder
5. Run "uv run main.py" - flask serves by default on port 127.0.0.1:5000 and you can interact with the chat bot via browser of your choice.

.venv was created automatically with "uv init" and I understandably didn't upload it here due to it's size and complexity. I have created a placeholder folder with the same name 
on GitHub to keep the same project structure as created by uv on my PC. Tested on Windows 11 and Mozilla. 
instructions.txt stores details about fictional cyber security company named Omega CyberSec and some minor instructions about bot behaviour. Enjoy chatting with Kevin :)
N.B.: llama3.2 is most probably NOT the best LLM choice for a chat bot, however it is good enough to start practice in the field of AI. 
PS: If you send "bye" conversation will end and you will be redirected to a "goodbye" page and Kevin will be deleted as a separate model. This page also gives you option 
to go back to initial page and start new conversation. 
