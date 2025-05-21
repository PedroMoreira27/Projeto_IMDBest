import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:imdbest/services/api_service.dart';
import 'package:imdbest/models/filme.dart';

@GenerateMocks([http.Client])
import 'api_service_test.mocks.dart';

void main() {
  late ApiService apiService;
  late MockClient mockClient;

  setUp(() {
    mockClient = MockClient();
    apiService = ApiService(client: mockClient);
  });

  group('ApiService Tests', () {
    test('buscarFilmesTmdb success', () async {
      final mockResponse = {
        'results': [
          {
            'id': 1,
            'title': 'Test Movie',
            'overview': 'Test Overview',
            'poster_path': '/test.jpg',
            'vote_average': 8.5,
            'release_date': '2024-01-01'
          }
        ]
      };

      when(mockClient.get(
        Uri.parse('https://api.themoviedb.org/3/movie/popular?api_key=${apiService.tmdbApiKey}&language=pt-BR&page=1'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode(mockResponse),
        200,
        headers: {'Content-Type': 'application/json'},
      ));

      final result = await apiService.buscarFilmesTmdb();
      expect(result.length, 1);
      expect(result[0].titulo, 'Test Movie');
    });

    test('buscarFilmeOmdb success', () async {
      final mockResponse = {
        'Title': 'Test Movie',
        'Year': '2024',
        'Plot': 'Test Plot',
        'Poster': 'http://test.com/poster.jpg',
        'imdbRating': '8.5',
        'imdbID': 'tt1234567'
      };

      when(mockClient.get(
        Uri.parse('https://www.omdbapi.com/?apikey=${apiService.omdbApiKey}&i=tt1234567&plot=full'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode(mockResponse),
        200,
        headers: {'Content-Type': 'application/json'},
      ));

      final result = await apiService.buscarFilmeOmdb('tt1234567');
      expect(result.titulo, 'Test Movie');
      expect(result.ano, '2024');
    });

    test('buscarFilmesPorNome success', () async {
      final mockResponse = {
        'results': [
          {
            'id': 1,
            'title': 'Search Result',
            'overview': 'Test Overview',
            'poster_path': '/test.jpg',
            'vote_average': 8.5,
            'release_date': '2024-01-01'
          }
        ]
      };

      when(mockClient.get(
        Uri.parse('https://api.themoviedb.org/3/search/movie?api_key=${apiService.tmdbApiKey}&language=pt-BR&query=test&page=1'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode(mockResponse),
        200,
        headers: {'Content-Type': 'application/json'},
      ));

      final result = await apiService.buscarFilmesPorNome('test');
      expect(result.length, 1);
      expect(result[0].titulo, 'Search Result');
    });

    test('buscarImdbIdTmdb success', () async {
      final mockResponse = {
        'imdb_id': 'tt1234567'
      };

      when(mockClient.get(
        Uri.parse('https://api.themoviedb.org/3/movie/123?api_key=${apiService.tmdbApiKey}&language=pt-BR'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode(mockResponse),
        200,
        headers: {'Content-Type': 'application/json'},
      ));

      final result = await apiService.buscarImdbIdTmdb(123);
      expect(result, 'tt1234567');
    });

    test('buscarFilmesTmdb failure', () async {
      when(mockClient.get(
        Uri.parse('https://api.themoviedb.org/3/movie/popular?api_key=${apiService.tmdbApiKey}&language=pt-BR&page=1'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode({'error': 'Internal Server Error'}),
        500,
        headers: {'Content-Type': 'application/json'},
      ));

      expect(
        () => apiService.buscarFilmesTmdb(),
        throwsException,
      );
    });

    test('buscarFilmeOmdb failure', () async {
      when(mockClient.get(
        Uri.parse('https://www.omdbapi.com/?apikey=${apiService.omdbApiKey}&i=tt1234567&plot=full'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode({'error': 'Internal Server Error'}),
        500,
        headers: {'Content-Type': 'application/json'},
      ));

      expect(
        () => apiService.buscarFilmeOmdb('tt1234567'),
        throwsException,
      );
    });
  });
} 