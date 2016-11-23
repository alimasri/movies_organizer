================
Movies Organizer
================


An application that helps users easily organize and enrich their movie collection repository.


Description
===========

Movies Organizer helps users easily organize their movie collection repository by using the IMDB API to categorize movies and enrich them with information such as rating, genre, etc.
The application first scans a given repository for folders and movie files.
Then it will use the folder/file name to guess some movie information.
These information are then sent to IMDB to be enriched.
The enriched information contain data about the movie genre, formatted movie name, release data, runtime and plot.
Movies then will be grouped by their genre and put in a folder formatted as follows [genres]/movie-name_year_rating.
For example: comedy,drama/Perfect Strangers_2016_7.7
This will make it easier for users to navigate their movies.
User may use simple file searches to filter their movies.
Example:
search for _7* to get all movies with rating 7, search for comedy to get all comedy movies, etc.
Installation and Usage
======================

Installing movies organizer is very simple.
First please note that you should have Python installed.
Download the project, navigate to the directory and run the command:

`python setup.py install`

This command will download and install the project with the required dependencies.
After the installation process is finished you can access the program from a command line interface using the following command:
movie_organizer --src "source folder" --dest "destination folder" [--auto]
You can simple choose the same folder for src and dest to move the files to the same directory.
In case src and dest were omitted, the program will proceed with the same directory the program was run from.
The auto switch is an option to automatically choose the movie guess (in case there was more than one movie with the same name)

Note
====

This project has been set up using PyScaffold 2.5.7. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
