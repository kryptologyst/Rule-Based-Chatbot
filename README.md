# Rule-Based Chatbot

A sophisticated rule-based chatbot implementation featuring advanced pattern matching, sentiment analysis, conversation context management, and a modern web interface.

## Features

### Core Functionality
- **Advanced Pattern Matching**: Uses regex patterns with confidence scoring
- **Intent Detection**: Identifies user intents (greeting, farewell, help, weather, etc.)
- **Sentiment Analysis**: Analyzes user sentiment using word-based classification
- **Context Awareness**: Maintains conversation history and context
- **Database Integration**: SQLite database for conversation storage and analytics

### Web Interface
- **Modern UI**: Responsive design with gradient backgrounds and smooth animations
- **Real-time Chat**: WebSocket-like experience with typing indicators
- **Statistics Dashboard**: View conversation analytics and intent distribution
- **Mobile Responsive**: Optimized for both desktop and mobile devices

### Technical Features
- **Type Hints**: Full Python type annotations for better code quality
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Robust error handling throughout the application
- **Modular Design**: Clean separation of concerns with classes and modules

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd 0170_Chatbot_using_rule-based_methods
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Console Mode
Run the chatbot in console mode for testing and development:

```bash
python chatbot.py
```

**Console Commands**:
- `stats` - View conversation statistics
- `history` - View recent conversation history
- `bye`, `exit`, `quit` - Exit the chatbot

### Web Interface
Run the Flask web application:

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

**Web Features**:
- Interactive chat interface
- Real-time conversation
- Statistics panel
- Conversation history
- Mobile-responsive design

## Project Structure

```
0170_Chatbot_using_rule-based_methods/
├── chatbot.py              # Core chatbot implementation
├── app.py                  # Flask web application
├── templates/
│   └── index.html         # Web interface template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── chatbot.db             # SQLite database (created automatically)
└── tests/
    └── test_chatbot.py    # Unit tests
```

## Architecture

### Core Classes

1. **ModernRuleBasedChatbot**: Main chatbot class
   - Intent detection and pattern matching
   - Response generation
   - Database operations
   - Statistics and analytics

2. **ConversationContext**: Manages conversation state
   - History tracking
   - Session management
   - Context awareness

3. **SentimentAnalyzer**: Simple sentiment analysis
   - Word-based classification
   - Positive/negative/neutral detection

4. **Intent Enum**: Defines possible user intents
   - GREETING, FAREWELL, HELP, WEATHER, etc.

### Database Schema

**conversations table**:
- `id`: Primary key
- `timestamp`: Conversation timestamp
- `user_input`: User message
- `bot_response`: Bot response
- `intent`: Detected intent
- `sentiment`: Sentiment analysis result
- `session_id`: Session identifier

**response_patterns table**:
- `id`: Primary key
- `intent`: Intent type
- `pattern`: Regex pattern
- `response`: Response text
- `usage_count`: Usage statistics

## API Endpoints

### Web Interface Endpoints

- `GET /` - Main chat interface
- `POST /chat` - Send message and get response
- `GET /history` - Get conversation history
- `GET /stats` - Get chatbot statistics
- `GET /health` - Health check endpoint

### API Response Format

```json
{
  "response": "Bot response text",
  "intent": "greeting",
  "confidence": 0.85,
  "sentiment": "positive"
}
```

## Customization

### Adding New Intents

1. Add new intent to `Intent` enum in `chatbot.py`
2. Add patterns and responses in `_initialize_patterns()` method
3. Test with various user inputs

### Modifying Responses

Edit the response patterns in the `_initialize_patterns()` method:

```python
Intent.NEW_INTENT: [
    {
        'patterns': [r'\b(pattern1|pattern2)\b'],
        'responses': [
            "Response 1",
            "Response 2",
            "Response 3"
        ]
    }
]
```

### Database Customization

Modify the `_init_database()` method to add new tables or fields as needed.

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Future Enhancements

- [ ] Machine learning integration for better intent detection
- [ ] Multi-language support
- [ ] Voice input/output capabilities
- [ ] Integration with external APIs (weather, news, etc.)
- [ ] Advanced analytics dashboard
- [ ] User authentication and personalization
- [ ] Plugin system for extensibility

## Troubleshooting

### Common Issues

1. **Database errors**: Ensure SQLite is properly installed
2. **Port conflicts**: Change the port in `app.py` if 5000 is occupied
3. **Import errors**: Verify all dependencies are installed correctly

### Debug Mode

Enable debug mode in Flask by setting `debug=True` in `app.py` for detailed error messages.

## Performance Considerations

- Database queries are optimized with proper indexing
- Conversation history is limited to recent exchanges
- Response patterns use compiled regex for better performance
- Web interface uses efficient DOM manipulation

## Security Notes

- Input validation is implemented for all user inputs
- SQL injection protection through parameterized queries
- Session management for web interface
- Error messages don't expose sensitive information

---

**Note**: This is a rule-based chatbot implementation. For production use with complex requirements, consider integrating machine learning models or using existing chatbot frameworks.
# Rule-Based-Chatbot
