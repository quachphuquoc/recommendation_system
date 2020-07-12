class Video {
  String _key;
  String _site;
  int _size;
  String _type;

  Video(this._key, this._site, this._size, this._type);

  String get type => _type;

  int get size => _size;

  String get site => _site;

  String get key => _key;

  factory Video.fromJson(Map<String, dynamic> json){
    return Video(
      json['key'],
      json['site'],
      json['size'],
      json['type']
    );
  }
}