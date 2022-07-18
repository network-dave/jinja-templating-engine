import os
import glob

from flask import Flask, request, Response, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap5

from jinja2 import Environment, FileSystemLoader, meta


# The directory containing the Jinja2 templates
TEMPLATE_FOLDER = "templates"

# Initialize the Flask application
app = Flask(__name__)

# Needed for CSRF protection, else WTForms will not run 
app.config['SECRET_KEY'] = 'any secret string'

# Load Bootstrap files from local resources instead of CDN
app.config["BOOTSTRAP_SERVE_LOCAL"] = True

# Bootstrap the app using to Bootstrap-Flask
bootstrap = Bootstrap5(app)


@app.route("/", methods=["GET"])
def view_template_list():
    '''
    Display a list of all the available templates with some quick help.

    '''
    # Get all the Jinja2 files inside the templates folder
    template_list = glob.glob("*.j2", root_dir=TEMPLATE_FOLDER)

    # Remove the file extension to keep only the name of the template
    template_list = [ t.strip(".j2") for t in template_list ]

    return render_template("template_list.html", items=template_list, template_folder=TEMPLATE_FOLDER)


@app.route("/templates/<template_name>", methods=["GET", "POST"])
def template_engine(template_name: str):
    '''
    Display or render templates

    The template name and related Jinja2 file name are retrieved from the URL.
    Template files shoud use the .j2 extension by default.

    '''
    # Build the template filename from the URL endpoint
    template_file = template_name + ".j2"

    # Use the GET method to retrieve the raw template as plain text
    if request.method == "GET":

        # Load the actual data from the .j2 file inside the template folder
        with open(os.path.join(TEMPLATE_FOLDER, template_file)) as f:
            data = f.read()

        # Return the raw content of the template file as plain text
        return Response(data, mimetype="text/plain")

    # Use the POST method to render the template
    elif request.method == "POST":

        # If we receive the request as application/json we return JSON
        if request.content_type == "application/json":
            variables = request.get_json()
            return jsonify(result=render_template(template_file, **variables))
        # If we receive the request as application/x-www-for-urlencoded we return plain text
        elif request.content_type == "application/x-www-form-urlencoded":
            variables = request.form.to_dict()
            return Response(response=render_template(template_file, **variables), mimetype="text/plain")


@app.route("/forms/<template_name>", methods=["GET"])
def form_generator(template_name: str):
    '''
    Automatically generate a Bootstrapped web form from a Jinja2 template
    
    '''
    # Define a new class with an input field for each variable in the template
    class FormGenerator(FlaskForm):

        # Build the template filename from the URL endpoint
        template_file = template_name + ".j2"

        # Get all variables in the Jinja2 template (hacky...)
        env = Environment(loader=FileSystemLoader("./templates/"))
        template_source = env.loader.get_source(env, template_file)[0]
        parsed_content = env.parse(template_source)
        variables = meta.find_undeclared_variables(parsed_content)
    
        # For each variable in the template, generate an input field in the web form (sorted alphabetically)
        for v in sorted(variables):
            vars()[v] = StringField(v.capitalize())
            
        submit = SubmitField("Submit")

    # Create the form object to be rendered
    form = FormGenerator()

    return render_template("form.html", template_name=template_name.capitalize(), form=form)


if __name__ == "__main__":
    # Run the development server on port 80 when called directly
    app.run(debug=True,host="0.0.0.0", port="80")

