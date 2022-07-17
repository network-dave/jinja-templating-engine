# Jinja Templating Engine

## About 

The Jinja Templating Engine is a REST API developped in Flask that permit quick rendering of Jinja2 templates through a simple API call.

You can also browse to the Templating Engine's URL to display a web page listing all available templates, with the possibility to view the raw template files.

The goal of this project is to provide a microservice / API to quickly render Jinja2 templates without depending on any specific web front-end (I'm a network engineer and I use this to render network device configurations from data coming from web forms).



## Getting started

### Build and run the Docker image

Clone the repository from GitHub and then build the Docker image:
```
git clone <url>
cd jinja-templating-engine
docker build -t jinja-templating-engin:latest .
docker run jinja-templating-engine
```

In this case you will need to mount your local directory containe your Jinja2 templates as a volume to the container's /app/templates directory.

### Run the Python code locally

Alternatively, you can run the app directly through Python3 and the Flask library: 
```
git clone <url>
pip3 install flask
python3 app.py
```
In this case you can directly copy your templates to the `templates/` directory. 



## Usage

### REST API

To render a template, send a POST request to `http://hostname[:port]/templates/<template-name>`, with the variables to be rendered as either `application/json` or `application/x-www-form-urlencoded` data. Specify the type of data inside the request's headers' `content-type` field.

Send JSON will return a JSON object with a singe key:value pair, the key being `result` and the value being a string containing the rendered template. 

Example:

```JSON
{
    "result": "This string contains your rendered template data\nCheers!"
}
```
Sending form data will return the rendered template as plain text.

You can also send a GET request to the API endpoint to retrieve the raw template in plain text.

### Web GUI

Browse to `http://hostname[:port]/` to display the homepage, which will list the available Jinja2 templates (all .j2 files located inside the `templates/` folder).

### Automatic web form generator

For each template you can use the automatic form generator at `http://hostname/forms/<template-name>`.

Caveat: at the time of this writing, the variables' input fields are ordered alphabetically instead of following the order the variables appear in the template.


## License

Licensed under the GPL v3 License - see LICENSE.md for more information.

© 2022 David Paneels - dpaneels@protonmail.com