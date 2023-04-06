# PersonalFinancesDashboard

Python used for this program: 3.11.0

To install required packages run:
```
pip install -r requirements.txt
```

To run code formatter and tests:
```
black --line-length 100 . ; pytest tests.py
```

To start the dashboard:
```
tmux new -s dashboard
source venv_dasboard/bin/activate
python3 -m streamlit run main.py --server.fileWatcherType poll
# using the default watchdog as filewatchertype exceeded the inotify instance limit 
Ctrl+b d # to detach from session
```