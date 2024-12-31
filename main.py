import json
import math
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns
import matplotlib.pyplot as plt
import emoji
from collections import Counter
import re
import os
import time
import pytz
from datetime import datetime
os.environ['TZ'] = 'Asia/Ho_Chi_Minh'
time.tzset()  # Áp dụng múi giờ mới nếu chạy trên colab
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
def tien_xu_ly_du_lieu_tin_nhan_thu_muc(folder_path):
    excluded_phrases = [
                "cuộc gọi",
                " file đính kèm",
                " về tin nhắn của bạn"
            ]

    processed_messages = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):  # Chỉ xử lý các tệp JSON
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                datas = json.load(file)

            # Xử lý dữ liệu trong từng tệp
            for data in datas.get('messages', []):
                if all(key in data for key in ['sender_name', 'content', 'timestamp_ms']):
                    sender_name = data['sender_name'].encode('latin1').decode('utf-8')
                    content = data['content'].encode('latin1').decode('utf-8')
                    timestamp = datetime.fromtimestamp(data['timestamp_ms'] / 1000).strftime("%Y-%m-%d %H:%M:%S")

                    # Kiểm tra xem nội dung có chứa bất kỳ cụm từ nào cần loại bỏ không
                    should_exclude = any(phrase in content.lower() for phrase in excluded_phrases)

                    if all([sender_name, content, timestamp]) and not should_exclude:
                        processed_messages.append({
                            "Người gửi": sender_name,
                            "Nội dung": content,
                            "Thời gian": timestamp
                        })
    df = pd.DataFrame(processed_messages)
    return df
def tien_xu_ly_du_lieu_tin_nhan_thu_muc_mess_ca_nhan(folder_path,ten_fb_cua_ban):
    excluded_phrases = [
                "cuộc gọi",
                " file đính kèm",
                " về tin nhắn của bạn"
            ]

    processed_messages = []
    total_messages = 0  # Đếm tổng số tin nhắn
    filtered_messages = 0  # Đếm số tin nhắn được lọc
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                datas = json.load(file)

            for data in datas.get('messages', []):
                total_messages += 1
                if all(key in data for key in ['sender_name', 'content', 'timestamp_ms']):
                    sender_name = data['sender_name'].encode('latin1').decode('utf-8')
                    content = data['content'].encode('latin1').decode('utf-8')
                    timestamp = datetime.fromtimestamp(data['timestamp_ms'] / 1000).strftime("%Y-%m-%d %H:%M:%S")

                    should_exclude = any(phrase in content.lower() for phrase in excluded_phrases)

                    if all([sender_name, content, timestamp]) and not should_exclude and ten_fb_cua_ban.lower()  in sender_name.lower():
                        processed_messages.append({
                            "Người gửi": sender_name,
                            "Nội dung": content,
                            "Thời gian": timestamp
                        })
                        filtered_messages += 1

    df = pd.DataFrame(processed_messages)
    
    # In thông tin về quá trình lọc
    print(f"Tổng số tin nhắn: {total_messages}")
    print(f"Số tin nhắn sau khi lọc: {filtered_messages}")
    print(f"Tỉ lệ lọc: {(filtered_messages/total_messages*100):.2f}%")
    
    return df
def count_words(text):
    if isinstance(text, str):
        return len(text.split())
    return 0
def ve_bieu_do_tin_nhan_va_so_tu(df, figsize=(10, 6), width=0.2, colors=('#FF9999', '#66B2FF')):
    df['Số từ'] = df['Nội dung'].apply(count_words)
    plt.figure(figsize=figsize)
    message_counts = df['Người gửi'].value_counts().sort_index()
    word_counts = df.groupby('Người gửi')['Số từ'].sum().sort_index()
    x = np.arange(len(message_counts))

    bars1 = plt.bar(x - width/2, message_counts, width, label='Số tin nhắn', color=colors[0])
    bars2 = plt.bar(x + width/2, word_counts, width, label='Tổng số từ', color=colors[1])
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
    plt.ylabel('Số lượng')
    plt.yticks([])
    plt.xticks(x, message_counts.index)
    plt.legend()

    plt.tight_layout()
    plt.show()
def phan_bo_tin_nhan_theo_thoi_gian(df, figsize=(16, 12)):
    df['Thời gian'] = pd.to_datetime(df['Thời gian'])
    df['Hour'] = df['Thời gian'].dt.hour
    df['Month'] = df['Thời gian'].dt.month
    df['DayOfWeek'] = df['Thời gian'].dt.dayofweek

    # Tạo biểu đồ
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=False)

    # Biểu đồ phân phối tin nhắn theo giờ
    hour_range = list(range(24))  # Tạo dải giờ từ 0 đến 23
    sns.countplot(data=df, x='Hour', ax=axes[0], palette='viridis', order=hour_range)
    axes[0].set_title('Phân phối thời gian nhắn tin theo giờ trong ngày')
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Số lượng tin nhắn')
    axes[0].set_xticklabels([f'{hour}h' for hour in hour_range])

    # Biểu đồ phân phối tin nhắn theo tháng
    month_range = list(range(1, 13))  # Tạo dải tháng từ 1 đến 12
    sns.countplot(data=df, x='Month', ax=axes[1], palette='coolwarm', order=month_range)
    axes[1].set_title('Phân phối tin nhắn theo tháng')
    axes[1].set_xlabel('')
    axes[1].set_ylabel('Số lượng tin nhắn')
    axes[1].set_xticklabels([f'T{month}' for month in month_range])

    # Biểu đồ phân phối tin nhắn theo thứ
    day_labels = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
    day_range = list(range(7))  # Tạo dải thứ từ 0 đến 6 (0 là Thứ 2)
    sns.countplot(data=df, x='DayOfWeek', ax=axes[2], palette='Set2', order=day_range)
    axes[2].set_title('Phân phối tin nhắn theo thứ trong tuần')
    axes[2].set_xlabel('')
    axes[2].set_ylabel('Số lượng tin nhắn')
    axes[2].set_xticklabels(day_labels)

    # Căn chỉnh bố cục
    plt.tight_layout()
    plt.show()
def phan_tich_tan_suat_tu(df, ngram_range=(1, 1), top_n=10, figsize=(15, 12)):
    vectorizer = CountVectorizer(ngram_range=ngram_range)

    senders = df['Người gửi'].unique()
    num_senders = len(senders)

    # Tính toán số hàng và cột cần thiết cho subplot
    cols = 2  # Số cột cố định là 2
    rows = math.ceil(num_senders / cols)

    fig, axes = plt.subplots(rows, cols, figsize=figsize, squeeze=False, gridspec_kw={'wspace': 0.4, 'hspace': 0.6})
    axes = axes.flatten()  # Chuyển mảng axes thành một danh sách để dễ duyệt

    colors = sns.color_palette("husl", num_senders)  # Tạo bảng màu tự động cho từng người gửi

    for idx, sender in enumerate(senders):
        sender_messages = df[df['Người gửi'] == sender]['Nội dung'].dropna()
        X = vectorizer.fit_transform(sender_messages)
        word_counts = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        word_frequency = word_counts.sum().sort_values(ascending=False)
        top_words = word_frequency.head(top_n)

        sns.barplot(
            x=top_words.values,
            y=top_words.index,
            ax=axes[idx],
            palette=sns.light_palette(colors[idx], reverse=True),
            orient='h',
            edgecolor="black"
        )
        axes[idx].set_title(f'Top {top_n} từ của {sender}')
        axes[idx].set_xlabel('Tần suất')
        axes[idx].set_ylabel('')

    # Nếu còn các ô subplot thừa, ẩn chúng đi
    for idx in range(len(senders), len(axes)):
        axes[idx].axis('off')

    # Vẽ tổng hợp tất cả các từ
    all_messages = df['Nội dung'].dropna()
    X = vectorizer.fit_transform(all_messages)
    word_counts = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    word_frequency = word_counts.sum().sort_values(ascending=False)
    top_words = word_frequency.head(top_n)

    fig, ax = plt.subplots(figsize=(figsize[0], figsize[1] // 2))
    sns.barplot(
        x=top_words.index,
        y=top_words.values,
        ax=ax,
        palette='viridis',
        edgecolor="black"
    )
    ax.set_title(f'Top {top_n} từ xuất hiện nhiều nhất trong cuộc trò chuyện')
    ax.set_xlabel('Từ')
    ax.set_ylabel('Tần suất')
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

    return {
        'vectorizer': vectorizer,
        'word_frequency': word_frequency
    }
def count_emojis(text):
        if not isinstance(text, str):
            return Counter()
        return Counter([c for c in text if c in emoji.EMOJI_DATA])
def phan_tich_tan_suat_emoji(df):
    emoji_list = []

    # Duyệt qua từng người gửi và nội dung tin nhắn để đếm emoji
    for sender in df['Người gửi'].unique():
        sender_messages = df[df['Người gửi'] == sender]['Nội dung'].dropna()
        all_emojis = Counter()

        for message in sender_messages:
            all_emojis.update(count_emojis(message))

        for emoji_char, count in all_emojis.items():
            emoji_list.append([sender, emoji_char, count])

    # Chuyển danh sách thành DataFrame

    emoji_counts = pd.DataFrame(emoji_list, columns=['Người gửi', 'Emoji', 'Số lượng'])
    emoji_counts_sorted = emoji_counts.sort_values(by='Số lượng', ascending=False)

    return emoji_counts_sorted
# đếm tin nhắn của bạn ở từng năm
def dem_tin_nhan_theo_nam(df, figsize=(12, 6)):
    # Chuyển cột Thời gian sang datetime nếu chưa phải
    df['Thời gian'] = pd.to_datetime(df['Thời gian'])
    
    # Thêm cột Year
    df['Year'] = df['Thời gian'].dt.year
    
    # Đếm số tin nhắn theo năm và người gửi
    yearly_counts = df.groupby(['Year', 'Người gửi']).size().unstack(fill_value=0)
    
    # Vẽ biểu đồ
    ax = yearly_counts.plot(kind='bar', figsize=figsize, width=0.8)
    
    # Thêm số liệu trên đầu mỗi cột
    for container in ax.containers:
        ax.bar_label(container, padding=3)
    
    plt.title('Số lượng tin nhắn theo năm')
    plt.xlabel('Năm')
    plt.ylabel('Số tin nhắn')
    plt.legend(title='Người gửi')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    return yearly_counts
# phân tích top 10 từ bạn sử dụng nhièu nhất mỗi năm
def phan_tich_tu_theo_nam(df, top_n=10, figsize=(15, 5),ngram_range=(1,1)):
  
    # Chuyển đổi cột thời gian sang datetime nếu chưa phải
    df['Thời gian'] = pd.to_datetime(df['Thời gian'])
    df['Year'] = df['Thời gian'].dt.year
    
    # Lấy danh sách các năm
    years = sorted(df['Year'].unique())
    
    # Tính số hàng cần thiết cho subplot
    n_rows = (len(years) + 2) // 3  # 3 biểu đồ mỗi hàng
    
    # Tạo figure với kích thước phù hợp
    fig, axes = plt.subplots(n_rows, 3, figsize=(figsize[0], figsize[1]*n_rows))
    axes = axes.flatten()  # Làm phẳng mảng axes
    
    # Xử lý từng năm
    for idx, year in enumerate(years):
        # Lọc dữ liệu theo năm
        year_data = df[df['Year'] == year]
        
        # Tạo vectorizer và xử lý văn bản
        vectorizer = CountVectorizer(stop_words=None,ngram_range=ngram_range)  # Có thể thêm stop_words nếu muốn
        X = vectorizer.fit_transform(year_data['Nội dung'].dropna())
        
        # Tính tần suất từ
        word_freq = pd.DataFrame({
            'word': vectorizer.get_feature_names_out(),
            'freq': X.sum(axis=0).A1
        })
        
        # Sắp xếp và lấy top N
        top_words = word_freq.sort_values('freq', ascending=True).tail(top_n)
        
        # Vẽ biểu đồ cho năm hiện tại
        sns.barplot(
            data=top_words,
            y='word',
            x='freq',
            ax=axes[idx],
            palette='viridis'
        )
        
        # Chỉnh sửa biểu đồ
        axes[idx].set_title(f'Top {top_n} từ năm {year}')
        axes[idx].set_xlabel('Tần suất')
        axes[idx].set_ylabel('')
        
        # Thêm giá trị lên thanh
        for i, v in enumerate(top_words['freq']):
            axes[idx].text(v, i, f' {v}', va='center')
    
    # Ẩn các subplot không sử dụng
    for idx in range(len(years), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    return None
