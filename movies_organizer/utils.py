import os
import re
import requests
import shutil
import sys

from guessit import guessit
import imdb
from requests import RequestException

from movies_organizer.movie import Movie

api = imdb.IMDb()

if sys.version[0] == "3":
    raw_input = input


def format_file_name(name):
    if name is None:
        return None
    return re.sub('[/:*?\"<>|]', '', name)


def print_movie_information(to_dir, movie):
    if movie is None or to_dir is None:
        return None
    with open(os.path.join(to_dir, 'info.txt'), 'w') as file:
        file.write('Title: {0}\n'
                   'Year: {1}\n'
                   'Release date: {2}\n'
                   'Rating: {3}\n'
                   'Runtime: {4}\n'
                   'Plot summary: {5}\n'
                   'Genres: {6}'.format(movie.title, movie.year, movie.release_date, movie.rating,
                                        print_time(movie.runtime), movie.plot,
                                        ' '.join([genre for genre in movie.genres])))


def download_cover(movie, path):
    if movie is None or movie.cover is None:
        return
    try:
        response = requests.get(movie.cover, stream=True)
        if response.ok:
            extension = os.path.splitext(movie.cover)[1]
            filename = "{0}_{1}{2}".format(movie.year, movie.title, extension)
            filename = format_file_name(filename.lower())
            with open(os.path.join(path, filename), 'wb') as image:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    image.write(block)
    except:
        pass


def move_files(src, dst, movie):
    if src is None or dst is None or movie is None:
        return False
    folder_name = '{0}_{1}_{2}'.format(movie.year, movie.title, movie.rating)
    folder_name = format_file_name(folder_name)
    if not os.path.exists(dst):
        os.makedirs(dst)
    dst = os.path.join(dst, folder_name)
    if not os.path.exists(dst):
        os.makedirs(dst)
    if os.path.isdir(src):
        # src is a directory
        files = os.listdir(src)
        for file in files:
            shutil.move(os.path.join(src, file), dst)
        shutil.rmtree(src)
    else:
        # src is a movie file
        shutil.move(src, dst)
    download_cover(movie, dst)
    print_movie_information(dst, movie)
    return True


def list_folders(path):
    if path is None: return
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            yield file


def print_time(mins):
    if mins is None: return None
    h, m = divmod(int(mins), 60)
    return "%02d:%02d" % (h, m)


def search(movie_title, auto_select):
    guess = guessit(movie_title)
    if guess is None:
        guess = {}
    if 'title' not in guess:
        guess['title'] = movie_title
    movies_list = api.search_movie(guess['title'])
    if movies_list is None:
        return None
    if auto_select is False:
        print("Found {0} movies".format(len(movies_list)))
    a_movie = None
    for movie_item in movies_list:
        if auto_select is True:
            try:
                if int(movie_item.get('year')) != int(guess.get('year')):
                    continue
            except:
                pass
        print('Title: {0}, Year: {1}'.format(movie_item.get('title'), movie_item.get('year')))
        flag = not auto_select
        answer = "y"
        while flag:
            answer = raw_input("Is this your movie? yes (y), no (n), skip (s)? ")
            if answer not in ['y', 'n', 's']:
                print('Invalid option')
            else:
                flag = False
        if answer == 'y':
            a_movie = movie_item
            break
        elif answer == 's':
            return None
    if a_movie is None:
        return None
    try:
        api.update(a_movie)
    except:
        pass
    movie = Movie()
    movie.title = a_movie.get('title')
    movie.year = a_movie.get('year')
    movie.release_date = a_movie.get('original air date')
    movie.rating = a_movie.get('rating')
    movie.runtime = a_movie.get('runtime')
    if movie.runtime is not None:
        movie.runtime = movie.runtime[0]
    movie.genres = a_movie.get('genres')
    movie.cover = a_movie.get('cover url')
    movie.plot = a_movie.get('plot outline')
    return movie
