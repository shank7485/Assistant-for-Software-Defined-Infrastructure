api.wsgi:
/home/ubuntu/Assistant-for-Software-Defined-Infrastructure/
   api.wsgi
   
   api.wsgi:
   ```
    #!/usr/bin/python

    import sys
    sys.path.insert(0, '/home/ubuntu/Assistant-for-Software-Defined-Infrastructure/')

    from api import app as application
   ```

Apache conf:
/etc/apache2/sites-available/
  assistant.conf
  
  assistant.conf:
  ```
    <VirtualHost *:80>
	    ServerName localhost
	    ServerAdmin ubuntu@localhost
	    WSGIScriptAlias / /home/ubuntu/Assistant-for-Software-Defined-Infrastructure/api.wsgi
	    <Directory /home/ubuntu/Assistant-for-Software-Defined-Infrastructure/>
		      Require all granted
	    </Directory>
	    ErrorLog ${APACHE_LOG_DIR}/error.log
	    LogLevel warn
	    CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    
    <VirtualHost *:443>
        ServerName localhost
        ServerAdmin ubuntu@localhost
        WSGIScriptAlias / /home/ubuntu/Assistant-for-Software-Defined-Infrastructure/api.wsgi
        <Directory /home/ubuntu/Assistant-for-Software-Defined-Infrastructure/>
		      Require all granted
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined

	SSLEngine on
        SSLCertificateFile /etc/apache2/ssl/apache.crt
        SSLCertificateKeyFile /etc/apache2/ssl/apache.key

     </VirtualHost>
   ```
   
   default-ssl.conf
   ```
   	<IfModule mod_ssl.c>
    		<VirtualHost _default_:443>
        		ServerAdmin ubuntu@localhost
        		ServerName localhost
       			ServerAlias localhost
        		DocumentRoot /home/ubuntu/Assistant-for-Software-Defined-Infrastructure/
        		ErrorLog ${APACHE_LOG_DIR}/error.log
        		CustomLog ${APACHE_LOG_DIR}/access.log combined
        		SSLEngine on
        		SSLCertificateFile /etc/apache2/ssl/apache.crt
        		SSLCertificateKeyFile /etc/apache2/ssl/apache.key
        		<FilesMatch "\.(cgi|shtml|phtml|php)$">
                        	SSLOptions +StdEnvVars
        		</FilesMatch>
        		<Directory /usr/lib/cgi-bin>
                        	SSLOptions +StdEnvVars
        		</Directory>
        		BrowserMatch "MSIE [2-6]" \
                        	nokeepalive ssl-unclean-shutdown \
                        	downgrade-1.0 force-response-1.0
        		BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown
     		</VirtualHost>
    </IfModule>
```

Update Ubuntu repos.
```
sudo apt-get update
```

Install Apache and enable mod_wsgi.
```
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi python-dev
sudo a2enmod wsgi
```

Clone Assistant repo.
```
cd /home/ubuntu/
git clone https://github.com/shank7485/Assistant-for-Software-Defined-Infrastructure.git
```

Copy api.wsgi contents into api.wsgi file.
```
sudo vi /home/ubuntu/Assistant-for-Software-Defined-Infrastructure/api.wsgi
```

Copy assistant.conf contents into assistant.conf.
```
sudo vi /etc/apache2/sites-available/assistant.conf
```

Enable site.
```
sudo a2ensite assistant
```

Restart Apache.
```
sudo /etc/init.d/apache2 restart
```

Enable SSL and restart.
```
sudo a2enmod ssl
sudo service apache2 restart
/etc/init.d/apache2 restart
```
Make directory for SSL keys and certs. 
## This is for testing purposes ONLY. For actual deployment, operator needs to certs/keys.
```
sudo mkdir /etc/apache2/ssl
# Generate Cert and Keys. (test keys)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt
```

Copy from reference default-ssl.conf
```
sudo vi /etc/apache2/sites-available/default-ssl.conf
sudo a2ensite default-ssl.conf
```

Restart Apache.
```
sudo /etc/init.d/apache2 restart
```

The new HTTPS endpoint can be seen by heading to <IP_address>:443 and HTTP at <IP_address>:80.
