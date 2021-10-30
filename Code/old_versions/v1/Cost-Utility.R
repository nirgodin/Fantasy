# Loading libraries
library(ggplot2)
library(ggpmisc)
library(gridExtra)
library(formattable)
library(dplyr)
library(tidyr)
library(sparkline)

# setting working directory
setwd('C:/Users/nirgo/Documents/GitHub/Fantasy')

# Import data
data <- read.csv('Data/Final Data.csv')

# Changing encoding for R doesn't catch well some of the latin players' names 
Encoding(data$Player) <- 'UTF-8'

# Drop duplicates
data <- data %>% distinct()
data <- data[!duplicated(data %>% select(Player, Gameweek)),]

# Transform Sel. column to numeric
data$Sel. <- sapply(data$Sel., function(x) sub('%', '', x) %>% as.numeric())

# Change role factors for legend visualizations
data$Role <- factor(data$Role, levels = c('GKP',
                                          'DEF',
                                          'MID',
                                          'FWD'))


##################################        COST-UTILITY ANALYSIS        ##################################


# Transform data to wide format
wide <- data %>% 
  select(Player,
         Role,
         Gameweek,
         Cost,
         Pts.) %>% 
  pivot_wider(id_cols = c(Player, Role),
              names_from = Gameweek,
              values_from = c(Pts., Cost))

# Remove rows with more than 50% NA
wide <- wide[which(rowMeans(!is.na(wide)) > 0.5), ]

# Calculate average points per gameweek
wide$pts_mean <- apply(wide[grepl('Pts', names(wide))], 1, function (x) mean(x, na.rm = T))

# Calculate average cost per gameweek
wide$cost_mean <- apply(wide[grepl('Cost', names(wide))], 1, function (x) mean(x, na.rm = T))

# Compute xG-Goals model residuals, indicating which players are best in seizing opportunities
cost_utility_reg <- lm(pts_mean ~ cost_mean, data = wide)
wide$value <- cost_utility_reg$residuals
wide$value <- wide$value %>% round(2)

# Cost vs. Points plot
ggplot(data = wide,
       aes(x = cost_mean, y = pts_mean)) +
  geom_text(data = wide,
            aes(label = Player, size = pts_mean, colour = Role)) + 
  scale_size(range = c(1, 3.5)) +  
  geom_smooth(data = wide,
              aes(x = cost_mean, y = pts_mean),
              method = 'lm',
              formula = y ~ x,
              se = F,
              colour = 'black') +
  stat_poly_eq(formula = y ~ x,
               parse = T,
               size = 5) + 
  scale_x_continuous(name = 'Cost') + 
  scale_y_continuous(name = 'Points') +
  guides(size = F) +
  theme(legend.title.align = 0.5) #+ 
#  facet_wrap(~ Role, scales = 'free')


##################################        STABILITY ANALYSIS        ##################################


# Calculate points standard deviaton
wide$std <- apply(wide[grepl('Pts', names(wide))], 1, function (x) sd(x, na.rm = T)*(-1))

# Calculate player stability, by passing standard deviation to MinMaxScaler
wide$stability <- normalize(wide$std, na.rm = T) %>% round(2)

# Pass to new dataframe and drop irrelevant columns
stab_df <- wide %>% select(Player,
                           pts_mean,
                           stability,
                           value)

# Drop players with low amount of points per game
stab_df <- stab_df[which(stab_df$pts_mean > 3),]

# Order by stability
stab_df <- stab_df[order(-stab_df$stability), ]

# Change colnames
colnames(stab_df) <- c('Player',
                       'Points Per Game',
                       'Stability',
                       'Value')

# Round Points per game column
stab_df$`Points Per Game` <- stab_df$`Points Per Game` %>% round(2)

# Pass the results to formattable
formattable(stab_df,
            align = c("l", rep("c", ncol(stab_df) - 1)),
            list(`Player` = formatter("span", style = ~ style(color = "grey", font.weight = "bold")),
                 `Points Per Game` = color_tile("#DeF7E9", "#71CA97"),
                 `Stability` = color_tile("#B1CBEB", "#3E7DCC"),
                 `Value` = color_tile("#FA614B66", "#FA614B"))
            )


# Stability vs. Points plot
ggplot(data = wide,
       aes(x = pts_mean, y = stability)) +
  geom_text(data = wide,
            aes(label = Player, colour = Role), size = 3) + 
  # scale_size(range = c(1, 3.5)) +  
  stat_smooth(data = wide,
              geom = 'line',
              size = 0.7,
              alpha = 0.9,
              aes(x = pts_mean, y = stability),
              method = 'lm',
              formula = y ~ x,
              se = F,
              colour = 'black') +
  stat_poly_eq(formula = y ~ x,
               parse = T,
               size = 3.5,
               label.x.npc = 0.98) + 
  scale_x_continuous(name = 'Points') + 
  scale_y_continuous(name = 'Stability') +
  guides(size = F) +
  theme(legend.title.align = 0.5) + 
  facet_wrap(~ Role, scales = 'free')

# Points vs. Value plot
ggplot(data = wide,
       aes(x = pts_mean, y = value)) +
  geom_text(data = wide,
            aes(label = Player, colour = Role), size = 3) + 
  stat_smooth(data = wide,
              geom = 'line',
              size = 0.7,
              alpha = 0.9,
              aes(x = pts_mean, y = value),
              method = 'lm',
              formula = y ~ x,
              se = F,
              colour = 'black') +
  stat_poly_eq(formula = y ~ x,
               parse = T,
               size = 3.5,
               label.x.npc = 0.98) + 
  scale_x_continuous(name = 'Points') + 
  scale_y_continuous(name = 'Value') +
  guides(size = F) +
  theme(legend.title.align = 0.5) + 
  facet_wrap(~ Role, scales = 'free')
