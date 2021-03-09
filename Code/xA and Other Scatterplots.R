# Loading libraries
library(ggplot2)
library(ggpmisc)
library(gridExtra)
library(formattable)
library(dplyr)

# setting working directory
setwd('C:/Users/nirgo/Documents/GitHub/Fantasy')

# Loading data. SGW - Single Game Week (i.e, not cumulative). CUM - cumulative data until GW 19.
sgw_data <- read.csv('Data/Final Data.csv')
cum_data <- read.csv('Data/Cumulative Merged Data/CMD_S21_GW_25.csv')

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

sgw_data$Role <- factor(sgw_data$Role, levels = c('GKP',
                                                  'DEF',
                                                  'MID',
                                                  'FWD'))

# Drop NAs
cum_data <- cum_data[!is.na(cum_data$Goals.scored),]
cum_data <- cum_data[!is.na(cum_data$Player_xG),]

sgw_data <- sgw_data[!is.na(sgw_data$Goals.scored),]
sgw_data <- sgw_data[!is.na(sgw_data$Player_xG),]


# Cumulative - xA vs. Assists
ggplot(data = cum_data[which(cum_data$Role != 'GKP'),], aes(x = Player_xA, y = Assists)) +
  geom_text(data = cum_data[which(cum_data$Role != 'GKP'),], aes(label = Player, size = Assists)) + 
  scale_size(range = c(1, 3.5)) + 
  geom_smooth(method = 'lm') +
  stat_poly_eq(formula = y ~ x, parse = T, size = 5) + 
  theme(legend.position = 'none') +
  scale_x_continuous(name = 'xA') + 
  scale_y_continuous(name = 'Assists') + 
  facet_wrap(~ Role, scales = 'free')

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


