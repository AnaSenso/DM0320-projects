# The best palce to grow (mongo_project)
![Foto](https://github.com/AnaSenso/mongo_project/blob/master/input/mongo-project.png)


## Description
The location of the compani is one of the most important factor to make it success. So it needs to be choosen very carefuly.

Altought being in a hot centre to develop the company is quite important the most important thing is to have happy employess this si why we focus on that employee survey select the best place to locat ethe office. and those are their suggestions:
- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not to far.
- Account managers need to travel a lot
- All people in the company have between 25 and 40 years, give them some place to go to party.
- Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.
- The CEO is Vegan


## Project description:

1. The first thin I did is to ponderate the suggestions base on the impact tht it would have in the company. This si ithe selection of the most revelant conditions:
    - Companies more than 10-year-old more than 2km ratio (affects 100% of the employees)
    - Bar to party (100%)
    - School nearby (30%)
    - Airport in the city (23%)
    - Starbucks near by (23%) 

2. Taking the companies database as baseline I cleaned is to keep just the plces that have a valid address anf oundation year.

3. After that I selected the best places based on the conditions siggested by the employees:
    - Select companies that were founden less than 10 years ago and compare then with the group of companies founded more than 10 years ago to get the conditon: *Companies more than 10-year-old more than 2km ratio (affects 100% of the employees)*
    - Use the google maps api to select the place tha thave a bar near by and remove the one tha tode not have it: *Bar to party (100%)*
    - Select places that have an elementary school in 1km ratio. I cchoose elementary school because all aemployees are young (between 30 to 40 years) and their kids are probably also young: *School nearby (30%)*
    - Usin gthe same Google maps api, select place that have a Starbuck quite close (50 metres). This is an importan condition to keep happy the executives: *tarbucks near by (23%)*
    - Finally we want to be in a city that has an airport, becuase the account managers need to travel a lot. So I comared all the cities of the resultant data frame with a dtabase tha thas all the airports inthe world. 

4. the resultant data frame contains the best locations base on this conditiosn to start searching for an office.


## Suggestion for future projects:
- I took the companies database to start working with someting, but in a given case we can subtitute is for a database of available plces to rent 