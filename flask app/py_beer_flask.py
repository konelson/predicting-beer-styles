import pickle
import pandas as pd
import numpy as np

# read in the model
beer_model = pickle.load(open("ensemble_model.pickle","rb"))
#mc_model = model_info['muffin_cupcake_model']

# create a function to take in user-entered amounts and apply the model
def beer_style(amounts_float, model=beer_model):
    
    # put everything in terms of tablespoons
    # flour, milk, sugar, butter, eggs, baking powder, vanilla, salt
   
   
    #multipliers = [16, 16, 16, 16, 3, .33, .33, .33]
    
    # sum up the total values to get the total number of tablespoons in the batter
    #total = np.dot(multipliers, amounts_float)

    # note the proportion of flour and sugar
    #flour_cups_prop = multipliers[0] * amounts_float[0] * 100.0 / total
    #sugar_cups_prop = multipliers[2] * amounts_float[2] * 100.0 / total

    # inputs into the model
    #input_df = [[flour_cups_prop, sugar_cups_prop]]
    
    

    if amounts_float[10] in ['yes', 'Yes']:
        amounts_float[10] = 1
    else:
        amounts_float[10] = 0

    if amounts_float[11] in ['yes', 'Yes']:
        amounts_float[11] = 1
    else:
        amounts_float[11] = 0

    if amounts_float[12] in ['yes', 'Yes']:
        amounts_float[12] = 1
    else:
        amounts_float[12] = 0

    if amounts_float[13] in ['yes', 'Yes']:
        amounts_float[13] = 1
    else:
        amounts_float[13] = 0
    


    input_df = [amounts_float] #could say amounts_float[0] to select features want to use


    # make a prediction
    prediction = beer_model.predict(input_df)[0]

    # return a message
    message_array = ["You are brewing an IPA!",
                     "You are brewing a Lager!",
                     "You are brewing a Stout!",
                     "You are brewing a Porter!",
                     "You are brewing a Saison!",
                     "You are brewing a Kolsch!",
                     "You are brewing an Ale!",
                     "You are brewing an APA!",
                     "You are brewing a Wheat!",
                     "You are brewing a Pilsner!",]

    return message_array[prediction]
