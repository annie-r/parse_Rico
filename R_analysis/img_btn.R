########################################
######## FOR ASSETS PAPER
###############################

app_rating = error_by_app[,c("app_id","rating")]

img_node =read.table(file="image_node_6_1_2018.csv", header=TRUE,
                     quote="'\"", sep=",",
                     encoding="UTF-8", fill=FALSE)
View(img_node)

img_nodes <- img_node[(img_node$class=="android.widget.ImageButton" | img_node$class=="android.widget.ImageView"
                  | img_node$class=="android.support.design.widget.FloatingActionButton")
                 & img_node$is_clickable=="True",]

View(as.data.frame(table(img_nodes$class)))

img_nodes <- node[(node$class=="android.widget.ImageButton" | node$class=="android.widget.ImageView"
                       | node$class=="android.support.design.widget.FloatingActionButton")
                      & node$is_clickable=="True",]


img_nodes$Num_Nodes_Share_Label = as.numeric(as.character(img_nodes$Num_Nodes_Share_Label))

img_nodes$shares_label = img_nodes$Num_Nodes_Share_Label>0
View(img_nodes)

#############
### By Class
img_node_bc = as.data.frame(table(img_nodes$class))
img_node_bc <- img_node_bc[img_node_bc$Freq > 0,]
img_node_bc <- rename(img_node_bc, c("Freq"="Num_Occur", "Var1"="class"))
tmp= as.data.frame(table(img_nodes$class,img_nodes$Speakable_Text_Present, useNA="no", exclude="na"))
tmp <- tmp[tmp$Freq > 0,]
tmp = rename(tmp, c("Var1"="class", "Var2"="has_label", "Freq"="count"))
tmp_wide = spread(tmp, has_label, count)
View(tmp_wide)
tmp_wide = rename(tmp_wide, c("False"="Missing","True"="Labeled"))
tmp_wide$Total = tmp_wide$Missing + tmp_wide$Labeled

img_node_bc = merge(img_node_bc, tmp_wide, by="class")
View(img_node_bc)
img_node_bc$Num_Occur = NULL

tmp = img_nodes[,c("class","app_id")]
tmp=as.data.frame(table(unique(tmp)))




################################
########### Missing Label
#######################
#### by app

img_btn_missing_label = as.data.frame(table(img_nodes[,c("app_id","Speakable_Text_Present")]))
View(temp)                     
img_btn_missing_label_wide = spread(img_btn_missing_label, Speakable_Text_Present,Freq )
img_btn_missing_label_wide = rename(img_btn_missing_label_wide, c("False"="Missing Label", "True"="Labeled"))
img_btn_missing_label_wide$prop_missing = img_btn_missing_label_wide$`Missing Label`/
  (img_btn_missing_label_wide$`Missing Label` + img_btn_missing_label_wide$Labeled) 
View(img_btn_missing_label_wide)
write.csv(img_btn_missing_label_wide[!is.na(img_btn_missing_label_wide$prop_missing),]$prop_missing, "img_btn_miss_label.csv")
hist(img_btn_missing_label_wide$prop_missing, labels=T, ylim=c(0,3000))
nrow(img_btn_missing_label_wide[img_btn_missing_label_wide$prop_missing==0,])
hist(img_btn_missing_label_wide[img_btn_missing_label_wide$prop_missing==0,])

### dist of extremes
summary(img_btn_missing_label_wide$Total)
summary(img_btn_missing_label_wide[img_btn_missing_label_wide$prop_missing<.1,]$Total)
summary(img_btn_missing_label_wide[img_btn_missing_label_wide$prop_missing>=.9,]$Total)

### prop vs rating
img_btn_missing_vs_rating = merge(app_rating, img_btn_missing_label_wide, all.y=T, all.x=F, by="app_id")
plot(img_btn_missing_vs_rating$rating, img_btn_missing_vs_rating$prop_missing,
     main="Missing Label by App Rating",
     xlab="App Rating", ylab="Proportion Missing Label",
     xlim=c(0,5))
to_write =img_btn_missing_vs_rating[
  !is.na(img_btn_missing_vs_rating$prop_missing),
  c("rating","prop_missing")] 
write.csv(to_write,
  "img_btn_missing_lab_vs_rating.csv")
cor.test(img_btn_missing_vs_rating$prop_missing, img_btn_missing_vs_rating$rating, method="spearman")

######
## by class missing label
##

img_bc = as.data.frame((unique(img_nodes[(img_nodes$class=="android.widget.ImageButton" | img_nodes$class=="android.widget.ImageView"
                                         | img_nodes$class=="android.support.design.widget.FloatingActionButton") 
                                         & img_nodes$is_clickable=="True",c("class","app_id")])))
class_counts = as.data.frame(table(img_bc$class))
class_counts = class_counts[class_counts$Freq>0,]
class_counts = rename(class_counts, c("Freq"="Num_Apps"))
View(class_counts)

error_count_bc = as.data.frame(table(img_nodes[,c("class","Speakable_Text_Present")]))
error_count_bc = error_count_bc[error_count_bc$Freq>0,]
error_count_bc_wide = spread(error_count_bc, Speakable_Text_Present, Freq)
error_count_bc_wide = rename (error_count_bc_wide, c("False"="Missing","True"="Labeled"))
error_count_bc_wide$Total = error_count_bc_wide$Labeled + error_count_bc_wide$Missing
error_count_bc_wide$Prop_Missing = error_count_bc_wide$Missing / error_count_bc_wide$Total

View(error_count_bc_wide)

############################
## Duplicate Label
#############


########## by class
dup_lab_img_node_bc= as.data.frame(table(img_nodes$class,img_nodes$shares_label, useNA="no", exclude="na"))
dup_lab_img_node_bc=rename(dup_lab_img_node_bc, c("Var1"="class","Var2"="Shares_Label", "Freq"="count"))
dup_lab_img_node_bc_wide = spread(dup_lab_img_node_bc, Shares_Label, count)
dup_lab_img_node_bc_wide = dup_lab_img_node_bc_wide[dup_lab_img_node_bc_wide$"TRUE">0,]
dup_lab_img_node_bc_wide = rename(dup_lab_img_node_bc_wide, c("TRUE"="Duplicate", "FALSE"="Not_Duplicate", "<NA>"="NA_Dup"))
dup_lab_img_node_bc_wide$Total = dup_lab_img_node_bc_wide$Duplicate +dup_lab_img_node_bc_wide$Not_Duplicate
dup_lab_img_node_bc_wide$prop_dup = dup_lab_img_node_bc_wide$Duplicate / dup_lab_img_node_bc_wide$Total
View(dup_lab_img_node_bc_wide)


View(img_node)

########## by app

dup_lab_img_node = as.data.frame(table(img_nodes[,c("app_id","shares_label")]))
View(dup_lab_img_node)
dup_lab_img_node_wide = spread(dup_lab_img_node, shares_label,Freq )
dup_lab_img_node_wide = rename(dup_lab_img_node_wide, c("FALSE"="Not_Dup", "TRUE"="Duplicate"))
dup_lab_img_node_wide$prop_dup = dup_lab_img_node_wide$Duplicate/
  (dup_lab_img_node_wide$Duplicate + dup_lab_img_node_wide$Not_Dup) 
View(dup_lab_img_node_wide)
write.csv(dup_lab_img_node_wide[!is.na(dup_lab_img_node_wide$prop_dup),]$prop_dup, "img_btn_dup_label.csv")
hist(dup_lab_img_node_wide$prop_dup, labels=T, ylim=c(0,3000))



#######################
#### Uniformative Label
################

uninformative_labels = c("[image]", "image", "Image", "alt image", "image description", "Image Des", 
                         "image description default", "Icon", "icon desc", "images", "Images", "Image Content", 
                         "ImageView", "View", "button", "Button", "contentDescription", "desc", "Desc", 
                         "Description", "Description Image")
uninf_labels_nodes = img_nodes_2
uninf_labels_nodes$is_uninformative = uninf_labels_nodes$label %in% uninformative_labels
uninf_labels_nodes[uninf_labels_nodes$label=="None",]$is_uninformative = NA

uninf_lab_img_node = as.data.frame(table(uninf_labels_nodes[,c("app_id","is_uninformative")]))
uninf_lab_img_node_wide = spread(uninf_lab_img_node, is_uninformative, Freq)
uninf_lab_img_node_wide = rename(uninf_lab_img_node_wide, c("TRUE"="uninformative", "FALSE"="informative"))
uninf_lab_img_node_wide$Total = uninf_lab_img_node_wide$uninformative + uninf_lab_img_node_wide$informative
## only consider apps with at least one labeled image-based button
uninf_lab_img_node_wide = uninf_lab_img_node_wide[uninf_lab_img_node_wide$Total>0,] 
uninf_lab_img_node_wide$prop_uninformative = uninf_lab_img_node_wide$uninformative / 
  uninf_lab_img_node_wide$Total

View(uninf_lab_img_node_wide)
write.csv(uninf_lab_img_node_wide[!is.na(uninf_lab_img_node_wide$prop_uninformative),]$prop_uninformative, "img_btn_uninformative_label.csv")
hist(uninf_lab_img_node_wide$prop_uninformative, labels=T, ylim=c(0,3500))
View(uninf_lab_img_node_wide)
nrow(uninf_lab_img_node_wide[uninf_lab_img_node_wide$prop_uninformative == 0,])


##### by class
uninf_lab_img_node_bc= as.data.frame(table(uninf_labels_nodes$class,uninf_labels_nodes$is_uninformative, useNA="no", exclude="na"))
uninf_lab_img_node_bc=rename(uninf_lab_img_node_bc, c("Var1"="class","Var2"="uninf_label", "Freq"="count"))
uninf_lab_img_node_bc_wide = spread(uninf_lab_img_node_bc, uninf_label, count)
View(uninf_lab_img_node_bc_wide)
uninf_lab_img_node_bc_wide = uninf_lab_img_node_bc_wide[uninf_lab_img_node_bc_wide$"<NA>">0,]
uninf_lab_img_node_bc_wide = rename(uninf_lab_img_node_bc_wide, c("TRUE"="Uninformative", "FALSE"="Informative", "<NA>"="NA_Uninf"))
uninf_lab_img_node_bc_wide$Total = uninf_lab_img_node_bc_wide$Uninformative + uninf_lab_img_node_bc_wide$Informative
uninf_lab_img_node_bc_wide$prop_uninf = uninf_lab_img_node_bc_wide$Uninformative / uninf_lab_img_node_bc_wide$Total
View(uninf_lab_img_node_bc_wide)


#########################################################
#############################################################
#######################################################


############## 
##########################################
##############################################
### IMAage Views only
img_views <- node[node$class=="android.widget.ImageView",]
View(img_views)
img_vw_app <- as.data.frame(unique(img_views[,c("app_id","Speakable_Text_Present")]))
View(img_vw_app)
temp = (as.data.frame(table(img_vw_app$app_id)))
temp$labeled_and_un = temp$Freq>1
View(temp)
img_vw_app = merge(temp[,c("app_id","labeled_and_un")], img_vw_app, by="app_id")
View(img_vw_app)
img_views = merge(temp[,c("app_id","labeled_and_un")], img_views, by="app_id")
t = img_views[img_views$labeled_and_un==TRUE,]
t = (t[floor(runif(5, min=0, max=nrow(t)+1)),])
