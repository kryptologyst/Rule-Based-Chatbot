#!/usr/bin/env python3
"""
Demo script for Modern Rule-Based Chatbot
This script demonstrates the chatbot's capabilities with various test cases
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import ModernRuleBasedChatbot, Intent
import time

def print_separator(title=""):
    """Print a separator with optional title"""
    print("\n" + "="*60)
    if title:
        print(f" {title}")
        print("="*60)

def demo_chatbot():
    """Demonstrate chatbot capabilities"""
    print_separator("Modern Rule-Based Chatbot Demo")
    
    # Initialize chatbot
    chatbot = ModernRuleBasedChatbot("demo_chatbot.db")
    
    # Test cases organized by intent
    test_cases = {
        "Greeting Intent": [
            "Hello!",
            "Hi there",
            "Good morning",
            "Hey, how are you?",
            "Greetings!"
        ],
        "Farewell Intent": [
            "Goodbye",
            "See you later",
            "Bye bye",
            "Farewell",
            "I have to go now"
        ],
        "Help Intent": [
            "I need help",
            "Can you assist me?",
            "I need support",
            "Help me please",
            "Guide me through this"
        ],
        "Weather Intent": [
            "What's the weather like?",
            "Is it raining?",
            "How's the temperature?",
            "Is it sunny today?",
            "Weather forecast please"
        ],
        "Thanks Intent": [
            "Thank you",
            "Thanks a lot",
            "I appreciate it",
            "Much appreciated",
            "Grateful for your help"
        ],
        "Complaint Intent": [
            "I have a problem",
            "There's an issue",
            "Something is wrong",
            "This is broken",
            "I'm having trouble"
        ],
        "Compliment Intent": [
            "Good job!",
            "Well done",
            "Excellent work",
            "Amazing!",
            "Great work"
        ],
        "Question Intent": [
            "What can you do?",
            "How does this work?",
            "Why is this happening?",
            "When will this be ready?",
            "Can you help me?"
        ],
        "Unknown Intent": [
            "asdfghjkl",
            "random text",
            "nonsense words",
            "xyz123",
            "qwertyuiop"
        ]
    }
    
    # Run test cases
    for category, test_inputs in test_cases.items():
        print_separator(f"Testing {category}")
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\nTest {i}: '{test_input}'")
            
            # Process input
            response = chatbot.process_input(test_input)
            
            # Display results
            print(f"Intent: {response.intent.value}")
            print(f"Confidence: {response.confidence:.2f}")
            print(f"Sentiment: {response.context.get('sentiment', 'unknown')}")
            print(f"Response: {response.text}")
            
            # Small delay for readability
            time.sleep(0.5)
    
    # Show statistics
    print_separator("Chatbot Statistics")
    stats = chatbot.get_statistics()
    
    print(f"Total conversations: {stats.get('total_conversations', 0)}")
    print(f"Session started: {stats.get('session_start', 'Unknown')}")
    
    print("\nIntent distribution:")
    for intent, count in stats.get('intent_distribution', {}).items():
        print(f"  {intent}: {count}")
    
    print("\nSentiment distribution:")
    for sentiment, count in stats.get('sentiment_distribution', {}).items():
        print(f"  {sentiment}: {count}")
    
    # Show conversation history
    print_separator("Recent Conversation History")
    history = chatbot.get_conversation_history()
    
    for i, entry in enumerate(history[:10], 1):  # Show last 10
        print(f"\n{i}. [{entry['timestamp'][:19]}]")
        print(f"   You: {entry['user_input']}")
        print(f"   Bot: {entry['bot_response']}")
        print(f"   Intent: {entry['intent']}, Sentiment: {entry['sentiment']}")
    
    # Interactive demo
    print_separator("Interactive Demo")
    print("Now you can chat with the bot! Type 'quit' to exit.")
    print("Special commands: 'stats' for statistics, 'history' for conversation history")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🤖 Bot: Goodbye! Thanks for trying the demo!")
                break
            
            if user_input.lower() == 'stats':
                stats = chatbot.get_statistics()
                print(f"\n📊 Statistics:")
                print(f"Total conversations: {stats.get('total_conversations', 0)}")
                print(f"Intent distribution: {stats.get('intent_distribution', {})}")
                print(f"Sentiment distribution: {stats.get('sentiment_distribution', {})}")
                continue
            
            if user_input.lower() == 'history':
                history = chatbot.get_conversation_history()
                print(f"\n📜 Recent History:")
                for entry in history[:5]:
                    print(f"[{entry['timestamp'][:19]}] You: {entry['user_input']}")
                    print(f"[{entry['timestamp'][:19]}] Bot: {entry['bot_response']}")
                continue
            
            response = chatbot.process_input(user_input)
            print(f"🤖 Bot: {response.text}")
            
            if response.confidence < 0.7:
                print(f"   (Intent: {response.intent.value}, Confidence: {response.confidence:.2f})")
                
        except KeyboardInterrupt:
            print("\n🤖 Bot: Goodbye! Thanks for trying the demo!")
            break
        except Exception as e:
            print(f"🤖 Bot: Sorry, I encountered an error: {e}")

def main():
    """Main function"""
    try:
        demo_chatbot()
    except Exception as e:
        print(f"Demo failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
