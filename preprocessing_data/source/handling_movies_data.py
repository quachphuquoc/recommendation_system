# Code sau sẽ xử lý nhứng thông tin sau đây của file movies.csv:
# - Xóa những hàng mà có giá trị tại cột 'overview' và 'poster_path' là nan
# - Xóa những hàng mà có giá trị tại cột 'original_language' khác en
# - Xử lý cột 'genres' và cột 'production_companies'
# - Xóa những cột sau: ['adult','imdb_id','spoken_languages','production_countries','status','title','video']

import pandas as pd
import numpy as np
import ast

#hàm dùng truyền vào map, xử lý list các dict thành string theo ý muốn
def converter(ob):
    return ob['name']

# Load dữ liệu
movies_df = pd.read_csv('the-movies-dataset/movies_metadata.csv')
print('movies_df shape: '+str(movies_df.shape))

# mảng chứa index của những phim mà có giá trị cột 'original_language' khác 'en'
lang_index = []
# Thêm index của những phim vừa nói ở trên vào mảng
for i in range(movies_df.shape[0]):
    if movies_df['original_language'][i] != 'en':
        lang_index.append(i)

# Xóa những dòng vừa tìm được
df_temp = movies_df.drop(lang_index)
print('df_temp shape: '+str(df_temp.shape))

# Xóa những dòng mà giá trị tại cột 'overview' và 'poster_path' là nan
df_temp = df_temp.dropna(subset=['overview'])
df_temp = df_temp.dropna(subset=['poster_path'])
print('df_temp shape: '+str(df_temp.shape))

# Ghi dữ liệu vào csv
df_temp.to_csv('./processed-csv/movies_temp.csv',index=False,header=True)

# Khong co dong nay thi code phia duoi bi loi o index thu 28???? (cu the lenh: df_temp['genres'][28])
df_temp = pd.read_csv('./processed-csv/movies_temp.csv')

# mảng chứa index của những dòng mà có giá trị tại cột 'genres' là '[]'
genres_none = []

for i in range(df_temp.shape[0]):
    # Xu ly cot genres
    genres_str = str(df_temp['genres'][i])
    genres = ast.literal_eval(genres_str)

    if len(genres) == 0:
        genres_none.append(i)
    else:
        result = '|'.join(map(converter,genres))
        df_temp['genres'][i] = result

    # Xu ly cot production companies
    production_companies_str = str(df_temp['production_companies'][i])
    production_companies = ast.literal_eval(production_companies_str)

    if len(production_companies) == 0:
        df_temp['production_companies'][i] = ""  
    else:
        result2 = '|'.join(map(converter,production_companies))
        df_temp['production_companies'][i] = result2

print('count none genres: '+str(len(genres_none)))

# Xóa dòng có giá trị tại cột 'genres' là '[]'
df_temp = df_temp.drop(genres_none)
# Xóa một số cột không cần thiết
df_temp = df_temp.drop(columns=['adult','imdb_id','spoken_languages','production_countries','status','title','video'])

print('df_temp shape: '+str(df_temp.shape))
# Ghi dữ liệu vào csv
df_temp.to_csv('./processed-csv/movies_temp2.csv',index=False,header=True)