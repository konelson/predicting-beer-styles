from flask import Flask, request, render_template
from py_beer_flask import beer_style

# create a flask object
app = Flask(__name__)

# creates an association between the / page and the entry_page function (defaults to GET)
@app.route('/')
def entry_page():
    return render_template('index.html')

# creates an association between the /predict_recipe page and the render_message function
# (includes POST requests which allow users to enter in data via form)
@app.route('/predict_recipe/', methods=['GET', 'POST'])
def render_message():

    # user-entered ingredients
    ingredients = ['size', 'og', 'fg', 'abv','ibu',
                   'color', 'boilsize', 'boiltime',
                   'boilgravity', 'efficiency', 'allgrain', 'biab', 'partialmash', 'extract']
    '''
    # error messages to ensure correct units of measure
    messages = ["The amount of flour must be in cups.",
                "The amount of milk must be in cups.",
                "The amount of sugar must be in cups.",
                "The amount of butter must be in cups.",
                "You must enter a number of eggs.",
                "The amount of baking powder must be in teaspoons.",
                "The amount of vanilla must be in teaspoons.",
                "The amount of salt must be in teaspoons.",
                "nine",
                "ten"
                ]
    '''
    # hold all amounts as floats
    amounts = []
    
    # takes user input and ensures it can be turned into a floats 
    #doing error check to make sure entered info is a float
    
    for i, ing in enumerate(ingredients):
        user_input = request.form[ing]
        float_ingredient = user_input
        #try:
            
            #float_ingredient = user_input
        #except:
         #   return render_template('index.html', message=messages[i])
        print('amounts', amounts)
        amounts.append(float_ingredient)
    
    # show user final message
    final_message = beer_style(amounts)
    return render_template('index.html', message=final_message)

if __name__ == '__main__':
    app.run(debug=True)