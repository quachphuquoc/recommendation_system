# Code sau gồm 2 phần (chạy phần 1 trước, phần 2 sau):
# - Phần 1: Xóa những dòng có giá trị tại cột 'tmdbId' là nan trong file links.csv
# - Phần 2: Xóa những dòng có giá trị tại cột 'tmdbId' trong file links (file đã xử lý ở phần 1)
#           mà không xuất hiện trong cột 'id' của file movies (file movies đã qua xử lý)

import pandas as pd
import numpy as np

# Code phần 1:
# Load dữ liệu
links_df = pd.read_csv('./the-movies-dataset/links.csv')
# Xóa những dòng có giá trị tại cột 'tmdbId' là nan 
df_temp = links_df.dropna(subset=['tmdbId'])
# Ghi dữ liệu vào csv
df_temp.to_csv('./processed-csv/links.csv',index=False,header=True)



# Code phần 2:
# Load dữ liệu
movies_df = pd.read_csv('./processed-csv/movies_temp2.csv')
links_df = pd.read_csv('./processed-csv/links.csv')

# mảng dùng để chứa index của những dòng có giá trị tại cột 'tmdbId' trong links_df
# mà không xuất hiện trong cột 'id' của movies_df
missing_movies = []

# Tìm index
for i in range(links_df.shape[0]):
    tmdbId = int(links_df['tmdbId'][i])
    if len(movies_df[movies_df['id']==tmdbId].index)==0:
        missing_movies.append(i)

# Xóa những dòng vừa tìm được
df_temp = links_df.drop(missing_movies)

# In thông tin
print('links_df:',links_df.shape)
print('movies_df:',movies_df.shape)
print('df_temp:',df_temp.shape)
print('len missing:',len(missing_movies))

# Ghi vào csv
df_temp.to_csv('./processed-csv/links2.csv',index=False,header=True)