# In this file we'll create some visualizations that are more easily produced in R than Python

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

# Single GW - xG vs. Goals scored
ggplot(data = sgw_data[which(sgw_data$Player_xG >= 0),],
       aes(x = Player_xG, y = Goals.scored)) +
  geom_point() + 
  geom_smooth(method = 'lm', se = F) +
  stat_poly_eq(formula = y ~ x, parse = T, size = 5) + 
  scale_x_continuous(name = 'xG') +
  scale_y_continuous(name = 'Goals Scored')

# Export plot
ggsave(filename = 'xG_Goals_SGW.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)

# Single GW - xG vs. Goals scored - by role
ggplot(data = sgw_data[which(sgw_data$Player_xG >= 0 & sgw_data$Role != 'GKP'),],
       aes(x = Player_xG, y = Goals.scored)) +
  geom_point(aes(colour = Role)) + 
  geom_smooth(method = 'lm', se = F, colour = 'black') +
  stat_poly_eq(formula = y ~ x, parse = T, size = 4) + 
  scale_x_continuous(name = 'xG') +
  scale_y_continuous(name = 'Goals Scored') + 
  facet_wrap(~ Role, scales = 'free') + 
  theme(legend.position = 'none')

# Export plot
ggsave(filename = 'xG_Goals_Role_SGW.png',
       path = './Visualizations',
       width = 8,
       height = 3.5)

# Compute xG-Goals model residuals, indicating which players are best in seizing opportunities
xG_reg <- lm(Goals.scored ~ Player_xG, data = cum_data[cum_data$Player_xG >= 0,])
cum_data$Seizure <- xG_reg$residuals
cum_data$Predicted <- predict(xG_reg)
seizure_df <- cum_data[order(cum_data$Seizure), c('Player', 'Seizure')]

best_scorer <- cum_data[cum_data$Seizure == max(cum_data$Seizure), 'Player']
worst_scorer <- cum_data[cum_data$Seizure == min(cum_data$Seizure), 'Player']


# Cumulative - xG vs. Goals scored
ggplot(data = cum_data[which(cum_data$Role != 'GKP'),],
       aes(x = Player_xG, y = Goals.scored)) +

    geom_text(data = cum_data[which(cum_data$Role != 'GKP'),], aes(label = Player, size = Goals.scored, colour=Role)) + 

    scale_size(range = c(1, 3.5)) +  

    geom_smooth(data = cum_data[which(cum_data$Role != 'GKP'),],
              aes(x = Player_xG, y = Goals.scored),
              method = 'lm',
              formula = y ~ x,
              se = F,
              colour = 'black') +

    stat_poly_eq(formula = y ~ x,
               parse = T,
               size = 5) + 

    scale_x_continuous(name = 'xG') + 
    scale_y_continuous(name = 'Goals Scored') +
    guides(size = F) +
  theme(legend.title.align = 0.5) # + 

  # geom_segment(aes(x = cum_data[Player == best_scorer, 'Player_xG'],
  #                  xend = cum_data[Player == best_scorer, 'Player_xG'],
  #                  y = cum_data[Player == best_scorer, 'Goals.scored'],
  #                  yend = cum_data[Player == best_scorer, 'Predicted']),
  #              linetype = 'dashed',
  #              color = 'red') + 
  # geom_segment(aes(x = cum_data[Player == worst_scorer, 'Player_xG'],
  #                  xend = cum_data[Player == worst_scorer, 'Player_xG'],
  #                  y = cum_data[Player == worst_scorer, 'Goals.scored'],
  #                  yend = cum_data[Player == worst_scorer, 'Predicted']),
  #              linetype = 'dashed',
  #              color = 'black') # + 
  # facet_wrap(~ Role, scales = 'free')

# Export plot
ggsave(filename = 'xG_Goals_Cum.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)


# Cumulative - xG vs. Goals scored - by role
ggplot(data = cum_data[which(cum_data$Role != 'GKP'),],
       aes(x = Player_xG, y = Goals.scored)) +
  
  geom_text(data = cum_data[which(cum_data$Role != 'GKP'),], aes(label = Player, size = Goals.scored, colour=Role)) + 
  
  scale_size(range = c(1.5, 3)) +  
  
  geom_smooth(data = cum_data[which(cum_data$Role != 'GKP'),],
              aes(x = Player_xG, y = Goals.scored),
              method = 'lm',
              formula = y ~ x,
              se = F,
              colour = 'black') +
  
  stat_poly_eq(formula = y ~ x,
               parse = T,
               size = 3.5) + 
  
  scale_x_continuous(name = 'xG') + 
  scale_y_continuous(name = 'Goals Scored') +
  guides(size = F) +
  theme(legend.position = 'none') + 
  facet_wrap(~ Role, scales = 'free')

# Export plot
ggsave(filename = 'xG_Goals_Role_Cum.png',
       path = './Visualizations',
       width = 8,
       height = 3.5)

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

rsq <- function(x, y) summary(lm(y~x))$r.squared
res <- function(x, y) summary(lm(y~x))$residuals

# Empty vectors for R2
def_r2_vec <- c()
mid_r2_vec <- c()
fwd_r2_vec <- c()

teams_r2_vec <- c()


for (gw in c(5:25)){
  
  # Players
  
  # Load data
  players_path <- paste('Data/Cumulative Merged Data/CMD_S21_GW_', as.character(gw), '.csv',
                        sep = '')
  data <- read.csv(players_path)
  
  # R2 cacluation and append
  def_r2 <- rsq(data[which(data$Role == 'DEF'), 'Player_xG'], data[which(data$Role == 'DEF'), 'Goals.scored'])
  mid_r2 <- rsq(data[which(data$Role == 'MID'), 'Player_xG'], data[which(data$Role == 'MID'), 'Goals.scored'])
  fwd_r2 <- rsq(data[which(data$Role == 'FWD'), 'Player_xG'], data[which(data$Role == 'FWD'), 'Goals.scored'])
  
  def_r2_vec <- append(def_r2_vec, def_r2)
  mid_r2_vec <- append(mid_r2_vec, mid_r2)
  fwd_r2_vec <- append(fwd_r2_vec, fwd_r2)
  
  
  # Teams
  
  # Load data
  teams_path <- paste('Data/PLT/PLT_S21_GW1_', as.character(gw), '.csv',
                        sep = '')
  data <- read.csv(teams_path)

  # R2 cacluation and append
  teams_r2 <- rsq(data$Team_xG, data$Team_G)
  teams_r2_vec <- append(teams_r2_vec, teams_r2)

}

df <- data.frame('GW' = c(5:25),
                 'DEF R2' = def_r2_vec,
                 'MID R2' = mid_r2_vec,
                 'FWD R2' = fwd_r2_vec,
                 'Teams R2' = teams_r2_vec)

# Defenders R2
def <- ggplot(data = df, aes(x = GW, y = DEF.R2)) + 
        geom_point(colour = '#F8766D') + 
        geom_line(alpha = 0.5, colour = '#F8766D') + 
        geom_smooth(method = 'lm',
                    formula = y ~ sqrt(x),
                    se = F,
                    colour = 'black') + 
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(), 
        plot.title = element_text(hjust = 0.5, size = 10)) +
  ggtitle('DEF') +
  scale_y_continuous(limits = c(0.28, 0.92))


# Midfielders R2
mid <- ggplot(data = df, aes(x = GW, y = MID.R2)) + 
  geom_point(colour = '#7CAE00') + 
  geom_line(alpha = 0.5, colour = '#7CAE00') + 
  geom_smooth(method = 'lm',
              formula = y ~ sqrt(x),
              se = F,
              colour = 'black') + 
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        plot.title = element_text(hjust = 0.5, size = 10)) +
  ggtitle('MID') +
  scale_y_continuous(limits = c(0.28, 0.92))


# Forwards R2
fwd <- ggplot(data = df, aes(x = GW, y = FWD.R2)) + 
  geom_point(colour = '#00BFC4') + 
  geom_line(alpha = 0.5,
            colour = '#00BFC4') + 
  geom_smooth(method = 'lm',
              formula = y ~ sqrt(x),
              se = F,
              colour = 'black') + 
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        plot.title = element_text(hjust = 0.5, size = 10)) +
  ggtitle('FWD') +
  scale_y_continuous(limits = c(0.28, 0.92))

# Grid Arrange
R2_Role_Plot <- grid.arrange(def, mid, fwd,
                             ncol = 3,
                             left = 'R Squared',
                             bottom = 'Gameweek')

# Export Plot
ggsave(plot = R2_Role_Plot,
       filename = 'R2_Role.png',
       path = './Visualizations',
       width = 8,
       height = 3.5)

