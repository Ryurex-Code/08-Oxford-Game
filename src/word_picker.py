"""
Word picker with adaptive weighting system for Oxford Vocabulary Trainer
"""
import random
import pandas as pd
from typing import List, Dict, Tuple, Optional
from utils import load_json_file, save_json_file, print_info, print_error

class WordPicker:
    """Handle word selection with adaptive weighting"""
    
    def __init__(self, data_df: pd.DataFrame, weights_file: str):
        """
        Initialize word picker
        
        Args:
            data_df: DataFrame containing word data
            weights_file: Path to weights JSON file
        """
        self.data_df = data_df
        self.weights_file = weights_file
        self.word_weights = self._load_weights()
        
        # Initialize weights for new words
        self._initialize_new_words()
        
    def _load_weights(self) -> Dict[str, Dict]:
        """Load word weights from file"""
        default_weights = {}
        weights = load_json_file(self.weights_file, default_weights)
        print_info(f"Loaded weights for {len(weights)} words")
        return weights
    
    def _save_weights(self) -> bool:
        """Save current weights to file"""
        success = save_json_file(self.weights_file, self.word_weights)
        if success:
            print_info(f"Saved weights for {len(self.word_weights)} words")
        return success
    
    def _initialize_new_words(self):
        """Initialize weights for words not in weights file"""
        new_words_count = 0
        
        for _, row in self.data_df.iterrows():
            word_key = f"{row['word']}_{row['class']}_{row['level']}"
            
            if word_key not in self.word_weights:
                self.word_weights[word_key] = {
                    'weight': 1.0,  # Default weight
                    'correct_count': 0,
                    'wrong_count': 0,
                    'total_attempts': 0,
                    'last_seen': None,
                    'consecutive_correct': 0,
                    'consecutive_wrong': 0
                }
                new_words_count += 1
        
        if new_words_count > 0:
            print_info(f"Initialized weights for {new_words_count} new words")
            self._save_weights()
    
    def get_weighted_word(self, level: Optional[str] = None) -> Optional[Tuple[str, str, str]]:
        """
        Select a word based on weights and level
        
        Args:
            level: CEFR level filter (a1, a2, b1, b2, c1, c2) or None for all
            
        Returns:
            Tuple of (word, class, level) or None if no words available
        """
        # Filter data by level if specified
        if level:
            filtered_df = self.data_df[self.data_df['level'] == level.lower()]
        else:
            filtered_df = self.data_df
        
        if filtered_df.empty:
            print_error(f"No words available for level: {level}")
            return None
        
        # Prepare weighted selection
        words_data = []
        weights = []
        
        for _, row in filtered_df.iterrows():
            word_key = f"{row['word']}_{row['class']}_{row['level']}"
            word_weight = self.word_weights.get(word_key, {}).get('weight', 1.0)
            
            words_data.append((row['word'], row['class'], row['level']))
            weights.append(word_weight)
        
        if not words_data:
            return None
        
        # Weighted random selection
        try:
            selected_word = random.choices(words_data, weights=weights, k=1)[0]
            return selected_word
        except Exception as e:
            print_error(f"Error in weighted selection: {e}")
            # Fallback to simple random selection
            return random.choice(words_data)
    
    def update_word_performance(self, word: str, word_class: str, level: str, is_correct: bool):
        """
        Update word performance statistics and adjust weight
        
        Args:
            word: The word
            word_class: Part of speech
            level: CEFR level
            is_correct: Whether the answer was correct
        """
        word_key = f"{word}_{word_class}_{level}"
        
        # Initialize if not exists
        if word_key not in self.word_weights:
            self.word_weights[word_key] = {
                'weight': 1.0,
                'correct_count': 0,
                'wrong_count': 0,
                'total_attempts': 0,
                'last_seen': None,
                'consecutive_correct': 0,
                'consecutive_wrong': 0
            }
        
        word_stats = self.word_weights[word_key]
        
        # Update basic stats
        word_stats['total_attempts'] += 1
        word_stats['last_seen'] = pd.Timestamp.now().isoformat()
        
        if is_correct:
            word_stats['correct_count'] += 1
            word_stats['consecutive_correct'] += 1
            word_stats['consecutive_wrong'] = 0
        else:
            word_stats['wrong_count'] += 1
            word_stats['consecutive_wrong'] += 1
            word_stats['consecutive_correct'] = 0
        
        # Calculate new weight using adaptive algorithm
        new_weight = self._calculate_adaptive_weight(word_stats)
        word_stats['weight'] = new_weight
        
        # Save updated weights
        self._save_weights()
        
        # Log performance update
        accuracy = word_stats['correct_count'] / word_stats['total_attempts'] * 100
        print_info(f"Updated '{word}': accuracy={accuracy:.1f}%, weight={new_weight:.2f}")
    
    def _calculate_adaptive_weight(self, stats: Dict) -> float:
        """
        Calculate adaptive weight based on performance statistics
        
        Args:
            stats: Word performance statistics
            
        Returns:
            New weight value
        """
        total_attempts = stats['total_attempts']
        correct_count = stats['correct_count']
        consecutive_correct = stats['consecutive_correct']
        consecutive_wrong = stats['consecutive_wrong']
        
        if total_attempts == 0:
            return 1.0
        
        # Calculate accuracy
        accuracy = correct_count / total_attempts
        
        # Base weight calculation
        if accuracy >= 0.8:  # High accuracy (80%+)
            base_weight = 0.3  # Lower weight (appears less often)
        elif accuracy >= 0.6:  # Moderate accuracy (60-79%)
            base_weight = 0.7
        elif accuracy >= 0.4:  # Low accuracy (40-59%)
            base_weight = 1.2
        else:  # Very low accuracy (<40%)
            base_weight = 2.0  # Higher weight (appears more often)
        
        # Consecutive performance modifiers
        if consecutive_correct >= 3:
            # Reduce weight significantly for consistently correct answers
            consecutive_modifier = 0.5
        elif consecutive_wrong >= 2:
            # Increase weight significantly for consecutive wrong answers
            consecutive_modifier = 2.5
        else:
            consecutive_modifier = 1.0
        
        # Attempt-based modifier (newer words get slight boost)
        if total_attempts <= 3:
            attempt_modifier = 1.2  # Slight boost for new words
        elif total_attempts >= 10:
            attempt_modifier = 0.9  # Slight reduction for well-practiced words
        else:
            attempt_modifier = 1.0
        
        # Calculate final weight
        final_weight = base_weight * consecutive_modifier * attempt_modifier
        
        # Ensure weight stays within reasonable bounds
        return max(0.1, min(5.0, final_weight))
    
    def get_word_statistics(self, word: str, word_class: str, level: str) -> Optional[Dict]:
        """Get statistics for a specific word"""
        word_key = f"{word}_{word_class}_{level}"
        return self.word_weights.get(word_key)
    
    def get_level_statistics(self, level: str) -> Dict:
        """Get aggregated statistics for a level"""
        level_words = []
        
        for word_key, stats in self.word_weights.items():
            if word_key.endswith(f"_{level}"):
                level_words.append(stats)
        
        if not level_words:
            return {
                'total_words': 0,
                'total_attempts': 0,
                'total_correct': 0,
                'average_accuracy': 0.0,
                'mastery_level': 0.0
            }
        
        total_words = len(level_words)
        total_attempts = sum(w['total_attempts'] for w in level_words)
        total_correct = sum(w['correct_count'] for w in level_words)
        
        average_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        
        # Calculate mastery level (percentage of words with >80% accuracy)
        mastered_words = sum(1 for w in level_words 
                           if w['total_attempts'] >= 3 and 
                           w['correct_count'] / w['total_attempts'] >= 0.8)
        mastery_level = (mastered_words / total_words * 100) if total_words > 0 else 0
        
        return {
            'total_words': total_words,
            'total_attempts': total_attempts,
            'total_correct': total_correct,
            'average_accuracy': average_accuracy,
            'mastery_level': mastery_level
        }
    
    def get_difficult_words(self, level: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Get words that need more practice (high weight)
        
        Args:
            level: Filter by level
            limit: Maximum number of words to return
            
        Returns:
            List of dictionaries with word info and stats
        """
        difficult_words = []
        
        for word_key, stats in self.word_weights.items():
            parts = word_key.split('_')
            if len(parts) >= 3:
                word = parts[0]
                word_class = parts[1]
                word_level = parts[2]
                
                # Filter by level if specified
                if level and word_level != level.lower():
                    continue
                
                # Only include words with attempts and high weight
                if stats['total_attempts'] >= 2 and stats['weight'] >= 1.5:
                    accuracy = (stats['correct_count'] / stats['total_attempts'] * 100) if stats['total_attempts'] > 0 else 0
                    
                    difficult_words.append({
                        'word': word,
                        'class': word_class,
                        'level': word_level,
                        'weight': stats['weight'],
                        'accuracy': accuracy,
                        'attempts': stats['total_attempts'],
                        'consecutive_wrong': stats['consecutive_wrong']
                    })
        
        # Sort by weight (descending) and return top results
        difficult_words.sort(key=lambda x: x['weight'], reverse=True)
        return difficult_words[:limit]
    
    def get_mastered_words(self, level: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Get words that have been mastered (low weight, high accuracy)
        
        Args:
            level: Filter by level
            limit: Maximum number of words to return
            
        Returns:
            List of dictionaries with word info and stats
        """
        mastered_words = []
        
        for word_key, stats in self.word_weights.items():
            parts = word_key.split('_')
            if len(parts) >= 3:
                word = parts[0]
                word_class = parts[1]
                word_level = parts[2]
                
                # Filter by level if specified
                if level and word_level != level.lower():
                    continue
                
                # Only include words with sufficient attempts and high accuracy
                if (stats['total_attempts'] >= 3 and 
                    stats['correct_count'] / stats['total_attempts'] >= 0.8):
                    
                    accuracy = stats['correct_count'] / stats['total_attempts'] * 100
                    
                    mastered_words.append({
                        'word': word,
                        'class': word_class,
                        'level': word_level,
                        'weight': stats['weight'],
                        'accuracy': accuracy,
                        'attempts': stats['total_attempts'],
                        'consecutive_correct': stats['consecutive_correct']
                    })
        
        # Sort by accuracy (descending) then by consecutive correct
        mastered_words.sort(key=lambda x: (x['accuracy'], x['consecutive_correct']), reverse=True)
        return mastered_words[:limit]
    
    def reset_word_stats(self, word: str, word_class: str, level: str):
        """Reset statistics for a specific word"""
        word_key = f"{word}_{word_class}_{level}"
        if word_key in self.word_weights:
            self.word_weights[word_key] = {
                'weight': 1.0,
                'correct_count': 0,
                'wrong_count': 0,
                'total_attempts': 0,
                'last_seen': None,
                'consecutive_correct': 0,
                'consecutive_wrong': 0
            }
            self._save_weights()
            print_info(f"Reset statistics for '{word}'")
    
    def reset_all_stats(self):
        """Reset all word statistics"""
        for word_key in self.word_weights:
            self.word_weights[word_key] = {
                'weight': 1.0,
                'correct_count': 0,
                'wrong_count': 0,
                'total_attempts': 0,
                'last_seen': None,
                'consecutive_correct': 0,
                'consecutive_wrong': 0
            }
        self._save_weights()
        print_info("Reset all word statistics")
    
    def export_statistics(self) -> Dict:
        """Export all statistics for analysis"""
        export_data = {
            'total_words': len(self.word_weights),
            'words': {}
        }
        
        for word_key, stats in self.word_weights.items():
            parts = word_key.split('_')
            if len(parts) >= 3:
                word = parts[0]
                word_class = parts[1]
                level = parts[2]
                
                accuracy = (stats['correct_count'] / stats['total_attempts'] * 100) if stats['total_attempts'] > 0 else 0
                
                export_data['words'][word_key] = {
                    'word': word,
                    'class': word_class,
                    'level': level,
                    'accuracy': accuracy,
                    **stats
                }
        
        return export_data
