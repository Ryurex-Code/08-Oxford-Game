"""
Game logic and scoring system for Oxford Vocabulary Trainer
"""
import os
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from utils import (
    load_json_file, save_json_file, clear_screen, print_header, 
    print_success, print_error, print_warning, print_info,
    format_word_display, display_game_stats, validate_user_input,
    get_level_description, Colors
)
from translator import LLMTranslator
from word_picker import WordPicker

class OxfordVocabGame:
    """Main game class for Oxford Vocabulary Trainer"""
    
    def __init__(self, word_picker: WordPicker, translator: LLMTranslator, scores_dir: str):
        """
        Initialize the game
        
        Args:
            word_picker: WordPicker instance
            translator: LLMTranslator instance
            scores_dir: Directory for score files
        """
        self.word_picker = word_picker
        self.translator = translator
        self.scores_dir = scores_dir
        self.scores_file = os.path.join(scores_dir, 'top_score.json')
        self.session_file = os.path.join(scores_dir, 'current_session.json')
        
        # Game state
        self.current_score = 0
        self.session_stats = {
            'start_time': None,
            'words_attempted': 0,
            'words_correct': 0,
            'current_streak': 0,
            'best_streak': 0,
            'level_stats': {}
        }
          # Load scores and word history
        self.top_scores = self._load_top_scores()
        self.word_history = self._load_word_history()
        
    def _load_top_scores(self) -> Dict:
        """Load top scores from file"""
        default_scores = {
            'overall': 0,
            'by_level': {
                'a1': 0, 'a2': 0, 'b1': 0, 'b2': 0, 'c1': 0, 'c2': 0
            },
            'by_mode': {
                'custom': 0,
                'adventure': 0
            },
            'sessions': []
        }
        return load_json_file(self.scores_file, default_scores)
    
    def _save_scores(self) -> bool:
        """Save current scores to file"""
        return save_json_file(self.scores_file, self.top_scores)
    
    def _save_session(self) -> bool:
        """Save current session data"""
        session_data = {
            'current_score': self.current_score,
            'stats': self.session_stats,
            'timestamp': datetime.now().isoformat()
        }
        return save_json_file(self.session_file, session_data)
    
    def _load_word_history(self) -> Dict:
        """Load word history from file"""
        history_file = os.path.join(self.scores_dir, 'word_history.json')
        default_history = {
            'recent_words': [],  # List of recent words that appeared in games
            'wrong_words': []    # List of words that were answered incorrectly
        }
        return load_json_file(history_file, default_history)
    
    def _save_word_history(self) -> bool:
        """Save word history to file"""
        history_file = os.path.join(self.scores_dir, 'word_history.json')
        return save_json_file(history_file, self.word_history)
    
    def _add_word_to_history(self, word: str, word_class: str, level: str, is_correct: bool, meanings: List[str]):
        """Add word to history tracking"""
        word_entry = {
            'word': word,
            'class': word_class,
            'level': level,
            'meanings': meanings,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to recent words (keep last 50)
        self.word_history['recent_words'].insert(0, word_entry)
        if len(self.word_history['recent_words']) > 50:
            self.word_history['recent_words'] = self.word_history['recent_words'][:50]
        
        # Add to wrong words if incorrect (keep last 100)
        if not is_correct:
            self.word_history['wrong_words'].insert(0, word_entry)
            if len(self.word_history['wrong_words']) > 100:
                self.word_history['wrong_words'] = self.word_history['wrong_words'][:100]
        
        self._save_word_history()
    
    def start_game_menu(self):
        """Display main game menu"""
        while True:
            clear_screen()
            print_header("🎓 Oxford Vocabulary Trainer 🎓", 60)
            
            print(f"{Colors.INFO}Welcome to the AI-powered vocabulary learning game!{Colors.RESET}")
            print(f"{Colors.INFO}Master Oxford 3000 words with intelligent AI translations.{Colors.RESET}\n")
            
            # Display current top scores
            overall_score = self.top_scores.get('overall', 0)
            print(f"{Colors.SUCCESS}🏆 Overall Top Score: {overall_score}{Colors.RESET}")
            
            # Display level scores
            level_scores = self.top_scores.get('by_level', {})
            print(f"\n{Colors.INFO}📊 Best Scores by Level:{Colors.RESET}")
            for level in ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']:
                score = level_scores.get(level, 0)
                description = get_level_description(level).split(' - ')[0]
                print(f"   {level.upper()}: {score:2d} ({description})")
            
            print(f"\n{Colors.WARNING}Choose your game mode:{Colors.RESET}")
            print("1. 🎯 Custom Mode (Choose specific level)")
            print("2. 🎲 Adventure Mode (Random levels A1-B2)")
            print("3. 📈 View Statistics")
            print("4. ⚙️  Settings")
            print("5. ❌ Exit")
            
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-5): {Colors.RESET}").strip()
            
            if choice == '1':
                self._custom_mode()
            elif choice == '2':
                self._adventure_mode()
            elif choice == '3':
                self._view_statistics()
            elif choice == '4':
                self._settings_menu()
            elif choice == '5':
                print_info("Thanks for playing! Keep learning! 📚")
                break
            else:
                print_error("Invalid choice. Please try again.")
                time.sleep(1)
    
    def _custom_mode(self):
        """Custom mode - user selects level"""
        clear_screen()
        print_header("🎯 Custom Mode", 50)
        
        print(f"{Colors.INFO}Choose your difficulty level:{Colors.RESET}\n")
        
        levels = ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']
        for i, level in enumerate(levels, 1):
            description = get_level_description(level)
            top_score = self.top_scores.get('by_level', {}).get(level, 0)
            print(f"{i}. {level.upper()} - {description} (Best: {top_score})")
        
        print("7. 🔄 Back to main menu")
        
        choice = input(f"\n{Colors.BOLD}Choose level (1-7): {Colors.RESET}").strip()
        
        try:
            if choice == '7':
                return
            
            level_index = int(choice) - 1
            if 0 <= level_index < len(levels):
                selected_level = levels[level_index]
                print_info(f"Starting Custom Mode with level {selected_level.upper()}")
                self._play_game(selected_level, 'custom')
            else:
                print_error("Invalid level selection.")
                time.sleep(1)
        except ValueError:
            print_error("Please enter a valid number.")
            time.sleep(1)
    
    def _adventure_mode(self):
        """Adventure mode - random levels A1-B2"""
        clear_screen()
        print_header("🎲 Adventure Mode", 50)
        
        print(f"{Colors.INFO}Adventure Mode - Random levels from A1 to B2!{Colors.RESET}")
        print(f"{Colors.WARNING}Each word will be from a random level to keep you on your toes!{Colors.RESET}\n")
        
        top_score = self.top_scores.get('by_mode', {}).get('adventure', 0)
        print(f"{Colors.SUCCESS}🏆 Adventure Mode Best Score: {top_score}{Colors.RESET}")
        
        input(f"\n{Colors.BOLD}Press Enter to start the adventure...{Colors.RESET}")
        print_info("Starting Adventure Mode!")
        self._play_game(None, 'adventure')  # None level means random selection
    
    def _play_game(self, level: Optional[str], mode: str):
        """
        Main game loop
        
        Args:
            level: CEFR level or None for random
            mode: 'custom' or 'adventure'
        """        # Initialize session
        self.current_score = 0
        self.session_stats = {
            'start_time': datetime.now().isoformat(),
            'words_attempted': 0,
            'words_correct': 0,
            'current_streak': 0,
            'best_streak': 0,
            'level_stats': {},
            'wrong_answers': [],  # Store wrong answer details
            'mode': mode,
            'target_level': level
        }
        
        print_info(f"Game started! Mode: {mode.title()}, Level: {level.upper() if level else 'Random A1-B2'}")
        
        while True:
            # Select word based on mode
            if mode == 'adventure':
                # Random level selection for adventure mode
                adventure_levels = ['a1', 'a2', 'b1', 'b2']
                current_level = random.choice(adventure_levels)
                word_data = self.word_picker.get_weighted_word(current_level)
            else:
                # Fixed level for custom mode
                current_level = level
                word_data = self.word_picker.get_weighted_word(level)
            
            if not word_data:
                print_error(f"No words available for level: {current_level or 'adventure'}")
                break
            
            word, word_class, word_level = word_data
            
            # Update level stats
            if word_level not in self.session_stats['level_stats']:
                self.session_stats['level_stats'][word_level] = {
                    'attempted': 0, 'correct': 0
                }
            
            # Display word
            clear_screen()
            current_top_score = self.top_scores.get('overall', 0)
            if mode == 'custom' and level:
                current_top_score = self.top_scores.get('by_level', {}).get(level, 0)
            elif mode == 'adventure':
                current_top_score = self.top_scores.get('by_mode', {}).get('adventure', 0)
            
            display_game_stats(self.current_score, current_top_score, word_level)
            
            print(format_word_display(word, word_class, word_level))
            
            # Get translation from AI
            print_info("🤖 AI is translating the word...")
            try:
                possible_meanings = self.translator.translate_word(word, word_class)
                
                if not possible_meanings:
                    print_error("Failed to get translation. Skipping word...")
                    continue
                
            except Exception as e:
                print_error(f"Translation error: {e}")
                print_warning("Using fallback translation...")
                possible_meanings = [f"[Translation for '{word}']"]
              # Get user input
            print(f"\n{Colors.BOLD}What is the meaning of this word in Indonesian?{Colors.RESET}")
            print(f"{Colors.INFO}(Type 'hint' for a clue, 'skip' to skip, 'quit' to end game){Colors.RESET}")
            
            user_answer = input(f"\n{Colors.BOLD}Your answer: {Colors.RESET}").strip()
            
            # Handle special commands
            if user_answer.lower() == 'quit':
                self._end_game(mode, level)
                return
            elif user_answer.lower() == 'skip':
                print_warning(f"Skipped! Possible meanings: {', '.join(possible_meanings[:3])}")
                
                # Store skipped word details
                wrong_answer_detail = {
                    'word': word,
                    'class': word_class,
                    'level': word_level,
                    'user_answer': '[SKIPPED]',                    'correct_meanings': possible_meanings
                }
                self.session_stats['wrong_answers'].append(wrong_answer_detail)
                
                self.word_picker.update_word_performance(word, word_class, word_level, False)
                self._add_word_to_history(word, word_class, word_level, False, possible_meanings)
                self._update_session_stats(word_level, False)
                input(f"\n{Colors.INFO}Press Enter to continue...{Colors.RESET}")
                continue
            elif user_answer.lower() == 'hint':
                # Show first letter of first meaning
                if possible_meanings:
                    hint = possible_meanings[0][:2] + "..."
                    print(f"{Colors.WARNING}Hint: {hint}{Colors.RESET}")
                    user_answer = input(f"\n{Colors.BOLD}Your answer: {Colors.RESET}").strip()
                else:
                    print_warning("No hint available")
                    continue
            
            # Validate answer
            is_correct = validate_user_input(user_answer, possible_meanings)
            
            if is_correct:
                # Correct answer
                self.current_score += 1
                self.session_stats['current_streak'] += 1
                
                # Update session stats
                self._update_session_stats(word_level, True)
                
                if self.session_stats['current_streak'] > self.session_stats['best_streak']:
                    self.session_stats['best_streak'] = self.session_stats['current_streak']
                
                print_success(f"Correct! 🎉 Score: {self.current_score}")
                print_info(f"Possible meanings: {', '.join(possible_meanings[:5])}")
                
                # Update word performance
                self.word_picker.update_word_performance(word, word_class, word_level, True)
                
                # Add word to history
                self._add_word_to_history(word, word_class, word_level, True, possible_meanings)
                
                # Save session after each correct answer
                self._save_session()
                
                input(f"\n{Colors.SUCCESS}Press Enter to continue...{Colors.RESET}")
                
            else:
                # Wrong answer - Game Over
                print_error(f"❌ Game Over! Your answer: '{user_answer}'")
                print_info(f"Correct meanings were: {', '.join(possible_meanings)}")
                
                # Store wrong answer details
                wrong_answer_detail = {
                    'word': word,
                    'class': word_class,
                    'level': word_level,
                    'user_answer': user_answer,
                    'correct_meanings': possible_meanings
                }
                self.session_stats['wrong_answers'].append(wrong_answer_detail)
                
                # Reset current streak
                self.session_stats['current_streak'] = 0
                  # Update word performance
                self.word_picker.update_word_performance(word, word_class, word_level, False)
                self._add_word_to_history(word, word_class, word_level, False, possible_meanings)
                self._update_session_stats(word_level, False)
                
                # End game
                self._end_game(mode, level)
                return
    
    def _update_session_stats(self, word_level: str, is_correct: bool):
        """Update session statistics"""
        if word_level not in self.session_stats['level_stats']:
            self.session_stats['level_stats'][word_level] = {
                'attempted': 0, 'correct': 0
            }
        
        self.session_stats['words_attempted'] += 1
        self.session_stats['level_stats'][word_level]['attempted'] += 1
        
        if is_correct:
            self.session_stats['words_correct'] += 1
            self.session_stats['level_stats'][word_level]['correct'] += 1
    
    def _end_game(self, mode: str, level: Optional[str]):
        """Handle game end and score saving"""
        clear_screen()
        print_header("🎮 Game Over", 50)
        
        print(f"{Colors.BOLD}Final Score: {self.current_score}{Colors.RESET}")
        
        # Check for new high scores
        new_records = []
        
        # Overall high score
        if self.current_score > self.top_scores.get('overall', 0):
            self.top_scores['overall'] = self.current_score
            new_records.append("Overall High Score! 🏆")
        
        # Level-specific high score
        if mode == 'custom' and level:
            level_scores = self.top_scores.setdefault('by_level', {})
            if self.current_score > level_scores.get(level, 0):
                level_scores[level] = self.current_score
                new_records.append(f"New {level.upper()} Level Record! 🎯")
        
        # Mode-specific high score
        mode_scores = self.top_scores.setdefault('by_mode', {})
        if self.current_score > mode_scores.get(mode, 0):
            mode_scores[mode] = self.current_score
            new_records.append(f"New {mode.title()} Mode Record! 🎲")
        
        # Display new records
        if new_records:
            print(f"\n{Colors.SUCCESS}🎉 NEW RECORD(S)! 🎉{Colors.RESET}")
            for record in new_records:
                print(f"{Colors.SUCCESS}   {record}{Colors.RESET}")
        
        # Save session to history
        self.session_stats['end_time'] = datetime.now().isoformat()
        self.session_stats['final_score'] = self.current_score
        
        sessions = self.top_scores.setdefault('sessions', [])
        sessions.append(self.session_stats.copy())
        
        # Keep only last 20 sessions
        if len(sessions) > 20:
            sessions = sessions[-20:]
            self.top_scores['sessions'] = sessions
        
        # Save all scores
        self._save_scores()
          # Display session stats
        self._display_session_summary()
        
        input(f"\n{Colors.INFO}Press Enter to return to main menu...{Colors.RESET}")
    
    def _display_session_summary(self):
        """Display detailed session summary"""
        print(f"\n{Colors.INFO}📊 Session Summary:{Colors.RESET}")
        print(f"   Words Attempted: {self.session_stats['words_attempted']}")
        print(f"   Words Correct: {self.session_stats['words_correct']}")
        print(f"   Best Streak: {self.session_stats['best_streak']}")
        
        if self.session_stats['words_attempted'] > 0:
            accuracy = (self.session_stats['words_correct'] / self.session_stats['words_attempted']) * 100
            print(f"   Accuracy: {accuracy:.1f}%")
          # Level breakdown
        if self.session_stats['level_stats']:
            print(f"\n{Colors.INFO}📈 Performance by Level:{Colors.RESET}")
            for level, stats in self.session_stats['level_stats'].items():
                if stats['attempted'] > 0:
                    level_accuracy = (stats['correct'] / stats['attempted']) * 100
                    print(f"   {level.upper()}: {stats['correct']}/{stats['attempted']} ({level_accuracy:.1f}%)")
        
        # Wrong answers breakdown
        if self.session_stats['wrong_answers']:
            print(f"\n{Colors.WARNING}❌ Words You Got Wrong:{Colors.RESET}")
            for i, wrong in enumerate(self.session_stats['wrong_answers'], 1):
                word = wrong['word']
                word_class = wrong['class']
                level = wrong['level']
                user_answer = wrong['user_answer']
                correct_meanings = wrong['correct_meanings']
                
                # Format correct meanings (show all)
                correct_display = ', '.join(correct_meanings)
                
                print(f"   {i}. {Colors.BOLD}{word.title()}{Colors.RESET} ({word_class}, {level.upper()})")
                if user_answer == '[SKIPPED]':
                    print(f"      Your answer: {Colors.WARNING}SKIPPED{Colors.RESET}")
                else:
                    print(f"      Your answer: {Colors.ERROR}'{user_answer}'{Colors.RESET}")
                print(f"      Correct: {Colors.SUCCESS}{correct_display}{Colors.RESET}")
                if i < len(self.session_stats['wrong_answers']):
                    print()  # Add blank line between entries except for last one
    
    def _view_statistics(self):
        """Display comprehensive statistics"""
        clear_screen()
        print_header("📊 Statistics", 60)
        
        # Overall stats
        print(f"{Colors.INFO}🏆 High Scores:{Colors.RESET}")
        print(f"   Overall: {self.top_scores.get('overall', 0)}")
        
        mode_scores = self.top_scores.get('by_mode', {})
        print(f"   Custom Mode: {mode_scores.get('custom', 0)}")
        print(f"   Adventure Mode: {mode_scores.get('adventure', 0)}")
        
        # Level stats
        print(f"\n{Colors.INFO}📈 Level High Scores:{Colors.RESET}")
        level_scores = self.top_scores.get('by_level', {})
        for level in ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']:
            score = level_scores.get(level, 0)
            description = get_level_description(level).split(' - ')[0]
            print(f"   {level.upper()}: {score:2d} ({description})")
        
        # Recent sessions
        sessions = self.top_scores.get('sessions', [])
        if sessions:
            print(f"\n{Colors.INFO}📅 Recent Sessions (Last 5):{Colors.RESET}")
            for i, session in enumerate(sessions[-5:], 1):
                score = session.get('final_score', 0)
                mode = session.get('mode', 'unknown')
                level = session.get('target_level', 'random')
                accuracy = 0
                if session.get('words_attempted', 0) > 0:
                    accuracy = (session.get('words_correct', 0) / session['words_attempted']) * 100
                
                print(f"   {i}. Score: {score:2d} | Mode: {mode:9s} | Level: {level or 'random':6s} | Accuracy: {accuracy:5.1f}%")
        
        # Word picker statistics
        print(f"\n{Colors.INFO}🎯 Learning Progress:{Colors.RESET}")
        for level in ['a1', 'a2', 'b1', 'b2']:
            level_stats = self.word_picker.get_level_statistics(level)
            mastery = level_stats.get('mastery_level', 0)
            avg_accuracy = level_stats.get('average_accuracy', 0)
            total_words = level_stats.get('total_words', 0)
            
            print(f"   {level.upper()}: {total_words:4d} words | Mastery: {mastery:5.1f}% | Avg Accuracy: {avg_accuracy:5.1f}%")
        
        # Difficult words
        difficult_words = self.word_picker.get_difficult_words(limit=5)
        if difficult_words:
            print(f"\n{Colors.WARNING}🔥 Words Needing Practice:{Colors.RESET}")
            for word_info in difficult_words:
                print(f"   {word_info['word']:12s} ({word_info['level'].upper()}) - Accuracy: {word_info['accuracy']:5.1f}%")
          # Mastered words
        mastered_words = self.word_picker.get_mastered_words(limit=5)
        if mastered_words:
            print(f"\n{Colors.SUCCESS}✅ Recently Mastered Words:{Colors.RESET}")
            for word_info in mastered_words:
                print(f"   {word_info['word']:12s} ({word_info['level'].upper()}) - Accuracy: {word_info['accuracy']:5.1f}%")
        
        # Recent words that appeared in games
        recent_words = self.word_history.get('recent_words', [])
        if recent_words:
            print(f"\n{Colors.INFO}🕐 Recently Appeared Words (Last 10):{Colors.RESET}")
            for i, word_entry in enumerate(recent_words[:10], 1):
                word = word_entry['word']
                word_class = word_entry['class']
                level = word_entry['level']
                meanings = word_entry['meanings']
                meanings_display = ', '.join(meanings[:3])
                if len(meanings) > 3:
                    meanings_display += f" (+{len(meanings) - 3} more)"
                print(f"   {i:2d}. {word:12s} ({word_class}, {level.upper()}) - {meanings_display}")
        
        # Words that were answered incorrectly
        wrong_words = self.word_history.get('wrong_words', [])
        if wrong_words:
            print(f"\n{Colors.WARNING}❌ Recently Missed Words (Last 10):{Colors.RESET}")
            for i, word_entry in enumerate(wrong_words[:10], 1):
                word = word_entry['word']
                word_class = word_entry['class']
                level = word_entry['level']
                meanings = word_entry['meanings']
                meanings_display = ', '.join(meanings[:3])
                if len(meanings) > 3:
                    meanings_display += f" (+{len(meanings) - 3} more)"
                print(f"   {i:2d}. {word:12s} ({word_class}, {level.upper()}) - {meanings_display}")        
        input(f"\n{Colors.INFO}Press Enter to return to main menu...{Colors.RESET}")
    
    def _settings_menu(self):
        """Settings and configuration menu"""
        while True:
            clear_screen()
            print_header("⚙️ Settings", 50)
            
            print("1. 🔄 Reset All Statistics")
            print("2. 🧹 Clear Translation Cache")
            print("3. 📊 Export Statistics")
            print("4. 🎯 Reset Specific Level")
            print("5. 🗑️  Wipe All Data (Factory Reset)")
            print("6. ℹ️  About")
            print("7. ↩️  Back to Main Menu")
            
            choice = input(f"\n{Colors.BOLD}Choose option (1-7): {Colors.RESET}").strip()
            
            if choice == '1':
                self._reset_statistics()
            elif choice == '2':
                self._clear_cache()
            elif choice == '3':
                self._export_statistics()
            elif choice == '4':
                self._reset_level()
            elif choice == '5':
                self._wipe_all_data()
            elif choice == '6':
                self._show_about()
            elif choice == '7':
                return
            else:
                print_error("Invalid choice. Please try again.")
                time.sleep(1)
    
    def _reset_statistics(self):
        """Reset all game statistics"""
        print_warning("⚠️  This will reset ALL your progress and high scores!")
        confirm = input(f"{Colors.BOLD}Type 'RESET' to confirm: {Colors.RESET}").strip()
        
        if confirm == 'RESET':
            # Reset word picker stats
            self.word_picker.reset_all_stats()
            
            # Reset scores
            self.top_scores = {
                'overall': 0,
                'by_level': {'a1': 0, 'a2': 0, 'b1': 0, 'b2': 0, 'c1': 0, 'c2': 0},
                'by_mode': {'custom': 0, 'adventure': 0},
                'sessions': []
            }
            self._save_scores()
            
            print_success("All statistics have been reset!")
        else:
            print_info("Reset cancelled.")
        
        time.sleep(2)
    
    def _clear_cache(self):
        """Clear translation cache"""
        self.translator.clear_cache()
        cache_stats = self.translator.get_cache_stats()
        print_success(f"Translation cache cleared! Was caching {cache_stats['cache_size']} translations.")
        time.sleep(2)
    
    def _export_statistics(self):
        """Export statistics to file"""
        try:
            export_data = {
                'export_time': datetime.now().isoformat(),
                'game_scores': self.top_scores,
                'word_statistics': self.word_picker.export_statistics(),
                'cache_stats': self.translator.get_cache_stats()
            }
            
            export_file = os.path.join(self.scores_dir, f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            if save_json_file(export_file, export_data):
                print_success(f"Statistics exported to: {export_file}")
            else:
                print_error("Failed to export statistics.")
        except Exception as e:
            print_error(f"Export error: {e}")
        
        time.sleep(2)
    
    def _reset_level(self):
        """Reset statistics for specific level"""
        print("Choose level to reset:")
        levels = ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']
        
        for i, level in enumerate(levels, 1):
            print(f"{i}. {level.upper()}")
        
        try:
            choice = int(input(f"\n{Colors.BOLD}Choose level (1-6): {Colors.RESET}")) - 1
            if 0 <= choice < len(levels):
                level = levels[choice]
                confirm = input(f"{Colors.WARNING}Reset {level.upper()} statistics? (y/N): {Colors.RESET}").strip().lower()
                
                if confirm == 'y':
                    # Reset level high score
                    self.top_scores['by_level'][level] = 0
                    self._save_scores()
                    print_success(f"Reset {level.upper()} statistics!")
                else:
                    print_info("Reset cancelled.")
            else:
                print_error("Invalid level selection.")
        except ValueError:
            print_error("Please enter a valid number.")
        
        time.sleep(2)
    
    def _show_about(self):
        """Show about information"""
        clear_screen()
        print_header("ℹ️ About Oxford Vocabulary Trainer", 60)
        
        print(f"{Colors.INFO}🎓 Oxford Vocabulary Trainer{Colors.RESET}")
        print(f"   AI-powered vocabulary learning game")
        print(f"   Version: 1.2.0")
        print(f"   Author: Rafi Project")
        print()
        print(f"{Colors.INFO}🤖 AI Features:{Colors.RESET}")
        print(f"   • LLaMA 3.1 8B Instant via Groq API for contextual translations")
        print(f"   • Advanced caching with persistent storage")
        print(f"   • Adaptive learning with weighted word selection")
        print(f"   • Smart answer validation (complete word matching)")
        print()
        print(f"{Colors.INFO}📚 Data Source:{Colors.RESET}")
        print(f"   • Oxford 3000 & 5000 most important English words")
        print(f"   • CEFR levels (A1, A2, B1, B2, C1, C2)")
        print(f"   • Part of speech classification")
        print()
        print(f"{Colors.INFO}🎮 Game Modes:{Colors.RESET}")
        print(f"   • Custom Mode: Choose specific CEFR level")
        print(f"   • Adventure Mode: Random levels A1-B2")
        print()
        print(f"{Colors.INFO}📊 Enhanced Statistics:{Colors.RESET}")
        print(f"   • Recently appeared words tracking (last 10)")
        print(f"   • Recently missed words tracking (last 10)")
        print(f"   • Complete session summaries (no truncation)")
        print(f"   • Detailed wrong answer breakdowns")
        print()
        print(f"{Colors.INFO}🧠 Learning Algorithm:{Colors.RESET}")
        print(f"   • Words you get wrong appear more frequently")
        print(f"   • Mastered words appear less often")
        print(f"   • Spaced repetition for optimal learning")
        print(f"   • Persistent word history tracking")
        print()
        print(f"{Colors.INFO}⚙️ Advanced Settings:{Colors.RESET}")
        print(f"   • Factory reset (complete data wipe)")
        print(f"   • Translation cache management")
        print(f"   • Statistics export and reset options")
        
        input(f"\n{Colors.INFO}Press Enter to return...{Colors.RESET}")
    
    def _wipe_all_data(self):
        """Wipe all data and reset to factory defaults"""
        clear_screen()
        print_header("🗑️ Factory Reset", 50)
        
        print_warning("⚠️  DANGER: This will PERMANENTLY DELETE ALL DATA!")
        print_warning("This includes:")
        print("   • All high scores and statistics")
        print("   • All learning progress and word weights")
        print("   • All translation cache")
        print("   • All session history")
        print("   • Recently appeared and missed words")
        print()
        print_warning("The application will reset to its initial state.")
        print_warning("This action CANNOT be undone!")
        
        print(f"\n{Colors.BOLD}Are you absolutely sure you want to continue?{Colors.RESET}")
        confirm1 = input(f"{Colors.ERROR}Type 'DELETE' to continue: {Colors.RESET}").strip()
        
        if confirm1 == 'DELETE':
            print(f"\n{Colors.ERROR}FINAL WARNING: All your progress will be lost forever!{Colors.RESET}")
            confirm2 = input(f"{Colors.ERROR}Type 'WIPE ALL DATA' to confirm: {Colors.RESET}").strip()
            
            if confirm2 == 'WIPE ALL DATA':
                try:
                    # Reset word picker stats
                    self.word_picker.reset_all_stats()
                    
                    # Reset all scores
                    self.top_scores = {
                        'overall': 0,
                        'by_level': {'a1': 0, 'a2': 0, 'b1': 0, 'b2': 0, 'c1': 0, 'c2': 0},
                        'by_mode': {'custom': 0, 'adventure': 0},
                        'sessions': []
                    }
                    self._save_scores()
                    
                    # Reset word history
                    self.word_history = {
                        'recent_words': [],
                        'wrong_words': []
                    }
                    self._save_word_history()
                    
                    # Clear translation cache
                    self.translator.clear_cache()
                    
                    # Remove session files
                    import glob
                    session_files = glob.glob(os.path.join(self.scores_dir, "*.json"))
                    for file_path in session_files:
                        try:
                            os.remove(file_path)
                        except:
                            pass  # Ignore errors for files that don't exist
                    
                    # Recreate essential files with default values
                    self._save_scores()
                    self._save_word_history()
                    
                    print_success("✅ Factory reset completed successfully!")
                    print_info("All data has been wiped. The application is now in its initial state.")
                    print_info("You can start fresh with a clean slate.")
                    
                except Exception as e:
                    print_error(f"Error during factory reset: {str(e)}")
                    print_warning("Some data may not have been completely removed.")
            else:
                print_info("Factory reset cancelled.")
        else:
            print_info("Factory reset cancelled.")
        
        input(f"\n{Colors.INFO}Press Enter to return to settings menu...{Colors.RESET}")
