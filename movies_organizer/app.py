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
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
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
        '--dest',
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
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    num_stars = 40
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Program started...")
    src = args.src if args.src is not None else "."
    dest = args.dest if args.dest is not None else src
    auto_select = args.auto
    movies = os.listdir(src)
    if movies is None:
        print('No movies found in: ' + src)
        exit(0)
    missing_movies = []
    for movie_title in movies:
        try:
            print(num_stars * "*")
            print("Searching for " + str(movie_title.encode("utf8")) + "...")
            movie = utils.search(movie_title, auto_select)
            if movie is None:
                print('Movie not found...')
                missing_movies.append(movie_title)
                continue
            utils.move_files(os.path.join(src, movie_title), dest, movie)
        except Exception as error:
            print(error)
            continue
    if len(missing_movies) != 0:
        print(num_stars * "*")
        print('Sorry we could not find the following movies:')
        for movie_title in missing_movies:
            print(str(movie_title.encode("utf8")))
            print(num_stars * "*")
    _logger.info("Process finished")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
