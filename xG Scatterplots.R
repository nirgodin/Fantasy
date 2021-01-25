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

# Cumulative - xG vs. Goals scored
ggplot(data = cum_data, aes(x = Player_xG, y = Goals.scored)) +
  geom_text(data = cum_data, aes(label = Player, size = Goals.scored)) + 
  scale_size(range = c(1,4)) + 
  geom_smooth(method = 'lm') +
  stat_poly_eq(formula = y ~ x, parse = T, size = 5) + 
  theme(legend.position = 'none') +
  scale_x_continuous(name = 'xG', limits = c(0,12.5), breaks = seq(0, 13, 2)) + 
  scale_y_continuous(name = 'Goals Scored', limits = c(0,13), breaks = seq(0, 13, 2))

# Export plot
ggsave(filename = 'xG_Goals.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)

# Cumulative - xA vs. Assists
ggplot(data = cum_data, aes(x = Player_xA, y = Assists)) +
  geom_text(data = cum_data, aes(label = Player, size = Assists)) + 
  scale_size(range = c(1,4)) + 
  geom_smooth(method = 'lm') +
  stat_poly_eq(formula = y ~ x, parse = T, size = 5) + 
  theme(legend.position = 'none') +
  scale_x_continuous(name = 'xA', limits = c(0,8), breaks = seq(0, 8, 2)) + 
  scale_y_continuous(name = 'Assists', limits = c(0,11), breaks = seq(0, 11, 2))

# Export plot
ggsave(filename = 'xA_Assists.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)

