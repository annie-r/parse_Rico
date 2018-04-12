## By Nodes
library(plyr) #ddply, rename
library(tidyr) # create wide data table

###########


##################
################ node data prep
## something weird going on with the nulls
node = read.table(file="image_node.csv", header=TRUE,
                  quote="'\"", sep=",",
                  encoding="UTF-8", fill=FALSE, skipNul=T)
node = read.table(file="node_drop_package.csv", header=TRUE,
                      quote="'\"", sep=",",
                      encoding="UTF-8", fill=FALSE, skipNul=T)
# convert to R NULL's
node[node=="na"] <- NA
node$X = NULL

node$Num_Nodes_Overlap_With = as.numeric(as.character(node$Num_Nodes_Overlap_With))
node$Num_Nodes_Share_Label = as.numeric(as.character(node$Num_Nodes_Share_Label))

node$android_widget = as.factor(node$android_widget)


## prep data



##################### of interest for shared label
node_of_interest = node[(node$class=="android.widget.ImageButton" | (node$class=="android.widget.ImageView" & node$is_clickable=="True") | node$class=="android.support.design.widget.FloatingActionButton"),]


####################### Investigating the labels themselves
#View(node_of_interest[node_of_interest$app_id=="com.pantech.app.vegaremoteshot",]) ?? why is it blank but not empty
labels_tab = unique(node_of_interest[,c("app_id","label")])
labels_freqs = as.data.frame(table(unique(node_of_interest[,c("app_id","label")])$label))
labels_freqs = rename(labels_freqs, c("Var1"="label", "Freq"="num_apps"))
# if it's not in any apps, it shouldn't be in the list. I don't know why it's there in the first place
labels_freqs = labels_freqs[labels_freqs$num_apps>0,]
View(labels_freqs)

unique_apps = as.data.frame(unique(node_of_interest$app_id))
unique_apps = rename(unique_apps, c("unique(node_of_interest$app_id)"="app_id"))
View(unique_apps)
total_num_apps = nrow(unique_apps)
total_num_apps

##### Looking for most common (across apps) labels that get repeated
tmp = unique(node_of_interest[node_of_interest$Num_Nodes_Share_Label >0 &
                                node_of_interest$Num_Nodes_Share_Label != node_of_interest$Num_Nodes_Overlap_With,
                              c("app_id","label")])
tmp2 = as.data.frame(table(tmp$label))
## order by freq. freq being the number of apps this appears in as a duplicate label
View(table(tmp$label))

#################
########## error by app
#########################

#####################################
######## by app


by_app_of_interest = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="False" | node_of_interest$Speakable_Text_Present=="True" ,c("app_id","Speakable_Text_Present")]$app_id))

View(by_app_of_interest)
by_app_of_interest = rename(by_app_of_interest, c("Var1"="app_id", "Freq"="total_elements_of_interest"))
#remove those with no elements of interest, I don't know how they got back in
by_app_of_interest = by_app_of_interest[by_app_of_interest$total_elements_of_interest >0,]

####
### sp text
tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="False",c("app_id","Speakable_Text_Present")]$app_id))
View(tmp)
tmp = rename(tmp, c("Var1"="app_id", "Freq"="missing_speakable_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")


by_app_of_interest$percent_missing_speakable_text =(by_app_of_interest$missing_speakable_text/by_app_of_interest$total_elements_of_interest)



###### by class

###
########### data prep
## image View
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageView" & 
                                             ( node_of_interest$Speakable_Text_Present=="False" | node_of_interest$Speakable_Text_Present=="True"),
                                            c("app_id","Speakable_Text_Present")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_view_total_sp_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageView" & 
                                             node_of_interest$Speakable_Text_Present=="False",
                                           c("app_id","Speakable_Text_Present")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_view_missing_speakable_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

by_app_of_interest$prop_image_view_missing_speakable_text =(by_app_of_interest$image_view_missing_speakable_text/by_app_of_interest$image_view_total_sp_text)

## image button
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageButton" & 
                                             ( node_of_interest$Speakable_Text_Present=="False" | node_of_interest$Speakable_Text_Present=="True"),
                                           c("app_id","Speakable_Text_Present")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_button_total_sp_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageButton" & 
                                             node_of_interest$Speakable_Text_Present=="False",
                                           c("app_id","Speakable_Text_Present")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_button_missing_speakable_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

by_app_of_interest$prop_image_btn_missing_speakable_text =(by_app_of_interest$image_button_missing_speakable_text/by_app_of_interest$image_button_total_sp_text)

## FAB
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.support.design.widget.FloatingActionButton" & 
                                             ( node_of_interest$Speakable_Text_Present=="False" | node_of_interest$Speakable_Text_Present=="True"),
                                           c("app_id","Speakable_Text_Present")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="FAB_total_sp_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.support.design.widget.FloatingActionButton" & 
                                             node_of_interest$Speakable_Text_Present=="False",
                                           c("app_id","Speakable_Text_Present")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="FAB_missing_speakable_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

by_app_of_interest$prop_FAB_missing_speakable_text =(by_app_of_interest$FAB_missing_speakable_text/by_app_of_interest$FAB_total_sp_text)


View(by_app_of_interest)
#######################################



### correlation of co-occurence
## same app, same error, different class
plot(by_app_of_interest$prop_image_view_missing_speakable_text, by_app_of_interest$prop_image_btn_missing_speakable_text,
     xlab="Proportion Image Views Missing Speakable Text",
     ylab = "Proportion Image Buttons Missing Speakable Text",
     main="Occurence of Error in Same App over Different Classes")

plot(by_app_of_interest$prop_image_view_missing_speakable_text, by_app_of_interest$prop_FAB_missing_speakable_text,
     xlab="Proportion Image Views Missing Speakable Text",
     ylab = "Proportion FAB Missing Speakable Text",
     main="Occurence of Error in Same App over Different Classes")
sum(!is.nan(by_app_of_interest$prop_image_view_missing_speakable_text)
    & !is.nan(by_app_of_interest$prop_FAB_missing_speakable_text))

plot(by_app_of_interest$prop_image_btn_missing_speakable_text, by_app_of_interest$prop_FAB_missing_speakable_text,
     xlab="Proportion Image Buttons Missing Speakable Text",
     ylab = "Proportion FAB Missing Speakable Text",
     main="Occurence of Error in Same App over Different Classes")
sum(!is.nan(by_app_of_interest$prop_image_btn_missing_speakable_text)
                         & !is.nan(by_app_of_interest$prop_FAB_missing_speakable_text))

plot(by_app_of_interest$prop_image_btn_missing_speakable_text, 
     by_app_of_interest$prop_FAB_missing_speakable_text,
     xlab="Proportion Image Buttons Missing Speakable Text",
     ylab = "Proportion FAB Missing Speakable Text",
     main="Occurence of Error in Same App over Different Classes" )
cor(by_app_of_interest$prop_image_btn_missing_speakable_text, 
    by_app_of_interest$prop_FAB_missing_speakable_text, use="pairwise.complete.obs",
    method="spearman")
library(car)
scatterplot(prop_image_btn_missing_speakable_text~prop_FAB_missing_speakable_text, data=by_app_of_interest)
apps_w_FAB_and_img_btn = nrow(by_app_of_interest[by_app_of_interest$FAB_total_sp_text > 0 & by_app_of_interest$image_button_total_sp_text >0,])
apps_w_FAB_and_img_btn


#############
## unhelpful label

unhelpful_labels = c("[image]", "image", "Image","Image Des", "alt image", "image description", "image description default", "Icon",
                    "button", "Button", "contentDescription","desc","Desc","Description","Description Image")
ifelse()

#####
### duplicate label


####### histograms
bin.width = 0.025
hist(by_app_of_interest$percent_missing_speakable_text, 
     xlab="Percent of Elements of Interest with Error", ylab="Number of Apps", 
     main = "Missing Speakable Text", labels=TRUE, ylim=c(0,2500),
     breaks=seq(0,1,by=bin.width))

hist(by_app_of_interest$percent_error, 
     xlab="Percent of Elements of Interest with Error", ylab="Number of Apps", 
     main = "Missing Speakable Text", labels=TRUE, ylim=c(0,2500),
     breaks=seq(0,1,by=bin.width))



#############################
########## co-occurence

miss_label_by_class = as.data.frame(table(node_of_interest[node_of_interest,c("app_id","Speakable_Text_Present")]))



error_by_class=as.data.frame(table(node_of_interest$class))
error_by_class = rename(error_by_class, c("Var1"="class","Freq"="num_elements"))
error_by_class = error_by_class[error_by_class$num_elements > 0,]

tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present == "False",]$class))
tmp = rename(tmp, c("Var1"="class","Freq"="num_missing_sp_text"))

error_by_class = merge(error_by_class,tmp, by="class")

error_by_class$prop_missing_text = error_by_class$num_missing_sp_text/error_by_class$num_elements

tmp = as.data.frame(table(unique(node_of_interest[,c("app_id","class")])$class))
View(tmp)

View(error_by_class)













#
