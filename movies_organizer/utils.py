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

if sys.version[0] == "3": raw_input = input


def format_file_name(name):
    return re.sub('[/:*?\"<>|]', '', name)


def print_movie_information(to_dir, movie):
    with open(os.path.join(to_dir, 'info.txt'), 'w') as file:
        file.write('Title: {0}\n'
                   'Year: {1}\n'
                   'Release date: {2}\n'
                   'Rating: {3}\n'
                   'Runtime: {4}\n'
                   'Plot summary: {5}'.format(movie.title, movie.year, movie.release_date, movie.rating,
                                              print_time(movie.runtime),
                                              movie.plot))


def download_cover(movie, path):
    try:
        response = requests.get(movie.cover, stream=True)
    except RequestException as error:
        print(error)
        return None
    if response.ok:
        extension = os.path.splitext(movie.cover)[1]
        filename = "{0}_{1}{2}".format(movie.title, movie.year, extension)
        filename = format_file_name(filename.lower())
        with open(os.path.join(path, filename), 'wb') as image:
            for block in response.iter_content(1024):
                if not block:
                    break
                image.write(block)


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
        print('Movie file {0} to {1}'.format(str(src.encode("utf8")), str(dest.encode("utf8"))))
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


def print_time(mins):
    h, m = divmod(int(mins), 60)
    return "%02d:%02d" % (h, m)


def search(movie_title, auto_select):
    guess = guessit(movie_title)
    if 'title' not in guess:
        guess['title'] = os.path.splitext(movie_title)[0]
    movies = api.search_movie(guess['title'])
    if movies is None:
        return None
    print("Found {0} movies".format(len(movies)))
    my_movie = None
    for current_movie in movies:
        if auto_select is True:
            if 'year' in guess and 'year' in current_movie:
                if int(current_movie.get('year')) != guess['year']:
                    continue
        print('Title: {0}, Year: {1}'.format(current_movie.get('title'), current_movie.get('year')))
        flag = not auto_select
        answer = "y"
        while flag:
            answer = raw_input("Is this your movie? yes (y), no (n), skip (s)? ")
            if answer not in ['y', 'n', 's']:
                print('Invalid option')
            else:
                flag = False
        if answer == 'y':
            my_movie = current_movie
            break
        elif answer == 's':
            return None
    if my_movie is None:
        return None
    print("Please wait, getting more information...")
    api.update(my_movie)
    movie = Movie()
    movie.title = my_movie['title']
    movie.year = my_movie['year']
    movie.release_date = my_movie['original air date']
    movie.rating = my_movie['rating']
    movie.runtime = my_movie['runtime'][0]
    movie.genres = my_movie['genres']
    movie.cover = my_movie['cover url']
    movie.plot = my_movie['plot outline']
    return movie
