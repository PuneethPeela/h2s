import openai
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.has_openai = self.openai_api_key and self.openai_api_key != 'your_openai_api_key_here'
        
        if self.has_openai:
            openai.api_key = self.openai_api_key
        
        # Only initialize AWS if credentials are provided
        try:
            aws_key = os.getenv('AWS_ACCESS_KEY_ID', '')
            if aws_key and aws_key != 'your_aws_access_key_here':
                self.textract = boto3.client(
                    'textract',
                    region_name=os.getenv('AWS_REGION', 'us-east-1'),
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
                )
            else:
                self.textract = None
        except Exception:
            self.textract = None

    def get_chat_response(self, prompt, context=""):
        # Use demo mode if OpenAI not configured
        if not self.has_openai:
            return self._get_demo_response(prompt)
        
        system_prompt = "You are a helpful AI Patient Assistant. Provide medical guidance but always include a disclaimer that you are not a doctor."
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context: {context}\n\nUser: {prompt}"}
                ],
                max_tokens=200,
                timeout=10  # 10 second timeout for faster responses
            )
            return response.choices[0].message.content
        except Exception as e:
            return self._get_demo_response(prompt, error=str(e))
    
    def _get_demo_response(self, message, error=None):
        """Intelligent demo responses when OpenAI unavailable"""
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ['symptom', 'sick', 'fever', 'pain', 'hurt', 'cough']):
            return ("🏥 **Health Concern Detected**\n\nI understand you're experiencing symptoms. While in demo mode, I can't provide AI-powered analysis, but I recommend:\n• Monitor your symptoms carefully\n• Stay hydrated and rest\n• Consult a healthcare professional if symptoms worsen\n\n⚠️ *Not medical advice. Configure OPENAI_API_KEY for full AI assistance.*")
        
        elif any(word in msg_lower for word in ['medication', 'medicine', 'drug', 'pill', 'prescription']):
            return ("💊 **Medication Query**\n\nIn production mode, I would provide detailed medication information. For now:\n• Check your prescriptions in the Medication Dashboard\n• Consult your pharmacist for drug interactions\n• Never adjust dosage without medical advice\n\n⚠️ *Demo mode - Configure API key for full functionality.*")
        
        elif any(word in msg_lower for word in ['appointment', 'doctor', 'visit', 'schedule']):
            return ("📅 **Care Navigation**\n\nUse the Appointments section to manage your healthcare visits. With full AI enabled, I would provide intelligent scheduling recommendations and specialist referrals.\n\n⚠️ *Demo response - Full AI available with API configuration.*")
        
        else:
            return (f"💬 **Message Received**: \"{message[:80]}{'...' if len(message) > 80 else ''}\"\n\nI'm operating in **demo mode** due to missing OpenAI API configuration. In production, I would provide context-aware medical assistance.\n\n**Try asking about**: symptoms, medications, or appointments!\n\n⚠️ *Configure OPENAI_API_KEY in .env for full AI capabilities.*")

    def extract_lab_data(self, file_bytes):
        if not self.textract:
            return "🧪 **Demo Mode**: AWS Textract not configured. In production, this would extract text from lab reports using OCR. Please configure AWS credentials for full functionality."
        
        try:
            response = self.textract.analyze_document(
                Document={'Bytes': file_bytes},
                FeatureTypes=['FORMS', 'TABLES']
            )
            extracted_text = ""
            for item in response['Blocks']:
                if item['BlockType'] == 'LINE':
                    extracted_text += item['Text'] + "\n"
            return extracted_text
        except Exception as e:
            return f"Error extracting data: {str(e)}"

ai_service = AIService()
