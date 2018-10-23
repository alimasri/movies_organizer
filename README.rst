================
Movies Organizer
================


An application that helps users easily organize and enrich their movie collection repository.


Description
===========

Movies Organizer helps users easily organize their movie collection repository by using the IMDB API to categorize movies and enrich them with information such as rating, genre, etc.

The application first scans a given repository for folders and movie files.
Then it uses the folder/file name to guess some movie information.
These information are then sent to IMDB to be enriched.

The enriched information contain data about the movie genre, formatted movie name, release data, runtime and plot.

Movies then will be grouped by their genre and put in a folder formatted as follows [genres]/movie-name_year_rating.
For example: comedy,drama/Perfect Strangers_2016_7.7

The folder will contain the movie file, the downloaded movie cover and an info.txt file that contains additional information about the movie.

This will make it easier for users to navigate their movies.

User may use simple file searches to filter their movies.

Example:
search for _7* to get all movies with rating 7, search for comedy to get all comedy movies, etc.

Installation
============

Installing the application is very simple.
To do so please follow the directions below:

1. Install Python https://www.python.org/downloads/ and add it to your path
2. Install Git https://git-scm.com/downloads and add it yo your path
3. Check if you have pip (python package manager) installed by running `pip --version`

 a. If not download the file [get-pip.py] (https://bootstrap.pypa.io/get-pip.py/), being careful to save it as a .py file rather than .txt
 b. Run it from the command prompt: python get-pip.py

4. Run the command `pip install git+https://github.com/alimasri/movies_organizer`

Usage
=====

After the installation process is finished you can access the program from a command line interface using the following command:

`movies_organizer [--src "source folder"] [--dst "destination folder"] [--auto]`

1. You can simply choose the same folder for src and dest or omit the dest option to move the files to the same directory.
2. In case src and dest were omitted, the program will proceed with the same directory the program was run from.
3. The auto switch is an option to automatically choose the movie guess (in case there was more than one movie with the same name)

Note
====

This project has been set up using PyScaffold 2.5.7. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
