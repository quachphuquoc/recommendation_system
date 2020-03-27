import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time


#Hàm trả về một chuỗi sau khi đã nối nội dung của các thuộc tính của một phim.
def combine_features(row):
    return row["cast"]+" "+row["genres"]+" "+row["crew"]

#Hàm trả về title của một bộ phim dựa vào index của nó.
def get_title_from_index(df,index):
    return df[df.index == index]["original_title"].values[0]

#Hàm trả về index của một bộ phim dựa vào title của nó.
def get_index_from_title(df,title):
    title=title.lower()
    return df[df.original_title.str.lower() == title]["id"].values[0]

#Hàm thực thi
def main():
    #Đọc dữ liệu đưa vào df

    df = pd.read_csv("processed-csv/movies.csv", encoding='latin-1')

    # biến features chứa một vài tên thuộc tính của bộ phim cần cho thuật toán
    features = ["cast", "genres", "crew"]

    # thay thế tất cả giá trị NaN thành chuỗi rỗng
    for feature in features:
        df[feature] = df[feature].fillna("")

    #tạo cột mới "combine_features" cho df, cột này sẽ chứa chuỗi các thuộc tính sau khi đã nối lại của một bộ phim
    df["combine_features"] = df.apply(combine_features,axis=1)

    #tạo đối tượng CountVectorizer()
    cv = CountVectorizer()

    #cung cấp chuỗi các thuộc tính đã được nối cho đối tượng CountVectorizer để tạo ra ma trận rời rạc
    count_matrix = cv.fit_transform(df["combine_features"].str.lower())

    print("count_matrix:")
    print(cv.get_feature_names())
    print(count_matrix.toarray())

    #Tính độ giống nhau giữa các bộ phim, trả về một ma trận thể hiện "độ giống nhau"
    cosine_sim = cosine_similarity(count_matrix)
    print("\nsimilarity_scores:")
    print(cosine_sim)

    #Tên bộ phim mà người dùng đã xem
    movie_user_likes = "Avenger"
    movie_user_likes = movie_user_likes.lower()
    print ("user finds movie's name: ", movie_user_likes)

    #index của bộ phim
    movie_index = get_index_from_title(df,movie_user_likes)
    print("\nmovie index: "+str(movie_index))

    #lấy ra những bộ phim có độ giống với bộ phim ở thứ index (lấy hàng thứ index của ma trận "độ giống nhau")
    #hàm enumerate() sẽ đánh index cho từng phần tử của mảng
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    print("\nsimilar_movies:")
    print(similar_movies)

    #Sắp xếp lại thứ tự của các bộ phim dựa vào chỉ số giống nhau với phim thứ "movie_index", bỏ vị trí đầu tiên
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]
    print("\nsorted_similar_movies:")
    print(sorted_similar_movies)

    #In ra tên 5 bộ phim giống với phim thứ "movie_index" nhất.
    i = 0
    print("\nTop 5 similar movies to \"" + movie_user_likes + "\" are:")
    for element in sorted_similar_movies:
        print(get_title_from_index(df,element[0]))
        i = i+1
        if i>=5:
            break


if __name__=='__main__':
    start = time.time()
    main()
    elapsed = time.time() - start
    print ("Time run: ",elapsed)


