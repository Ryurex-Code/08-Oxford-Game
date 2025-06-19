# 🎓 Oxford Vocabulary Trainer - Cara Penggunaan Lengkap

## Setup Cepat

1. **Dapatkan API Key Groq (GRATIS)**
   - Kunjungi: https://console.groq.com/
   - Daftar/login dengan akun Anda
   - Buat API key baru
   - Copy API key

2. **Konfigurasi Environment**
   - Buka file `.env` 
   - Ganti `your_groq_api_key_here` dengan API key Anda
   - Simpan file

3. **Jalankan Aplikasi**
   ```bash
   python main.py
   ```

## Contoh Konfigurasi .env

```env
# Groq API Configuration
GROQ_API_KEY=gsk_abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx

# Game Configuration
DEFAULT_DATASET=oxford_3000
MAX_RETRIES=3
TRANSLATION_TIMEOUT=10
```

## Mode Permainan

### 🎯 Custom Mode
- Pilih level spesifik (A1, A2, B1, B2, C1, C2)
- Fokus pembelajaran per level
- Cocok untuk belajar sistematis
- Track high score per level

### 🎲 Adventure Mode  
- Level acak A1-B2
- Lebih menantang dan bervariasi
- Cocok untuk menguji kemampuan overall
- Dynamic difficulty progression

## Panduan Bermain Lengkap

### Kontrol Game
1. **Ketik jawaban**: Terjemahan Indonesia dari kata Inggris
2. **'hint'**: Minta petunjuk 2 huruf pertama
3. **'skip'**: Lewati kata (dihitung salah, masuk ke wrong words)
4. **'quit'**: Keluar dari permainan dan lihat summary

### Validasi Jawaban (BARU!)
- **Validasi kata lengkap**: "kap" TIDAK diterima untuk "kapal"
- **Multi-word support**: "mata uang" diterima untuk compound words
- **Case-insensitive**: "Rumah" = "rumah" = "RUMAH"
- **Exact matching**: Harus kata lengkap yang tepat

### Session Summary (ENHANCED!)
Setelah game berakhir, Anda akan melihat:
- **Words Attempted**: Total kata yang dicoba
- **Words Correct**: Total jawaban benar
- **Accuracy**: Persentase keberhasilan
- **Best Streak**: Streak terpanjang dalam sesi
- **Level Breakdown**: Performance per level
- **❌ Words You Got Wrong**: Daftar lengkap kata yang salah dengan:
  - Nama kata, kelas kata, dan level
  - Jawaban Anda
  - **SEMUA jawaban benar** (tidak ada truncation lagi!)

## 📊 Menu Statistics (BARU!)

### High Scores
- Overall top score
- High score per level (A1-C2)
- High score per mode (Custom/Adventure)

### Recent Sessions
- 5 sesi terakhir dengan detail score, mode, level, dan accuracy

### Learning Progress  
- Mastery level per level
- Average accuracy per level
- Total words per level

### 🕐 Recently Appeared Words (FITUR BARU!)
- **10 kata terakhir** yang muncul dalam game
- Format: kata (kelas, level) - arti1, arti2, arti3 (+X more)
- Membantu review kata-kata yang baru dipelajari

### ❌ Recently Missed Words (FITUR BARU!)
- **10 kata terakhir** yang dijawab salah atau di-skip
- Format sama dengan recently appeared
- **Fokus belajar** pada kata-kata yang perlu diperbaiki

## ⚙️ Settings Menu (ENHANCED!)

### 1. 🔄 Reset All Statistics
- Reset semua high score dan progress
- Konfirmasi dengan mengetik 'RESET'

### 2. 🧹 Clear Translation Cache
- Hapus cache terjemahan AI
- Useful jika ada masalah translation

### 3. 📊 Export Statistics  
- Export semua data ke file JSON
- Backup progress Anda

### 4. 🎯 Reset Specific Level
- Reset progress level tertentu saja
- Pilih level A1-C2

### 5. 🗑️ Wipe All Data (Factory Reset) - FITUR BARU!
- **HAPUS SEMUA DATA** kembali ke kondisi awal
- Double confirmation safety:
  1. Ketik 'DELETE' untuk konfirmasi pertama
  2. Ketik 'WIPE ALL DATA' untuk konfirmasi final
- Menghapus:
  - Semua high score dan statistik
  - Semua learning progress dan word weights
  - Semua translation cache
  - Semua session history
  - Recently appeared dan missed words
  - **TIDAK DAPAT DIBATALKAN!**

### 6. ℹ️ About
- Informasi aplikasi dan fitur terbaru

## Fitur AI Translation (ENHANCED!)

- Menggunakan **LLaMA 3.1 8B Instant** via Groq API
- Memberikan **multiple makna** kata kontekstual
- **Advanced caching** dengan persistent storage
- **Smart retry logic** dengan exponential backoff
- Fallback system untuk reliability
- **Offline capability** dengan cached translations

## Sistem Pembelajaran Adaptif (IMPROVED!)

### Word Weighting Algorithm
- **Kata yang salah** → weight naik → muncul lebih sering
- **Kata yang benar** → weight turun → muncul lebih jarang  
- **Consecutive wrong** → weight naik drastis
- **Consecutive correct** → weight turun drastis

### Performance Tracking
- **Accuracy tracking** per kata individual
- **Last seen timestamp** untuk spaced repetition
- **Total attempts** dan success rate
- **Word history** dengan persistent storage

### Spaced Repetition
- Kata sulit mendapat **prioritas tinggi**
- Kata mudah **fade ke background**
- **New words** mendapat boost selection
- **Adaptive intervals** berdasarkan performance
## Tips Bermain & Strategi Belajar

### Untuk Pemula
1. **Mulai dari A1**: Bangun fondasi yang kuat
2. **Gunakan 'hint'**: Jika kesulitan, minta petunjuk
3. **Jangan takut 'skip'**: Lewati kata yang terlalu sulit, akan muncul lagi
4. **Review Statistics**: Cek Recently Missed Words untuk fokus belajar

### Untuk Advanced
1. **Adventure Mode**: Challenge yourself dengan random levels
2. **Target Accuracy**: Usahakan 80%+ accuracy per level
3. **Factory Reset**: Mulai fresh untuk test kemampuan real
4. **Export Statistics**: Backup progress sebelum reset

### Mengoptimalkan Pembelajaran
- **Consistency**: Main setiap hari 10-15 menit
- **Review Wrong Words**: Fokus pada Recently Missed Words
- **Progressive Learning**: A1 → A2 → B1 → B2 secara bertahap
- **Challenge Yourself**: Adventure mode setelah menguasai level tertentu

## Fitur AI Translation (ENHANCED!)

- Menggunakan **LLaMA 3.1 8B Instant** via Groq API
- Memberikan **multiple makna** kata kontekstual
- **Advanced caching** dengan persistent storage
- **Smart retry logic** dengan exponential backoff
- Fallback system untuk reliability
- **Offline capability** dengan cached translations

## Sistem Pembelajaran Adaptif (IMPROVED!)

### Word Weighting Algorithm
- **Kata yang salah** → weight naik → muncul lebih sering
- **Kata yang benar** → weight turun → muncul lebih jarang  
- **Consecutive wrong** → weight naik drastis
- **Consecutive correct** → weight turun drastis

### Performance Tracking
- **Accuracy tracking** per kata individual
- **Last seen timestamp** untuk spaced repetition
- **Total attempts** dan success rate
- **Word history** dengan persistent storage

### Spaced Repetition
- Kata sulit mendapat **prioritas tinggi**
- Kata mudah **fade ke background**
- **New words** mendapat boost selection
- **Adaptive intervals** berdasarkan performance

## Troubleshooting & FAQ

### Error Messages
**Error: GROQ_API_KEY not configured**
- Pastikan sudah mengisi API key di file `.env`
- Restart aplikasi setelah edit `.env`

**Translation fails / "Failed to translate"**
- Periksa koneksi internet
- Verifikasi API key masih valid di console.groq.com
- Check quota limit API

**ImportError / Module not found**
- Jalankan: `pip install -r requirements.txt`
- Pastikan Python 3.8+ terinstall

**"No words available for level"**
- Pastikan file `data/oxford_3000.csv` ada
- Check format CSV sesuai dengan header yang benar

### Performance Issues
**Aplikasi lambat**
- Clear translation cache di Settings
- Factory reset jika data terlalu banyak
- Check storage space tersisa

**Memory usage tinggi**
- Restart aplikasi setiap beberapa jam usage
- Factory reset untuk clean start

### Data & Progress
**Kehilangan progress**
- Export statistics secara berkala
- Backup folder `scores/` manual
- Jangan hapus file di folder `scores/`

**Ingin mulai ulang sepenuhnya**
- Gunakan Factory Reset di Settings
- Atau hapus manual folder `scores/`

## Testing & Validation

### Test Installation
```bash
python main.py --test  # (fitur coming soon)
```

### Manual Testing Checklist
1. ✅ API key configured correctly
2. ✅ Can load word data
3. ✅ AI translation working
4. ✅ Game modes accessible
5. ✅ Statistics saving properly
6. ✅ Word history tracking

## Advanced Features

### Data Export Format
Exported statistics dalam format JSON dengan struktur:
```json
{
  "high_scores": {...},
  "word_weights": {...},
  "word_history": {...},
  "export_timestamp": "..."
}
```

### File Structure
```
scores/
├── top_score.json      # High scores
├── word_weights.json   # Learning weights
├── word_history.json   # Recently appeared/missed words
└── current_session.json # Active session data
```

## Dukungan & Support

### Self-Help
1. **Baca error message** dengan teliti
2. **Check file `.env`** sudah benar
3. **Restart aplikasi** setelah perubahan config
4. **Verifikasi koneksi internet** aktif

### Troubleshooting Steps
1. Jalankan aplikasi dengan Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`  
3. Verify Groq API key valid dan aktif
4. Check file permissions di folder `scores/`
5. Pastikan ada space storage yang cukup

---

**Selamat Belajar! 🎓📚**  
Master bahasa Inggris dengan kekuatan AI dan adaptive learning!
