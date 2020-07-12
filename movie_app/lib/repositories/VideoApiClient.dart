import 'package:movie_app/models/Video.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class VideoApiClient {
  static String _baseURL = "https://api.themoviedb.org/3/movie/";
  static String _apiKey = "802b2c4b88ea1183e50e6b285a27696e";

  static Future<Video> fetchVideo(int id) async {
    String url = _baseURL + id.toString() + "/videos?api_key=" + _apiKey + "&language=en-US";

    final response = await http.get(url);

    if (response.statusCode == 200){
      List<dynamic> results = json.decode(response.body)['results'];
      results = results.where((element) => element['site']=='YouTube' && element['type']=='Trailer').toList();
      if (results.length == 0){
        return null;
      }
      else{
        results.sort((a,b){
          if (b['size']>a['size'])
            return 1;
          return -1;
        });

        return Video.fromJson(results[0]);
      }
    }
    else{
      return null;
    }
  }
}