import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:imdbest/services/auth_service.dart';

@GenerateMocks([http.Client])
import 'auth_service_test.mocks.dart';

void main() {
  late AuthService authService;
  late MockClient mockClient;

  setUp(() {
    mockClient = MockClient();
    authService = AuthService();
  });

  group('AuthService Tests', () {
    test('login success', () async {
      final mockResponse = {
        'token': 'mock_token',
        'usuario': {
          'id': 1,
          'nome': 'Test User',
          'email': 'test@example.com'
        }
      };

      when(mockClient.post(
        Uri.parse('http://127.0.0.1:5000/auth/login'),
        headers: anyNamed('headers'),
        body: anyNamed('body'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode(mockResponse),
        200,
        headers: {'Content-Type': 'application/json'},
      ));

      final result = await authService.login('test@example.com', 'password123');
      expect(result, equals(mockResponse));
    });

    test('login failure', () async {
      final mockError = {'mensagem': 'Credenciais inválidas'};

      when(mockClient.post(
        Uri.parse('http://127.0.0.1:5000/auth/login'),
        headers: anyNamed('headers'),
        body: anyNamed('body'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode(mockError),
        401,
        headers: {'Content-Type': 'application/json'},
      ));

      expect(
        () => authService.login('wrong@example.com', 'wrongpass'),
        throwsException,
      );
    });

    test('registrar success', () async {
      final mockResponse = {
        'mensagem': 'Usuário registrado com sucesso',
        'usuario': {
          'id': 1,
          'nome': 'New User',
          'email': 'new@example.com'
        }
      };

      when(mockClient.post(
        Uri.parse('http://127.0.0.1:5000/auth/registrar'),
        headers: anyNamed('headers'),
        body: anyNamed('body'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode(mockResponse),
        201,
        headers: {'Content-Type': 'application/json'},
      ));

      final result = await authService.registrar(
        'New User',
        'new@example.com',
        'password123',
      );
      expect(result, equals(mockResponse));
    });

    test('registrar failure', () async {
      final mockError = {'mensagem': 'Email já cadastrado'};

      when(mockClient.post(
        Uri.parse('http://127.0.0.1:5000/auth/registrar'),
        headers: anyNamed('headers'),
        body: anyNamed('body'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode(mockError),
        400,
        headers: {'Content-Type': 'application/json'},
      ));

      expect(
        () => authService.registrar(
          'Existing User',
          'existing@example.com',
          'password123',
        ),
        throwsException,
      );
    });
  });
} 