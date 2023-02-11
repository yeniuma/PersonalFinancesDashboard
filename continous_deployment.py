import git
from flask import Flask, request

app = Flask(__name__)
LISTENING_PORT = 8000

@app.route('/', methods=['POST'])
def gitpull():
    git_repo = git.Repo()
    git_repo.git.checkout("origin/master")
    git_repo.git.pull()
    print("Repo successfully updated")


if __name__ == '__main__':
    app.run(port=LISTENING_PORT, debug=False)