import tiktoken
import openai
import json
import os

## OPENAI API ##
# Interface for interacting with the OpenAI GPT API
class ChatGPTInterface:
    # Fields
    openaiApiKey = None
    model        = None
    pricing      = None
    client       = None

    # Initialize the ChatGPTInterface with a specified model and pricing
    def __init__(self, model, pricing):  
        # Get the OpenAI API key from environment variables
        self.openaiApiKey = os.environ["OPENAI_API_KEY"]

        # Create an OpenAI client using the API key
        self.client = openai.OpenAI(api_key=self.openaiApiKey)

        # Set the model and pricing to be used
        self.model = model
        self.pricing = pricing


    # Estimate the cost for a given string based on the number of tokens
    def getPriceForString(self, prompt):
        numTokens = self.getNumTokensFromString(prompt)
        price = numTokens / 1e6 * self.pricing
        return price

    # Send a request to the OpenAI API and return the response message
    def sendRequest(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": prompt,
            }]
        )
        # Return the content of the response message
        return response.choices[0].message.content
    
    # Create a conversation and send multiple messages
    def createConversation(self):
        return ChatGPTConversation(self.client, self.model)

# Class to handle a conversation with the OpenAI GPT API
class ChatGPTConversation:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.messages = []

    # Send a message and get a reply
    def sendMessage(self, prompt):
        self.messages.append({'role': 'user', 'content': prompt})
        response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
        reply = response.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply

    # Get the full list of messages in the conversation
    def getMessages(self):
        return self.messages

    # Get the last available reply from the LLM
    def getLastReply(self):
        for message in reversed(self.messages):
                if message['role'] == 'assistant':
                    return message['content']
        return None

# Tokenizer for the ChatGPT model
class ChatGPTTokenizer:
    def __init__(self, encoder="cl100k_base"):
        self.encoder = encoder

    def getNumTokens(self, text):
        numTokens = len(tiktoken.get_encoding(self.encoder).encode(text))
        return numTokens

# Interface for interacting with the OpenAI GPT API in Batch mode
class ChatGPTBatchInterface:

    # Fields
    openaiApiKey    = None
    model           = None
    client          = None

    # Objects
    batchInputFile  = None
    batchOutputFile = None

    # Initialize the ChatGPTInterface with a specified model and pricing
    def __init__(self, model):  
        # Get the OpenAI API key from environment variables
        self.openaiApiKey = os.environ["OPENAI_API_KEY"]

       # Create an OpenAI client using the API key
        self.client = openai.OpenAI(api_key=self.openaiApiKey)

        # Set the model and pricing to be used
        self.model = model
    
    # List all batches
    def listBatches(self):
        # Get the list of batches
        batches = self.client.batches.list(limit=10)

        # Print the details of each batch
        print("--- 📋 Total Batches: {}".format(len(batches)))
        for i, batch in enumerate(batches, start=1):
            print("------ 🔹 Batch {}: {}".format(i, batch))
    
    # Create the input file in the correct jsonl format
    def prepareBatchJsonl(self, elements, outputPath):
        # Create a JSONL file from the list of elements
        with open(outputPath, 'w') as jsonlFile:
            for i,element in enumerate(elements):
                jsonlFile.write(json.dumps({
                    "custom_id"     : "request_{}".format(i),
                    "method"        : "POST",
                    "url"           : "/v1/chat/completions",
                    "body"          : {
                            "model"     : self.model,
                            "messages"  : [
                                {"role" : "system", "content": element}
                            ],
                            "max_tokens": 120000
                    }
                }) + '\n')

    # Create a batch on the OpenAI Client
    def createBatch(self, filePath):
        # Create a batch input file using the specified file path
        batchInputFile = self.client.files.create(
            file    = open(filePath, "rb"),
            purpose = "batch"
            )
        
        # Store it
        self.batchInputFile = batchInputFile

        # Return it
        return batchInputFile
        
    # Upload the batch input file to the OpenAI API
    def uploadBatch(self): 
        # Get the file ID of the input file
        batchInputFileId = self.batchInputFile.id

        # Create a batch job using the input file
        batchOutputFile = self.client.batches.create(
                input_file_id       = batchInputFileId,
                endpoint            = "/v1/chat/completions",
                completion_window   = "24h",
                metadata            = {
                    "description": "nightly eval job"
                }
            )
        
        # Store it
        self.batchOutputFile = batchOutputFile  

        # Save it
        self.saveBatchObject()

        # Return it
        return batchOutputFile
    
    # Save the batch output file to a JSON file
    def saveBatchObject(self):
        # Save the batchOutputFile to a JSON file
        outputFileName = "batchDetails_{}.json".format(self.batchOutputFile['id'])
        with open(outputFileName, 'w') as jsonFile:
            json.dump(self.batchOutputFile, jsonFile, indent=4)

    # Get the results of the batch job
    def getBatchResults(self):
        # Get the file ID of the output file
        fileResponse = self.client.files.content(self.outputFile.id)
        
        # Print the content of the output file and return
        print(fileResponse.text)
        return fileResponse.text
    
# Class to handle ChatGPT embeddings
class openAiEmbeddingsInterface:
    def __init__(self, model="text-embedding-3-small"):
        # Get the OpenAI API key from environment variables
        self.openaiApiKey = os.environ["OPENAI_API_KEY"]

        # Create an OpenAI client using the API key
        self.client = openai.OpenAI(api_key=self.openaiApiKey)

        # Set the model to be used for embeddings
        self.model = model

    # Generate embeddings for a given text
    def getEmbedding(self, text):
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )

        # Return the embedding vector
        return response.data[0].embedding