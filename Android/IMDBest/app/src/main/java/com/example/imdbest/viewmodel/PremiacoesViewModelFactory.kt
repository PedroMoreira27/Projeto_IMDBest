package com.example.imdbest.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.imdbest.api.OmdbApi
import com.example.imdbest.api.TmdbApiService

class PremiacoesViewModelFactory(
    private val tmdbApi: TmdbApiService,
    private val omdbApi: OmdbApi
) : ViewModelProvider.Factory {

    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(PremiacoesViewModel::class.java)) {
            return PremiacoesViewModel(tmdbApi, omdbApi) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
