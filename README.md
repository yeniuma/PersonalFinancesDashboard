# PersonalFinancesDashboard

Python used for this program: 3.11.0

To install required packages run:
```
pip install -r requirements.txt
# OR if you have conda
conda install --file requirements.txt
```

To start continous deployment process in the background:
```
nohup ngrok http 8000 &
curl http://127.0.0.1:4040/api/tunnels # to get the public url
nohup python continous_deployment.py &
```

To start application process in the background:
```
nohup streamlit run continous_deployment.py &
```

Useful commands:
```
lsof -i :80 #check what is using port 80
```