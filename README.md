# mathcontest_server
Inner server for math contest at the vk group MathJokes

For the server to work correctly, you need to install all packages from the requirements.txt file

The start script is start_server.sh
You also can add environment variables such as:
SECRET_KEY
DATABASE_URL
ADMIN_SECRET
in the same way, as FLASK_APP is added in the start_server.sh file.

To see all the routes look into the app/routes.py

It is possible to play multiplayer hot-seat game: 
python3 other_clients/console_hotseat_client.py

We are also working on a console http client.  It's file is other_clients/http_client.py, but it is raw yet.

And remember - everything is subject to change
 