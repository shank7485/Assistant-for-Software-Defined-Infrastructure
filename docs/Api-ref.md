#API Documentation:

* URLS/Endpoints: 
    
    ```
    /,
    /login,
    /logout,
    /chat,
    /set,
    /consoleScreen,
    /getConsoleLog
    ```

* Methods Supported(Currently):
    
    ```
    /login -- GET, POST
    Others – GET
    ```

* URL Params:
    
    ```
    /chat – question
    /set – key, value
    /consoleScreen – ip
    /getConsoleLog – ip
    others – N/A
    ```

* Data Params:
    
    ```
    /login[POST] – {username: “admin”, password: “admin”}
    others – N/A
    ```

* Success Response (Code):
    
    ``` 
    /logout – 302 (Redirect)
    /getConsoleLog – 302 (Redirect)
    Others – 200 (OK)
    ```
 
* Error Response (Code): 
    
    ```
    /login – 401 Unauthorized, 400 Bad Request
    /getConsoleLog – 404 Not Found
    Others – 500 Internal Server Error if hit directly otherwise
    no error codes as everything will be redirected to the /login page.
    ```

* Return/Output data:
    
    ```
    / -- render html page (login.html)
    /login – render html page (login.html)
    /login (successful login) – render html page (chat-screen.html)
    /logout – render html page (login.html)
    /chat – JSON response
    /set – JSON response
    /consoleScreen – render html page (console.html)
    /getConsoleLog – output a text file with logs
    ```

* Privilege levels required:
    
    ```
    Cloud Admin credentials for some operations
    ```

* Network Ports Used(Currently):
    
    ```
    8081
    ```

* APIs exposed:
    
    ```
    /login
    ```

* Command Line Arguments:
    
    ``` 
    N/A
    ```

* Environment Variables:
    
    ```
    N/A
    ```

* Scripting Languages:
    
    ```
    Python,
    English (Debatable)
    ```

* Web Services:

    ```
    Flask
    ```

* Description/Functionality:
    
    ```  
    / -- This endpoint just redirects to the login page

    /login – This endpoint renders a login.html page which is a basic html login form with username and password as it’s fields.
    If a user enters correct credentials then it redirects to the chat-screen.html page which is a basic chat-widget
    for the user to have interaction with the chatbot in a conversational manner.

    /logout – This endpoint will simply logout the user and redirect to the login page.

    /chat – This endpoint is the where the user will send messages to the ChatBot for cloud management/deployment
    and will receive responses from the bot in an interactive way. For example: “Create a VM” will be send here.
    Based on the messages and the bot’s response OpenStack API calls will also be made.

    /set – This endpoint is where the user selects/sets options.
    For example- If a user asks the bot to delete a network, the bot will respond with a list of networks.
    The user will select the network he/she wants to delete with this endpoint.

    /consoleScreen – This endpoint simply renders the console.html page which serves as the console screen for deployment.

    /getConsoleLog – This endpoint outputs a .txt file with the live deployment logs on to the console screen. 



