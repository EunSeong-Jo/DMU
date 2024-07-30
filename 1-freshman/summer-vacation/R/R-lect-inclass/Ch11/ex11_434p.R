library(boot)
head(survival)
cor(survival$dose,survival$surv)

model <- lm(surv~dose, data=survival)
model

pred <- predict(model, survival['dose'])
pred

MAE <- sum(abs(pred-survival$surv))/nrow(survival)
MAE
