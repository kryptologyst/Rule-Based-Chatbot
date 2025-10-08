# Project 170. Modern Rule-Based Chatbot
# Description:
# A modern rule-based chatbot using advanced pattern matching, context awareness,
# sentiment analysis, and a web interface. Features conversation history,
# mock database integration, and improved user experience.

import re
import json
import sqlite3
import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Intent(Enum):
    """Enumeration of possible user intents"""
    GREETING = "greeting"
    FAREWELL = "farewell"
    HELP = "help"
    WEATHER = "weather"
    THANKS = "thanks"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"
    QUESTION = "question"
    UNKNOWN = "unknown"

@dataclass
class Response:
    """Data class for chatbot responses"""
    text: str
    intent: Intent
    confidence: float
    context: Optional[Dict] = None

class ConversationContext:
    """Manages conversation context and history"""
    
    def __init__(self):
        self.history: List[Tuple[str, str]] = []
        self.user_name: Optional[str] = None
        self.session_start = datetime.datetime.now()
        self.topics_discussed: List[str] = []
    
    def add_exchange(self, user_input: str, bot_response: str):
        """Add a conversation exchange to history"""
        self.history.append((user_input, bot_response))
        # Keep only last 10 exchanges to manage memory
        if len(self.history) > 10:
            self.history = self.history[-10:]
    
    def get_recent_context(self, n: int = 3) -> List[Tuple[str, str]]:
        """Get recent conversation context"""
        return self.history[-n:] if self.history else []

class SentimentAnalyzer:
    """Simple sentiment analysis for rule-based chatbot"""
    
    def __init__(self):
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'awesome', 'love', 'like', 'happy', 'pleased', 'satisfied'
        }
        self.negative_words = {
            'bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'frustrated',
            'disappointed', 'sad', 'upset', 'annoyed', 'problem', 'issue'
        }
    
    def analyze(self, text: str) -> str:
        """Analyze sentiment of text"""
        words = set(re.findall(r'\b\w+\b', text.lower()))
        
        positive_count = len(words.intersection(self.positive_words))
        negative_count = len(words.intersection(self.negative_words))
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

class ModernRuleBasedChatbot:
    """Modern rule-based chatbot with advanced features"""
    
    def __init__(self, db_path: str = "chatbot.db"):
        self.db_path = db_path
        self.context = ConversationContext()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.response_patterns = self._initialize_patterns()
        self._init_database()
    
    def _initialize_patterns(self) -> Dict[Intent, List[Dict]]:
        """Initialize response patterns for different intents"""
        return {
            Intent.GREETING: [
                {
                    'patterns': [r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b'],
                    'responses': [
                        "Hello! How can I help you today?",
                        "Hi there! What can I do for you?",
                        "Greetings! How may I assist you?"
                    ]
                }
            ],
            Intent.FAREWELL: [
                {
                    'patterns': [r'\b(bye|goodbye|see you|farewell|exit|quit)\b'],
                    'responses': [
                        "Goodbye! Have a great day!",
                        "See you later! Take care!",
                        "Farewell! It was nice chatting with you!"
                    ]
                }
            ],
            Intent.HELP: [
                {
                    'patterns': [r'\b(help|assist|support|guide)\b'],
                    'responses': [
                        "I'm here to help! What do you need assistance with?",
                        "Sure, I can assist you. Please describe your issue.",
                        "I'd be happy to help! What's on your mind?"
                    ]
                }
            ],
            Intent.WEATHER: [
                {
                    'patterns': [r'\b(weather|temperature|rain|sunny|cloudy)\b'],
                    'responses': [
                        "I'm not connected to a weather API yet, but I bet it's a beautiful day!",
                        "Weather information isn't available right now, but I hope you're having a great day!",
                        "I can't check the weather, but I'm sure it's lovely wherever you are!"
                    ]
                }
            ],
            Intent.THANKS: [
                {
                    'patterns': [r'\b(thanks|thank you|appreciate|grateful)\b'],
                    'responses': [
                        "You're welcome!",
                        "My pleasure!",
                        "Happy to help!",
                        "No problem at all!"
                    ]
                }
            ],
            Intent.COMPLAINT: [
                {
                    'patterns': [r'\b(problem|issue|complaint|wrong|error|bug|broken)\b'],
                    'responses': [
                        "I'm sorry to hear you're having an issue. Can you tell me more about it?",
                        "I understand your frustration. Let me help you resolve this.",
                        "I apologize for the inconvenience. What seems to be the problem?"
                    ]
                }
            ],
            Intent.COMPLIMENT: [
                {
                    'patterns': [r'\b(good job|well done|excellent|amazing|great work)\b'],
                    'responses': [
                        "Thank you so much! I appreciate your kind words.",
                        "That's very kind of you to say!",
                        "I'm glad I could help!"
                    ]
                }
            ],
            Intent.QUESTION: [
                {
                    'patterns': [r'\b(what|how|why|when|where|who|can you|could you)\b'],
                    'responses': [
                        "That's an interesting question! Let me think about that.",
                        "I'd be happy to help with that. Could you provide more details?",
                        "That's a great question! What specifically would you like to know?"
                    ]
                }
            ]
        }
    
    def _init_database(self):
        """Initialize SQLite database for conversation storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    intent TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    session_id TEXT NOT NULL
                )
            ''')
            
            # Create response patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS response_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    intent TEXT NOT NULL,
                    pattern TEXT NOT NULL,
                    response TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    def _detect_intent(self, user_input: str) -> Tuple[Intent, float]:
        """Detect user intent with confidence score"""
        user_input_lower = user_input.lower().strip()
        
        for intent, patterns_list in self.response_patterns.items():
            for pattern_group in patterns_list:
                for pattern in pattern_group['patterns']:
                    if re.search(pattern, user_input_lower, re.IGNORECASE):
                        # Calculate confidence based on pattern match strength
                        confidence = 0.8 if re.search(pattern, user_input_lower) else 0.6
                        return intent, confidence
        
        return Intent.UNKNOWN, 0.0
    
    def _get_response(self, intent: Intent, user_input: str) -> str:
        """Get appropriate response for detected intent"""
        if intent == Intent.UNKNOWN:
            return self._get_fallback_response(user_input)
        
        patterns_list = self.response_patterns.get(intent, [])
        if not patterns_list:
            return self._get_fallback_response(user_input)
        
        # Get responses for the intent
        responses = []
        for pattern_group in patterns_list:
            responses.extend(pattern_group['responses'])
        
        # Simple response selection (could be enhanced with ML)
        import random
        return random.choice(responses)
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Generate fallback response for unknown intents"""
        fallback_responses = [
            "I'm not sure how to respond to that. Could you rephrase?",
            "That's interesting! Can you tell me more about what you're looking for?",
            "I'm still learning! Could you try asking that in a different way?",
            "I don't quite understand. Could you provide more details?"
        ]
        
        # Use sentiment to customize fallback
        sentiment = self.sentiment_analyzer.analyze(user_input)
        if sentiment == 'negative':
            return "I'm sorry I couldn't help with that. Is there something else I can assist you with?"
        
        import random
        return random.choice(fallback_responses)
    
    def _save_conversation(self, user_input: str, response: str, intent: Intent, sentiment: str):
        """Save conversation to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversations 
                (timestamp, user_input, bot_response, intent, sentiment, session_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.datetime.now().isoformat(),
                user_input,
                response,
                intent.value,
                sentiment,
                str(self.context.session_start)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
    
    def process_input(self, user_input: str) -> Response:
        """Process user input and return response"""
        # Detect intent
        intent, confidence = self._detect_intent(user_input)
        
        # Analyze sentiment
        sentiment = self.sentiment_analyzer.analyze(user_input)
        
        # Generate response
        response_text = self._get_response(intent, user_input)
        
        # Create response object
        response = Response(
            text=response_text,
            intent=intent,
            confidence=confidence,
            context={'sentiment': sentiment, 'session_id': str(self.context.session_start)}
        )
        
        # Update context
        self.context.add_exchange(user_input, response_text)
        
        # Save to database
        self._save_conversation(user_input, response_text, intent, sentiment)
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, user_input, bot_response, intent, sentiment
                FROM conversations 
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT 20
            ''', (str(self.context.session_start),))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'timestamp': row[0],
                    'user_input': row[1],
                    'bot_response': row[2],
                    'intent': row[3],
                    'sentiment': row[4]
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"Failed to get conversation history: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get chatbot usage statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get total conversations
            cursor.execute('SELECT COUNT(*) FROM conversations')
            total_conversations = cursor.fetchone()[0]
            
            # Get intent distribution
            cursor.execute('''
                SELECT intent, COUNT(*) 
                FROM conversations 
                GROUP BY intent 
                ORDER BY COUNT(*) DESC
            ''')
            intent_distribution = dict(cursor.fetchall())
            
            # Get sentiment distribution
            cursor.execute('''
                SELECT sentiment, COUNT(*) 
                FROM conversations 
                GROUP BY sentiment 
                ORDER BY COUNT(*) DESC
            ''')
            sentiment_distribution = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'total_conversations': total_conversations,
                'intent_distribution': intent_distribution,
                'sentiment_distribution': sentiment_distribution,
                'session_start': self.context.session_start.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}

def main():
    """Main function to run the chatbot in console mode"""
    chatbot = ModernRuleBasedChatbot()
    
    print("🤖 Modern RuleBot: Hi! I'm an advanced rule-based chatbot.")
    print("Type 'bye', 'exit', or 'quit' to end the conversation.")
    print("Type 'stats' to see conversation statistics.")
    print("Type 'history' to see recent conversation history.")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['bye', 'exit', 'quit']:
                print("🤖 Modern RuleBot: Goodbye! 👋")
                break
            
            if user_input.lower() == 'stats':
                stats = chatbot.get_statistics()
                print("\n📊 Chatbot Statistics:")
                print(f"Total conversations: {stats.get('total_conversations', 0)}")
                print(f"Session started: {stats.get('session_start', 'Unknown')}")
                print("\nIntent distribution:")
                for intent, count in stats.get('intent_distribution', {}).items():
                    print(f"  {intent}: {count}")
                print("\nSentiment distribution:")
                for sentiment, count in stats.get('sentiment_distribution', {}).items():
                    print(f"  {sentiment}: {count}")
                continue
            
            if user_input.lower() == 'history':
                history = chatbot.get_conversation_history()
                print("\n📜 Recent Conversation History:")
                for entry in history[:5]:  # Show last 5
                    print(f"[{entry['timestamp'][:19]}] You: {entry['user_input']}")
                    print(f"[{entry['timestamp'][:19]}] Bot: {entry['bot_response']}")
                    print(f"Intent: {entry['intent']}, Sentiment: {entry['sentiment']}")
                    print("-" * 40)
                continue
            
            response = chatbot.process_input(user_input)
            print(f"🤖 Modern RuleBot: {response.text}")
            
            # Show confidence and intent for debugging
            if response.confidence < 0.7:
                print(f"   (Intent: {response.intent.value}, Confidence: {response.confidence:.2f})")
                
        except KeyboardInterrupt:
            print("\n🤖 Modern RuleBot: Goodbye! 👋")
            break
        except Exception as e:
            print(f"🤖 Modern RuleBot: Sorry, I encountered an error: {e}")

if __name__ == "__main__":
    main()
