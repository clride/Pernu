# chatapp

```
![Alt text](documentation/picures/Chat.png)
```

- This is the repository of chatapp (no name currently), it contains frontend (web) backend (database (SQLite), python), and cross-platform app (godot-widgets)
- My first full-stack kind of project
- PIP dependencies are listed in pip.txt => run pip install -r pip.txt
- other dependencies include python 3.12 and it's build components aswell as Godot 4.6

# Current feature state

- Account creation and login [x]
- passwords are hashed and stored in a database [x]
- Chatting Interface on the desktop app [x]

# Current Goals

- Implement a very simple message system across server and client simple message system across server and client
- Generate auth tokens on the server
- Store authentication tokens in the OS keychain / auto login
- Consider switching from SQLite to PostgreSQL
- Implement the Server as a docker container
