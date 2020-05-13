# What should I watch next? (data-analysis-pipeline)
![Foto](https://github.com/AnaSenso/data-analysis-pipeline/blob/master/input/tv-show-recommendations.png)

## Description
Do yo know that feeling when you finished that amazing tv show? like when you saw the last episode of 'The Sopranos', or when you reached the end od Big Bang Theory.

This program is meant to recomend you series based on your preferences your standards and will tell you what day of the week ant what hor and in wich network you ca see it. 

You need to add the genere and the minimum imdb score of the show that you want to see next. 

On top of that, and just to be coucious tof howm musch time do we spen watching TV, the program gives the number of hours that you will spend watching it.

## Project description:
Given a data base of the best rated tvs shows in imdb, the program will return a suggestion of them based on a genre and a minimum raiting.

1. Clean the data bese in the file ../src/data.py
   - Drop usless colmuns
   - Create columns for all generes

2. Fill the data base with te info form the API in ../input/data.py
   - Get the API url of every tv show form the show tittle in the dataframe
   - Create a anew data fram with info form the API:
     - Number of episodes
     - Time, Day and Network were you can see the show
   (the API measures takes many shows with similar titles, but the most acurated one is the first, this is why the item [0] is selected always)
   - Create a new column with the number of hours invested in whatching every show

3. Clean the resultant dataframe in the file ../src/data2.py

4. Create the file ../src/main.py that will return all the tv shows with the following parameters in a data frame and the average of time that will take you to watch them

## Bibliography:
- Data base: https://www.kaggle.com/ezzaldin6/tv-shows-dataset
- API: https://www.tvmaze.com/api#show-main-information