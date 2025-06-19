"""
Utility functions for Oxford Vocabulary Trainer
"""
import json
import os
import pandas as pd
from typing import Dict, List, Optional, Tuple
from colorama import Fore, Style, init

# Initialize colorama for Windows
init(autoreset=True)

class Colors:
    """Color constants for terminal output"""
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text: str, width: int = 60):
    """Print a formatted header"""
    print("\n" + "=" * width)
    print(f"{Colors.HEADER}{text.center(width)}{Colors.RESET}")
    print("=" * width + "\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.SUCCESS}✓ {text}{Colors.RESET}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.ERROR}✗ {text}{Colors.RESET}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.RESET}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.INFO}ℹ {text}{Colors.RESET}")

def load_json_file(filepath: str, default: dict = None) -> dict:
    """Load JSON file with error handling"""
    if default is None:
        default = {}
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return default.copy()
    except json.JSONDecodeError as e:
        print_error(f"Error loading {filepath}: {e}")
        return default.copy()
    except Exception as e:
        print_error(f"Unexpected error loading {filepath}: {e}")
        return default.copy()

def save_json_file(filepath: str, data: dict) -> bool:
    """Save dictionary to JSON file with error handling"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print_error(f"Error saving to {filepath}: {e}")
        return False

def load_oxford_data(filepath: str) -> pd.DataFrame:
    """Load Oxford CSV data with validation"""
    try:
        df = pd.read_csv(filepath)
        
        # Validate required columns
        required_columns = ['word', 'class', 'level']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")
        
        # Clean and validate data
        df = df.dropna()
        df['word'] = df['word'].str.strip().str.lower()
        df['class'] = df['class'].str.strip().str.lower()
        df['level'] = df['level'].str.strip().str.lower()
        
        # Filter valid levels
        valid_levels = ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']
        df = df[df['level'].isin(valid_levels)]
        
        print_success(f"Loaded {len(df)} words from {os.path.basename(filepath)}")
        return df
        
    except FileNotFoundError:
        print_error(f"Data file not found: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        print_error(f"Error loading data: {e}")
        return pd.DataFrame()

def validate_user_input(user_input: str, valid_meanings: List[str]) -> bool:
    """Validate user input against possible meanings"""
    if not user_input or not valid_meanings:
        return False
    
    # Clean user input
    user_input = user_input.strip().lower()
    
    # Check exact matches and word-boundary matches
    for meaning in valid_meanings:
        meaning_clean = meaning.strip().lower()
        
        # Exact match
        if user_input == meaning_clean:
            return True
        
        # Check if user input matches any complete word in the meaning
        # Split both user input and meaning into words
        user_words = user_input.split()
        meaning_words = meaning_clean.split()
        
        # Check if all user words are present as complete words in meaning
        if len(user_words) == 1 and len(user_words[0]) >= 3:
            # Single word input - check if it matches any complete word in meanings
            for meaning_word in meaning_words:
                if user_words[0] == meaning_word:
                    return True
        elif len(user_words) > 1:
            # Multi-word input - check if all words are present
            user_words_set = set(user_words)
            meaning_words_set = set(meaning_words)
            if user_words_set.issubset(meaning_words_set):
                return True
    
    return False

def format_word_display(word: str, word_class: str, level: str) -> str:
    """Format word display for gameplay"""
    level_colors = {
        'a1': Fore.GREEN,
        'a2': Fore.LIGHTGREEN_EX,
        'b1': Fore.YELLOW,
        'b2': Fore.LIGHTYELLOW_EX,
        'c1': Fore.RED,
        'c2': Fore.LIGHTRED_EX
    }
    
    level_color = level_colors.get(level.lower(), Fore.WHITE)
    
    return f"""
{Colors.HEADER}Word:{Colors.RESET} {Colors.BOLD}{word.title()}{Colors.RESET}
{Colors.INFO}Class:{Colors.RESET} {word_class.title()}
{Colors.INFO}Level:{Colors.RESET} {level_color}{level.upper()}{Colors.RESET}
"""

def get_level_description(level: str) -> str:
    """Get CEFR level description"""
    descriptions = {
        'a1': 'Beginner - Basic everyday expressions',
        'a2': 'Elementary - Simple phrases and frequently used expressions',
        'b1': 'Intermediate - Clear standard input on familiar matters',
        'b2': 'Upper-Intermediate - Complex text on concrete and abstract topics',
        'c1': 'Advanced - Wide range of demanding texts',
        'c2': 'Proficient - Virtually everything heard or read'
    }
    return descriptions.get(level.lower(), 'Unknown level')

def display_game_stats(current_score: int, top_score: int, level: str):
    """Display current game statistics"""
    print(f"\n{Colors.INFO}📊 Game Stats:{Colors.RESET}")
    print(f"   Current Score: {Colors.BOLD}{current_score}{Colors.RESET}")
    print(f"   Top Score: {Colors.SUCCESS}{top_score}{Colors.RESET}")
    print(f"   Level: {Colors.WARNING}{level.upper()}{Colors.RESET}")
    print("-" * 30)

def parse_llm_response(response: str) -> List[str]:
    """Parse LLM response to extract Indonesian meanings"""
    if not response:
        return []
    
    # Split by common separators and clean
    separators = [',', ';', '\n', '|', '-']
    meanings = [response]
    
    for sep in separators:
        new_meanings = []
        for meaning in meanings:
            new_meanings.extend(meaning.split(sep))
        meanings = new_meanings
    
    # Clean and filter meanings
    cleaned_meanings = []
    for meaning in meanings:
        cleaned = meaning.strip()
        # Remove common prefixes/artifacts
        prefixes_to_remove = ['*', '-', '•', '1.', '2.', '3.', '4.', '5.']
        for prefix in prefixes_to_remove:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
        
        # Filter out empty strings and very short words
        if cleaned and len(cleaned) >= 2:
            cleaned_meanings.append(cleaned)
    
    return cleaned_meanings[:10]  # Limit to 10 meanings max
