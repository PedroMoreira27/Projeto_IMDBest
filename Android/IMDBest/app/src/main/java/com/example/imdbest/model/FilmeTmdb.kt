package com.example.imdbest.model

data class FilmeDetalheTmdb(
    val id: Int,
    val title: String,
    val overview: String?,
    val tagline: String?,
    val release_date: String?,
    val poster_path: String?,
    val imdb_id: String?
)
