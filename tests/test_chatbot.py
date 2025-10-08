"""
Unit tests for Modern Rule-Based Chatbot
"""
import unittest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot import (
    ModernRuleBasedChatbot, 
    ConversationContext, 
    SentimentAnalyzer, 
    Intent, 
    Response
)

class TestSentimentAnalyzer(unittest.TestCase):
    """Test cases for SentimentAnalyzer class"""
    
    def setUp(self):
        self.analyzer = SentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        self.assertEqual(self.analyzer.analyze("I love this amazing product!"), 'positive')
        self.assertEqual(self.analyzer.analyze("This is great and wonderful"), 'positive')
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        self.assertEqual(self.analyzer.analyze("I hate this terrible product"), 'negative')
        self.assertEqual(self.analyzer.analyze("This is bad and awful"), 'negative')
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection"""
        self.assertEqual(self.analyzer.analyze("The weather is okay"), 'neutral')
        self.assertEqual(self.analyzer.analyze("Hello there"), 'neutral')
    
    def test_mixed_sentiment(self):
        """Test mixed sentiment (should return neutral)"""
        self.assertEqual(self.analyzer.analyze("I love this but hate that"), 'neutral')

class TestConversationContext(unittest.TestCase):
    """Test cases for ConversationContext class"""
    
    def setUp(self):
        self.context = ConversationContext()
    
    def test_add_exchange(self):
        """Test adding conversation exchanges"""
        self.context.add_exchange("Hello", "Hi there!")
        self.assertEqual(len(self.context.history), 1)
        self.assertEqual(self.context.history[0], ("Hello", "Hi there!"))
    
    def test_history_limit(self):
        """Test that history is limited to 10 exchanges"""
        for i in range(15):
            self.context.add_exchange(f"Message {i}", f"Response {i}")
        
        self.assertEqual(len(self.context.history), 10)
        # Should keep the last 10 exchanges
        self.assertEqual(self.context.history[0], ("Message 5", "Response 5"))
        self.assertEqual(self.context.history[-1], ("Message 14", "Response 14"))
    
    def test_get_recent_context(self):
        """Test getting recent context"""
        for i in range(5):
            self.context.add_exchange(f"Message {i}", f"Response {i}")
        
        recent = self.context.get_recent_context(3)
        self.assertEqual(len(recent), 3)
        self.assertEqual(recent[0], ("Message 2", "Response 2"))
        self.assertEqual(recent[-1], ("Message 4", "Response 4"))

class TestModernRuleBasedChatbot(unittest.TestCase):
    """Test cases for ModernRuleBasedChatbot class"""
    
    def setUp(self):
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.chatbot = ModernRuleBasedChatbot(self.temp_db.name)
    
    def tearDown(self):
        # Clean up temporary database
        os.unlink(self.temp_db.name)
    
    def test_greeting_intent(self):
        """Test greeting intent detection"""
        response = self.chatbot.process_input("Hello there!")
        self.assertEqual(response.intent, Intent.GREETING)
        self.assertIn("Hello", response.text)
    
    def test_farewell_intent(self):
        """Test farewell intent detection"""
        response = self.chatbot.process_input("Goodbye!")
        self.assertEqual(response.intent, Intent.FAREWELL)
        self.assertIn("Goodbye", response.text)
    
    def test_help_intent(self):
        """Test help intent detection"""
        response = self.chatbot.process_input("I need help")
        self.assertEqual(response.intent, Intent.HELP)
        self.assertIn("help", response.text.lower())
    
    def test_weather_intent(self):
        """Test weather intent detection"""
        response = self.chatbot.process_input("What's the weather like?")
        self.assertEqual(response.intent, Intent.WEATHER)
        self.assertIn("weather", response.text.lower())
    
    def test_thanks_intent(self):
        """Test thanks intent detection"""
        response = self.chatbot.process_input("Thank you very much!")
        self.assertEqual(response.intent, Intent.THANKS)
        self.assertIn("welcome", response.text.lower())
    
    def test_complaint_intent(self):
        """Test complaint intent detection"""
        response = self.chatbot.process_input("I have a problem with this")
        self.assertEqual(response.intent, Intent.COMPLAINT)
        self.assertIn("sorry", response.text.lower())
    
    def test_compliment_intent(self):
        """Test compliment intent detection"""
        response = self.chatbot.process_input("Good job!")
        self.assertEqual(response.intent, Intent.COMPLIMENT)
        self.assertIn("thank", response.text.lower())
    
    def test_question_intent(self):
        """Test question intent detection"""
        response = self.chatbot.process_input("What can you do?")
        self.assertEqual(response.intent, Intent.QUESTION)
        self.assertIn("question", response.text.lower())
    
    def test_unknown_intent(self):
        """Test unknown intent handling"""
        response = self.chatbot.process_input("asdfghjkl")
        self.assertEqual(response.intent, Intent.UNKNOWN)
        self.assertIn("not sure", response.text.lower())
    
    def test_confidence_scoring(self):
        """Test confidence scoring"""
        response = self.chatbot.process_input("Hello")
        self.assertGreater(response.confidence, 0.5)
        
        response = self.chatbot.process_input("asdfghjkl")
        self.assertEqual(response.confidence, 0.0)
    
    def test_response_structure(self):
        """Test response object structure"""
        response = self.chatbot.process_input("Hello")
        
        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.text, str)
        self.assertIsInstance(response.intent, Intent)
        self.assertIsInstance(response.confidence, float)
        self.assertIsInstance(response.context, dict)
    
    def test_context_management(self):
        """Test conversation context management"""
        self.chatbot.process_input("Hello")
        self.chatbot.process_input("How are you?")
        
        self.assertEqual(len(self.chatbot.context.history), 2)
    
    def test_database_operations(self):
        """Test database operations"""
        # Process a message to save to database
        self.chatbot.process_input("Hello")
        
        # Check if conversation was saved
        history = self.chatbot.get_conversation_history()
        self.assertGreater(len(history), 0)
        
        # Check statistics
        stats = self.chatbot.get_statistics()
        self.assertGreater(stats.get('total_conversations', 0), 0)
    
    def test_case_insensitive_matching(self):
        """Test case insensitive pattern matching"""
        response1 = self.chatbot.process_input("HELLO")
        response2 = self.chatbot.process_input("hello")
        response3 = self.chatbot.process_input("Hello")
        
        self.assertEqual(response1.intent, Intent.GREETING)
        self.assertEqual(response2.intent, Intent.GREETING)
        self.assertEqual(response3.intent, Intent.GREETING)
    
    def test_multiple_patterns(self):
        """Test multiple pattern matching"""
        greetings = ["hi", "hello", "hey", "greetings", "good morning"]
        
        for greeting in greetings:
            response = self.chatbot.process_input(greeting)
            self.assertEqual(response.intent, Intent.GREETING)
    
    def test_sentiment_integration(self):
        """Test sentiment analysis integration"""
        response = self.chatbot.process_input("I love this!")
        self.assertEqual(response.context['sentiment'], 'positive')
        
        response = self.chatbot.process_input("I hate this!")
        self.assertEqual(response.context['sentiment'], 'negative')
    
    def test_fallback_responses(self):
        """Test fallback response generation"""
        response = self.chatbot.process_input("xyzabc123")
        self.assertEqual(response.intent, Intent.UNKNOWN)
        self.assertIsInstance(response.text, str)
        self.assertGreater(len(response.text), 0)

class TestResponseClass(unittest.TestCase):
    """Test cases for Response dataclass"""
    
    def test_response_creation(self):
        """Test Response object creation"""
        response = Response(
            text="Hello!",
            intent=Intent.GREETING,
            confidence=0.8,
            context={'sentiment': 'positive'}
        )
        
        self.assertEqual(response.text, "Hello!")
        self.assertEqual(response.intent, Intent.GREETING)
        self.assertEqual(response.confidence, 0.8)
        self.assertEqual(response.context['sentiment'], 'positive')
    
    def test_response_without_context(self):
        """Test Response object creation without context"""
        response = Response(
            text="Hello!",
            intent=Intent.GREETING,
            confidence=0.8
        )
        
        self.assertIsNone(response.context)

class TestIntentEnum(unittest.TestCase):
    """Test cases for Intent enum"""
    
    def test_intent_values(self):
        """Test Intent enum values"""
        self.assertEqual(Intent.GREETING.value, "greeting")
        self.assertEqual(Intent.FAREWELL.value, "farewell")
        self.assertEqual(Intent.HELP.value, "help")
        self.assertEqual(Intent.WEATHER.value, "weather")
        self.assertEqual(Intent.THANKS.value, "thanks")
        self.assertEqual(Intent.COMPLAINT.value, "complaint")
        self.assertEqual(Intent.COMPLIMENT.value, "compliment")
        self.assertEqual(Intent.QUESTION.value, "question")
        self.assertEqual(Intent.UNKNOWN.value, "unknown")

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestSentimentAnalyzer,
        TestConversationContext,
        TestModernRuleBasedChatbot,
        TestResponseClass,
        TestIntentEnum
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
