## About
This project scrapes the official Fantasy Premier League stats, and advanced soccer stats (such as xG) about teams and players from Understat.com. In addition, it merges the data from the two sources, and uploads the data to a Heroku PostgreSQL database directly from Python.

## Motivation
This data is very valuable for better understanding of the English Premier League, the Fantasy game and most important - soccer in general.

## Some Application Examples
### *are xG and xA stats good predictors?*
xG (expected goals) is an advanced soccer stat produced by training deep learning models on goaling opportunities that became very popular in the last years. For each goaling opportunity the xG returns a number between 0 to 1, representing the probability to score (and the same goes for xA for Assists). But are these stats really good in predicting the number of goals and assists of a player in a given game? let's check this question by examining a scatterplot of the xG stats and the actual goals scored, and the correlation between them.

<p align="center">
  <img src="/Visualizations/xG_Goals.png" width="600"/>
</p>

<p align="center">
  <img src="/Visualizations/xA_Assists.png" width="600"/>
</p>

### *who are the best players in seizing goaling opportunities?*
