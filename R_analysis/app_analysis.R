# To answer questions about co-occurences of similar errors within same app

###### Import data by app
#error_by_app_old = read.csv("app_errors.csv")
## THERE IS AN APP NAMED net.ayudaporfavor.Love,"Love quotes""
all_nodes = read.table(file="app_6_1_2018.csv", header=TRUE,
                       quote="'\"", sep=",",
                       encoding="UTF-8", fill=FALSE)
all_nodes = all_nodes[all_nodes$num_nodes>0,]
write.csv(as.data.frame(table(all_nodes$category)),"all_nodes_cat_count.csv")


apps_without_talkback_nodes = read.table(file="app_6_1_2018.csv", header=TRUE,
                            quote="'\"", sep=",",
                            encoding="UTF-8", fill=FALSE)
nrow(apps_without_talkback_nodes[apps_without_talkback_nodes$num_nodes>0 & apps_without_talkback_nodes$num_talkback_nodes==0,])
nrow(apps_without_talkback_nodes[apps_without_talkback_nodes$num_nodes>0,])
apps_without_talkback_nodes = (apps_without_talkback_nodes[apps_without_talkback_nodes$num_nodes>0 & apps_without_talkback_nodes$num_talkback_nodes==0,])



error_by_app = read.table(file="error_by_app.csv", header=TRUE,
                                                  quote="'\"", sep=",",
                          encoding="UTF-8", fill=FALSE)
#error_by_app = read.table(file="by_app_size_fix.csv", header=TRUE,
#                          quote="'\"", sep=",",
#                        encoding="UTF-8", fill=FALSE)
error_by_app = read.table(file="app_recalc.csv", header=TRUE,
                          quote="'\"", sep=",",
                          encoding="UTF-8", fill=FALSE)
error_by_app = read.table(file="app_drop_package.csv", header=TRUE,
                          quote="'\"", sep=",",
                          encoding="UTF-8", fill=FALSE)
error_by_app = read.table(file="app_6_1_2018.csv", header=TRUE,
                          quote="'\"", sep=",",
                          encoding="UTF-8", fill=FALSE)
View(error_by_app)
View(error_by_app[error_by_app$num_talkback_nodes==0,])
# attempt to remove apps that have only null views as estimated by having no nodes at all

error_by_app = error_by_app[error_by_app$num_nodes>0,]
View(error_by_app)
num_apps = nrow(error_by_app)
num_apps

#isolate apps that have no focusable elements but have at least one valid element
apps_without_talkback_nodes = error_by_app[error_by_app$num_talkback_nodes ==0,]

# remove apps without talkback focusable elements for remaining tests
error_by_app=error_by_app[error_by_app$num_talkback_nodes > 0,] ## need to make sure this is correct!

error_by_app$percent_and = error_by_app$num_talkback_android_default/error_by_app$num_talkback_nodes
error_by_app$percent_not_and = 1- error_by_app$percent_and


## prep data
error_by_app$num_downloads = factor(error_by_app$num_downloads, 
                  levels=c("None", "  100 - 500  ","  500 - 1,000  ","  1,000 - 5,000  ","  5,000 - 10,000  ",
                           "  10,000 - 50,000  ","  50,000 - 100,000  ","  100,000 - 500,000  ",
                           "  500,000 - 1,000,000  ","  1,000,000 - 5,000,000  ",
                          "  5,000,000 - 10,000,000  ","  10,000,000 - 50,000,000  ",
                          "  50,000,000 - 100,000,000  ","  100,000,000 - 500,000,000  ",
                          "  500,000,000 - 1,000,000,000  ","  1,000,000,000 - 5,000,000,000  "),
                  ordered=TRUE)


error_by_app$date_updated = as.Date(error_by_app$date_updated, "%B %d, %Y")

# set all as numeric
error_by_app$rating = as.numeric(paste(error_by_app$rating))
error_by_app$num_ratings = as.numeric(error_by_app$num_ratings)
error_by_app$Num_Missing_Speakable_Text_Per_Node[error_by_app$Num_Missing_Speakable_Text_Per_Node=='na'] <- NaN # is done by coeersion automatically in next step
error_by_app$Num_Missing_Speakable_Text_Per_Node = as.numeric(paste(error_by_app$Num_Missing_Speakable_Text_Per_Node))
error_by_app$Num_Not_Wide_Enough_Per_Node = as.numeric(paste(error_by_app$Num_Not_Wide_Enough_Per_Node))
error_by_app$Num_Not_Tall_Enough_Per_Node = as.numeric(paste(error_by_app$Num_Not_Tall_Enough_Per_Node))
error_by_app$Num_Editable_Textview_Cont_Desc_Per_Node = as.numeric(paste(error_by_app$Num_Editable_Textview_Cont_Desc_Per_Node))
error_by_app$Num_Fully_Overlapping_Clickable_Per_Node = as.numeric(paste(error_by_app$Num_Fully_Overlapping_Clickable_Per_Node))
error_by_app$Num_Clickable_Duplicate_Text_Per_Node = as.numeric(paste(error_by_app$Num_Clickable_Duplicate_Text_Per_Node))
error_by_app$Num_Non_Clickable_Duplicate_Text_Per_Node = as.numeric(paste(error_by_app$Num_Non_Clickable_Duplicate_Text_Per_Node))
error_by_app$Num_Redundant_Description_Per_Node = as.numeric(paste(error_by_app$Num_Redundant_Description_Per_Node))


summary(error_by_app)

#########3 Import data by node
#node = read.csv("all_node.csv")
#node = read.csv("by_node_size_fix.csv")
node = read.csv("node_drop_package.csv", encoding="UTF-8")
node = read.table(file="node_drop_package.csv", header=TRUE,
                  quote="'\"", sep=",",
                  encoding="UTF-8", fill=FALSE, skipNul=T)

## Prep data
node$Num_Nodes_Overlap_With = as.numeric(node$Num_Nodes_Overlap_With)
node$Num_Nodes_Share_Label = as.numeric(node$Num_Nodes_Share_Label)

node$android_widget = as.factor(node$android_widget)
View(node)
##############################################################
## Dist of percent of elements with error per app

hist(error_by_app$percent_not_and,
     xlab="Percent of Nodes with Error", ylab="Number of Apps",
     main="Not Android Default"
     )


# histogram of each error in percentage form
hist(error_by_app$Num_Missing_Speakable_Text_Per_Node, 
     xlab="Percent of Nodes with Error", ylab="Number of Apps", 
     main = "Missing Speakable Text", labels=TRUE, ylim=c(0,8000), xlim=c(0,1))
nrow(error_by_app[!is.na(error_by_app$Num_Missing_Speakable_Text_Per_Node),])
nrow(error_by_app[error_by_app$Num_Missing_Speakable_Text_Per_Node==0,])

hist(error_by_app$Num_Not_Wide_Enough_Per_Node, 
     xlab="Percent of Nodes with Error", ylab="Number of Apps", 
     main = "Not Wide Enough", labels=TRUE, ylim=c(0,10000), xlim=c(0,1))
hist(error_by_app$Num_Not_Tall_Enough_Per_Node,  ylim=c(0,10000), xlim=c(0,1),
     labels=TRUE,
     xlab="Percent of Nodes with Error", ylab="Number of Apps", 
     main = "Not Tall Enough")
nrow(error_by_app[!is.na(error_by_app$Num_Not_Tall_Enough_Per_Node),])

hist(error_by_app$Num_Editable_Textview_Cont_Desc_Per_Node, breaks=20,
     xlab="Percent of Nodes with Error", ylab="Number of Apps", 
     main = "Editable Textview with Content Desc", labels=T)
nrow(error_by_app[!is.na(error_by_app$Num_Clickable_Duplicate_Text_Per_Node),])

hist(error_by_app$Num_Fully_Overlapping_Clickable_Per_Node,
     xlab="Percent of Nodes with Error", ylab="Number of Apps", 
     main = "Fully Overlapping Clickable", labels=T)
hist(error_by_app$Num_Clickable_Duplicate_Text_Per_Node,
     xlab="Percent of Nodes with Error", ylab="Number of Apps", 
     main = "Duplicate Text on Clickable", labels=T, ylim=c(0,8000))
nrow(error_by_app[!is.na(error_by_app$Num_Clickable_Duplicate_Text_Per_Node),])

hist(error_by_app$Num_Non_Clickable_Duplicate_Text_Per_Node,
     xlab="Percent of Nodes with Error", ylab="Number of Apps", 
     main = "Duplicate Text on Non-Clickable", labels=T, ylim=c(0,8000))
nrow(error_by_app[!is.na(error_by_app$Num_Non_Clickable_Duplicate_Text_Per_Node),])

hist(error_by_app$Num_Redundant_Description_Per_Node, breaks=20,
     xlab="Percent of Nodes with Error", ylab="Number of Apps", 
     main = "Redundant Description", labels=T)
hist(error_by_app[error_by_app$Num_Redundant_Description_Per_Node>0,]$Num_Redundant_Description_Per_Node)

###################################
############ Android Widgets
plot(error_by_app$rating, error_by_app$percent_not_and)
View(error_by_app[,c("Num_Redundant_Description_Per_Node","Num_Not_Tall_Enough_Per_Node","percent_not_and")])


################## Num not tall enough
View(error_by_app[error_by_app$Num_Not_Tall_Enough_Per_Node==1,])
hist(error_by_app[error_by_app$Num_Not_Tall_Enough_Per_Node>0.05 & error_by_app$Num_Not_Tall_Enough_Per_Node <0.2,]$Num_Not_Tall_Enough_Per_Node)
nrow(error_by_app[error_by_app$Num_Not_Tall_Enough_Per_Node>0.05 & error_by_app$Num_Not_Tall_Enough_Per_Node <0.2,])
## the small drop doesn't seem to have to do with rating
hist(error_by_app[error_by_app$Num_Not_Tall_Enough_Per_Node>0.05 & error_by_app$Num_Not_Tall_Enough_Per_Node <0.2,]$rating)
hist(error_by_app[ error_by_app$Num_Not_Tall_Enough_Per_Node >=0.2,]$rating)

# looks at node class composition of apps with and within the blip, 
summary(error_by_app$Num_Not_Tall_Enough_Per_Node)
#compare 1sst quartile to the upper half
#Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's 
# 0.0000  0.1394  0.2727  0.3082  0.4506  1.0000     342 
hist(error_by_app[error_by_app$Num_Not_Tall_Enough_Per_Node>0.1394 & error_by_app$Num_Not_Tall_Enough_Per_Node <0.2727,]$Num_Not_Tall_Enough_Per_Node)
hist(error_by_app[error_by_app$Num_Not_Tall_Enough_Per_Node>=0.2727,]$Num_Not_Tall_Enough_Per_Node)
hist(error_by_app[error_by_app$Num_Not_Tall_Enough_Per_Node>0.05& error_by_app$Num_Not_Tall_Enough_Per_Node <0.4,]$Num_Not_Tall_Enough_Per_Node)
nrow(error_by_app[error_by_app$Num_Not_Tall_Enough_Per_Node>0.05 & error_by_app$Num_Not_Tall_Enough_Per_Node <0.2,])

tall_by_app = error_by_app[,c("app_id","Num_Not_Tall_Enough_Per_Node")]
View(tall_by_app)
for (i in 1:nrow(tall_by_app)){
if(is.na(tall_by_app$Num_Not_Tall_Enough_Per_Node[i]) |tall_by_app$Num_Not_Tall_Enough_Per_Node[i]<0.1394){tall_by_app$blip[i] =NA} 
  else if(tall_by_app$Num_Not_Tall_Enough_Per_Node[i]>=0.2727){tall_by_app$blip[i]=FALSE}else{tall_by_app$blip[i]=TRUE}
}

tall_node = node[,1:5]
View(tall_node)
tall_node = merge(tall_by_app, tall_node, SORT=FALSE, by="app_id")
View(tall_node)
View(table(tall_node[tall_node$blip==TRUE,]$class))


########### Speakble Text Missing
View(error_by_app)
View(error_by_app[,c("app_id","Num_Missing_Speakable_Text_Per_Node","Num_Redundant_Description_Per_Node")])

################################################################
##################### Coorelation b/t error and rating
plot(error_by_app$category, error_by_app$Num_Missing_Speakable_Text_Per_Node, 
     xlab = "App Category", ylab="Percent Elements with Missing Speakable Text")
plot(error_by_app$rating, error_by_app$Num_Missing_Speakable_Text_Per_Node, 
     xlab = "Rating", ylab="Percent Elements with Missing Speakable Text")
plot(error_by_app$rating ~ error_by_app$Num_Missing_Speakable_Text_Per_Node)
plot(error_by_app$percent_not_and, error_by_app$Num_Missing_Speakable_Text_Per_Node, 
     xlab = "Percent Not Android", ylab="Percent Elements with Missing Speakable Text")

cor(error_by_app[,c("rating","Num_Missing_Speakable_Text_Per_Node")],use = "complete.obs")

library(corrplot)
(names(error_by_app))
View(error_by_app)
corr_vars = error_by_app[,c("date_updated","category","num_ratings","rating","Num_Missing_Speakable_Text_Per_Node",
                            "Num_Not_Wide_Enough_Per_Node","Num_Not_Tall_Enough_Per_Node","Num_Editable_Textview_Cont_Desc_Per_Node",
                            "Num_Fully_Overlapping_Clickable_Per_Node","Num_Non_Clickable_Duplicate_Text_Per_Node","Num_Redundant_Description_Per_Node" )] 
M<-cor(corr_vars[,5:11],use = "complete.obs") 
View(M)
library(corrplot)
corrplot(M, method="circle")

library(car)
scatterplotMatrix(corr_vars)

#####################################
############## ImageButton and FAB cooccurance of missing speakable text


#### NOT CORRECT
temp = node[node$class=="android.support.design.widget.FloatingActionButton" | node$class=="android.widget.ImageButton",c("app_id","class","node_id","Speakable_Text_Present")]
temp = merge(temp[temp$class=="android.support.design.widget.FloatingActionButton", c("app_id","class","Speakable_Text_Present")],temp[temp$class=="android.widget.ImageButton", c("app_id","class","Speakable_Text_Present")], by="app_id")
temp = rename(temp, c("Speakable_Text_Present.x"="FAB.Speak_Text_Pres", "Speakable_Text_Present.y"="ImgBn.Speak_Text_Pres"))

View(temp)
ImgBn_FAB_ba = as.data.frame(table(temp$FAB.Speak_Text_Pres,temp$ImgBn.Speak_Text_Pres, dnn=list("FAB.Speak_Text_Pres","ImgBn.Speak_Text_Pres")))
View(ImgBn_FAB_ba)

############################
##### Ads vs Not




#################################
############ Unfocusable apps
###############
#### Unfocusable apps
##
nrow(apps_without_talkback_nodes)
write.csv(apps_without_talkback_nodes[floor(runif(10, min=0, max=nrow(apps_without_talkback_nodes)+1)),], "Sample_Unfocusable_Apps.csv")
write.csv(apps_without_talkback_nodes, "without_tb_nodes.csv")
write.csv(as.data.frame(table(apps_without_talkback_nodes$category)),"unfocusable_apps_category.csv")
plot(apps_without_talkback_nodes$num_downloads)
plot(apps_without_talkback_nodes$category)
plot(error_by_app$num_downloads)
plot(error_by_app$category)
