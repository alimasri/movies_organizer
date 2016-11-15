import os
import re
import requests
import shutil

from guessit import guessit
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
    try:
        response = requests.get(movie.cover, stream=True)
    except Exception as error:
        print(error)
        return None
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


def move_files(src, dest, movie):
    folder_name = '{0}_{1}_{2}'.format(movie.title, movie.year, movie.rating)
    folder_name = format_file_name(folder_name)
    genres_path = ','.join(str(e) for e in movie.genres).lower()
    dest = os.path.join(dest, genres_path)
    if not os.path.exists(dest):
        os.makedirs(dest)
    dest = os.path.join(dest, folder_name)
    if not os.path.exists(dest):
        os.makedirs(dest)
    if os.path.isdir(src):
        # src is a directory
        files = os.listdir(src)
        print('Moving files from {0} to {1}'.format(src, dest))
        for file in files:
            shutil.move(os.path.join(src, file), dest)
        shutil.rmtree(src)
    else:
        # src is a movie file
        print('Movie file {0} to {1}'.format(src, dest))
        shutil.move(src, dest)
    print('Downloading movie cover...')
    download_cover(movie, dest)
    print('Printing movie information...')
    print_movie_information(dest, movie)
    print('Done')
    return None


def list_folders(path):
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            yield file


def search(movie_title, auto_select):
    guess = guessit(movie_title)
    if 'title' not in guess:
        guess['title'] = os.path.splitext(movie_title)[0]
    movies = imdb.search_for_title(guess['title'])
    if movies is None:
        return None
    print("Found {0} movies".format(len(movies)))
    imdb_id = -1
    for movie in movies:
        print('Title: {0}, Year: {1}'.format(movie.get('title'), movie.get('year')))
        # if the select first option is set then set the flag to false in order to skip the loop
        flag = not auto_select
        # if the select first option is set then the answer is y to get the movie information directly
        answer = "y"
        while flag:
            answer = input("Is this your movie? yes (y), no (n), skip (s)? ")
            if answer not in ['y', 'n', 's']:
                print('Invalid option')
            else:
                flag = False
        if answer == 'y':
            if 'year' in guess and 'year' in movie and (int(movie.get('year')) != guess['year']):
                continue
            print("Please wait, getting more information...")
            imdb_id = movie.get('imdb_id')
            break
        elif answer == 's':
            return None
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
