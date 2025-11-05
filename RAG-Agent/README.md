RAG by definition stands for **R**etrieval **A**ugmented **G**eneration and roughly explained you can open a document and ask an LLM model about document content (e.g. 
ask to summarize content, ask for details that are not easy to find, etc.). <br>
Technologies used in the project: <br>
 - Backend - Flask. <br>
 - Frontend - Html and css. I've prompted Ollama for the frontend code (yes, I know - I'm lazy and I don't have the patience to build web pages on my own) and <br>
   I made some minor tweaks. <br>
 - LLM - ollama3.2. <br>
 - Vector database - Chroma. <br>
 - Agent framework - LangChain. <br>
 - Project management - uv. Dependencies in pyproject.toml as usual. 

 I have tested the system and it works properly with .pdf, .docx and .txt documents. 


<img width="975" height="318" alt="initial" src="https://github.com/user-attachments/assets/96f3f96a-90ca-4f3a-af99-fa4e320506cf" />
<img width="976" height="318" alt="file_selected" src="https://github.com/user-attachments/assets/6d3f571d-54d4-44b5-8c5f-306951777133" />
<img width="965" height="722" alt="rag_opened" src="https://github.com/user-attachments/assets/78c2bb6c-2111-4361-9270-ebe8ee6f8076" />
<img width="954" height="570" alt="question_answered" src="https://github.com/user-attachments/assets/dea0ad06-8699-4ad8-b39e-02ff57b93fd1" />
