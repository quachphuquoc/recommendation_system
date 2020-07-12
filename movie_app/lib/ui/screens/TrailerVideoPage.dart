import 'package:flutter/material.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';

class TrailerVideoPage extends StatelessWidget{
  String _keyVideo;

  TrailerVideoPage(this._keyVideo);

  YoutubePlayerController _controller;

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    _controller = YoutubePlayerController(
      initialVideoId: _keyVideo,
      flags: YoutubePlayerFlags(
        autoPlay: true,
      )
    );

    return Scaffold(
      body: Container(
        color: Colors.black,
        child: Center(
          child: YoutubePlayerBuilder(
            player: YoutubePlayer(
              controller: _controller,
            ),
            builder: (context, player){
              return player;
            },
          ),
        ),
      ),
    );
  }
}