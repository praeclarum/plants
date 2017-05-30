kill -9 $(ps aux | grep '[p]ython ./app3.py' | awk '{print $2}')

