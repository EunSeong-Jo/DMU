library(arules)
data(Adult)
Adult

str(Adult)
head(as(Adult, 'data.frame'))

rules <- apriori(Adult)
inspect(head(rules))

adult.rules <- apriori(Adult, parameter=list(support=0.1, confidence=0.6),
                       appearance=list(rhs=c('income=small', 'income=large'),
                                       default='lhs'),
                       control=list(verbose=F))
adult.rules.sorted <- sort(adult.rules, by='lift')
inspect(head(adult.rules.sorted))
inspect(head(adult.rules.sorted, n=20))

library(arulesViz)
plot(adult.rules.sorted, method="scatterplot")
plot(adult.rules.sorted, method='graph', control=list(type='items', alpha=0.5))
