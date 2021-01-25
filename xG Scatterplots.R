library(ggplot2)
library(ggpmisc)

setwd('C:/Users/nirgo/Documents/GitHub/Fantasy')

sgw_data <- read.csv('Final Data.csv')
cum_data <- read.csv('./Cumulative Merged Data/CMD_S21_GW_19.csv')

Encoding(cum_data$Player) <- 'UTF-8'

ggplot(data = sgw_data, aes(x = Player_xG, y = Goals.scored, color = Cost)) +
  geom_point() + 
  scale_color_gradient(low = 'orange', high = 'red') +
  stat_poly_eq(formula = y ~ x, parse = T)

# Cumulaive - xG vs. Goals scored
ggplot(data = cum_data, aes(x = Player_xG, y = Goals.scored)) +
  geom_text(data = cum_data, aes(label = Player, size = Goals.scored)) + 
  scale_size(range = c(1,4)) + 
  geom_smooth(method = 'lm') +
  stat_poly_eq(formula = y ~ x, parse = T) + 
  theme(legend.position = 'none')

# Cumulaive - xA vs. Assists
ggplot(data = cum_data, aes(x = Player_xA, y = Assists)) +
  geom_text(data = cum_data, aes(label = Player, size = Assists)) + 
  scale_size(range = c(1,4)) + 
  geom_smooth(method = 'lm') +
  stat_poly_eq(formula = y ~ x, parse = T) + 
  theme(legend.position = 'none')
