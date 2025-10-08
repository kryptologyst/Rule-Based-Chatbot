# Web interface for Modern Rule-Based Chatbot
from flask import Flask, render_template, request, jsonify, session
import uuid
import os
from chatbot import ModernRuleBasedChatbot

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Global chatbot instance
chatbot = ModernRuleBasedChatbot()

@app.route('/')
def index():
    """Main chat interface"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400
        
        # Process the input
        response = chatbot.process_input(user_input)
        
        return jsonify({
            'response': response.text,
            'intent': response.intent.value,
            'confidence': response.confidence,
            'sentiment': response.context.get('sentiment', 'neutral') if response.context else 'neutral'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def get_history():
    """Get conversation history"""
    try:
        history = chatbot.get_conversation_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def get_stats():
    """Get chatbot statistics"""
    try:
        stats = chatbot.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
