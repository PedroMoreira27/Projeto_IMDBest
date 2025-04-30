package com.example.imdbest.api

import com.example.imdbest.model.FilmeBuscaTmdbResponse
import com.example.imdbest.model.FilmeDetalheTmdb
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface TmdbApiService {

    @GET("search/movie")
    suspend fun buscarFilmes(
        @Query("api_key") apiKey: String,
        @Query("query") query: String
    ): FilmeBuscaTmdbResponse

    @GET("movie/{movie_id}")
    suspend fun buscarDetalhesFilme(
        @Path("movie_id") movieId: Int,
        @Query("api_key") apiKey: String
    ): FilmeDetalheTmdb

    companion object {
        fun create(): TmdbApiService {
            val retrofit = Retrofit.Builder()
                .baseUrl("https://api.themoviedb.org/3/")
                .addConverterFactory(GsonConverterFactory.create())
                .build()
            return retrofit.create(TmdbApiService::class.java)
        }
    }
}
