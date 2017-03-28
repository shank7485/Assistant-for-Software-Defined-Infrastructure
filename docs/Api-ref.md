# API Documentation:

* URLs/Endpoints: 
    
    ```
    /,
    /login,
    /logout,
    /chat,
    /set,
    /consoleScreen,
    /getConsoleLog
    ```

* Methods Supported (Currently):
    
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
    Others – N/A
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
    login,
    All other APIs are redirected to the login API,
    so they are not publicly exposed.
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
    N/A
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
    ```

* Sample URL Params:
    
    ```
    /set – key=flavor, value=’m1.tiny’
           key=image, value='cirros-0.3.4-x86_64-uec'
           key=vm_name, value=’Test_VM’
           key=net_name, value=’Test_Net’
           key=vm_create_confirm, value=’yes’
           key=vm_delete, value=’Test_VM’
           key=vm_delete_confirm, value=’yes’
           key=network_name, value=’Test_VM’
   	       key=subnet_name, value=’Test_Subnet’
 	       key=cidr, value=’10.10.2.0/24’
 	       key=network_create_confirm, value=’yes’
           key=network_delete, value=’Test_Net’
           key=network_delete_confirm, value=’yes’
  	       key=vm_delete_all, value=’yes’
           key=network_delete_all, value=’yes’
           key=type_of_deployment, value=’all-in-one’
   	       key=ipaddress_confirm, value=’192.168.9.13’
           key=deploy_confirm, value=’yes’
           key=cloud_clean_up, value=’yes’
    ```
   
[Conversation Corpus](https://github.com/shank7485/Assistant-for-Software-Defined-Infrastructure/blob/master/openstack-corpus/conversation.corpus.json)
    
    ```
    /chat -- The above (Conversation Corpus) link contains all the sample questions and answers which also form part of the initial dataset we need to feed the bot.
             Note: It would be impossible to reproduce the exact questions a user might ask.
    ```
    
* ConsoleScreen and getConsoleLog APIs output/description:
    
    ```
    These APIs are used for the deployment part of the project.
    We are using OpenStack-Ansible for deployment of OpenStack cloud.

    OpenStack-Ansible Deployment uses a combination of Ansible and Linux Containers (LXC) to install and manage OpenStack.
    Ansible provides an automation platform to simplify system and application deployment.
    Ansible manages systems using Secure Shell (SSH) instead of unique protocols that require remote daemons or agents.

    When the user clicks to get the Console logs from the chat screen,these are the four steps performed:
    1) Configuration
    2) Install and bootstrap Ansible
    3) Run playbooks (which are YAML files for orchestration)
    4) Install and Verify Services (This step is displayed on the screen)

    Some of the services which you can see being installed and verified can be categorized as:
    1) Infrastructure services:
        ♣	MariaDB with Galera
        ♣	RabbitMQ
        ♣	Memcached
        ♣	Load Balancer
        ♣	Utility container
        ♣	Log aggregation host
    2) OpenStack services:
        ♣	Block Storage (cinder)
        ♣	Compute (nova)
        ♣	Dashboard (horizon)
        ♣	Identity (keystone)
        ♣	Image (glance)
        ♣	Networking (neutron)
        ♣	Object Storage (swift)
        ♣	Orchestration (heat)
    ```

