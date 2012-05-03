args = commandArgs(trailingOnly = TRUE)
data = read.csv(args[1])
data2 = data[,2:4]
rownames(data2) = data$id
dmat = dist(data2)
hier = hclust(dmat)
clust = cutree(hier,args[3])
write(clust,args[2])