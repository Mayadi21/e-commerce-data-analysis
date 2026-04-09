# 📊 E-Commerce Data Analysis Dashboard

Proyek ini berisi analisis data e-commerce serta dashboard interaktif menggunakan **Streamlit**.

---

## 📁 Struktur Project

```
submission/
├── notebook.ipynb
├── readme.md
├── requirements.txt
├── url.txt
│
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
│
└── data/
    ├── customers_dataset.csv
    ├── geolocation_dataset.csv
    ├── orders_dataset.csv
    ├── order_items_dataset.csv
    ├── order_payments_dataset.csv
    ├── order_reviews_dataset.csv
    ├── products_dataset.csv
    ├── product_category_name_translation.csv
    └── sellers_dataset.csv
```

---

## ⚙️ 1. Membuat Virtual Environment (Windows)

Buka terminal di folder project, lalu jalankan:

```bash
python -m venv ecomm-analysis
```

Aktifkan virtual environment:

```bash
ecomm-analysis\Scripts\activate
```

---

## 📦 2. Install Dependencies

Install semua library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

---

## 📓 3. Menjalankan Notebook (Analisis Data)

Jalankan Jupyter Notebook:

```bash
jupyter notebook
```

Kemudian buka file:

```
notebook.ipynb
```

---

## 🚀 4. Menjalankan Dashboard Streamlit

Masuk ke folder dashboard (opsional):

```bash
cd dashboard
```

Jalankan aplikasi Streamlit:

```bash
streamlit run dashboard.py
```

---

## 🌐 5. Akses Dashboard

Setelah dijalankan, buka browser dan akses:

```
http://localhost:8501
```

---

## 💡 Catatan

* Pastikan virtual environment sudah aktif sebelum menjalankan perintah.
* Jika ada error module tidak ditemukan, install ulang dengan:

  ```bash
  pip install -r requirements.txt
  ```

