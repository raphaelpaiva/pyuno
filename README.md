# PyUno

Yes, just another Uno implementation in python :p

## Running

PyUno was developed with python 3.9. I did not test this with other versions. You are welcome to do so : ).

## Local CLI

```bash
# Install all required libs:
pip install -r requirements.txt

# Have fun!
python cli_local.py
```

The CLI interface is very crude.

Commands available are:
* exit: This will exit the game.
* draw: This will draw a card from the discard pile.
* play <_card number_> [_suite_]: this will play the card refered by the number below it. If the card requires a suite, like the *+4* or *w (wild)* you can provide a suite name after the number.
* pass: This will skip your turn.

## Server

```bash
# Install all required libs:
pip install -r requirements.txt
```

The server is built with flask. You can run the slooooooow version directely with:

```bash
python webserver.py
```

Or the (windows only for now) faster version with waitress:

```powershell
# This will install all required dependencies and start the server.
.\webserver.ps1
```

I promisse we'll have a docker version soon.

## Remote CLI

The remote client for now is the CLI one:

```bash
python cli_remote.py
```

All the parameters to the game are hardcoded for now. Yes, nasty :D.

Have fun!