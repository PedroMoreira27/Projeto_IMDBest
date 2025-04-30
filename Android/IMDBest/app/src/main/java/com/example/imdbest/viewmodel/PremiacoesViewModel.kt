package com.example.imdbest.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.imdbest.api.OmdbApi
import com.example.imdbest.api.TmdbApiService
import com.example.imdbest.model.FilmeTmdb
import com.example.imdbest.model.FilmeDetalheTmdb
import com.example.imdbest.util.Event
import kotlinx.coroutines.launch

class PremiacoesViewModel(
    private val tmdbApi: TmdbApiService,
    private val omdbApi: OmdbApi
) : ViewModel() {

    private val _filmes = MutableLiveData<List<FilmeTmdb>>()
    val filmes: LiveData<List<FilmeTmdb>> = _filmes

    private val _filmeDetalhado = MutableLiveData<Event<FilmeDetalheTmdb>>()
    val filmeDetalhado: LiveData<Event<FilmeDetalheTmdb>> = _filmeDetalhado

    private val _premios = MutableLiveData<String>()
    val premios: LiveData<String> = _premios

    private val apiKeyTmdb = "d41a10c6861b1402691065387415ca43"

    fun buscarFilmes(nome: String) {
        viewModelScope.launch {
            try {
                val resultado = tmdbApi.buscarFilmes(apiKeyTmdb, nome)
                _filmes.value = resultado.results
            } catch (e: Exception) {
                _filmes.value = emptyList()
            }
        }
    }

    fun buscarDetalhesFilme(movieId: Int) {
        viewModelScope.launch {
            try {
                val detalhes = tmdbApi.buscarDetalhesFilme(movieId, apiKeyTmdb)
                _filmeDetalhado.value = Event(detalhes)
            } catch (e: Exception) {
                // Se der erro, não dispara nada
            }
        }
    }

    fun buscarPremios(imdbID: String) {
        viewModelScope.launch {
            try {
                val resultado = omdbApi.buscarDetalhesFilme(imdbID)
                _premios.value = resultado.Awards ?: "Sem informações de premiações."
            } catch (e: Exception) {
                _premios.value = "Erro ao buscar premiações."
            }
        }
    }
    fun limparPremios() {
        _premios.value = null
    }
}
