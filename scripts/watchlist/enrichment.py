
def add_movie_rating(movies):
    ratings = load_tv("data/ratings-live-votes.csv")

    ratings = ratings[
        ["uuid", "vote_key"]
    ]

    movies = movies.merge(
        ratings,
        on="uuid",
        how="left"
    )
    movies["vote_key"] = (
        movies["vote_key"]
        .str.split("-")
        .str[-1]
    )
    rating_map = {
        "1": 1,
        "27": 2,
        "28": 3,
        "29": 4,
        "3": 5
    }

    movies["rating"] = (
        movies["vote_key"]
        .map(rating_map)
    )

    return movies

def add_tmdb_info(movies):

    infos = []

    for _, movie in movies.iterrows():

        info = get_movie_info(
            movie["imdb_id"]
        )

        if info:
            info["uuid"] = movie["uuid"]
            infos.append(info)


    tmdb_df = pd.DataFrame(infos)


    movies = movies.merge(
        tmdb_df,
        on="uuid",
        how="left"
    )

    return movies