# predicting_beer_styles

**Ensemble gradient boosted decision tree and random forest model that categorizes beers by style in a flask app**

1.  beer_style_formatting
    - cleans and formats data to create style categories
2.  beer_style_psql
    - loads data to PostgreSQL and join beer table to style table
3.  beer_EDA
    - exploratory data analysis that selects styles for model build-out
4.  beer_models
    - creates individual supervised learning models for each style
5.  beer_model_tuning_random_forest
    - tunes parameters on random forest model, visualizes output using graphviz
6.  beer_model_tuning_gradient_boosting
    - tunes parameters on gradient boosted decision tree model, visualizes output using graphviz
7.  beer_ensembling
    - combines random forest and gradien boosted decision trees using voting classifier to increase adjusted r-squared
