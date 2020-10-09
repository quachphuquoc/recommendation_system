import 'package:http/http.dart' as http;
import 'dart:convert';

class UserApiClient{
  //Config _localhost base on ip of computer
  static String _localhost = "http://10.45.167.81:8000";

  static Future<Map<String, dynamic>> Login(String user_name, String password) async {
    http.Response response = await http.post(
        _localhost+"/api/login",
      headers: <String, String>{
        'Content-Type': 'application/json'
      },
      body: jsonEncode(<String,String>{
        'user_name': user_name,
        'password': password
      })
    );

    Map<String, dynamic> res_data = json.decode(response.body);

    return res_data;
  }
}