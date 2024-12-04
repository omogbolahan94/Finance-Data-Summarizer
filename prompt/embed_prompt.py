from data_handler import extract_text_from_text
from app import text_splitter_recursive
from data_handler import search_documents


with open('Prompt template (1).docx', 'r') as file:
    document_text = extract_text_from_docx(file)

prompt_chunks = text_splitter_recursive.split_text(prompt.page_content)

# iterate through each of the prompt
generated_prompt = " "

for input_text in prompt_chunks:
  results = search_documents(input_text)
  for doc in results:
      generated_prompt += doc['metadata']['text']

  generated_prompt += '\n\n'