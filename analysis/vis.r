install.packages("arules")
install.packages("arulesViz")
library("arules")
library("arulesViz")

# TODO: get it relative path
setwd("C:/Users/eozer/Documents/GitHub/Apriori")
rules <- read.PMML("pmml_rules.xml")

inspect(rules[1])

inspectDT(rules)
plotly_arules(rules)
plot(rules2,method="graph",interactive=TRUE,shading=NA)