# Pylunch

``PyLunch`` was designed to scrape restaurants for it's daily menus and show them in multiple ways and formats.

## Getting stated
`PyLunch` is a scraper, to use it, you have to install it. It is available at [PyLunch](https://gitlab.com/pestanko/pylunch)

### Install the released version

You can install the `PyLunch` using the `pip`:
```bash
$ pip install pylunch
```


### Install the development version from github
- Python 3.6 or later
- (Optional) [pipenv](https://github.com/pypa/pipenv)

Or you can add it as a development dependency using the ``pipenv``

```bash
$ git clone https://github.com/pestanko/pylunch.git
$ cd pylunch
$ pipenv install # install the dependencies
```

### First Run
In order to run the tool correctly you need to configure it.

At first run the tool will create config folder in the home directory with restaurants database, 
by default it will be empty.

To use the `zomato` resolver you need to add the `zomato_key` to your configuration.
In order to get the zomato key you need to go to the [Zomato Api documentation](https://developers.zomato.com/api)

```bash
$ pylunch cfg-set zomato_key "<YOUR_KEY>"
```

To use the telegram integration, you need to set the telegram bot token property ``telegram_token``.
To get the telegram bot token please take a look [here](https://core.telegram.org/bots).

```bash
$ pylunch cfg-set telegram_token "<YOUR_KEY>"
```

Also if you have already created or exported database of the restaurants, you an import it using the command `import`:
Example file is located in: `resources/restaurants.yml` available [here](https://gitlab.com/pestanko/pylunch/raw/master/resources/restaurants.yml).

```bash
$ pylunch import restaurants.yml
```

In order to export the restaurants database file, you can use the export command.
```bash
$ pylunch export -f exported.yml
```

## Run the cli tool

Hera is a help output with available commands

```bash
# Show the help
$ pylunch --help

Usage: pylunch [OPTIONS] COMMAND [ARGS]...

  PyLunch CLI tool

Options:
  --version              Show the version and exit.
  -L, --log-level TEXT   Set log level (d|i|w|e) - default=w
  -C, --no-cache         Disable cache
  -c, --config-dir TEXT  Location to the configuration directory
  -F, --format TEXT      Set output format
  --help                 Show this message and exit.

Commands:
  add            Adds a new restaurant
  cache-clear    Clear a current cache for a day
  cache-content  Show the current cache for a day
  cfg-edit       Edit a configuration using the editor (Ex: VIM)
  cfg-set        Set a config value in the user configuration
  config         Shows the current configuration
  console        Start the interactive console (IPython)
  disable        Disables the restaurants
  edit           Edits restaurants DB file
  enable         Enables the restaurants
  export         Export restaurants
  import         Import restaurants
  info           Get info for the restaurant
  ls             List all available restaurants
  menu           Get menu for a restaurant
  rm             Removes the restaurant
  telegram-bot   Start the telegram bot


```



