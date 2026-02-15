import openai
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key
        
        self.textract = boto3.client(
            'textract',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

    def get_chat_response(self, prompt, context=""):
        system_prompt = "You are a helpful AI Patient Assistant. provide medical guidance but always include a disclaimer that you are not a doctor."
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context: {context}\n\nUser: {prompt}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error connecting to AI service: {str(e)}"

    def extract_lab_data(self, file_bytes):
        try:
            response = self.textract.analyze_document(
                Document={'Bytes': file_bytes},
                FeatureTypes=['FORMS', 'TABLES']
            )
            # Simplified parsing logic for demo purposes
            extracted_text = ""
            for item in response['Blocks']:
                if item['BlockType'] == 'LINE':
                    extracted_text += item['Text'] + "\n"
            return extracted_text
        except Exception as e:
            return f"Error extracting data: {str(e)}"

ai_service = AIService()
