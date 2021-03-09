# Loading libraries
library(ggplot2)
library(ggpmisc)
library(gridExtra)
library(formattable)
library(dplyr)
library(tidyr)

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


##################################        sINGLE GAMEWEEK        ##################################


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


####################################         CUMULATIVE         ####################################


# Cumulative - xG vs. Goals scored
ggplot(data = cum_data[which(cum_data$Role != 'GKP'),],
       aes(x = Player_xG, y = Goals.scored)) +
    geom_text(data = cum_data[which(cum_data$Role != 'GKP'),],
              aes(label = Player, size = Goals.scored, colour=Role)) + 
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
    theme(legend.title.align = 0.5) 

# Export plot
ggsave(filename = 'xG_Goals_Cum.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)



# Cumulative - xG vs. Goals scored - by role
ggplot(data = cum_data[which(cum_data$Role != 'GKP'),],
       aes(x = Player_xG, y = Goals.scored)) +
  geom_text(data = cum_data[which(cum_data$Role != 'GKP'),],
            aes(label = Player, size = Goals.scored, colour=Role)) + 
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


####################################         R SQUARED         ####################################


# Define a function that return R2 for each model
rsq <- function(x, y) summary(lm(y~x))$r.squared

# Dataframe to append the each r2
r2_df <- data.frame('GW' = c(5:25))

# Iterate different roles
for (role in c('ALL', 'DEF', 'MID', 'FWD')) {
  
  # Empty vector to append R square values
  r2_vec <- c()
  
  # Itertating through gameweeks
  for (gw in c(5:25)){
    
    # Load data
    players_path <- paste('Data/Cumulative Merged Data/CMD_S21_GW_', as.character(gw), '.csv',
                          sep = '')
    data <- read.csv(players_path)
    
    # R2 cacluation and append
    if (role == 'ALL'){
      r2 <- rsq(data$Player_xG,
                data$Goals.scored)
    }
    else {
      r2 <- rsq(data[which(data$Role == role), 'Player_xG'],
                data[which(data$Role == role), 'Goals.scored'])
    }
    r2_vec <- append(r2_vec, r2)
  }
  
  # Add column to the R2 dataframe
  r2_df[[role]] <- r2_vec
}

# All Players R2 Plot
ggplot(data = r2_df, aes(x = GW, y = ALL)) + 
  geom_point() + 
  geom_line() + 
  geom_smooth(method = 'lm',
              formula = y ~ sqrt(x),
              se = F) + 
  xlab('Gameweek') + 
  ylab('R Squared')

# Export plot
ggsave(filename = 'R2_Plot.png',
       path = './Visualizations',
       width = 8,
       height = 4.46666)

# Transform R2 dataframe to long format
r2_df <- pivot_longer(r2_df %>% select(-ALL),
                      !GW,
                      names_to = 'Role',
                      values_to = 'R2')

# Set roles as factor
r2_df$Role <- factor(r2_df$Role, levels = c('DEF',
                                            'MID',
                                            'FWD'))

# Plot
ggplot(data = r2_df,
       aes(x = GW, y = R2)) + 
  geom_point(aes(colour = Role)) + 
  geom_line(aes(colour = Role)) + 
  geom_smooth(method = 'lm',
              formula = y ~ sqrt(x),
              se = F,
              colour = 'black') + 
  xlab('Gameweek') +
  ylab('R Squared') + 
  theme(legend.position = 'none') +
  facet_wrap(~ Role)

# Export Plot
ggsave(filename = 'R2_Role.png',
       path = './Visualizations',
       width = 8,
       height = 3.5)


####################################         OPPORTUNITIES SEIZURE         ####################################


# Compute xG-Goals model residuals, indicating which players are best in seizing opportunities
xG_reg <- lm(Goals.scored ~ Player_xG, data = cum_data[cum_data$Player_xG >= 0,])
cum_data$Seizure <- xG_reg$residuals
cum_data$Predicted <- predict(xG_reg)
seizure_df <- cum_data[order(cum_data$Seizure), c('Player', 'Seizure')]

best_scorer <- cum_data[cum_data$Seizure == max(cum_data$Seizure), 'Player']
worst_scorer <- cum_data[cum_data$Seizure == min(cum_data$Seizure), 'Player']


# + 

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



