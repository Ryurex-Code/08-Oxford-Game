"""
LLM Translator using Groq API for Oxford Vocabulary Trainer
"""
import os
import time
from typing import List, Optional
from groq import Groq
from dotenv import load_dotenv
from utils import print_error, print_warning, print_info, parse_llm_response

class LLMTranslator:
    """Handle LLM translation using Groq API"""
    
    def __init__(self):
        """Initialize the translator with Groq client"""
        load_dotenv()
        
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"  # Use the appropriate model for your needs
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.timeout = int(os.getenv('TRANSLATION_TIMEOUT', 10))
        
        # Cache for translations to avoid repeated API calls
        self.translation_cache = {}
        
    def create_translation_prompt(self, word: str, word_class: str) -> str:
        """Create optimized prompt for translation"""
        return f"""Translate the English word "{word}" (as a {word_class}) into Indonesian. 
Provide all possible meanings in different contexts, separated by commas.
Return ONLY a list of Indonesian meanings without explanation or additional text.
Focus on the most common and useful meanings.

Example format: "lari, menjalankan, mengelola, berlari, mengoperasikan"

Word: {word}
Class: {word_class}
Indonesian meanings:"""

    def translate_word(self, word: str, word_class: str) -> List[str]:
        """
        Translate word using LLM with caching and error handling
        
        Args:
            word: English word to translate
            word_class: Part of speech (noun, verb, etc.)
            
        Returns:
            List of Indonesian meanings
        """
        # Create cache key
        cache_key = f"{word.lower()}_{word_class.lower()}"
        
        # Check cache first
        if cache_key in self.translation_cache:
            print_info(f"Using cached translation for '{word}'")
            return self.translation_cache[cache_key]
        
        # Attempt translation with retries
        for attempt in range(self.max_retries):
            try:
                print_info(f"Translating '{word}' (attempt {attempt + 1}/{self.max_retries})...")
                
                prompt = self.create_translation_prompt(word, word_class)
                
                # Make API call with timeout
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional English-Indonesian translator. Provide accurate, contextual translations without explanations."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=150,
                    temperature=0.3,  # Lower temperature for more consistent results
                    timeout=self.timeout
                )
                
                # Extract response content
                translation_text = response.choices[0].message.content.strip()
                
                # Parse the response
                meanings = parse_llm_response(translation_text)
                
                if meanings:
                    # Cache successful translation
                    self.translation_cache[cache_key] = meanings
                    print_info(f"Successfully translated '{word}' with {len(meanings)} meanings")
                    return meanings
                else:
                    print_warning(f"Empty translation received for '{word}'")
                    
            except Exception as e:
                error_msg = str(e)
                print_error(f"Translation attempt {attempt + 1} failed: {error_msg}")
                
                # Wait before retry (exponential backoff)
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    print_info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
        
        # Fallback if all attempts fail
        print_error(f"Failed to translate '{word}' after {self.max_retries} attempts")
        return self._get_fallback_translation(word, word_class)
    
    def _get_fallback_translation(self, word: str, word_class: str) -> List[str]:
        """
        Provide fallback translations for common words
        
        Args:
            word: English word
            word_class: Part of speech
            
        Returns:
            List of basic Indonesian meanings
        """
        # Basic fallback dictionary for common words
        fallback_dict = {
            # Common verbs
            'be': ['adalah', 'menjadi', 'berada'],
            'have': ['mempunyai', 'memiliki', 'punya'],
            'do': ['melakukan', 'mengerjakan', 'berbuat'],
            'say': ['berkata', 'mengatakan', 'mengucapkan'],
            'get': ['mendapat', 'memperoleh', 'mengambil'],
            'make': ['membuat', 'menciptakan', 'menjadikan'],
            'go': ['pergi', 'berjalan', 'berangkat'],
            'know': ['tahu', 'mengetahui', 'kenal'],
            'take': ['mengambil', 'membawa', 'menerima'],
            'see': ['melihat', 'memandang', 'menonton'],
            'come': ['datang', 'tiba', 'hadir'],
            'think': ['berpikir', 'mengira', 'menganggap'],
            'look': ['melihat', 'menatap', 'tampak'],
            'want': ['ingin', 'mau', 'menginginkan'],
            'give': ['memberi', 'memberikan', 'menyerahkan'],
            'use': ['menggunakan', 'memakai', 'menggunakan'],
            'find': ['menemukan', 'mencari', 'mendapati'],
            'tell': ['menceritakan', 'memberitahu', 'mengabarkan'],
            'ask': ['bertanya', 'meminta', 'menanyakan'],
            'work': ['bekerja', 'kerja', 'pekerjaan'],
            'feel': ['merasa', 'merasakan', 'perasaan'],
            'try': ['mencoba', 'berusaha', 'coba'],
            'leave': ['meninggalkan', 'pergi', 'keluar'],
            'call': ['memanggil', 'menelepon', 'menyebut'],
            
            # Common nouns
            'time': ['waktu', 'masa', 'kali'],
            'person': ['orang', 'pribadi', 'individu'],
            'year': ['tahun', 'tahunan'],
            'way': ['cara', 'jalan', 'metode'],
            'day': ['hari', 'siang'],
            'thing': ['hal', 'benda', 'sesuatu'],
            'man': ['pria', 'laki-laki', 'orang'],
            'world': ['dunia', 'bumi'],
            'life': ['kehidupan', 'hidup', 'nyawa'],
            'hand': ['tangan', 'kaki tangan'],
            'part': ['bagian', 'sebagian', 'komponen'],
            'child': ['anak', 'bocah', 'kecil'],
            'eye': ['mata', 'pandangan'],
            'woman': ['wanita', 'perempuan', 'ibu'],
            'place': ['tempat', 'lokasi', 'wilayah'],
            'work': ['pekerjaan', 'kerja', 'tugas'],
            'week': ['minggu', 'pekan'],
            'case': ['kasus', 'hal', 'keadaan'],
            'point': ['poin', 'titik', 'hal'],
            'home': ['rumah', 'tempat tinggal', 'kampung halaman'],
            'water': ['air', 'cairan'],
            'room': ['ruang', 'kamar', 'tempat'],
            'mother': ['ibu', 'mama'],
            'area': ['area', 'daerah', 'wilayah'],
            'money': ['uang', 'duit', 'modal'],
            'story': ['cerita', 'kisah', 'dongeng'],
            'fact': ['fakta', 'kenyataan', 'hal'],
            'month': ['bulan'],
            'lot': ['banyak', 'sekali', 'tempat'],
            'right': ['benar', 'kanan', 'hak'],
            'study': ['belajar', 'studi', 'penelitian'],
            'book': ['buku', 'kitab'],
            'word': ['kata', 'perkataan', 'ucapan'],
            'business': ['bisnis', 'usaha', 'perdagangan'],
            'issue': ['masalah', 'isu', 'terbitan'],
            'side': ['sisi', 'samping', 'pihak'],
            'kind': ['jenis', 'macam', 'baik hati'],
            'head': ['kepala', 'ketua', 'pimpinan'],
            'house': ['rumah', 'gedung'],
            'service': ['layanan', 'jasa', 'dinas'],
            'friend': ['teman', 'sahabat', 'kawan'],
            'father': ['ayah', 'bapak', 'papa'],
            'power': ['kekuatan', 'tenaga', 'listrik'],
            'hour': ['jam', 'waktu'],
            'game': ['permainan', 'pertandingan', 'game'],
            'line': ['garis', 'baris', 'antrian'],
            'end': ['akhir', 'ujung', 'tamat'],
            'member': ['anggota', 'peserta'],
            'law': ['hukum', 'undang-undang', 'aturan'],
            'car': ['mobil', 'kereta'],
            'city': ['kota', 'perkotaan'],
            'community': ['komunitas', 'masyarakat', 'lingkungan'],
            'name': ['nama', 'sebutan'],
            'president': ['presiden', 'ketua'],
            'team': ['tim', 'kelompok', 'regu'],
            'minute': ['menit', 'kecil', 'detail'],
            'idea': ['ide', 'gagasan', 'pikiran'],
            'kid': ['anak', 'bocah'],
            'body': ['tubuh', 'badan', 'mayat'],
            'information': ['informasi', 'keterangan', 'data'],
            'back': ['punggung', 'belakang', 'kembali'],
            'parent': ['orang tua', 'induk'],
            'face': ['wajah', 'muka', 'menghadapi'],
            'others': ['yang lain', 'orang lain'],
            'level': ['tingkat', 'level', 'taraf'],
            'office': ['kantor', 'jabatan'],
            'door': ['pintu', 'gerbang'],
            'health': ['kesehatan', 'sehat'],
            'person': ['orang', 'pribadi'],
            'art': ['seni', 'kesenian'],
            'war': ['perang', 'peperangan'],
            'history': ['sejarah', 'riwayat'],
            'party': ['pesta', 'partai', 'kelompok'],
            'result': ['hasil', 'akibat', 'kesimpulan'],
            'change': ['perubahan', 'ganti', 'uang kembalian'],
            'morning': ['pagi', 'subuh'],
            'reason': ['alasan', 'sebab'],
            'research': ['penelitian', 'riset'],
            'girl': ['gadis', 'perempuan', 'anak perempuan'],
            'guy': ['lelaki', 'pria', 'orang'],
            'moment': ['saat', 'momen', 'waktu'],
            'air': ['udara', 'angin', 'penampilan'],
            'teacher': ['guru', 'pengajar'],
            'force': ['kekuatan', 'memaksa', 'pasukan'],
            'education': ['pendidikan', 'pengajaran'],
            
            # Common adjectives
            'good': ['baik', 'bagus', 'hebat'],
            'new': ['baru', 'segar'],
            'first': ['pertama', 'awal'],
            'last': ['terakhir', 'lalu', 'bertahan'],
            'long': ['panjang', 'lama'],
            'great': ['hebat', 'besar', 'bagus'],
            'little': ['kecil', 'sedikit'],
            'own': ['sendiri', 'memiliki'],
            'other': ['lain', 'yang lain'],
            'old': ['tua', 'lama'],
            'right': ['benar', 'kanan'],
            'big': ['besar', 'raya'],
            'high': ['tinggi', 'naik'],
            'different': ['berbeda', 'beda'],
            'small': ['kecil', 'kecil-kecil'],
            'large': ['besar', 'luas'],
            'next': ['berikutnya', 'selanjutnya'],
            'early': ['awal', 'dini', 'cepat'],
            'young': ['muda', 'remaja'],
            'important': ['penting', 'utama'],
            'few': ['sedikit', 'beberapa'],
            'public': ['umum', 'publik', 'rakyat'],
            'bad': ['buruk', 'jelek', 'jahat'],
            'same': ['sama', 'serupa'],
            'able': ['mampu', 'bisa', 'sanggup'],
        }
        
        word_lower = word.lower()
        if word_lower in fallback_dict:
            print_warning(f"Using fallback translation for '{word}'")
            return fallback_dict[word_lower]
        
        # If no fallback available, return generic response
        print_warning(f"No fallback available for '{word}'")
        return [f"[Terjemahan untuk '{word}']"]
    
    def batch_translate(self, words_data: List[tuple]) -> dict:
        """
        Translate multiple words in batch
        
        Args:
            words_data: List of tuples (word, word_class)
            
        Returns:
            Dictionary mapping word to translations
        """
        translations = {}
        total_words = len(words_data)
        
        print_info(f"Starting batch translation of {total_words} words...")
        
        for i, (word, word_class) in enumerate(words_data, 1):
            print_info(f"Progress: {i}/{total_words} - Translating '{word}'")
            translations[word] = self.translate_word(word, word_class)
            
            # Brief pause between requests to avoid rate limiting
            time.sleep(0.5)
        
        print_info(f"Batch translation completed! Translated {len(translations)} words.")
        return translations
    
    def clear_cache(self):
        """Clear translation cache"""
        self.translation_cache.clear()
        print_info("Translation cache cleared")
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        return {
            'cache_size': len(self.translation_cache),
            'cached_words': list(self.translation_cache.keys())
        }
