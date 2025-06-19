# 🎓 Oxford Vocabulary Trainer

An AI-powered vocabulary learning game that helps you master English words from the Oxford 3000 list using intelligent LLM translations and adaptive learning algorithms.

## ✨ Features

### 🎮 Game Modes
- **Custom Mode**: Choose specific CEFR levels (A1, A2, B1, B2, C1, C2)
- **Adventure Mode**: Random levels from A1-B2 for dynamic learning

### 🤖 AI-Powered Translation
- Uses **LLaMA 3.1 8B Instant** via Groq API for contextual Indonesian translations
- Provides multiple meanings and contexts for each word
- Smart fallback system for reliable operation
- Translation caching for improved performance

### 🧠 Adaptive Learning System
- **Weighted Word Selection**: Difficult words appear more frequently
- **Spaced Repetition**: Mastered words appear less often
- **Performance Tracking**: Detailed statistics for each word
- **Streak Tracking**: Monitor learning progress
- **Smart Validation**: Precise answer checking with complete word matching

### 📊 Comprehensive Statistics
- High scores by level and game mode
- Accuracy tracking and learning progress
- Word mastery analysis
- **Recently Appeared Words**: Track last 10 words that appeared in games
- **Recently Missed Words**: Track last 10 words answered incorrectly
- Session history with detailed breakdowns
- **Word History Tracking**: Persistent storage of learning progress

### ⚙️ Advanced Settings
- Reset all statistics
- Clear translation cache
- Export statistics to JSON
- Reset specific levels
- **Factory Reset**: Complete data wipe back to initial state
- Translation cache management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone or download the project**
   ```bash
   cd oxford_vocab_trainer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   ```bash
   # Copy the example environment file
   copy .env.example .env
   
   # Edit .env and add your Groq API key
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the game**
   ```bash
   python main.py
   ```

### Getting Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## 🎯 How to Play

### Custom Mode
1. Select **Custom Mode** from main menu
2. Choose your desired CEFR level (A1-C2)
3. Translate English words to Indonesian
4. Build your score with correct answers
5. Game ends on first wrong answer

### Adventure Mode
1. Select **Adventure Mode** for random levels
2. Face words from A1-B2 levels randomly
3. Test your knowledge across different difficulties
4. Challenge yourself with unpredictable vocabulary

### Game Controls
- **Type your answer**: Indonesian translation of the word
- **'hint'**: Get a clue for the current word
- **'skip'**: Skip the current word (counts as wrong)
- **'quit'**: End the current game session

## 🏗️ Project Structure

```
oxford_vocab_trainer/
│
├── data/
│   ├── oxford_3000.csv         # Oxford 3000 word list
│   └── oxford_5000.csv         # Oxford 5000 word list (optional)
│
├── src/
│   ├── game.py                 # Game logic and scoring
│   ├── translator.py           # LLM translation handler
│   ├── word_picker.py          # Adaptive word selection
│   └── utils.py                # Utility functions
│
├── scores/
│   ├── top_score.json          # High scores storage
│   ├── word_weights.json       # Word difficulty weights
│   ├── word_history.json       # Recently appeared and missed words
│   └── current_session.json    # Current session data
│
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🧠 Learning Algorithm

The app uses an intelligent adaptive learning system:

### Word Weighting System
- **High accuracy words (80%+)**: Lower weight → appear less often
- **Low accuracy words (<40%)**: Higher weight → appear more often
- **Consecutive correct answers**: Significantly reduce weight
- **Consecutive wrong answers**: Significantly increase weight

### Performance Tracking
- Accuracy percentage per word
- Consecutive correct/wrong streaks
- Last seen timestamp
- Total attempts and success rate

### Spaced Repetition
- Words you struggle with get priority
- Mastered words fade into background
- New words get slight boost in selection

## 📊 Statistics & Features

### Score Tracking
- Overall high score
- High scores by CEFR level
- High scores by game mode
- Session history (last 20 sessions)

### Learning Analytics
- Words needing practice
- Recently mastered words
- Level-wise mastery percentage
- Accuracy trends

### Export & Reset
- Export all statistics to JSON
- Reset individual levels
- Clear translation cache
- Full statistics reset
- **Factory Reset**: Complete data wipe to restore initial state
- **Word History Management**: Track and review learning progress

## � Enhanced Statistics & Features

### Score Tracking
- Overall high score
- High scores by CEFR level
- High scores by game mode
- Session history (last 20 sessions)
- **New Record Notifications**: Celebrate achievements

### Learning Analytics
- Words needing practice
- Recently mastered words
- Level-wise mastery percentage
- Accuracy trends
- **Recently Appeared Words (Last 10)**: See what words you've encountered
- **Recently Missed Words (Last 10)**: Focus on words that need practice

### Smart Answer Validation
- **Precise word matching**: No more partial answers being accepted
- **Complete word validation**: "kap" won't be accepted for "kapal"
- **Multi-word support**: Handle compound translations correctly
- **Case-insensitive matching**: Focus on meaning, not capitalization

### Session Summary Enhancements
- **Complete answer display**: All correct meanings shown (no truncation)
- **Detailed wrong answer breakdown**: See exactly what you got wrong
- **Performance metrics**: Accuracy, streak, and level breakdown

### AI Translation
- **Model**: LLaMA 3.1 8B Instant via Groq API
- **Features**: 
  - Contextual translation with multiple meanings
  - **Advanced caching system** for performance optimization
  - **Persistent cache storage** for offline capability
  - Fallback dictionary for reliability
  - Error handling and retries
  - **Smart retry logic** with exponential backoff

### Answer Validation Engine
- **Intelligent word matching**: Complete word validation only
- **Multi-word phrase support**: Handle complex translations
- **Boundary detection**: Prevent substring false positives
- **Flexible matching**: Support various answer formats while maintaining accuracy

### Data Processing & Storage
- **Source**: Oxford 3000/5000 word lists
- **Format**: CSV with word, class (part of speech), level
- **Validation**: Automatic data cleaning and validation
- **Persistent History**: Word appearance and error tracking
- **Efficient Storage**: JSON-based data persistence

### Performance Optimizations
- **Advanced translation caching** to reduce API calls
- **Persistent cache storage** for faster subsequent sessions
- Weighted random selection for balanced gameplay
- Efficient data structures for statistics
- **Background auto-saving** of progress
- **Factory reset capability** for clean starts

## 🎮 Game Modes Explained

### Custom Mode
Perfect for focused learning:
- Choose specific CEFR level
- Systematic vocabulary building
- Track progress per level
- Ideal for structured learning

### Adventure Mode
For dynamic challenge:
- Random levels A1-B2
- Unpredictable difficulty
- Broader vocabulary exposure
- Fun and engaging experience

## 📈 Learning Tips

1. **Start with A1**: Build foundation before advancing
2. **Use hints wisely**: Learn from partial clues
3. **Review statistics**: Identify weak areas
4. **Regular practice**: Consistency improves retention
5. **Challenge yourself**: Try Adventure mode when confident

## 🔧 Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
DEFAULT_DATASET=oxford_3000
MAX_RETRIES=3
TRANSLATION_TIMEOUT=10
```

### Customization
- Modify word weights in `word_picker.py`
- Adjust translation prompts in `translator.py`
- Customize UI colors in `utils.py`
- Add new game modes in `game.py`

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional language support
- GUI interface (Gradio/Streamlit)
- Mobile app version
- More game modes
- Enhanced AI prompts

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Oxford University Press** for the Oxford 3000/5000 word lists
- **Groq** for providing fast LLM inference
- **LLaMA** team for the language model
- **Python community** for excellent libraries

## 🐛 Troubleshooting

### Common Issues

**ImportError: No module named 'package'**
```bash
pip install -r requirements.txt
```

**Translation fails**
- Check Groq API key in `.env`
- Verify internet connection
- Check API quota/limits

**No words available**
- Verify CSV files in `data/` directory
- Check file format and headers
- Ensure proper CEFR level filtering

**Performance issues**
- Clear translation cache in settings
- Reset word statistics if needed
- Check available disk space

### Testing Installation
```bash
python main.py --test
```

This runs a quick test to verify:
- Environment configuration
- Data file loading
- API connectivity
- Translation functionality

## 📞 Support

For issues or questions:
1. Check this README
2. Review error messages carefully
3. Test with `python main.py --test`
4. Verify API key and internet connection

---

**Happy Learning! 🎓📚**

Master English vocabulary with the power of AI and adaptive learning!
