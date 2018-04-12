# electrovcs
A frontend interface and backend visualization service for climate data visualization



# TODO

### backend

* /vis/list: GET -> get the list of the users visualizations including defaults
* /vis/list: POST -> create a new visualization folder, with the included string as a python script
* /viz/run: POST -> run the requested vis
* /viz/show/?name= : GET -> return the image associated with the given viz name

### frontend

* Setup react project
* Authenticate with django-pam
* more stuff

#### How to run the frontend
* cd into the frontend folder
* run `npm install`
* run `npm run dev` (This will bundle up the jsx files and watch the files)
* In a new terminal window run `npm start` this will open the electron app using the bundled files
