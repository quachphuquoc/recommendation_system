import 'package:movie_app/models/Movie.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:movie_app/repositories/MovieApiClient.dart';
import 'package:movie_app/ui/screens/MovieDetailPage.dart';
import 'package:movie_app/ui/screens/MoreMoviesPage.dart';

class HomePageBloc {
  void buttonMoreTap(BuildContext context, String title, List<int> movies){
    Navigator.push(context, MaterialPageRoute(builder: (context) => MoreMoviesPage(title, movies)));
  }

  void movieItemSelected(BuildContext context,Movie movie,String listName){
    if (movie != null){
      Navigator.push(context, MaterialPageRoute(builder: (context) => MovieDetailPage(movie,listName)));
    }
    else{
      showDialog(
          context: context,
          barrierDismissible: false,
          builder: (BuildContext context){
            return AlertDialog(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10)
              ),
              title: Container(
                margin: EdgeInsets.only(top: 10, bottom: 10),
                child: Text("Error!", style: TextStyle(color: Colors.red, fontSize: 25)),
              ),
              content: Text("Sorry! This movie has no Data."),
              actions: <Widget>[
                FlatButton(
                  child: Text("OK", style: TextStyle(fontSize: 15, color: Colors.blue),),
                  onPressed: (){
                    Navigator.of(context).pop();
                  },
                )
              ],
              elevation: 24.0,
            );
          }
      );
    }
  }

  List<Future<Movie>> loadMovies(List<int> list_id){
    return MovieApiClient.loadMovies(list_id);
  }

  Future<Map<String, dynamic>> loadRecommendedMovies(int userId) async {
    Map<String, dynamic> res_data = await MovieApiClient.loadRecommendedMovies(userId);
    return res_data;
  }
}