"""
Configuration file for Modern Rule-Based Chatbot
"""
import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Database settings
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'chatbot.db')
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Chatbot settings
    MAX_CONVERSATION_HISTORY = int(os.environ.get('MAX_CONVERSATION_HISTORY', 10))
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', 0.6))
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'chatbot.log')
    
    # Sentiment analysis settings
    SENTIMENT_POSITIVE_WORDS = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
        'awesome', 'love', 'like', 'happy', 'pleased', 'satisfied',
        'brilliant', 'outstanding', 'perfect', 'superb', 'marvelous'
    }
    
    SENTIMENT_NEGATIVE_WORDS = {
        'bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'frustrated',
        'disappointed', 'sad', 'upset', 'annoyed', 'problem', 'issue',
        'horrible', 'disgusting', 'annoying', 'frustrating', 'disappointing'
    }
    
    # Response patterns configuration
    RESPONSE_PATTERNS = {
        'greeting': {
            'patterns': [r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b'],
            'responses': [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Greetings! How may I assist you?",
                "Hey! Nice to meet you. What brings you here?"
            ]
        },
        'farewell': {
            'patterns': [r'\b(bye|goodbye|see you|farewell|exit|quit)\b'],
            'responses': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Farewell! It was nice chatting with you!",
                "Bye! Feel free to come back anytime!"
            ]
        },
        'help': {
            'patterns': [r'\b(help|assist|support|guide)\b'],
            'responses': [
                "I'm here to help! What do you need assistance with?",
                "Sure, I can assist you. Please describe your issue.",
                "I'd be happy to help! What's on your mind?",
                "I'm ready to assist! How can I be of service?"
            ]
        },
        'weather': {
            'patterns': [r'\b(weather|temperature|rain|sunny|cloudy|forecast)\b'],
            'responses': [
                "I'm not connected to a weather API yet, but I bet it's a beautiful day!",
                "Weather information isn't available right now, but I hope you're having a great day!",
                "I can't check the weather, but I'm sure it's lovely wherever you are!",
                "Weather data isn't available, but I hope the skies are clear for you!"
            ]
        },
        'thanks': {
            'patterns': [r'\b(thanks|thank you|appreciate|grateful)\b'],
            'responses': [
                "You're welcome!",
                "My pleasure!",
                "Happy to help!",
                "No problem at all!",
                "Glad I could assist!"
            ]
        },
        'complaint': {
            'patterns': [r'\b(problem|issue|complaint|wrong|error|bug|broken)\b'],
            'responses': [
                "I'm sorry to hear you're having an issue. Can you tell me more about it?",
                "I understand your frustration. Let me help you resolve this.",
                "I apologize for the inconvenience. What seems to be the problem?",
                "I'm here to help fix this. Can you provide more details?"
            ]
        },
        'compliment': {
            'patterns': [r'\b(good job|well done|excellent|amazing|great work|brilliant)\b'],
            'responses': [
                "Thank you so much! I appreciate your kind words.",
                "That's very kind of you to say!",
                "I'm glad I could help!",
                "Your feedback means a lot to me!"
            ]
        },
        'question': {
            'patterns': [r'\b(what|how|why|when|where|who|can you|could you)\b'],
            'responses': [
                "That's an interesting question! Let me think about that.",
                "I'd be happy to help with that. Could you provide more details?",
                "That's a great question! What specifically would you like to know?",
                "I'm here to answer your questions! What would you like to know?"
            ]
        }
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    DATABASE_PATH = ':memory:'
    LOG_LEVEL = 'ERROR'

# Configuration mapping
config_map: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    config_class = config_map.get(config_name, DevelopmentConfig)
    return config_class()
