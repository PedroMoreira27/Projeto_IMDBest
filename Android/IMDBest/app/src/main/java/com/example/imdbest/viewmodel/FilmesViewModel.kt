package com.example.imdbest.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.imdbest.api.TmdbApiService
import com.example.imdbest.model.FilmeTmdb
import com.example.imdbest.model.FilmeDetalheTmdb
import kotlinx.coroutines.launch

class FilmesViewModel(
    private val tmdbApi: TmdbApiService
) : ViewModel() {

    private val _filmes = MutableLiveData<List<FilmeTmdb>>()
    val filmes: LiveData<List<FilmeTmdb>> = _filmes

    private val _filmeDetalhado = MutableLiveData<FilmeDetalheTmdb?>()
    val filmeDetalhado: LiveData<FilmeDetalheTmdb?> = _filmeDetalhado

    private val apiKey = "d41a10c6861b1402691065387415ca43" // Troque pela sua chave do TMDB

    fun buscarFilmes(nome: String) {
        viewModelScope.launch {
            try {
                val resposta = tmdbApi.buscarFilmes(apiKey, nome)
                _filmes.value = resposta.results
            } catch (e: Exception) {
                _filmes.value = emptyList()
            }
        }
    }

    fun buscarDetalhesFilme(movieId: Int) {
        viewModelScope.launch {
            try {
                val detalhes = tmdbApi.buscarDetalhesFilme(movieId, apiKey)
                _filmeDetalhado.value = detalhes
            } catch (e: Exception) {
                _filmeDetalhado.value = null
            }
        }
    }

    fun limparFilmeDetalhado() {
        _filmeDetalhado.value = null
    }
}
