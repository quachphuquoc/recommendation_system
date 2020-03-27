# Code sau sẽ xử lý nhứng thông tin sau đây của file credits.csv:
# Xóa những giá trị nan của 3 thuộc tính: cast, crew, id
# Xử lí cast thành chuổi có dạng: name0 | name1 | ... (Lấy tên diễn viên)
# Xử lí crew thành chuổi có dạng: name0 | name1 | ... (Lấy tên các thành viên trong đoàn)

import pandas as pd
import numpy as np
import ast

#hàm dùng truyền vào map, xử lý list các dict thành string theo ý muốn
# def converter(ob):
#     return ob['name']
#
# # Load dữ liệu
# credits_df = pd.read_csv('the-movies-dataset/credits.csv')
# print('credits_df shape: '+str(credits_df.shape))
#
#
#
# # Khong co dong nay thi code phia duoi bi loi o index thu 28???? (cu the lenh: df_temp['credits'][28])
# df_temp = pd.read_csv('./processed-csv/credits.csv')
#
# # mảng chứa index của những dòng mà có giá trị tại cột 'cast' là '[]'
# credits_cast_none = []
#
# # mảng chứa index của những dòng mà có giá trị tại cột 'crew' là '[]'
# credits_crew_none = []
#
# #
#
# #Xu ly cot crew
# df_temp2 = pd.read_csv('./processed-csv/credits.csv')
#
# for i in range(df_temp2.shape[0]):
#     # Xu ly cot crew
#     credits_str2 = str(df_temp2['crew'][i])
#     credits_crew = ast.literal_eval(credits_str2)
#
#     if len(credits_crew) == 0:
#         credits_crew_none.append(i)
#     else:
#         result = '|'.join(map(converter,credits_crew))
#         df_temp2['crew'][i] = result
#
#
#
#
# print('count none credits: '+str(len(credits_crew_none)))
#
#
# # Xóa dòng có giá trị tại cột 'crew' là '[]'
# df_temp2 = df_temp2.drop(credits_crew_none)
#
# print('df_temp shape: '+str(df_temp2.shape))
# # Ghi dữ liệu vào csv
# df_temp2.to_csv('./processed-csv/credits_temp2.csv',index=False,header=True)
#


# Xóa các trường index của file credits không có trong file movie.
# Load dữ liệu
movies_df = pd.read_csv('./the-movies-dataset/movies.csv')
credits_df = pd.read_csv('./processed-csv/credits_temp2.csv')

# Mảng chứa index những credits cho phim mà không có trong movies.csv
missing_movies = []

print('processing...')

# Tìm những index vừa nói
for i in range(movies_df.shape[0]):
    movieId = movies_df['id'][i]
    if len(credits_df[credits_df['id']==movieId].index) == 0:
        missing_movies.append(i)

# In thông tin
print('missing:', len(missing_movies))
print('7 index:',missing_movies[0:7])

# Xóa những hàng vừa tìm được
df_temp = credits_df.drop(missing_movies)

# Ghi vào csv
df_temp.to_csv('./processed-csv/credits_temp2.csv',index=False,header=True)

# In thông tin
print('movies df:', movies_df.shape)
print('df temp:', df_temp.shape)
print('credits df:', credits_df.shape)


# Kết quả credits giảm 1480 thuộc tính so với file movie