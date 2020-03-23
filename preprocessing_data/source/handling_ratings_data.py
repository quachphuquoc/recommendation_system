# Code sau gồm 2 phần (Chạy từng phần, phần 1 trước, phần 2 sau):
# - Phần 1: Xóa những hàng ratings cho những phim mà có movieId không có trong file links.csv
# - Phần 2: Thay movieId thành tmdbId trong file ratings.csv

import pandas as pd
import numpy as np

# Code phần 1:
# Load dữ liệu
ratings_df = pd.read_csv('./the-movies-dataset/ratings.csv')
links_df = pd.read_csv('./processed-csv/links2.csv')

# Mảng chứa index những ratings cho phim mà không có trong links.csv
missing_ratings = []

print('processing...')

# Tìm những index vừa nói
for i in range(ratings_df.shape[0]):
    movieId = ratings_df['movieId'][i]
    if len(links_df[links_df['movieId']==movieId].index) == 0:
        missing_ratings.append(i)

# In thông tin
print('missing:', len(missing_ratings))
print('7 index:',missing_ratings[0:7])

# Xóa những hàng vừa tìm được
df_temp = ratings_df.drop(missing_ratings)

# Ghi vào csv
df_temp.to_csv('./processed-csv/ratings.csv',index=False,header=True)

# In thông tin
print('ratings df:', ratings_df.shape)
print('df temp:', df_temp.shape)
print('links df:', links_df.shape)





# Code phần 2:
# Load dữ liệu
links_df = pd.read_csv('./processed-csv/links2.csv')
ratings_df = pd.read_csv('./processed-csv/ratings.csv')

# Dict chứa những movieId cần thay thế thành tmdbId (key là movieId, value là tmdbId)
rep_dict = {}

# Thêm từng phần tử vào dict theo cú pháp: movieId: tmdbId
for i in range(links_df.shape[0]):
    movieId = links_df['movieId'][i]
    tmdbId = links_df['tmdbId'][i]
    rep_dict[movieId] = int(tmdbId)

# Tạo dataframe trống.
df_temp = pd.DataFrame(columns=ratings_df.columns)

# Lấy mỗi lần ra 100k dòng của ratings_df để thay thế movieId bằng tmdbId rồi thêm vào df_temp
# sau đó xóa 100k dòng đó trong ratings_df
while ratings_df.shape[0] != 0:
    df = ratings_df.head(100000).copy()
    df['movieId'].replace(rep_dict,inplace=True)
    df_temp = df_temp.append(df,ignore_index=True)
    ratings_df.drop(df.index,inplace=True)

# Ghi dữ liệu vào csv
df_temp.to_csv('./processed-csv/ratings2.csv',index=False,header=True)

# In thông tin
print('ratings df:', ratings_df.shape)
print('df temp:', df_temp.shape)
print('links df:', links_df.shape)
print('count key dict:', len(rep_dict))