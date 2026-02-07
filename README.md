# chatapp

![A showcase of the Chat UI Prototype](documentation/pictures/Chat.png)
![A showcase of Login UI](documentation/pictures/Login.png)
![A showcase of the Signup UI](documentation/pictures/Create-Account-Website.png)

- This is the repository of chatapp (no name currently), it contains frontend (web) backend (database (SQLite), python), and the cross-platform app (godot-widgets)
- My first full-stack kind of project
- PIP dependencies are listed in pip.txt => run pip install -r pip.txt
- other dependencies include python 3.12 and it's build components aswell as Godot 4.6

# Current feature state

- [x] Account creation and login
- [x] passwords are hashed and stored in a database
- [x] Chatting Interface on the desktop app
- [x] Simple message system across server and client
- [x] Authentication tokens are generated on the server
- [x] Authentication tokens are stored in the client's OS keychain (auto login)

# Current Goals

- [ ] Consider switching from SQLite to PostgreSQL
- [ ] Consider moving the client implementation to C#
- [ ] Implement the Server as a docker container