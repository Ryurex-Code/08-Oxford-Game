"""
Oxford Vocabulary Trainer - Main Entry Point
AI-powered vocabulary learning game using Oxford 5000 words

Author: Rafi Project
Version: 1.0.0
"""
import os
import sys
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

try:
    import pandas as pd
    from dotenv import load_dotenv
    
    from utils import (
        load_oxford_data, clear_screen, print_header, 
        print_success, print_error, print_warning, print_info, Colors
    )
    from translator import LLMTranslator
    from word_picker import WordPicker
    from game import OxfordVocabGame
    
except ImportError as e:
    print(f"❌ Missing required packages: {e}")
    print("Please install required packages:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def check_environment():
    """Check if environment is properly configured"""
    issues = []
    
    # Check for .env file
    env_file = current_dir / '.env'
    if not env_file.exists():
        issues.append("⚠️  .env file not found. Please copy .env.example to .env and configure your Groq API key.")
    
    # Load environment variables
    load_dotenv()
    
    # Check for Groq API key
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key or groq_key == 'your_groq_api_key_here':
        issues.append("⚠️  GROQ_API_KEY not configured. Please set your Groq API key in .env file.")
    
    # Check data files
    data_dir = current_dir / 'data'
    oxford_3000_file = data_dir / 'oxford_3000.csv'
    oxford_5000_file = data_dir / 'oxford_5000.csv'
    
    if not oxford_3000_file.exists():
        issues.append(f"❌ Oxford 3000 data file not found: {oxford_3000_file}")
    
    if not oxford_5000_file.exists():
        issues.append(f"⚠️  Oxford 5000 data file not found: {oxford_5000_file} (optional)")
    
    return issues

def display_welcome():
    """Display welcome message and setup instructions"""
    clear_screen()
    print_header("🎓 Oxford Vocabulary Trainer Setup 🎓", 70)
    
    print(f"{Colors.INFO}Welcome to the AI-powered vocabulary learning game!{Colors.RESET}")
    print(f"{Colors.INFO}This game uses LLaMA 4 via Groq API for intelligent translations.{Colors.RESET}\n")
    
    print(f"{Colors.WARNING}📋 Setup Requirements:{Colors.RESET}")
    print("1. 🔑 Groq API Key (free at https://console.groq.com/)")
    print("2. 📊 Oxford 5000 data file (included)")
    print("3. 🐍 Python packages (install with: pip install -r requirements.txt)")
    
    print(f"\n{Colors.INFO}🚀 Getting Started:{Colors.RESET}")
    print("1. Copy .env.example to .env")
    print("2. Add your Groq API key to .env file")
    print("3. Run this script again")
    print()

def main():
    """Main application entry point"""
    # Check environment setup
    issues = check_environment()
    
    if issues:
        display_welcome()
        print(f"{Colors.ERROR}⚠️  Setup Issues Found:{Colors.RESET}")
        for issue in issues:
            print(f"   {issue}")
        
        print(f"\n{Colors.INFO}📖 Setup Instructions:{Colors.RESET}")
        print("1. Get a free Groq API key:")
        print("   • Visit: https://console.groq.com/")
        print("   • Sign up/login")
        print("   • Create an API key")
        print()
        print("2. Configure your environment:")
        print("   • Copy .env.example to .env")
        print("   • Edit .env and add your API key:")
        print("     GROQ_API_KEY=your_actual_api_key_here")
        print()
        print("3. Install dependencies:")
        print("   pip install -r requirements.txt")
        
        return
    
    try:
        # Initialize components
        print_info("🔧 Initializing Oxford Vocabulary Trainer...")
          # Load data
        data_dir = current_dir / 'data'
        oxford_file = data_dir / 'oxford_5000.csv'
        
        print_info(f"📚 Loading vocabulary data from {oxford_file.name}...")
        vocabulary_df = load_oxford_data(str(oxford_file))
        
        if vocabulary_df.empty:
            print_error("Failed to load vocabulary data. Please check the data file.")
            return
        
        # Initialize translator
        print_info("🤖 Initializing AI translator...")
        try:
            translator = LLMTranslator()
            print_success("AI translator ready!")
        except Exception as e:
            print_error(f"Failed to initialize translator: {e}")
            print_warning("Please check your Groq API key configuration.")
            return
        
        # Initialize word picker
        scores_dir = current_dir / 'scores'
        scores_dir.mkdir(exist_ok=True)
        weights_file = scores_dir / 'word_weights.json'
        
        print_info("🎯 Initializing adaptive word picker...")
        word_picker = WordPicker(vocabulary_df, str(weights_file))
        print_success("Word picker ready!")
        
        # Initialize game
        print_info("🎮 Initializing game engine...")
        game = OxfordVocabGame(word_picker, translator, str(scores_dir))
        print_success("Game engine ready!")
        
        print_success("✅ All systems initialized successfully!")
        print()
        
        # Start game
        game.start_game_menu()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Game interrupted by user. Goodbye! 👋{Colors.RESET}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        print_info("Please check your configuration and try again.")
        import traceback
        print("\nDetailed error information:")
        traceback.print_exc()

def quick_test():
    """Quick test function for development"""
    print_info("🧪 Running quick test...")
    
    # Test environment
    issues = check_environment()
    if issues:
        print_error("Environment issues found:")
        for issue in issues:
            print(f"  {issue}")
        return
      # Test data loading
    data_dir = current_dir / 'data'
    oxford_file = data_dir / 'oxford_5000.csv'
    df = load_oxford_data(str(oxford_file))
    
    if not df.empty:
        print_success(f"✅ Data loaded successfully: {len(df)} words")
        
        # Show sample words
        sample_words = df.head(3)
        print_info("Sample words:")
        for _, row in sample_words.iterrows():
            print(f"  {row['word']} ({row['class']}, {row['level']})")
    
    # Test translator initialization
    try:
        translator = LLMTranslator()
        print_success("✅ Translator initialized successfully")
        
        # Test single translation
        test_word = "hello"
        test_class = "exclamation"
        print_info(f"Testing translation of '{test_word}'...")
        
        meanings = translator.translate_word(test_word, test_class)
        if meanings:
            print_success(f"✅ Translation successful: {meanings[:3]}")
        else:
            print_warning("Translation returned empty results")
            
    except Exception as e:
        print_error(f"❌ Translator test failed: {e}")
    
    print_info("🧪 Quick test completed!")

if __name__ == "__main__":
    # Check if running in test mode
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        quick_test()
    else:
        main()
