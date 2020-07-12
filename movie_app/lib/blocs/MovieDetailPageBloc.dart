import 'dart:async';
import 'package:flutter/material.dart';
import 'package:movie_app/models/Video.dart';
import 'package:movie_app/repositories/VideoApiClient.dart';
import 'package:movie_app/ui/screens/TrailerVideoPage.dart';

class MovieDetailPageBloc {
  StreamController _ratingBarController = new StreamController();
  int _rating = 0;

  MovieDetailPageBloc(){
    _ratingBarController.sink.add(_rating);
  }

  Stream get ratingBarStream => _ratingBarController.stream;

  void iconStarButtonPress(int value){
    _rating = value;
    _ratingBarController.sink.add(_rating);
    // Gọi api, thêm hoặc sửa dữ liệu vào bảng ratings database
  }

  Future<void> iconPlayButtonPress(BuildContext context, int id) async {
    Video video = await VideoApiClient.fetchVideo(id);
    if (video != null){
      Navigator.push(context, MaterialPageRoute(builder: (context) => TrailerVideoPage(video.key)));
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
              content: Text("Sorry! This movie has no Trailer."),
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

  void dispose(){
    _ratingBarController.close();
  }
}