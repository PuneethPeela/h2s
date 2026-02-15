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
        
        # Medical knowledge base for intelligent demo responses
        self.medical_knowledge = self._load_medical_knowledge()

    def _load_medical_knowledge(self):
        """Comprehensive medical knowledge for intelligent demo responses"""
        return {
            'symptoms': {
                'fever': {
                    'advice': 'Monitor temperature, stay hydrated, rest. Seek immediate care if fever >103°F or lasts >3 days.',
                    'red_flags': 'Severe headache, difficulty breathing, persistent vomiting'
                },
                'cough': {
                    'advice': 'Stay hydrated, humidifier may help. Persistent cough >2 weeks needs evaluation.',
                    'red_flags': 'Blood in mucus, chest pain, difficulty breathing'
                },
                'headache': {
                    'advice': 'Rest in quiet dark room, hydrate. Consider OTC pain relievers.',
                    'red_flags': 'Sudden severe headache, vision changes, confusion, neck stiffness'
                },
                'stomach pain': {
                    'advice': 'Light diet (BRAT: bananas, rice, applesauce, toast), stay hydrated.',
                    'red_flags': 'Severe pain, blood in stool, persistent vomiting, fever'
                }
            },
            'medications': {
                'general': 'Always consult healthcare provider before starting/stopping medications.',
                'interactions': 'Inform doctor of ALL medications including supplements.',
                'timing': 'Take medications as prescribed, same time each day for consistency.'
            },
            'preventive_care': {
                'checkups': 'Annual physical recommended for adults.',
                'screenings': 'Age-appropriate screenings (mammogram, colonoscopy, etc.).',
                'vaccinations': 'Stay current with recommended vaccines.'
            }
        }

    def get_chat_response(self, prompt, context=""):
        """Highly intelligent AI assistant with real medical knowledge"""
        # Use demo mode if OpenAI not configured
        if not self.has_openai:
            return self._get_intelligent_demo_response(prompt, context)
        
        system_prompt = """You are an expert AI Medical Assistant with deep medical knowledge.
        Provide accurate, helpful medical guidance while always including appropriate disclaimers.
        Be empathetic, clear, and concise. Always recommend professional medical consultation for serious concerns."""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "assistant", "content": context} if context else {"role": "system", "content": ""},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.7,
                timeout=10
            )
            return response.choices[0].message.content
        except Exception as e:
            return self._get_intelligent_demo_response(prompt, context)
    
    def _get_intelligent_demo_response(self, message, context=""):
        """Highly intelligent medical assistant - Demo mode with real medical knowledge"""
        msg_lower = message.lower()
        
        # Symptom Analysis
        if any(word in msg_lower for word in ['fever', 'temperature', 'hot', 'chills']):
            return self._format_medical_response(
                "Fever Assessment",
                self.medical_knowledge['symptoms']['fever']['advice'],
                "🚨 Seek immediate care if: " + self.medical_knowledge['symptoms']['fever']['red_flags'],
                "Monitor temperature every 4 hours, stay hydrated with water/electrolyte drinks"
            )
        
        elif any(word in msg_lower for word in ['cough', 'throat', 'congestion', 'cold']):
            return self._format_medical_response(
                "Respiratory Symptoms",
                self.medical_knowledge['symptoms']['cough']['advice'],
                "🚨 Warning signs: " + self.medical_knowledge['symptoms']['cough']['red_flags'],
                "Honey tea, steam inhalation, and adequate rest can help"
            )
        
        elif any(word in msg_lower for word in ['headache', 'migraine', 'head pain']):
            return self._format_medical_response(
                "Headache Management",
                self.medical_knowledge['symptoms']['headache']['advice'],
                "🚨 Emergency if: " + self.medical_knowledge['symptoms']['headache']['red_flags'],
                "Track triggers (stress, food, sleep) in a headache diary"
            )
        
        elif any(word in msg_lower for word in ['stomach', 'nausea', 'vomiting', 'diarrhea', 'abdominal']):
            return self._format_medical_response(
                "Gastrointestinal Concerns",
                self.medical_knowledge['symptoms']['stomach pain']['advice'],
                "🚨 Seek care if" + self.medical_knowledge['symptoms']['stomach pain']['red_flags'],
                "Avoid solid foods initially, gradually reintroduce bland foods"
            )
        
        # Medication Queries
        elif any(word in msg_lower for word in ['medication', 'medicine', 'drug', 'pill', 'prescription', 'dose']):
            return self._format_medical_response(
                "Medication Information",
                self.medical_knowledge['medications']['general'],
                "Important: " + self.medical_knowledge['medications']['interactions'],
                "Best Practice: " + self.medical_knowledge['medications']['timing'],
                show_demo_note=True
            )
        
        # Appointment/Care Navigation
        elif any(word in msg_lower for word in ['appointment', 'doctor', 'visit', 'schedule', 'specialist']):
            return ("📅 **Care Navigation Assistance**\n\n"
                   f"Based on your query: \"{message[:60]}...\"\n\n"
                   "**Recommendations:**\n"
                   "• Use the Appointments section to schedule visits\n"
                   "• Primary care for general health concerns\n"
                   "• Specialists for specific conditions (referral usually needed)\n"
                   "• Urgent care for non-emergency immediate needs\n"
                   "• Emergency room for life-threatening situations\n\n"
                   "⚕️ *With full AI enabled, I would provide intelligent specialist recommendations and optimal scheduling.*\n\n"
                   "⚠️ Demo Mode Active")
        
        # General Health Query
        else:
            return (f"💬 **Medical Assistant Response**\n\n"
                   f"Query: \"{message[:100]}{'...' if len(message) > 100 else ''}\"\n\n"
                   "I understand your health concern. In demo mode, I'm providing general guidance.\n\n"
                   "**General Health Tips:**\n"
                   "• Stay hydrated (8 glasses water daily)\n"
                   "• Get adequate sleep (7-9 hours)\n"
                   "• Regular exercise (30 min most days)\n"
                   "• Balanced diet with fruits & vegetables\n"
                   "• Manage stress through relaxation techniques\n\n"
                   "**When to Seek Care:**\n"
                   "• Severe or worsening symptoms\n"
                   "• Symptoms lasting >1-2 weeks\n"
                   "• High fever, chest pain, difficulty breathing\n\n"
                   "⚕️ *Configure OPENAI_API_KEY for fully intelligent, context-aware medical assistance*\n\n"
                   "⚠️ Not a substitute for professional medical advice")
    
    def _format_medical_response(self, title, advice, warning, tip, show_demo_note=False):
        """Professional medical response formatting"""
        response = f"🏥 **{title}**\n\n"
        response += f"**Guidance:** {advice}\n\n"
        response += f"{warning}\n\n"
        response += f"💡 **Helpful Tip:** {tip}\n\n"
        
        if show_demo_note:
            response += "⚕️ *Full AI integration provides detailed drug information, interactions, and personalized recommendations*\n\n"
        
        response += "⚠️ **Medical Disclaimer:** This is general information, not medical advice. Consult healthcare professionals for personalized guidance. Demo mode active - configure OPENAI_API_KEY for advanced AI assistance."
        
        return response

    def extract_lab_data(self, file_bytes):
        """Extract text from lab reports using OCR"""
        if not self.textract:
            return ("🧪 **Lab Report Processing - Demo Mode**\n\n"
                   "AWS Textract OCR not configured. In production:\n"
                   "• Extracts all text from lab PDFs/images\n"
                   "• Identifies key values (glucose, cholesterol, etc.)\n"
                   "• Highlights abnormal results\n"
                   "• Provides AI-powered interpretation\n\n"
                   "Configure AWS credentials for full functionality.")
        
        try:
            response = self.textract.analyze_document(
                Document={'Bytes': file_bytes},
                FeatureTypes=['FORMS', 'TABLES']
            )
            extracted_text = ""
            for item in response['Blocks']:
                if item['BlockType'] == 'LINE':
                    extracted_text += item['Text'] + "\n"
            return extracted_text if extracted_text else "No text could be extracted from the document."
        except Exception as e:
            return f"Error processing lab report: {str(e)}"

ai_service = AIService()
