## About
This project scrapes the official Fantasy Premier League stats, and advanced soccer stats (such as xG) about teams and players from Understat.com. In addition, it merges data from these two sources into, and uploads it to a Heroku PostgreSQL database directly from Python.

## Motivation
This data is very valuable for better understanding of the English Premier League, the Fantasy game and most importantly - soccer in general.

## Some Application Examples
### *Seizing goaling opportunities?*
Which are the players who makes the maximum from their goaling opportunities? This question is of great interest for football managers, and rightly so. Luckily, the development of the xG stat made this pretty easy. For each goaling opportunity the xG returns a number between 0 to 1, representing the probability to score. And so, by comparing the xG of each player to his actual goals scored, we can get a solid quantitative value for this metric by subtracting the xG from the Goals made. Another way used here is to plot the two variables. The more a player is above the regression line the better he is in seizing opportnities, and on the contrary. From this plot (data due to GW19) we can learn, for example, the Heung Min Son and Kevin De-Bruyne - two of the best players in the EPL - have about the same goaling opportunities, but Son uses those much much efficiently than De-Bruyne. 

<p align="center">
  <img src="/Visualizations/xG_Goals.png" width="600"/>
</p>

### *who are the players with the best value in the Fantasy game?*

<p align="center">
  <img src="/Visualizations/Cost_Pts.png" width="600"/>
</p>

### *are xG and xA stats good predictors?*
xG (expected goals) is an advanced soccer stat produced by training deep learning models on goaling opportunities that became very popular in the last years.  (and the same goes for xA for Assists). But are these stats really good in predicting the number of goals and assists of a player in a given game? let's check this question by examining a scatterplot of the xG stats and the actual goals scored, and the correlation between them.
