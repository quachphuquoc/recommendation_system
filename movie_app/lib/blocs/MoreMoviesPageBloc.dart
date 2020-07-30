import 'dart:async';

import 'package:flutter/material.dart';
import 'package:movie_app/models/Movie.dart';
import 'package:movie_app/repositories/MovieApiClient.dart';
import 'package:movie_app/ui/screens/MovieDetailPage.dart';

class MoreMoviesPageBloc {
  StreamController _pageController = new StreamController();
  ScrollController _scrollController = new ScrollController();
  int _currentPage = 0;
  bool _isStart = true;

  bool get isStart => _isStart;
  ScrollController get scrollController => _scrollController;

  MoreMoviesPageBloc(){
    _pageController.sink.add(_currentPage);
  }

  Stream get pageStream => _pageController.stream;

  List<Future<Movie>> loadMovies(List<int> list_id){
    return MovieApiClient.loadMovies(list_id);
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

  void pageButtonPress(int page){
    if (_isStart == true){
      if (page == 5){
        _isStart = false;
      }
      _currentPage = page;
      _pageController.sink.add(_currentPage);
    }
    else{
      if (page == 0){
        _isStart = true;
      }
      _currentPage = page + 4;
      _pageController.sink.add(_currentPage);
    }
    _scrollController.animateTo(0, duration: Duration(seconds: 2), curve: Curves.ease);
  }

  void dispose(){
    _pageController.close();
  }
}