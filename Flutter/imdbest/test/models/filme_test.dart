import 'package:flutter_test/flutter_test.dart';
import 'package:imdbest/models/filme.dart';

void main() {
  group('Filme Model Tests', () {
    test('fromTmdbJson creates Filme instance correctly', () {
      final json = {
        'id': 123,
        'title': 'Test Movie',
        'release_date': '2024-01-01',
        'poster_path': '/test.jpg',
      };

      final filme = Filme.fromTmdbJson(json);

      expect(filme.tmdbId, 123);
      expect(filme.titulo, 'Test Movie');
      expect(filme.ano, '2024');
      expect(filme.posterUrl, 'https://image.tmdb.org/t/p/w500/test.jpg');
      expect(filme.imdbId, null);
    });

    test('fromTmdbJson handles missing fields', () {
      final json = {
        'id': 123,
        'title': null,
        'release_date': null,
        'poster_path': null,
      };

      final filme = Filme.fromTmdbJson(json);

      expect(filme.tmdbId, 123);
      expect(filme.titulo, '');
      expect(filme.ano, '');
      expect(filme.posterUrl, null);
      expect(filme.imdbId, null);
    });

    test('fromOmdbJson creates Filme instance correctly', () {
      final json = {
        'Title': 'Test Movie',
        'Year': '2024',
        'Poster': 'http://test.com/poster.jpg',
        'imdbID': 'tt1234567',
        'imdbRating': '8.5',
        'Plot': 'Test plot',
        'Director': 'Test Director',
        'Actors': 'Actor 1, Actor 2',
        'Genre': 'Action, Drama',
        'Ratings': [
          {
            'Source': 'Rotten Tomatoes',
            'Value': '90%'
          }
        ]
      };

      final filme = Filme.fromOmdbJson(json);

      expect(filme.titulo, 'Test Movie');
      expect(filme.ano, '2024');
      expect(filme.posterUrl, 'http://test.com/poster.jpg');
      expect(filme.imdbId, 'tt1234567');
      expect(filme.notaImdb, '8.5');
      expect(filme.sinopse, 'Test plot');
      expect(filme.diretor, 'Test Director');
      expect(filme.elenco, 'Actor 1, Actor 2');
      expect(filme.genero, 'Action, Drama');
      expect(filme.rottenTomatoes, '90%');
    });

    test('fromOmdbJson handles missing fields', () {
      final json = {
        'Title': null,
        'Year': null,
        'Poster': null,
        'imdbID': null,
        'imdbRating': null,
        'Plot': null,
        'Director': null,
        'Actors': null,
        'Genre': null,
        'Ratings': []
      };

      final filme = Filme.fromOmdbJson(json);

      expect(filme.titulo, '');
      expect(filme.ano, '');
      expect(filme.posterUrl, null);
      expect(filme.imdbId, null);
      expect(filme.notaImdb, null);
      expect(filme.sinopse, null);
      expect(filme.diretor, null);
      expect(filme.elenco, null);
      expect(filme.genero, null);
      expect(filme.rottenTomatoes, null);
    });

    test('fromOmdbJson handles missing Rotten Tomatoes rating', () {
      final json = {
        'Title': 'Test Movie',
        'Year': '2024',
        'Ratings': [
          {
            'Source': 'Internet Movie Database',
            'Value': '8.5/10'
          }
        ]
      };

      final filme = Filme.fromOmdbJson(json);

      expect(filme.rottenTomatoes, null);
    });
  });
} 