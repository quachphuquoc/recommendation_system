#!pip install git+https://github.com/quachphuquoc/QPQ.git
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from QPQ import Reader, Dataset, SVD
from QPQ.model_selection import cross_validate


import warnings; warnings.simplefilter('ignore')

print ("Access")

md = pd. read_csv('/content/drive/My Drive/KhoaLuanTotNghiep/Data/movies.csv')
 
md.head()

md['genres']=md['genres'].str.split('|')
vote_counts = md[md['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = md[md['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
print ("vote_averages ~ Điểm bình chọn: ",C)

#phim điểm xuất phát là 0.95
m = vote_counts.quantile(0.95)
print ("vote_counts ~ Số phiếu bầu tối thiểu: ", m)

# Lấy năm trong 'release_date' nhằm giúp lọc theo năm
md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

# Tìm xem số lượng phim đạt tiêu chuẩn dựa trên các chỉ số: vote_averages, vote_counts
qualified = md[(md['vote_count'] >= m) & (md['vote_count'].notnull()) & (md['vote_average'].notnull())][['original_title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
qualified['vote_count'] = qualified['vote_count'].astype('int')
qualified['vote_average'] = qualified['vote_average'].astype('int')
print ("Số lượng phim đủ điều kiện: ",qualified.shape)

#weighted_rating là công thức xếp hạng phim dựa trên IMDB. Công thức ok nhất.
#Tham khảo: https://help.imdb.com/article/imdb/track-movies-tv/ratings-faq/G67Y87TFYYP6TWAV#
def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

qualified['wr'] = qualified.apply(weighted_rating, axis=1)
qualified = qualified.sort_values('wr', ascending=False).head(250)

#Top 15 moives
print ("Top 15 movies: ",qualified.head(15))

# Qua kết quả ở trên và tiến hành so sánh phim trên IMDB thì thấy người dùng ngoài quan tâm ranks thì họ còn muốn thấy chi tiết là top thể loại nữa.
# Vậy tiếp tục thí nghiệm lấy genres vào để chi xuất.
# Tiến thành lấy genres
s = md.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'genre'
gen_md = md.drop('genres', axis=1).join(s)

#Xây dựng biểu đồ dựa trên thể loại cụ thể và giảm xuống 0.85 (có thể tăng giảm tùy ý)
def build_chart(genre, percentile=0.85):
    df = gen_md[gen_md['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)

    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['original_title', 'year', 'vote_count', 'vote_average', 'popularity']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')

    qualified['wr'] = qualified.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(250)

    return qualified

# Top 15 phim dựa trên Romance
print ("15 romance movies: ",build_chart('Romance').head(15))

# Kết quả khá khả quan

# Hiện tại hết ý tưởng tìm kiếm khác của người dùng.

#Content-base
# Ý tưởng dựa trên 2 trường phái:
# + Movie: Overviews và Taglines
# + Movie: Cast, director(director) và Genre


##Content-base: Overviews + taglines --> description
### Ý tưởng là sử dụng TfidfVectorizer, do trường Overviews và taglines sẽ gặp các từ phổ biến với tần số cao mà không có giá trị. Sử dụng TfidfVectorizer sẽ giúp giải quyết được vấn đề.
### Hiện tại bị lỗi ở phần sorted cosine_similar khi sử dụng phương pháp TfidfVectorizer, tạm thời đánh dấu sử lí sau.
links = pd.read_csv('/content/drive/My Drive/KhoaLuanTotNghiep/Data/links.csv')
links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')

#Kiểm tra id
md['id'] = md['id'].astype('int')
smd = md[md['id'].isin(links)]
print (smd.shape)


# # Gom Overviews và Taglines thành description trong mô hình
smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])

print ("desciption matrix: ",tfidf_matrix.shape)


# tính cosine similar bằng ky thuat linear_kernel
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print ("Kiem tra cosine_sim: ",cosine_sim.all())


smd = smd.reset_index()
titles = smd['original_title']
indices = pd.Series(smd.index, index=smd['original_title'])


# Phát hiện vấn đề: do tập movies là crap bởi nhiều nguồn, nên sẽ xảy ra trường hợp trùng phim. Điển hình là bộ phim 'The Dark Knight' có tới 2 bộ phim trong tập movies
#Hàm lấy ra khuyến nghị.
def get_recommendations(title):
    idx = indices[title]
    sim_scores=cosine_sim[idx]

    #Trường hợp movies bị trùng
    if len(sim_scores) > 1:
      sim_scores=sim_scores[0]
    sim_scores = list(enumerate(sim_scores))

    #Sắp xếp lại sim_scores
    #sim_scores=sim_scores.sort(key=lambda x: x[1], reverse=True)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

# Đưa ra khuyến nghị với bộ phim: The Dark Knight
get_recommendations('The Dark Knight').head(10)

##Content-base: Cast, director và Genre
# Sử dụng CountVectorizer với trường hợp này. Lí do là các trường Cast, director và Genre đã được xử lí clean, nên không gặp vấn đề của description.

#Đọc file keywords

keywords = pd.read_csv('/content/drive/My Drive/KhoaLuanTotNghiep/Data/keywords.csv')
keywords['id'] = keywords['id'].astype('int')
md['id'] = md['id'].astype('int')

md.shape


md = md.merge(keywords, on='id')
smd = md[md['id'].isin(links)]

#Kiểm tra
print("TOI  ",smd.shape)
smd['cast']=smd['cast'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
smd['cast']=smd['cast'].apply(lambda x: str.lower(x.replace("|", " ")))
smd['cast']=smd['cast'].str.split()

print(smd['cast'][0])

print(smd['director'])


smd['keywords'] = smd['keywords'].apply(literal_eval)

print(len(smd['cast'][0]))

# Lấy 3 diễn viên để kiểm thử
smd['cast'] = smd['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)

# Tiến hành lấy các keyword trong file keywords, hiện tại các từ khóa nằm trong trường name của file chưa xử lí.
smd['keywords'] = smd['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

# Xử lí chuối thành chuỗi chữ thường. Mục đích so sánh không bị lỗi.
smd['cast'] = smd['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
smd['director'] = smd['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))

#Đưa director thành 3 lần để tăng hệ số bằng với diễn viên.
smd['director'] = smd['director'].apply(lambda x: [x,x, x])

s = smd.apply(lambda x: pd.Series(x['keywords']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'keyword'

#Đếm tần số các keyword được tìm kiếm
s = s.value_counts()

#In ra 5 từ keyword được truy xuất nhiều nhất.
print ("Tần xuất các từ được truy xuất: ",s[:5])

#Loại bỏ hết các từ được truy xuất 1 lần. Không có giá trị trong thuật toán.
s = s[s > 1]

# Nhầm giúp so sánh các từ cùng từ loại, ở đây phân tích các từ tiếng anh.
# Ví dụ như sở hữu cách trong tiếng anh.
stemmer = SnowballStemmer('english')


def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words

# Xử lý các keyword và chuyển chuổi thành chuỗi thường.
smd['keywords'] = smd['keywords'].apply(filter_keywords)
smd['keywords'] = smd['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
smd['keywords'] = smd['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])

# Kết nối các trường: Keywords, cast, director và genres thành soup.
smd['soup'] = smd['keywords'] + smd['cast'] + smd['director'] + smd['genres']
smd['soup'] = smd['soup'].apply(lambda x: ' '.join(x))

# print("soup: ",smd['soup'])

# Tiến hành đưa vào ma trận, sử dụng CoutVectorizer. CountVectorizer ở đây dùng để đếm từ, thích hợp trong trường hợp này.
count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
count_matrix = count.fit_transform(smd['soup'])

# Cosine_sim
cosine_sim = cosine_similarity(count_matrix)
smd = smd.reset_index()
titles = smd['original_title']

# Đưa ra index của bộ phim trong smd
indices = pd.Series(smd.index, index=smd['original_title'])

get_recommendations('The Dark Knight').head(10)

# Cải tiến thí nghiệm recommendations bằng phương pháp kết hợp cả 2 trường phái là:
# + Movie: Overviews và Taglines
# + Movie: Cast, director(director) và Genre

def improved_recommendations(title):
    idx = indices[title]
    sim_scores=cosine_sim[idx]

    #Trường hợp movies bị trùng
    if len(sim_scores) > 1:
      sim_scores=sim_scores[0]
    sim_scores = list(enumerate(sim_scores))


    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]

    movies = smd.iloc[movie_indices][['original_title', 'vote_count', 'vote_average', 'year']]
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(20)
    return qualified


improved_recommendations('The Dark Knight')

#Mix lại kết quả ko tốt, ko khả quan so với chạy riêng lẻ

# Collaborative Filtering
# Đặt vấn đề: Hiện tại content base chỉ giải quyết là đưa ra gợi ý dựa trên tổng thể, tức là toàn bộ người dùng (Ở đây có thể áp dụng cho người dùng khách).
#             Tuy nhiên vấn đề cho từng cá nhân lại không giải quyết được, tức là một người đã có tài khoản và lịch sử dụng thì họ sẽ không nhận được thứ họ muốn mà chỉ là khuyến nghị trên tổng thể thôi.
# Giải quyết vấn đề này: Collaborative Filtering sẽ giải quyết được vấn đề trên và đưa ra các gợi ý dựa trên lịch sử các nhân của người dùng đó.
# Tuy nhiên, để tránh hiệu xuất không được cao, nên sử dụng giải thuật SVD (giải thuật phân rã giá trị) để giảm lỗi trung bình bình phương(RMSE) trước để đưa ra khuyến nghị tốt hơn

# Đọc file ratings
ratings = pd.read_csv('/content/drive/My Drive/KhoaLuanTotNghiep/Data/ratings.csv')
ratings.head()

reader = Reader()
# Lấy các cột cần thiết như useID, movieID, rating
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
# data.split(n_folds=5)

# Tiến hành tính toán
svd = SVD()
cross_validate(svd, data, measures=['RMSE', 'MAE'])

# Bắt đầu traning mô hình
trainset = data.build_full_trainset()
svd.fit(trainset)

# Xem người dùng Id 1
ratings[ratings['userId'] == 1]

svd.predict(1, 302, 3)
# Với dự đoán useID 1 và bộ phim là 302 thì ta có độ dự đoán vượt ngưỡng là 4.04, kết quả cho biết bộ phim có id 302 không được người dùng thích.

# Tiến hành xây dựng Hybrid dựa trên content base và Collaborative Filtering
# Hybrid
# Ý tưởng dựa trên useID và Title.

# Hàm chuyển đổi thành kiểu int
def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan
# Đọc file links
id_map = pd.read_csv('/content/drive/My Drive/KhoaLuanTotNghiep/Data/links.csv')[['movieId', 'tmdbId']]
id_map['tmdbId'] = id_map['tmdbId'].apply(convert_int)
id_map.columns = ['movieId', 'id']
id_map = id_map.merge(smd[['original_title', 'id']], on='id').set_index('original_title')
indices_map = id_map.set_index('id')

# Hàm hybrid
def hybrid(userId, title):
    idx = indices[title]
    tmdbId = id_map.loc[title]['id']
    #print(idx)
    movie_id = id_map.loc[title]['movieId']
    
    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    
    movies = smd.iloc[movie_indices][['original_title', 'vote_count', 'vote_average', 'year', 'id']]
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map.loc[x]['movieId']).est)
    movies = movies.sort_values('est', ascending=False)
    return movies.head(10)
# Kiểm tra người dùng 1 và bộ phim tên Avatar
hybrid(1, 'Avatar')

hybrid(3, 'Avatar')

hybrid(500, 'Avatar')

