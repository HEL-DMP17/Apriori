install.packages("arules")
install.packages("arulesViz")
install.packages("visNetwork")
install.packages("igraph")
library("arules")
library("arulesViz")
library("visNetwork")
library("igraph")

# TODO: get it relative path
setwd("C:/Users/eozer/Documents/GitHub/Apriori")
rules <- read.PMML("pmml_rules.xml")

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
    , edges = ig_df$edges,  main = "ARule Network", width = "100%"
) %>% 
    visEdges(shadow = FALSE,
             arrows =list(to = list(enabled = TRUE, scaleFactor = 2)),
             color = list(color = "lightblue", highlight = "red")) %>%
    visOptions( highlightNearest = T, nodesIdSelection = TRUE)

# Interactive table
inspectDT(rules)

# Interactive scatter plot
plotly_arules(rules)
