package com.example.imdbest.api

import com.example.imdbest.model.OmdbFilmeDetalhe
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Query

interface OmdbApi {

    @GET("/")
    suspend fun buscarDetalhesFilme(
        @Query("i") imdbID: String,
        @Query("apikey") apiKey: String = "f201fb92"
    ): OmdbFilmeDetalhe

    companion object {
        fun create(): OmdbApi {
            val retrofit = Retrofit.Builder()
                .baseUrl("https://www.omdbapi.com/")
                .addConverterFactory(GsonConverterFactory.create())
                .build()
            return retrofit.create(OmdbApi::class.java)
        }
    }
}
