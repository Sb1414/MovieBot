async def response_parser(movie_data: dict):
    title = movie_data.get('name') or movie_data.get('alternativeName') or movie_data.get('enName')
    year = movie_data.get('year')
    genres = [genre['name'] for genre in movie_data.get('genres', [])]
    description = movie_data.get('description') or movie_data.get('shortDescription')
    rating = movie_data.get('rating', {}).get('kp') or movie_data.get('rating', {}).get('imdb')
    movie_length = movie_data.get('movieLength')
    formatted_description = f"🎬 Название: {title}\n"
    if year:
        formatted_description += f"📅 Год выпуска: {year}\n"
    if genres:
        formatted_description += f"🎭 Жанры: {', '.join(genres)}\n"
    if description:
        formatted_description += f"📝 Описание: {description}\n"
    if rating:
        formatted_description += f"⭐ Рейтинг: {rating}\n"
    if movie_length:
        formatted_description += f"⏱️ Длительность: {movie_length} минут\n"
    return formatted_description
