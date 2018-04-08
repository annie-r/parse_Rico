rat = read.csv("rating.csv",header=FALSE)
rat_with_neg = read.csv("rating.csv",header=FALSE)
summary(rat)
# -1 is for unrated apps
rat[rat == -1] <- NA
plot(rat)
hist(rat$V1)
rat$V1 = as.numeric(rat$V1)
rat_with_neg = as.numeric(rat_with_neg$V1)
hist(rat_with_neg)
View(rat_with_neg)
boxplot(rat)
boxplot(rat_with_neg)
