# YoutubeParty
https://party.cosinic.com/

# Requirements
You should have Docker installed and configured correctly (i.e. creating and connecting to machines functions correctly)

# Building/Deploying
`deploy.sh` should build and deploy YoutubeParty for you. To access/verify that it is running, you can check [localhost:8080](http://localhost:8080) (the web app) or [localhost:8081](http://localhost:8081) (adminer page). If you installed Docker using Docker Toolbox for Windows, note that you will have to replace `localhost` with the IP address of the VirtualBox machine (e.g. `192.168.99.100`)

# Deploying on Server
Before this, you must have a github ssh key pair within your user account. It's found in  `~/.ssh/`.  
Run these commands to pull and restart the server with newest commits.  
First, `cd /home/daven/youtube-party` in order to get to the right place.  
Then run the following:  

> git pull
> sudo systemctl stop ytparty  

Then wait for it to be done. If it hangs, press Ctrl+C and move to next step.  

> sudo systemctl start ytparty
