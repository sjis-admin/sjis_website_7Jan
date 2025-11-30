"""
Ollama LLM integration for the chatbot.
"""
import logging

logger = logging.getLogger(__name__)

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("Ollama package not installed. Chatbot will use rule-based responses only.")


class OllamaService:
    """
    Service for interacting with Ollama LLM.
    """
    
    def __init__(self, model='llama3.2:3b'):
        """
        Initialize Ollama service.
        
        Args:
            model: The Ollama model to use. Default is 'llama3.2:3b' (fast and efficient)
                   Other options: 'llama2', 'mistral', 'phi', etc.
        """
        self.model = model
        self.available = OLLAMA_AVAILABLE
        
        if self.available:
            self._check_ollama_connection()
    
    def _check_ollama_connection(self):
        """Check if Ollama is running and accessible."""
        try:
            # Try to list available models
            ollama.list()
            logger.info(f"Successfully connected to Ollama. Using model: {self.model}")
        except Exception as e:
            logger.warning(f"Ollama is installed but not running: {e}")
            self.available = False
    
    def generate_response(self, user_message, context):
        """
        Generate a response using Ollama.
        
        Args:
            user_message: The user's question
            context: Retrieved context from the database
            
        Returns:
            Generated response text or None if Ollama unavailable
        """
        if not self.available:
            return None
        
        try:
            # Build the prompt
            system_prompt = (
                "You are a helpful AI assistant for St. Joseph International School (SJIS). "
                "Answer questions based on the provided school information. "
                "Be friendly, professional, and concise. "
                "If you don't have enough information to answer, say so politely. "
                "Keep responses under 300 words."
            )
            
            user_prompt = f"""User Question: {user_message}

School Information:
{context}

Please answer the question based on the school information provided above. Be helpful and conversational."""
            
            # Call Ollama
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user',
                        'content': user_prompt
                    }
                ],
                options={
                    'temperature': 0.7,  # Balance between creativity and consistency
                    'top_p': 0.9,
                    'num_predict': 400,  # Max tokens
                }
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            logger.error(f"Error generating Ollama response: {e}")
            return None
    
    def is_available(self):
        """Check if Ollama is available."""
        return self.available
