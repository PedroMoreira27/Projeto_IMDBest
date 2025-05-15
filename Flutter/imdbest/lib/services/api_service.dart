import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/filme.dart';

class ApiService {
  final String tmdbApiKey = 'd41a10c6861b1402691065387415ca43';
  final String omdbApiKey = 'f201fb92';

  // Exemplo: Buscar filmes populares no TMDB
  Future<List<Filme>> buscarFilmesTmdb() async {
    final url = Uri.parse(
      'https://api.themoviedb.org/3/movie/popular?api_key=$tmdbApiKey&language=pt-BR&page=1',
    );
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List results = data['results'];
      return results.map((json) => Filme.fromTmdbJson(json)).toList();
    } else {
      throw Exception('Erro ao buscar filmes no TMDB');
    }
  }

  // Exemplo: Buscar detalhes de um filme no OMDB
  Future<Filme> buscarFilmeOmdb(String imdbId) async {
    final url = Uri.parse(
      'https://www.omdbapi.com/?apikey=$omdbApiKey&i=$imdbId&plot=full',
    );
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Filme.fromOmdbJson(data);
    } else {
      throw Exception('Erro ao buscar filme no OMDB');
    }
  }

  Future<List<Filme>> buscarFilmesPorNome(String query) async {
    final url = Uri.parse(
      'https://api.themoviedb.org/3/search/movie?api_key=$tmdbApiKey&language=pt-BR&query=$query&page=1',
    );
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List results = data['results'];
      return results.map((json) => Filme.fromTmdbJson(json)).toList();
    } else {
      throw Exception('Erro ao buscar filmes por nome no TMDB');
    }
  }

  Future<String?> buscarImdbIdTmdb(int tmdbId) async {
    final url = Uri.parse(
      'https://api.themoviedb.org/3/movie/$tmdbId?api_key=$tmdbApiKey&language=pt-BR',
    );
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['imdb_id'];
    }
    return null;
  }
}