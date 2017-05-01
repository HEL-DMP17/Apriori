# install.packages("arules")
# install.packages("arulesViz")
# install.packages("visNetwork")
# install.packages("igraph")

library("arules")
library("arulesViz")
library("visNetwork")
library("igraph")

# Change this, because this is .... R
setwd("C:/Users/eozer/Documents/GitHub/Apriori")

rules <- read.PMML("pmml_rules.xml")
rules <- head(sort(rules, by="lift"), 50)


ig <- plot( rules, method="graph", control=list(type="items") )

# let's bypass saveAsGraph and just use our igraph
ig_df <- get.data.frame( ig, what = "both" )
nodez = data.frame(
    id = ig_df$vertices$name
    ,value = ig_df$vertices$support # could change to lift or confidence
    ,title = ifelse(ig_df$vertices$label == "",ig_df$vertices$name, ig_df$vertices$label)
    ,ig_df$vertices
)

# Interactive assoc rule network
visNetwork(
    nodes = nodez
    , edges = ig_df$edges,  main = "First 50 association rule network sorted by lift",
    width = "100%", height = "700px"
) %>% 
    visIgraphLayout() %>%
    visEdges(shadow = FALSE,
             arrows =list(to = list(enabled = TRUE, scaleFactor = 2)),
             color = list(color = "lightblue", highlight = "red")) %>%
    visOptions(highlightNearest = list(enabled = T, hover = F),
               nodesIdSelection = TRUE) %>% 
    visInteraction(navigationButtons = TRUE)
# Interactive table
inspectDT(rules)

# Interactive scatter plot
plotly_arules(rules)

