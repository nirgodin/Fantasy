# In this file we'll create some visualizations that are more easily produced in R than Python

# Loading libraries
library(ggplot2)
library(ggpmisc)
library(formattable)
library(dplyr)

# setting working directory
setwd('C:/Users/nirgo/Documents/GitHub/Fantasy/Data')

# Loading data. SGW - Single Game Week (i.e, not cumulative). CUM - cumulative data until GW 19.
sgw_data <- read.csv('Final Data.csv')
cum_data <- read.csv('./Cumulative Merged Data/CMD_S21_GW_24.csv')

# Changing encoding for R doesn't catch well some of the latin players' names 
Encoding(cum_data$Player) <- 'UTF-8'
Encoding(sgw_data$Player) <- 'UTF-8'

# Drop duplicates
sgw_data <- sgw_data %>% distinct()
cum_data <- cum_data %>% distinct()

# Transform Sel. column to numeric
cum_data$Sel. <- unlist(lapply(cum_data$Sel., function(x) sub('%', '', x) %>% as.numeric()))

# Change role factors for legend visualizations
cum_data$Role <- factor(cum_data$Role, levels = c('GKP',
                                                  'DEF',
                                                  'MID',
                                                  'FWD'))

# Single GW - xG vs. Goals scored
ggplot(data = sgw_data[sgw_data$Player_xG >= 0,], aes(x = Player_xG, y = Goals.scored)) +
  geom_point() + 
  geom_smooth() +
  stat_poly_eq(formula = y ~ x, parse = T, size = 5) + 
  scale_x_continuous(name = 'xG', limits = c(0,2.5), breaks = seq(0, 3, 1)) + 
  scale_y_continuous(name = 'Goals Scored', limits = c(0,4), breaks = seq(0, 3, 1))

# Export plot
ggsave(filename = 'xG_Goals_SGW.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)

# Cumulative - xG vs. Goals scored
ggplot(data = cum_data, aes(x = Player_xG, y = Goals.scored)) +
  geom_text(data = cum_data, aes(label = Player, size = Goals.scored, colour=Role)) + 
  scale_size(range = c(1,4)) + 
  geom_smooth(method = 'lm') +
  stat_poly_eq(formula = y ~ x, parse = T, size = 5) + 
  scale_x_continuous(name = 'xG', limits = c(0,12), breaks = seq(0, 12, 2)) + 
  # scale_y_continuous(name = 'Goals Scored', limits = c(0,13), breaks = seq(0, 13, 2)) + 
  guides(size = F)

# Export plot
ggsave(filename = 'xG_Goals.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)

# Compute xG-Goals model residuals, indicating which players are best in seizing opportunities
xG_reg <- lm(Player_xG ~ Goals.scored, data = cum_data)
cum_data$Seizure <- xG_reg$residuals

seizure_df <- cum_data[order(cum_data$Seizure),c('Player', 'Seizure')]

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

# Cumulative - Cost vs. Points
ggplot(data = cum_data, aes(x = Cost, y = Pts.)) +
  geom_text(data = cum_data[cum_data$Pts. > 25,], aes(label = Player, size = Cost, colour = Role)) + 
  scale_size(range = c(1,4)) + 
  geom_smooth(method = 'lm') +
  stat_poly_eq(formula = y ~ x, parse = T, size = 5) + 
  scale_x_continuous(name = 'Cost', limits = c(4,12.5), breaks = seq(4, 13, 2)) + 
  scale_y_continuous(limits = c(20,150), breaks = seq(20, 150, 20)) +
  guides(size = F)

# Export plot
ggsave(filename = 'Cost_Pts.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)

# Compute Cost-Pts. linear model residuals
cost_pts_reg <- lm(Pts. ~ Cost, data = cum_data)
cum_data$cp_resid <- cost_pts_reg$residuals

# Plot value against selected
ggplot(data = cum_data, aes(x = cp_resid, y = Sel.)) + 
  geom_text(data = cum_data[cum_data$Pts. > 25,], aes(label = Player, colour = Role), size = 3) +
  geom_smooth() + 
  facet_wrap(~ Role, scales = 'free')
  # stat_poly_eq(formula = y ~ x, parse = T, size = 5) + 
  # scale_x_continuous(name = 'Cost', limits = c(4,12.5), breaks = seq(4, 13, 2)) + 
  # scale_y_continuous(limits = c(20,150), breaks = seq(20, 150, 20)) +
  # guides(size = F)
