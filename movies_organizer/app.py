import argparse
import logging
import os
import sys

from movies_organizer import utils, __version__

__author__ = "Ali Masri"
__copyright__ = "Ali Masri"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Movie library organizer")
    parser.add_argument(
        '--version',
        action='version',
        version='movies_organizer {ver}'.format(ver=__version__))
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    parser.add_argument(
        '--src',
        help="the source directory",
        type=str,
        metavar="TEXT")
    parser.add_argument(
        '--dst',
        help="the destination folder",
        type=str,
        metavar="TEXT")
    parser.add_argument(
        '--auto',
        const=True,
        default=False,
        nargs='?',
        help="automatically select a movie from the search results",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    num_stars = 40
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Program started...")
    src = args.src if args.src is not None else "."
    auto_select = args.auto
    dst = args.dst if args.dst is not None else src
    movies = os.listdir(src)
    if movies is None:
        print('No movies found in: ' + src)
        exit(0)
    missing_movies = []
    for file_name in movies:
        movie_title = os.path.splitext(file_name)[0]
        try:
            print(num_stars * "*")
            print("Searching for " + str(movie_title.encode("utf8")) + "...")
            movie = utils.search(movie_title, auto_select)
            if movie is None:
                print('Movie not found...')
                missing_movies.append(movie_title)
                continue
            utils.move_files(os.path.join(src, file_name), dst, movie)
        except Exception as error:
            print('Error: ' + str(error))
            continue
    if len(missing_movies) != 0:
        print(num_stars * "*")
        print('Sorry we could not find the following movies:')
        for movie_title in missing_movies:
            print(str(movie_title.encode("utf8")))
            print(num_stars * "*")
    _logger.info("Process finished")


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
