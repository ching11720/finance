# load data
data = read.table("data2.csv", h=T, sep=",")
data = read.csv("data2.csv")
# check varaible names
colnames(data)

## Correlation Coefficient & Test
cor(data$average, data$A, method = "pearson")

## Correlation test
cor.test(data$average, data$A, method = "pearson")
