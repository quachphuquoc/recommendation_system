import pandas as pd
import ast

#hàm dùng truyền vào map, xử lý list các dict thành string theo ý muốn
def converter(ob):
    return ob['name']

credits_df = pd.read_csv('./the-movies-dataset/credits.csv')
movies_df = pd.read_csv('./processed-csv/movies_temp3.csv')
#movies_df = pd.read_csv('./the-movies-dataset/movies_metadata.csv')

# mảng dùng để chứa index của những dòng có giá trị tại cột 'tmdbId' trong links_df
# mà không xuất hiện trong cột 'id' của movies_df
missing_movies = []

# Tìm index
for i in range(credits_df.shape[0]):
    movies_id = credits_df['id'][i]
    if len(movies_df[movies_df['id']==movies_id].index)==0:
        missing_movies.append(i)

# Xóa những dòng vừa tìm được
df_temp = credits_df.drop(missing_movies)
df_temp.drop_duplicates(subset='id',inplace=True)
movies_df.drop_duplicates(subset='id',inplace=True)

df_temp.to_csv('./processed-csv/credits.csv',index=False,header=True)

# In thông tin
print('credits:', credits_df.shape)
print('movies:', movies_df.shape)
print('df_temp:',df_temp.shape)
print('len missing:',len(missing_movies))

df_temp = pd.read_csv('./processed-csv/credits.csv')

for i in range(df_temp.shape[0]):
    # Xu ly cot cast
    cast_str = str(df_temp['cast'][i])
    casts = ast.literal_eval(cast_str)
    
    if len(casts)==0:
        df_temp['cast'][i] = ""
    else:
        result = '|'.join(map(converter,casts))
        df_temp['cast'][i] = result
    
    # Xu ly cot crew
    crew_str = str(df_temp['crew'][i])
    crews = ast.literal_eval(crew_str)

    if len(crews)==0:
        df_temp['crew'][i] = ""
    else:
        director = next((item['name'] for item in crews if item['job'] == 'Director'), "")
        df_temp['crew'][i] = director

df_temp.to_csv('./processed-csv/credits2.csv',index=False,header=True)

print('df temp:', df_temp.shape)

# Đọc những file về movies và credits mới nhất
movies_df = pd.read_csv('./processed-csv/movies_temp3.csv')
credits_df = pd.read_csv('./processed-csv/credits2.csv')

# thêm 2 cột 'cast' và 'director' vào movies_df
movies_df['cast'] = credits_df['cast']
movies_df['director'] = credits_df['crew']

# ghi ra file csv
movies_df.to_csv('./processed-csv/movies_temp4.csv',index=False,header=True)