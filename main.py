#-------------------------------------------------------------------------
# Author: Nir Levanon, Daniel Pidtylok, Almog Asraf       
# Last updated: 24.11.2020
#-------------------------------------------------------------------------

# Import webapp2  - Python web framework compatible with Google App Engine
import webapp2
# Import Jinja and os libraries
import jinja2
import os

# Load Jinja
jinja_environment =jinja2.Environment(loader=
                                      jinja2.FileSystemLoader
                                     (os.path.dirname(__file__)))

# ---------------------------------------------------------
# Main page - show the group details and links to 3 pictures 
# Handles /
# --------------------------------------------------------
class MainPage(webapp2.RequestHandler):
    def get(self):
        # Create a template object
        main_page_template = jinja_environment.get_template('main_page.html')

        # Creating an HTML page and response
        # Send nothing
        self.response.write(main_page_template.render({'i_boolean_matrix': False }))

# -----------------------------------------
# Class to show the picture
# Handles /show_picture
# -----------------------------------------
class ShowPicture(webapp2.RequestHandler):
    def get(self):

        # Create an boolean matrix which will be send to main_page.html:
         # Matrix's size is defined accordingly to the input_size
         # "0" means False. In the html file, it will be interpreted to white color.
         # "1" means True. In the html file, it will be interpreted to black color.
         # Any else pix, will be interpreted as "1".
        def create_boolean_matrix (num_of_rows,num_of_coloums,input_pixs):
            lst_of_rows_binary=[]
            start = 0 
            end = num_of_coloums
            while start < len (input_pixs):
                single_row_binary = input_pixs[start:end]
                lst_of_rows_binary.append(single_row_binary)
                start = start + num_of_coloums
                end = end + num_of_coloums
            lst_of_rows_boolean=[]
            for row in lst_of_rows_binary:
                single_row_boolean = []
                for pix in row:
                    if pix == "0":
                        single_row_boolean.append(False)
                    else:
                        single_row_boolean.append(True)
                lst_of_rows_boolean.append(single_row_boolean)
            return lst_of_rows_boolean

        # Transform the input sixe to a list.
        # Accordingly, define the number of rows and coloums.
        input_size = self.request.get('size').split(",")
        num_of_rows = int(input_size[0])
        num_of_coloums = int(input_size[1])

        # transform the input pixs to a list.
        input_pixs = self.request.get('pixs').split(",")
        
        # Check the inputs:
         # If the input size fits to the input pixs - create the boolean matrix.
         # If the input size bigger than the input pixs:
          # First, complete the difference with "1" pix.
          # Then, Create the boolean matrix.
         # If the input size smaller than the input pixs - create the boolean matrix accordingly to input size.
        if num_of_rows*num_of_coloums == len (input_pixs):
            boolean_matrix = create_boolean_matrix(num_of_rows,num_of_coloums,input_pixs)
        elif num_of_rows*num_of_coloums > len (input_pixs):
            num_of_missing_pixs=int((num_of_rows*num_of_coloums)-len(input_pixs))
            for missing_pix in range (0,num_of_missing_pixs):
                input_pixs.append("1")
            boolean_matrix = create_boolean_matrix(num_of_rows,num_of_coloums,input_pixs)
        else:
            input_pixs_shorter = input_pixs[0:(num_of_rows*num_of_coloums)]
            boolean_matrix = create_boolean_matrix(num_of_rows,num_of_coloums,input_pixs_shorter)
            
        # Creating a dictionary - for template's input parameter pixs, we pass our "boolean_matrix" object
        parameters_for_template = {'i_boolean_matrix': boolean_matrix,
                                   'x': num_of_rows,
                                   'y': num_of_coloums,
                                   'len': len(boolean_matrix)}
            
        #Create a template object
        show_picture_template = jinja_environment.get_template('main_page.html')
            
        #Creating a HTML page and response
        self.response.write(show_picture_template.render(parameters_for_template))
	
# --------------------------------------------------
# Routing
# --------
# /             - shows the main page
# /show_picture - shows the picture
# --------------------------------------------------
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/show_picture', ShowPicture)],
                              debug=True)