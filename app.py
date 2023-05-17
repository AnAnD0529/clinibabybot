from flask import Flask, request, render_template
from langchain import OpenAI
from llama_index import SimpleDirectoryReader, LangchainEmbedding, GPTListIndex,GPTSimpleVectorIndex, PromptHelper
from llama_index import LLMPredictor, ServiceContext
import os
from algorithm import find_most_similar_file 

os.environ['OPENAI_API_KEY'] = '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'

# Set up the index
def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 256
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 200

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.4, model_name="text-davinci-002", max_tokens=num_outputs))

    files = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    gen_index = GPTSimpleVectorIndex.from_documents(files, service_context=service_context)

    gen_index.save_to_disk('index.json')

    return gen_index

# Load the index
index = construct_index('C:/Users/anand.k/Desktop/dim/cleaned_fiels/data')

# Set up the Flask app
app = Flask(__name__)

# Define the route for the chatbot page
@app.route('/')
def chatbot():
    return render_template('chatbot.html')

# Define the route for the chatbot response API
@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    query = request.form['query']
    if not query:
        # If the user entered nothing
        return "Please enter a vaild input."
    elif len(query) <= 4:
        # If the user entered less than 4 characters
        return "Your message is too short. Please enter a message with at least 4 characters."
    else:
        # If the user entered a valid message
        response = index.query(query, response_mode="compact").response
        # Split the response into a list of sentences
        sentences = response.split('. ')
        #get the similar file name
        most_similar_file = find_most_similar_file(response, "C:/Users/anand.k/Desktop/dim/static/docx_files")
        most_similar_file = most_similar_file.replace (".docx", ".pdf")
        most_similar_file = most_similar_file.replace (" ", "_")
        # Modify this return statement
    return '<span style="color: black;"><strong>Bot:</strong></span>'+'<ul style="font-family: Segoe UI; background-color: #F0F0F0; border-radius: 6px !important; color: royalblue !important;">' + ''.join(['<li> ' + sentence.strip() + '</li>' for sentence in sentences]) + '</ul>' + \
           '<p><b>Learn more:</b> <a href="/static/manuals/' + most_similar_file + '" target="_blank">' + most_similar_file + '</a></p>'



    #return '<ol style="font-family:Segoe UI; background-color: #F0F0F0; border-radius:6px !important; color:royalblue !important;" ><span style="color:black;"><strong>Bot:</strong></span>' + ''.join(['<li> ' + sentence.strip() + '</li>' for sentence in sentences]) + \
           #'<p><b>Learn more :</b> <a href=/static/manuals/'+ most_similar_file +' target="_blank">' + most_similar_file + '</a></p>'




if __name__ == '__main__':
    app.run(debug=True)


"""    return '<ol>' + ''.join(['<li>' + sentence.strip() + '</li>' for sentence in sentences]) + '</ol>' + \
           '<p>The most similar file to your query is: ' + most_similar_file + '</p>' 
           # prints the response as a unordered list
           """





"""return '<ol start="1">' + ''.join(['<li>' + sentence.strip().replace('*', str(index) + '.', 1) + '</li>' for index, sentence in enumerate(sentences, start=1)]) + '</ol>' + \
           '<p>The most similar file to your query is: <a href="'+ similar_file +'">' + similar_file + '</a></p>'
"""