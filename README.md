

# movies_organizer

A lightweight Python command-line tool that automatically organizes your movie collection. It parses movie filenames, fetches metadata from IMDb, and moves files into neatly structured directories. It also downloads cover art and generates a summary file for each movie.

## Features
- 🎬 **Smart Filename Parsing**: Uses `guessit` to extract title and year from raw filenames
- 🔍 **IMDb Integration**: Fetches detailed metadata (rating, runtime, genres, plot, release date)
- 📂 **Automatic Organization**: Moves files into `YEAR_TITLE_RATING` folders
- 🖼️ **Cover Art Download**: Saves the official movie poster inside the organized folder
- 📝 **Info Generation**: Creates an `info.txt` file with plot summary and metadata
- 🤖 **Interactive or Automated**: Manually confirm matches or enable `--auto` for silent matching based on release year

## Requirements
- Python 3.x
- `guessit`
- `python-imdb`
- `requests`

## Installation
```bash
git clone https://github.com/alimasri/movies_organizer.git
cd movies_organizer
pip install -e .
```

## Usage
Run the organizer from your terminal:
```bash
python -m movies_organizer --src /path/to/downloaded/movies --dst /path/to/library
```

### CLI Arguments
| Flag | Description |
|------|-------------|
| `--src PATH` | Source directory containing unorganized movie files (defaults to current directory) |
| `--dst PATH` | Destination directory for organized folders (defaults to `--src`) |
| `--auto`     | Automatically select the first matching IMDb result with the correct release year |
| `-v`         | Set log level to INFO |
| `-vv`        | Set log level to DEBUG |
| `--version`  | Show program version and exit |

**Interactive Mode**: By default, the tool will prompt you to confirm each movie match:
```
Found 3 movies
Title: Inception, Year: 2010
Is this your movie? yes (y), no (n), skip (s)?
```

## License
MIT License

## Author
Ali Masri
