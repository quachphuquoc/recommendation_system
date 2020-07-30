import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:movie_app/blocs/MoreMoviesPageBloc.dart';
import 'package:movie_app/models/Movie.dart';
import 'package:movie_app/ui/items/MovieItem.dart';
import 'package:movie_app/blocs/HomePageBloc.dart';

class MoreMoviesPage extends StatefulWidget{
  String _title;
  List<int> _movies;
  int _pages;

  MoreMoviesPage(String title, List<int> movies){
    this._title = title;
    this._movies = movies;
    this._pages = (this._movies.length/20).ceil();
  }

  @override
  MoreMoviesPageState createState() => MoreMoviesPageState();
}

class MoreMoviesPageState extends State<MoreMoviesPage>{
  //HomePageBloc _bloc = new HomePageBloc();
  MoreMoviesPageBloc _bloc = new MoreMoviesPageBloc();
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    //List<Future<Movie>> movies = _bloc.loadMovies(widget._movies);

    return Scaffold(
      appBar: AppBar(
        actions: <Widget>[IconButton(icon: Icon(null))],
        backgroundColor: Color(0xFF2d3450),
        title: Center(
          child: Text(
            widget._title,
            style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold, color: Colors.white),
          ),
        ),
      ),
      body: StreamBuilder(
        stream: _bloc.pageStream,
        builder: (context, snapshot){
          if (widget._movies.length <= 20){
            List<Future<Movie>> movies = _bloc.loadMovies(widget._movies);
            return Container(
                width: double.infinity,
                height: double.infinity,
                color: Color(0xFF2d3450),
                child: ListView.builder(
                  cacheExtent: 0.0,
                  itemCount: movies.length,
                  itemBuilder: (context, index){
                    return GestureDetector(
                      child: MovieItemForMore(movies[index],"more_page"),
                      onTap: () async{
                        _bloc.movieItemSelected(context, await movies[index], "more_page");
                      },
                    );
                  },
                )
            );
          }
          int currentPage = snapshot.data;
          int start = currentPage*20;
          List<Future<Movie>> movies = _bloc.loadMovies(widget._movies.sublist(start,start+20));
          print("len movies: ${movies.length}, start: $start, end: ${start+20-1}");
          return Container(
            width: double.infinity,
            height: double.infinity,
            color: Color(0xFF2d3450),
            child: ListView.builder(
              cacheExtent: 0.0,
              controller: _bloc.scrollController,
              itemCount: movies.length + 1,
              itemBuilder: (context, index){
                if (index == movies.length){
                  return Center(
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: List.generate(6, (index){
                        String text;
                        if (_bloc.isStart){
                          if (index == 5){
                            text = '>';
                          }
                          else{
                            text = (index + 1).toString();
                          }
                          return SizedBox(
                            width: 55,
                            child: RaisedButton(
                              onPressed: (){
                                _bloc.pageButtonPress(index);
                              },
                              child: Text(text,
                                style: TextStyle(
                                  color: index == currentPage ? Colors.black : Colors.white,
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold
                                ),
                              ),
                              color: index == currentPage ? Color.fromRGBO(254,160,2,1.0) : Colors.black,
                            ),
                          );
                        }
                        else{
                          if (index == 0){
                            text = '<';
                          }
                          else{
                            text = (index + 5).toString();
                          }
                          return SizedBox(
                            width: 55,
                            child: RaisedButton(
                              onPressed: (){
                                _bloc.pageButtonPress(index);
                              },
                              child: Text(text,
                                style: TextStyle(
                                    color: (index + 4) == currentPage ? Colors.black : Colors.white,
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold
                                ),
                              ),
                              color: (index + 4) == currentPage ? Color.fromRGBO(254,160,2,1.0) : Colors.black,
                            ),
                          );
                        }
                      }),
                    ),
                  );
                }

                return GestureDetector(
                  child: MovieItemForMore(movies[index],"more_page"),
                  onTap: () async{
                    _bloc.movieItemSelected(context, await movies[index], "more_page");
                  },
                );
              },
            ),
          );
        },
      )
    );
  }

}