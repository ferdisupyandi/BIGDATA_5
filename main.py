import pymongo
import streamlit as st
from pymongo import MongoClient

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://joel:joel123@cluster1.zow4e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["TokoOnline"]  # Nama database

collection_name = "KatalogRoti"

produk_collection = db[collection_name]  # Nama koleksi

if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)


produk_data = [
    {'nama': 'Roti Tawar Biasa', 'harga': 10000, 'kategori': 'Roti Tawar', 'stok': 20},
    {'nama': 'Roti Tawar Pandan', 'harga': 10000, 'kategori': 'Roti Tawar', 'stok': 15},
    {'nama': 'Roti Kopi', 'harga': 5000, 'kategori': 'Roti Manis', 'stok': 10},
    {'nama': 'Roti Pizza', 'harga': 5000, 'kategori': 'Roti Manis', 'stok': 20},
    {'nama': 'Roti Kacang Ijo', 'harga': 5000, 'kategori': 'Roti Manis', 'stok': 20}

]   

produk_collection.insert_many(produk_data)

for produk in produk_collection.find():
    print(produk)

# Judul Aplikasi
st.title("Tambah / Update Stok Produk")

# Form Input Produk
with st.form("form_tambah_produk"):
    st.text("Kelompok - 5")
    st.text("- MUHAMMAD AKMAL DZULFIKAR         | 20230040069")
    st.text("- fERDI SUPYANDI                   | 20230040048")


    nama_produk = st.text_input("Nama Produk")
    harga = st.number_input("Harga", min_value=0)
    kategori = st.selectbox("Kategori", ["Roti Tawar", "Roti Manis", "lainnya"])
    stok_tambah = st.number_input("Tambah Stok", min_value=0)

    # Tombol Simpan
    submit = st.form_submit_button("Simpan")

    if submit:
        if nama_produk and harga > 0 and stok_tambah >= 0:
            # Cek apakah produk sudah ada di database
            existing_product = produk_collection.find_one({"nama": nama_produk})

            if existing_product:
                # Jika produk sudah ada, update stok
                new_stok = existing_product["stok"] + stok_tambah
                produk_collection.update_one(
                    {"nama": nama_produk},
                    {"$set": {"stok": new_stok, "harga": harga, "kategori": kategori}}
                )
                st.success(f"✅ Stok produk '{nama_produk}' berhasil ditambahkan! Stok sekarang: {new_stok}")
            else:
                # Jika produk belum ada, tambahkan baru
                data_produk = {
                    "nama": nama_produk,
                    "harga": harga,
                    "kategori": kategori,
                    "stok": stok_tambah
                }
                produk_collection.insert_one(data_produk)
                st.success(f"✅ Produk baru '{nama_produk}' berhasil ditambahkan!")

        else:
            st.error("❌ Mohon isi semua data dengan benar!")