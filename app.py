import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Uygulama Başlığı ve Açıklama
st.title("Renk Analizi Uygulaması")
st.write("Bilgisayarınızdan bir resim yükleyin, ardından 'Analiz Et' düğmesine basarak en baskın 5 rengi keşfedin.")

# Resim Yükleme
uploaded_file = st.file_uploader("Resim Yükleyin (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Yüklenen resmi göster
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Resim", use_column_width=True)
    
    # Analiz butonu
    if st.button("Analiz Et"):
        # İşlem hızını artırmak için resmi yeniden boyutlandırın
        image_small = image.resize((200, 200))
        image_np = np.array(image_small)
        
        # Eğer resimde alfa kanalı varsa, sadece RGB kanallarını al
        if image_np.shape[-1] == 4:
            image_np = image_np[..., :3]
        
        # Piksel verilerini (R, G, B) şeklinde yeniden şekillendir
        pixels = image_np.reshape(-1, 3)
        
        # Benzersiz renkleri ve bunların sayısını hesapla
        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
        
        # Renkleri, en çok olandan en aza doğru sırala
        sorted_idx = np.argsort(-counts)
        top_colors = unique_colors[sorted_idx][:5]
        top_counts = counts[sorted_idx][:5]
        
        # Sonuçları metinsel olarak göster
        st.subheader("En Baskın 5 Renk:")
        for i, (color, count) in enumerate(zip(top_colors, top_counts)):
            st.write(f"{i+1}. Renk: RGB{tuple(color)} - {count} piksel")
        
        # Histogram grafiği ile görselleştirme
        fig, ax = plt.subplots()
        # Renk değerlerini 0-1 aralığına normalize et (matplotlib için)
        colors_normalized = [tuple(color/255) for color in top_colors]
        ax.bar(range(5), top_counts, color=colors_normalized)
        ax.set_xticks(range(5))
        ax.set_xticklabels([f"RGB{tuple(color)}" for color in top_colors], rotation=45)
        ax.set_xlabel("Renkler")
        ax.set_ylabel("Piksel Sayısı")
        ax.set_title("En Baskın 5 Rengin Histogramı")
        st.pyplot(fig)
