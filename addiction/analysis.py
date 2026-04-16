import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

BASE_PATH = r"C:\Users\User\Desktop\ADDICTION"

# ১. ডেটা লোড করা
data_path = os.path.join(BASE_PATH, "data", "international_clinical_data.csv")
df = pd.read_csv(data_path)

# ২. টাইটেলগুলো প্রসেস করা
text = " ".join(df['Title'])

# ৩. WordCloud তৈরি করা
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# ৪. ইমেজটি 'outputs' ফোল্ডারে সেভ করা
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
output_image_path = os.path.join(BASE_PATH, "outputs", "clinical_wordcloud.png")
plt.savefig(output_image_path)
print(f"Visualization saved at: {output_image_path}")