args = commandArgs(trailingOnly = TRUE)
#setwd('~/Dropbox/bionlp/');
data_filename = args[1];
num_clusters = as.numeric(args[2]);

data = read.table(data_filename,header=T);
rownames(data) = data$id;
titles = data$Title;
id = data$id;
authors = data$Authors;
places = data$Places;
data = data[,c(-1,-2,-3,-4)]
shared_tasks_idx = grep("(W09-14)|(W11-18)",id);

## KMEANS CLUSTERING
cl = kmeans(data, num_clusters, nstart = 25)
sink( paste(data_filename,num_clusters,'clusters_output.txt',sep="_"));
for (i in 1:num_clusters){
  cat ('cluster', i, '\n');
  print (sort(cl$centers[i,],T))
  print (titles[cl$cluster == i])
 # print (authors[cl$cluster == i])
 # print (places[cl$cluster == i])
}
sink();
