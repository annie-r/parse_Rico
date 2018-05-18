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

## don't use for counts, just info
app_info = read.table(file="app_recalc.csv", header=TRUE,
                      quote="'\"", sep=",",
                      encoding="UTF-8", fill=FALSE, skipNul=T)

app_info = app_info[,1:7]
View(app_info)
app_info[app_info$num_downloads=="None",]$num_downloads = NA
app_info$num_downloads = factor(app_info$num_downloads, 
                                    levels=c("  100 - 500  ","  500 - 1,000  ","  1,000 - 5,000  ","  5,000 - 10,000  ",
                                             "  10,000 - 50,000  ","  50,000 - 100,000  ","  100,000 - 500,000  ",
                                             "  500,000 - 1,000,000  ","  1,000,000 - 5,000,000  ",
                                             "  5,000,000 - 10,000,000  ","  10,000,000 - 50,000,000  ",
                                             "  50,000,000 - 100,000,000  ","  100,000,000 - 500,000,000  ",
                                             "  500,000,000 - 1,000,000,000  ","  1,000,000,000 - 5,000,000,000  "),
                                    ordered=TRUE)


app_info$date_updated = as.Date(app_info$date_updated, "%B %d, %Y")

# set all as numeric
app_info$rating = as.numeric(paste(app_info$rating))
app_info$num_ratings = as.numeric(app_info$num_ratings)
## prep data


#
#### DEFINE by_app_of_interest
by_app_of_interest = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="False" | 
                                                            node_of_interest$Speakable_Text_Present=="True" ,c("app_id","Speakable_Text_Present")]$app_id))

View(by_app_of_interest)
by_app_of_interest = rename(by_app_of_interest, c("Var1"="app_id", "Freq"="total_elements_of_interest"))
#remove those with no elements of interest, I don't know how they got back in
by_app_of_interest = by_app_of_interest[by_app_of_interest$total_elements_of_interest >0,]
by_app_of_interest = (merge(app_info, by_app_of_interest, by="app_id",all.y=T))



######################
##################### unhelpful label
node_of_interest = node[(node$class=="android.widget.ImageButton" | (node$class=="android.widget.ImageView" & node$is_clickable=="True") | node$class=="android.support.design.widget.FloatingActionButton"),]
#node_of_interest2 = node[is.element(node$class, class_of_interest) & node$is_clickable == "True",]
class_of_interest## unhelpful label
class_of_interest = c("android.widget.ImageView","android.widget.ImageButton","android.support.design.widget.FloatingActionButton")
unhelpful_labels = c("[image]", "image", "Image","Image Des", "alt image", "image description", "image description default", "image_button",
                     "images", "Images", "ImageView", "View", "Image Content",
                     "Icon", "icon desc",
                     "button", "Button", "contentDescription","desc","Desc","Description","Description Image")
node_of_interest$is_unhelpful_label = ifelse(is.element(node_of_interest$label, unhelpful_labels), "True", "False")

####################### Investigating the labels themselves
#View(node_of_interest[node_of_interest$app_id=="com.pantech.app.vegaremoteshot",]) ?? why is it blank but not empty
labels_tab = unique(node_of_interest[,c("app_id","label")])
labels_freqs = as.data.frame(table(unique(node_of_interest[,c("app_id","label")])$label))
labels_freqs = rename(labels_freqs, c("Var1"="label", "Freq"="num_apps"))
# if it's not in any apps, it shouldn't be in the list. I don't know why it's there in the first place
labels_freqs = labels_freqs[labels_freqs$num_apps>0,]
View(labels_freqs)

## raw frequency of labels, not count of how many apps appeared in


labels_freqs = as.data.frame(table((node_of_interest[node_of_interest$Num_Nodes_Share_Label >0 & node_of_interest$Num_Nodes_Share_Label,])$label))
labels_freqs = rename(labels_freqs, c("Var1"="label", "Freq"="num_dups"))

labels_freqs = as.data.frame(table((node_of_interest[node_of_interest$Num_Nodes_Share_Label >0,])$label))
labels_freqs = rename(labels_freqs, c("Var1"="label", "Freq"="num_dups"))
# if it's not in any apps, it shouldn't be in the list. I don't know why it's there in the first place
labels_freqs = labels_freqs[labels_freqs$num_apps>0,]
View(labels_freqs)

unique_apps = as.data.frame(unique(node_of_interest$app_id))
unique_apps = rename(unique_apps, c("unique(node_of_interest$app_id)"="app_id"))
View(unique_apps)
total_num_apps = nrow(unique_apps)
total_num_apps

##### Looking for most common (across apps) labels that get repeated
tmp = unique(node_of_interest[node_of_interest$Num_Nodes_Share_Label >0,
                              c("app_id","label")])
tmp = as.data.frame(table(tmp$label))
## order by freq. freq being the number of apps this appears in as a duplicate label
View(tmp)

#################
########## error by app
#########################

#####################################
######## by app


###############################
#


####
### sp text
tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="False",c("app_id","Speakable_Text_Present")]$app_id))
View(tmp)
tmp = rename(tmp, c("Var1"="app_id", "Freq"="missing_speakable_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")


by_app_of_interest$percent_missing_speakable_text =(by_app_of_interest$missing_speakable_text/by_app_of_interest$total_elements_of_interest)

####
## see below

###### by class by app

###
########### data prep

########
########### speakable text by class within same app
#######

## image View
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageView" & 
                                             ( node_of_interest$Speakable_Text_Present=="False" | node_of_interest$Speakable_Text_Present=="True"),
                                            c("app_id","Speakable_Text_Present")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_view_total_sp_text"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageView" & node_of_interest$is_clickable =="True" &
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


############




#######
#### Uninformative label
############

# only look within labeled nodes
tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="True" &
                                             (node_of_interest$is_unhelpful_label=="True" | node_of_interest$is_unhelpful_label=="False"),
                                           c("app_id","is_unhelpful_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="unhelpful_label_total"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="True" 
                                           & node_of_interest$is_unhelpful_label=="True",
                                           c("app_id","is_unhelpful_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="unhelpful_label"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")
by_app_of_interest$prop_unhelpful_label =(by_app_of_interest$unhelpful_label/by_app_of_interest$unhelpful_label_total)



###
# by class
##

# clickable image View
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageView" & node_of_interest$is_clickable == "True" & 
                                            node_of_interest$Speakable_Text_Present == "True" &
                                             ( node_of_interest$is_unhelpful_label=="False" | node_of_interest$is_unhelpful_label=="True"),
                                           c("app_id","is_unhelpful_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_view_total_unhelp_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageView" & node_of_interest$is_clickable == "True" & 
                                             node_of_interest$Speakable_Text_Present=="True" &
                                             node_of_interest$is_unhelpful_label == "True",
                                           c("app_id","is_unhelpful_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_view_unhelp_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)
by_app_of_interest$prop_of_lab_image_view_unhelp_lab =(by_app_of_interest$image_view_unhelp_lab/by_app_of_interest$image_view_total_unhelp_lab)

## image button
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageButton" & 
                                             node_of_interest$Speakable_Text_Present == "True" &
                                             ( node_of_interest$is_unhelpful_label=="False" | node_of_interest$is_unhelpful_label=="True"),
                                           c("app_id","is_unhelpful_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_button_total_unhelp_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageButton" & 
                                             node_of_interest$Speakable_Text_Present=="True" &
                                             node_of_interest$is_unhelpful_label == "True",
                                           c("app_id","is_unhelpful_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_button_unhelp_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)
by_app_of_interest$prop_of_lab_image_button_unhelp_lab =(by_app_of_interest$image_button_unhelp_lab/by_app_of_interest$image_button_total_unhelp_lab)



#FAB
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.support.design.widget.FloatingActionButton" 
                                           & node_of_interest$Speakable_Text_Present == "True" &
                                             ( node_of_interest$is_unhelpful_label=="False" | node_of_interest$is_unhelpful_label=="True"),
                                           c("app_id","is_unhelpful_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="FAB_total_unhelp_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.support.design.widget.FloatingActionButton" & 
                                             node_of_interest$Speakable_Text_Present=="True" &
                                             node_of_interest$is_unhelpful_label == "True",
                                           c("app_id","is_unhelpful_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="FAB_unhelp_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)
by_app_of_interest$prop_of_lab_FAB_unhelp_lab =(by_app_of_interest$FAB_unhelp_lab/by_app_of_interest$FAB_total_unhelp_lab)

############


#############
### Duplicate Label
###########

# only look within labeled nodes
# tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="True" &
#                                              (node_of_interest$dup_label==TRUE | node_of_interest$dup_label==FALSE),
#                                            c("app_id","dup_label")]$app_id))
# tmp = rename(tmp, c("Var1"="app_id", "Freq"="dup_label_total"))
# by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")
# 
# tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="True" 
#                                            & node_of_interest$dup_label==TRUE,
#                                            c("app_id","dup_label")]$app_id))
# tmp = rename(tmp, c("Var1"="app_id", "Freq"="dup_label"))
# by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")
# 
# by_app_of_interest$prop_dup_label =(by_app_of_interest$dup_label/by_app_of_interest$unhelpful_label_total)
## total is done elsewhere?


###
# by class
##

# clickable image View
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageView" & node_of_interest$is_clickable == "True" & 
                                             node_of_interest$Speakable_Text_Present == "True" &
                                             ( node_of_interest$dup_label == TRUE | node_of_interest$dup_label==FALSE),
                                           c("app_id","dup_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_view_total_dup_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageView" & node_of_interest$is_clickable == "True" & 
                                             node_of_interest$Speakable_Text_Present=="True" &
                                             node_of_interest$dup_label == TRUE,
                                           c("app_id","dup_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_view_dup_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)
by_app_of_interest$prop_of_lab_image_view_dup_lab =(by_app_of_interest$image_view_dup_lab/by_app_of_interest$image_view_total_dup_lab)

## image button
tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageButton" &  
                                             node_of_interest$Speakable_Text_Present == "True" &
                                             ( node_of_interest$dup_label == TRUE | node_of_interest$dup_label==FALSE),
                                           c("app_id","dup_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_button_total_dup_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.widget.ImageButton" &  
                                             node_of_interest$Speakable_Text_Present=="True" &
                                             node_of_interest$dup_label == TRUE,
                                           c("app_id","dup_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="image_button_dup_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)
by_app_of_interest$prop_of_lab_image_button_dup_lab =(by_app_of_interest$image_button_dup_lab/by_app_of_interest$image_button_total_dup_lab)



#FAB

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.support.design.widget.FloatingActionButton" &
                                             node_of_interest$Speakable_Text_Present == "True" &
                                             ( node_of_interest$dup_label == TRUE | node_of_interest$dup_label==FALSE),
                                           c("app_id","dup_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="FAB_total_dup_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)

tmp = as.data.frame(table(node_of_interest[node_of_interest$class=="android.support.design.widget.FloatingActionButton"  & 
                                             node_of_interest$Speakable_Text_Present=="True" &
                                             node_of_interest$dup_label == TRUE,
                                           c("app_id","dup_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="FAB_dup_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id", all.x=T)
by_app_of_interest$prop_of_lab_FAB_dup_lab =(by_app_of_interest$FAB_dup_lab/by_app_of_interest$FAB_total_dup_lab)


#############

#######3
### duplicate label

#### correlation of error rate w/ app characteristics
by_app_of_interest[by_app_of_interest$num_downloads="None",]$num_downloads = NA



plot(by_app_of_interest[by_app_of_interest$num_downloads!="None",]$num_downloads,
     xlab="Number of Downloads",
     ylab="number of apps",
     main="distribution of app downloads",
     ylim=c(0,2000))

plot(by_app_of_interest[by_app_of_interest$num_downloads!="None",]$num_downloads, 
     by_app_of_interest[by_app_of_interest$num_downloads!="None",]$percent_missing_speakable_text,
     xlab="Number of Downloads", ylab="Proportion Image-Based Buttons Missing Labels", 
     main="Number of Downloads versus Proportion Missing Labels")
library(car)
scatterplot(by_app_of_interest[by_app_of_interest$num_downloads!="None",]$num_downloads, 
            by_app_of_interest[by_app_of_interest$num_downloads!="None",]$percent_missing_speakable_text)
summary(by_app_of_interest$num_downloads)
numeric_downloads = rename(by_app_of_interest$num_downloads,
                           c("  100 - 500  "="a","  500 - 1,000  "="b","  1,000 - 5,000  "="c",
                             "  5,000 - 10,000  "="d",
                            "  10,000 - 50,000  "="e","  50,000 - 100,000  "="f",
                            "  100,000 - 500,000  "="g",
                            "  500,000 - 1,000,000  "="h","  1,000,000 - 5,000,000  "="i",
                            "  5,000,000 - 10,000,000  "="j","  10,000,000 - 50,000,000  "="k",
                            "  50,000,000 - 100,000,000  "="l","  100,000,000 - 500,000,000  "="m",
                            "  500,000,000 - 1,000,000,000  "="n","  1,000,000,000 - 5,000,000,000  "="o")
                           )
tmp = as.numeric(by_app_of_interest[by_app_of_interest$num_downloads!="None",]$num_downloads)
View(tmp)


library(pspearman)
#rating by missing label
spearman.test(by_app_of_interest$rating, 
              by_app_of_interest$percent_missing_speakable_text,
              approximation = "AS89")


# num downloads by percent missing
spearman.test(by_app_of_interest[!is.na(by_app_of_interest$num_downloads),]$num_downloads, 
              by_app_of_interest[!is.na(by_app_of_interest$num_downloads),]$percent_missing_speakable_text,
              approximation = "AS89")

# num downloads by dup labels
spearman.test(by_app_of_interest[!is.na(by_app_of_interest$num_downloads) & 
                                   !is.nan(by_app_of_interest$prop_dup_label),]$num_downloads, 
              by_app_of_interest[!is.na(by_app_of_interest$num_downloads) &
                                   !is.nan(by_app_of_interest$prop_dup_label),]$prop_dup_label,
              approximation = "AS89")
plot (by_app_of_interest[!is.na(by_app_of_interest$num_downloads) & 
                           !is.nan(by_app_of_interest$prop_dup_label),]$num_downloads, 
      by_app_of_interest[!is.na(by_app_of_interest$num_downloads) &
                           !is.nan(by_app_of_interest$prop_dup_label),]$prop_dup_label,
      main="Number of Downloads versus Proportion Duplicate Label",
      xlab="Number of Downloads",
      ylab="Poportion of labeled image-based buttons with duplicate label")


cor(by_app_of_interest[by_app_of_interest$num_downloads!="None",]$num_downloads, 
     by_app_of_interest[by_app_of_interest$num_downloads!="None",]$percent_missing_speakable_text)
cor.test(as.numeric(by_app_of_interest[by_app_of_interest$num_downloads!="None",]$num_downloads), 
         by_app_of_interest[by_app_of_interest$num_downloads!="None",]$percent_missing_speakable_text, 
         method="spearman", use="pairwise.complete.obs", exact=F)

## by num downloads for dup text




bin.width = 0.25
hist(by_app_of_interest$rating,
     xlab="Rating",
     ylab="number of apps",
     main="distribution of app rating",
     labels=T, breaks=seq(0,5,by=bin.width),
     ylim=c(0,2000))

plot(by_app_of_interest$rating, by_app_of_interest$percent_missing_speakable_text,
     xlab="App Rating (out of 5)", ylab="Proportion Missing Labels", 
     main="App Rating versus Proportion Missing Labels", xlim=c(0,5))

M = cor(by_app_of_interest$percent_missing_speakable_text, 
        by_app_of_interest[,c("rating")],method="spearman",use="pairwise.complete.obs")
M



plot(by_app_of_interest$rating, by_app_of_interest$prop_dup_label,
     xlab="App Rating (5 pt scale)", ylab="Proportion Missing Speakable Text", 
     main="App Rating versus Proportion Error", xlim=c(0,5))


plot(by_app_of_interest$num_downloads, by_app_of_interest$prop_dup_label,
     xlab="App Rating (5 pt scale)", ylab="Proportion Missing Speakable Text", 
     main="App Rating versus Proportion Error", xlim=c(0,5))

############

##################################
### correlation of co-occurence
## same app, same error, different class
################################33

#### missing speakable text
plot(by_app_of_interest$prop_image_view_missing_speakable_text, by_app_of_interest$prop_image_btn_missing_speakable_text,
     xlab="Proportion Image Views Missing Speakable Text",
     ylab = "Proportion Image Buttons Missing Speakable Text",
     main="Occurence of Error in Same App over Different Classes")
sum(!is.nan(by_app_of_interest$prop_image_view_missing_speakable_text)
    & !is.nan(by_app_of_interest$prop_image_btn_missing_speakable_text))

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

##########################################
######### correlation of making different mistakes within the same app

## Mis-Dup
res = cor.test(by_app_of_interest$percent_missing_speakable_text, 
               by_app_of_interest$prop_dup_label,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res
plot(by_app_of_interest$percent_missing_speakable_text, 
     by_app_of_interest$prop_dup_label,
     main="Relationship Between Different Error Prevalence within Apps",
     xlab="Proportion of Elements Missing Labels",
     ylab="Proportion of Elements with Duplicate Labels")

##Mis - Uninf
res = cor.test(by_app_of_interest$percent_missing_speakable_text, 
               by_app_of_interest$prop_unhelpful_label,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res
plot(by_app_of_interest$percent_missing_speakable_text, 
     by_app_of_interest$prop_unhelpful_label,
     main="Relationship Between Different Error Prevalence within Apps",
     xlab="Proportion of Elements Missing Labels",
     ylab="Proportion of Elements with Uninformative Labels")
## dup-uninf
res = cor.test(by_app_of_interest$prop_dup_label, 
               by_app_of_interest$prop_unhelpful_label,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res
plot(by_app_of_interest$prop_dup_label, 
     by_app_of_interest$prop_unhelpful_label,
     main="Relationship Between Different Error Prevalence within Apps",
     xlab="Proportion of Elements with Duplicate Labels",
     ylab="Proportion of Elements with Uninformative Labels")

########################################



###########
### same app, same class, different error
########3
plot(by_app_of_interest$prop_image_btn_missing_speakable_text, by_app_of_interest$prop_of_lab_image_button_dup_lab,
     xlab="Proportion Image Buttons Missing Label",
     ylab = "Proportion Image Buttons With Duplicate Text",
     main="Occurence of Different Error in Image Button in Same App")
sum(!is.nan(by_app_of_interest$prop_image_view_missing_speakable_text)
    & !is.nan(by_app_of_interest$prop_image_btn_missing_speakable_text))

plot(by_app_of_interest$prop_FAB_missing_speakable_text, by_app_of_interest$prop_of_lab_FAB_dup_lab,
     xlab="Proportion FABs Missing Label",
     ylab = "Proportion FAB With Duplicate Text",
     main="Occurence of Different Error in FABs in Same App")

plot(by_app_of_interest$prop_image_view_missing_speakable_text, by_app_of_interest$prop_of_lab_image_view_unhelp_lab,
     xlab="Proportion Image View Missing Label",
     ylab = "Proportion Image View With Duplicate Text",
     main="Occurence of Different Error in Image View in Same App")
#####
### FAB
## missing-dup
res = cor.test(by_app_of_interest$prop_FAB_missing_speakable_text, 
               by_app_of_interest$prop_of_lab_FAB_dup_lab,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res
## miss-uninf
by_app_of_interest[is.nan(by_app_of_interest$prop_of_lab_FAB_dup_lab),]$prop_of_lab_FAB_unhelp_lab=NA
by_app_of_interest[is.nan(by_app_of_interest$prop_FAB_missing_speakable_text),]$prop_FAB_missing_speakable_text=NA
res = cor.test(by_app_of_interest$prop_FAB_missing_speakable_text, 
               by_app_of_interest$prop_of_lab_FAB_unhelp_lab,
               na.action=na.exclude,
               use="complete.obs", method="spearman", exact=FALSE)
cor(by_app_of_interest$prop_FAB_missing_speakable_text, 
    by_app_of_interest$prop_of_lab_FAB_unhelp_lab,
    use="pairwise.complete.obs", method="spearman")
res
## dup-uninf

res = cor.test(by_app_of_interest$prop_of_lab_FAB_dup_lab, 
               by_app_of_interest$prop_of_lab_FAB_unhelp_lab,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res
#####

#####
### Image Button
## missing-dup
res = cor.test(by_app_of_interest$prop_image_btn_missing_speakable_text, 
               by_app_of_interest$prop_of_lab_image_button_dup_lab,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res

## miss-uninf
res = cor.test(by_app_of_interest$prop_image_btn_missing_speakable_text, 
               by_app_of_interest$prop_of_lab_image_button_unhelp_lab,
               na.action=na.exclude,
               use="complete.obs", method="spearman", exact=FALSE)

res

## dup-uninf
res = cor.test(by_app_of_interest$prop_of_lab_image_button_dup_lab, 
               by_app_of_interest$prop_of_lab_image_button_unhelp_lab,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res
#####

#####
### Image Button
## missing-dup
res = cor.test(by_app_of_interest$prop_image_view_missing_speakable_text, 
               by_app_of_interest$prop_of_lab_image_view_dup_lab,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res

## miss-uninf
res = cor.test(by_app_of_interest$prop_image_view_missing_speakable_text, 
               by_app_of_interest$prop_of_lab_image_view_unhelp_lab,
               na.action=na.exclude,
               use="complete.obs", method="spearman", exact=FALSE)

res

## dup-uninf
res = cor.test(by_app_of_interest$prop_of_lab_image_view_dup_lab, 
               by_app_of_interest$prop_of_lab_image_view_unhelp_lab,
               use="pairwise.complete.obs", method="spearman", exact=FALSE)
res
#####
########################################

#########3
### different class, same error, same app
###########

####
### Missing Label

## FAB-btn
res = cor.test(by_app_of_interest$prop_FAB_missing_speakable_text, 
               by_app_of_interest$prop_image_btn_missing_speakable_text,
               na.action=na.exclude,
               use="complete.obs", method="spearman", exact=FALSE)

res

## FAB-view
res = cor.test(by_app_of_interest$prop_FAB_missing_speakable_text, 
               by_app_of_interest$prop_image_view_missing_speakable_text,
               na.action=na.exclude,
               use="complete.obs", method="spearman", exact=FALSE)

res
##btn-view

###
## Unhelpful Label

## FAB-btn
## FAB-view
##btn-view


###
## Duplicate Label
## FAB-btn
## FAB-view
##btn-view



################################################
#####
### duplicate label


####### histograms
bin.width = 0.025
h = hist(by_app_of_interest$percent_missing_speakable_text, 
     xlab="Proportion of Elements of Interest with Error", ylab="Number of Apps", 
     main = "Missing Speakable Text", labels=TRUE, ylim=c(0,2500),
     breaks=seq(0,1,by=bin.width))
nrow(by_app_of_interest[by_app_of_interest$percent_missing_speakable_text==0,])
nrow(by_app_of_interest[by_app_of_interest$percent_missing_speakable_text==1,])




bin.width = 0.025
hist(by_app_of_interest[by_app_of_interest$unhelpful_label_total>0,]$prop_unhelpful_label, 
     xlab="Proportion of Elements of Interest with Unhelpful Label", ylab="Number of Apps", 
     main = "Unhelpful Label Distribution within Apps with at least 1 labeled element", labels=TRUE, ylim=c(0,4000),
     breaks=seq(0,1,by=bin.width))
nrow(by_app_of_interest[by_app_of_interest$unhelpful_label_total>0 & 
                          by_app_of_interest$prop_unhelpful_label == 0,])
sum(!is.nan(by_app_of_interest$prop_unhelpful_label))



######################



#############################
########## by-class

#### Missing Label
miss_label_by_class = as.data.frame(table(node_of_interest[node_of_interest,c("app_id","Speakable_Text_Present")]))



error_by_class=as.data.frame(table(node_of_interest$class))
error_by_class = rename(error_by_class, c("Var1"="class","Freq"="num_elements"))
error_by_class = error_by_class[error_by_class$num_elements > 0,]


#####
tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present == "False",]$class))
tmp = rename(tmp, c("Var1"="class","Freq"="num_missing_sp_text"))

error_by_class = merge(error_by_class,tmp, by="class")

error_by_class$prop_missing_text = error_by_class$num_missing_sp_text/error_by_class$num_elements

tmp = as.data.frame(table(unique(node_of_interest[,c("app_id","class")])$class))
View(tmp)

View(error_by_class)



####### by class
#############


View(node_of_interest)


tmp = as.data.frame(table(node_of_interest[node_of_interest$is_unhelpful_label == "True",]$class))
tmp = rename(tmp, c("Var1"="class","Freq"="num_unhelpful_label"))
tmp = tmp[is.element(tmp$class, class_of_interest),]

error_by_class = merge(error_by_class,tmp, by="class")

error_by_class$prop_unhelpful_label = error_by_class$num_unhelpful_label/error_by_class$num_elements

error_by_class$prop_of_labeled_w_unhelpful = error_by_class$num_unhelpful_label/(error_by_class$num_elements - error_by_class$num_missing_sp_text)

tmp = as.data.frame(table(unique(node_of_interest[,c("app_id","class")])$class))




#unhelpful label by class



unhelp_label = as.data.frame(table(node_of_interest[
                                           node_of_interest$Speakable_Text_Present == "True" &
                                             ( node_of_interest$is_unhelpful_label=="False" | node_of_interest$is_unhelpful_label=="True"),
                                           c("class","is_unhelpful_label")]$class))
unhelp_label = rename(unhelp_label, c("Var1"="class", "Freq"="labeled_total_unhelp_lab"))
unhelp_label = unhelp_label[unhelp_label$labeled_total_unhelp_lab>0,]

tmp = as.data.frame(table(node_of_interest[
    node_of_interest$Speakable_Text_Present == "True" &
    ( node_of_interest$is_unhelpful_label=="True"),
    c("class","is_unhelpful_label")]$class))
tmp= rename(tmp, c("Var1"="class", "Freq"="num_unhelp_lab"))
tmp = tmp[is.element(tmp$class,class_of_interest),]
unhelp_label = merge(unhelp_label, tmp, by="class")

unhelp_label$prop_unhelp_lab_out_of_lab = unhelp_label$num_unhelp_lab/unhelp_label$labeled_total_unhelp_lab

View(unhelp_label)

#####################3
#############################
### duplicate label 
##########################
################


############
###### by class
########

node_of_interest$dup_label = (node_of_interest$Num_Nodes_Share_Label > 0)
dup_label = as.data.frame(table(node_of_interest[
    node_of_interest$Speakable_Text_Present == "True" &
    ( node_of_interest$dup_label == TRUE  | node_of_interest$dup_label==FALSE),
  c("class","dup_label")]$class))
dup_label = rename(dup_label, c("Var1"="class", "Freq"="labeled_total_dup_lab"))
dup_label = dup_label[is.element(dup_label$class, class_of_interest),]

tmp = as.data.frame(table(node_of_interest[
  node_of_interest$Speakable_Text_Present == "True" &
    ( node_of_interest$dup_label==TRUE),
  c("class","dup_label")]$class))
tmp= rename(tmp, c("Var1"="class", "Freq"="num_have_dup_label"))
tmp = tmp[is.element(tmp$class,class_of_interest),]
dup_label = merge(dup_label, tmp, by="class")

dup_label$prop_dup_lab_out_of_lab = dup_label$num_have_dup_label/dup_label$labeled_total_dup_lab


tmp = as.data.frame(table(node_of_interest[
    ( node_of_interest$dup_label == TRUE  | node_of_interest$dup_label==FALSE),
  c("class","dup_label")]$class))
tmp = rename(tmp, c("Var1"="class", "Freq"="total_dup_lab"))
tmp = tmp[is.element(tmp$class, class_of_interest),]
dup_label = merge(dup_label, tmp, by="class")

dup_label$prop_dup_lab_out_of_all = dup_label$num_have_dup_label/dup_label$total_dup_lab

View(dup_label)



###################
###dup label
# only look within labeled nodes
# by app
tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="True" &
                                             (node_of_interest$dup_label==TRUE | node_of_interest$dup_label==FALSE),
                                           c("app_id","dup_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="dup_label_total_out_of_lab"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")

tmp = as.data.frame(table(node_of_interest[node_of_interest$Speakable_Text_Present=="True" 
                                           & node_of_interest$dup_label==TRUE,
                                           c("app_id","dup_label")]$app_id))
tmp = rename(tmp, c("Var1"="app_id", "Freq"="dup_label"))
by_app_of_interest = merge(by_app_of_interest, tmp, by="app_id")
by_app_of_interest$prop_dup_label =(by_app_of_interest$dup_label/by_app_of_interest$dup_label_total_out_of_lab)


###
## hist by app

bin.width = 0.025
hist(by_app_of_interest[by_app_of_interest$dup_label_total_out_of_lab>0,]$prop_dup_label, 
     xlab="Proportion of Elements of Interest with Duplicate Label", ylab="Number of Apps", 
     main = "Duplicate Label Distribution within Apps with at least 1 labeled element", labels=TRUE,
     ylim=c(0,3000),
     breaks=seq(0,1,by=bin.width))
nrow(by_app_of_interest[by_app_of_interest$dup_label_total_out_of_lab>0 & 
                          by_app_of_interest$prop_dup_label == 0,])
nrow(by_app_of_interest[by_app_of_interest$dup_label_total_out_of_lab>0 & 
                          by_app_of_interest$prop_dup_label == 1,])
sum(!is.nan(by_app_of_interest$prop_dup_label))


#
