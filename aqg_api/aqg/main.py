import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import time
from django.conf import settings
from langchain_community.vectorstores import FAISS
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import json
from bert_score import score
  

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
class AQG:
    def __init__(self, topic):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key = os.getenv("GOOGLE_API_KEY"),
            model="models/text-embedding-004"
        )

        self.bert_model = "distilbert-base-uncased"  #'bert-base-uncased'

        self.tunned_model_name = 'gemini-1.5-flash'
        #'tunedModels/devfinetuning-nwnreiak3wnm'
        #'tunedModels/squad-20-finetuning-4wit82ep3wqb'
        #"tunedModels/v2transformeddata900-7cugacwfz6aq"
        #"tunedModels/v2transformeddata900-azdrbcm78c87" 
        #"tunedModels/squadtransformeddata200-4accjjr8ziho"
        #"tunedModels/v2transformeddata700-ld43ej64c3vp" 
        #"tunedModels/transformeddata700-9qzhm7id6ado" 
        #'tunedModels/squadtransformeddata200-4accjjr8ziho'  

        self.vectorstore = FAISS.load_local(
            settings.VECTOR_DB_DIR, 
            self.embeddings,
            allow_dangerous_deserialization=True 
        )
        
        # self.client = genai.Client(api_key = os.getenv("GOOGLE_API_KEY"))  

        self.tunnedModel = genai.GenerativeModel(
            model_name = self.tunned_model_name,
            generation_config= {
                "temperature": 0.5,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 500,
                "response_mime_type": "text/plain",
            },
        )

        self.client = self.tunnedModel
            
        self.topic = topic
        
    def generator(self, num_questions, context, topic = ""):     
                            
        prompt = f"""
            Your task is to generate {num_questions} questions based on the context below. 
            Each question is separate by a new line   
            Instruction:
             - Only use WH-questions.
             - Avoid overly complex sentence structures and make sure each question has a clear focus.
             - The questions should be specifically related to the context and avoid unnecessary broadness or vagueness.
             - Ensure the phrasing and structure of the questions are similar to wordings in the context.
             - The questions should be short and simple.
            Context:
            {context}
            """
                
        
        response = self.client.generate_content(prompt)
        
        print(response.text)
        
        questions = []

        for line in response.text.split("\n"):
            if(len(line) > 0):
                questions.append(line)
        
        print(questions)
        
        results = { 
            'topic': topic,
            'questions': questions
        }
        
        
        return results  
     
    def retriever(self, topic, num_documents):
           
            search_results = self.vectorstore.similarity_search_with_score(topic, k=num_documents)
            
            threshold = 0.7 
            
            filtered_results = [
                (doc, score) for doc, score in search_results if score <= threshold
            ]
            
            if len(filtered_results) == 0:
                return Response(
                    'No relevant content found for the given topic', 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return filtered_results
    
    def generator_evaluate(self):
        with open('aqg_api/aqg/evaluate_dataset/dev-v2.0.json', 'r') as f:
            squad_data = json.load(f)

        processed_data = []

        for article in squad_data["data"]:
            for paragraph in article["paragraphs"]:
                context_data = {
                    "context": paragraph["context"],
                    "qas": []
                }
                for qa in paragraph["qas"]:
                    question_data = {
                        "question": qa["question"],
                        "answers": [ans["text"] for ans in qa["answers"]]
                    }
                    context_data["qas"].append(question_data)
                
                processed_data.append(context_data)        
        
        max_f1_scores = []
        scores = []
        i = 0
        while i < len(processed_data):
            data = processed_data[i]
            context = data["context"]
            qas = data['qas']
            questions = [item['question'] for item in qas]

            response = self.generator(1, context, topic = context)            
            _generated_question = response['questions']
            
            _, _, F1 = score(
                _generated_question * len(questions), 
                questions, 
                lang="en", 
                rescale_with_baseline=True, 
                model_type="distilbert-base-uncased"
                )
            
            scores.append(max(F1).item())
            
            max_f1_scores.append({
                "max_f1": max(F1).item(),
                "ref_q": questions[F1.argmax().item()],
                "gen_q": _generated_question
            })
            
            print(i)
            i = i+1
            
            time.sleep(4)
            
        return {
            "max_f1_scores": max_f1_scores,
            "average_f1": sum(scores)/len(scores)
        } 
    