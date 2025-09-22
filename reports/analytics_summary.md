# 📊 Analytics Summary

## 📰 Distribusi Sumber
Total artikel relatif seimbang – **Tempo: 396** dan **Detik: 341** – sehingga analisis dapat dilakukan tanpa perlu pembobotan khusus.

## 📈 Tren Harian
- Lonjakan publikasi terjadi pada **20–21 September**  
  - **Detik:** puncak 152 artikel  
  - **Tempo:** puncak 187 artikel  
- Setelah itu terjadi penurunan tajam pada 22 September.  
- **Rolling mean 7 hari** menegaskan **Tempo lebih konsisten** dan rata-rata volume hariannya di atas Detik.

## ✍️ Panjang Artikel
- Mayoritas artikel berada di kisaran **200–400 kata** (≈ **2–3 menit** baca), menunjukkan konten berita yang ringkas dan mudah dikonsumsi.
- **Tempo** cenderung sedikit lebih panjang (**median ±330 kata**) dibanding **Detik** (**±305 kata**).
- Sejumlah kecil artikel **>800 kata** menjadi **outlier**.

## 🗂️ Kualitas Data
- **Missing value:** hanya kolom **`author`** dengan sekitar **5%** nilai hilang.
- **Duplikasi:** kolom **`published_at`** memiliki sekitar **20%** duplikasi timestamp, menandakan banyak artikel dipublikasikan di waktu yang sama.

## 🔎 Topik / Rubrik Populer
- Kedua portal banyak menulis tentang **“Indonesia”, “negara”, dan “masyarakat”**.
- **Detik:** menonjolkan isu peristiwa seperti *korban* dan *kecelakaan*.
- **Tempo:** lebih fokus pada politik/tokoh publik seperti *wahyudin* dan *partai*.

---

## 🌟 Insight Utama
- **Sumber paling konsisten:** **Tempo**.
- **Slot waktu publikasi paling ramai:** **20–21 September**.
- **Rubrik dominan:** Isu nasional & masyarakat; **Detik** lebih ke peristiwa, **Tempo** ke politik.

---

## 💡 Rekomendasi
- **Pembersihan Data:** Tangani missing value pada kolom `author` dan kelola duplikasi `published_at` bila diperlukan analisis berbasis timestamp unik.
- **Analisis Trafik:** Gunakan periode **20–21 September** sebagai patokan puncak trafik publikasi/berita.
- **Analisis Topik:** Pertimbangkan perbedaan fokus liputan  
  - Detik: peristiwa  
  - Tempo: politik/tokoh  
  saat membuat analisis perbandingan tema.
- **Normalisasi Panjang Artikel:** Untuk analitik lanjutan (mis. sentiment, topik modeling) lakukan normalisasi agar outlier artikel sangat panjang tidak mempengaruhi hasil.

---

## ✅ Kesimpulan
**Tempo** sedikit lebih produktif dan stabil. **Puncak publikasi terjadi 20–21 September**, dan topik berita dari kedua portal berpusat pada **isu nasional** dengan fokus spesifik yang berbeda.