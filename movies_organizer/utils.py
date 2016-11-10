import os
import re
import requests
import shutil

from imdbpie import Imdb

from movies_organizer.movie import Movie

imdb = Imdb()


def format_file_name(name):
    return re.sub('[/:*?\"<>|]', '', name)


def print_movie_information(to_dir, movie):
    file = open(os.path.join(to_dir, 'info.txt'), 'w')
    file.write('Title: {0}\n'
               'Year: {1}\n'
               'Release date: {2}\n'
               'Rating: {3}\n'
               'Runtime: {4}\n'
               'Plot summary: {5}'.format(
        movie.title, movie.year, movie.release_date, movie.rating, movie.runtime, movie.plot))
    file.close()


def download_cover(movie, path):
    response = requests.get(movie.cover, stream=True)
    if response.ok:
        extension = os.path.splitext(movie.cover)[1]
        filename = "{0}_{1}{2}".format(movie.title, movie.year, extension)
        filename = format_file_name(filename.lower())
        image = open(os.path.join(path, filename), 'wb')
        for block in response.iter_content(1024):
            if not block:
                break
            image.write(block)
        image.close()


def move_files(from_dir, to_dir, movie):
    folder_name = '{0}_{1}_{2}'.format(movie.title, movie.year, movie.rating)
    folder_name = format_file_name(folder_name)
    genres_path = ', '.join(str(e) for e in movie.genres).lower()
    to_dir = os.path.join(to_dir, genres_path)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    to_dir = os.path.join(to_dir, folder_name)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    files = os.listdir(from_dir)
    print('Moving files from {0} to {1}'.format(from_dir, to_dir))
    for file in files:
        shutil.copy(os.path.join(from_dir, file), to_dir)
    print('Downloading movie cover...')
    download_cover(movie, to_dir)
    print('Printing movie information...')
    print_movie_information(to_dir, movie)
    print('Done')
    return None


def list_folders(path):
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            yield file


def search(movie_title, select_first):
    movie_title = re.sub(r'\(.*\)|\[.*\]', '', movie_title)
    # TODO: add more possible options
    possible_titles = [movie_title]
    movies = []
    for possible_title in possible_titles:
        movies.extend(imdb.search_for_title(possible_title))
    if movies is None:
        return None
    print("Found {0} movies".format(len(movies)))
    imdb_id = -1
    for movie in movies:
        print('Title: {0}, Year: {1}'.format(movie.get('title'), movie.get('year')))
        # if the select first option is set then set the flag to false in order to skip the loop
        flag = not select_first
        # if the select first option is set then the answer is y to get the movie information directly
        answer = "y"
        while flag:
            answer = input("Is this your movie? yes (y), no (n), skip (s)? ")
            if answer not in ['y', 'n', 's']:
                print('Invalid option')
            else:
                flag = False
        if answer == 'y':
            print("Please wait, getting more information...")
            imdb_id = movie.get('imdb_id')
            break
        elif answer == 's':
            break
    if imdb_id == -1:
        return None
    info = imdb.get_title_by_id(imdb_id)
    movie = Movie()
    movie.title = info.title
    movie.year = info.year
    movie.release_date = info.release_date
    movie.rating = info.rating
    movie.runtime = info.runtime
    movie.genres = info.genres
    movie.cover = info.poster_url
    movie.plot = info.plot_outline
    return movie
