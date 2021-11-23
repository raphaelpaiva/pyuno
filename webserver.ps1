pip install -r .\requirements_devel.txt -r .\requirements_web.txt
waitress-serve --listen=*:5000 webserver:app