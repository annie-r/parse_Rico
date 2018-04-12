## By Nodes
library(plyr) #ddply, rename
library(tidyr) # create wide data table

#### BEWARE POS GOOD OR BAD CHANGES PER ERROR


#node = read.csv("all_node_webview.csv")
#node = read.csv("by_node_size_fix.csv")
node = read.csv("image_node.csv", encoding="UTF-8")
# convert to R NULL's
node[node=="na"] <- NA
#View(node)

node$Num_Nodes_Overlap_With = as.numeric(as.character(node$Num_Nodes_Overlap_With))
node$Num_Nodes_Share_Label = as.numeric(as.character(node$Num_Nodes_Share_Label))

summary(node)


node$android_widget = as.factor(node$android_widget)

percent_andr_widget = nrow(node[node$android_widget=="True",])/nrow(node)


### simple stats






###########
#### investigate errors by class
#########
error_by_class = table(node$class)
error_by_class = rename(as.data.frame(error_by_class), c("Var1"="class","Freq"="class_count"))
View(error_by_class)

# get the number of apps that have at least one element of a given class
tmp = node[,c("app_id","class")]
tmp = unique(tmp)
apps_with_class = as.data.frame(table(tmp$class))
apps_with_class = rename(apps_with_class, c("Var1"="class","Freq"="num_apps_with_class"))
View(apps_with_class)
error_by_class = merge(error_by_class,apps_with_class, by="class")
View(error_by_class)
#error_by_class <- rename(error_by_class, c("Var1"="class","Freq.x"="class.count", "Freq.y"="speakable_text_present.count"))
#View(error_by_class)

### if "android widget" column
and.widget.classes <- data.frame(unique(node[,c("class","android_widget", "ad")]))
View(and.widget.classes)

error_by_class <- merge(error_by_class, and.widget.classes, by="class")

###########
##################### Parse Data By Error By Class
############

############
############ Sp Text 

sp_text_by_class <- as.data.frame(table(node$class,node$Speakable_Text_Present, useNA="no", exclude="na"))
View(sp_text_by_class)
sp_text_by_class = rename(sp_text_by_class, c("Var1"="class","Var2"="speakable_text_present","Freq"="has_sp_text_count"))
sp_text_bc_wide = spread(sp_text_by_class, speakable_text_present,has_sp_text_count ) 
sp_text_bc_wide$total = (sp_text_bc_wide$False + sp_text_bc_wide$True)

sp_text_bc_wide = merge(error_by_class, sp_text_bc_wide, by="class")
View(error_by_class)
View(sp_text_bc_wide)
sp_text_bc_wide$percent_speak_text_missing = sp_text_bc_wide$False/sp_text_bc_wide$total


##########
# ########## Wide Enough
wide_en_by_class = as.data.frame(table(node$class,node$Element_Wide_Enough, useNA="no", exclude="na"))
wide_en_by_class = rename(wide_en_by_class, c("Var1"="class","Var2"="wide_enough","Freq"="wide_enough_count"))
wide_en_bc_wide = spread(wide_en_by_class, wide_enough, wide_enough_count)
wide_en_bc_wide$total = (wide_en_bc_wide$False + wide_en_bc_wide$True)
wide_en_bc_wide = merge(error_by_class, wide_en_bc_wide, by="class")
wide_en_bc_wide$percent_not_wide_enough = wide_en_bc_wide$False/wide_en_bc_wide$total
View(wide_en_bc_wide)

# ######################
########## Tall Enough
tall_en_by_class = as.data.frame(table(node$class,node$Element_Tall_Enough, useNA="no", exclude="na"))
tall_en_by_class = rename(tall_en_by_class, c("Var1"="class","Var2"="tall_enough","Freq"="tall_enough_count"))
tall_en_bc_wide = spread(tall_en_by_class, tall_enough, tall_enough_count)
tall_en_bc_wide$total = tall_en_bc_wide$True + tall_en_bc_wide$False
tall_en_bc_wide = merge(error_by_class, tall_en_bc_wide, by="class")
## To match others, this is percent BAD
tall_en_bc_wide$percent_not_tall_enough = tall_en_bc_wide$False/tall_en_bc_wide$total
View(tall_en_bc_wide)

###### TALL VS WIDE
tall_vs_wide = merge(tall_en_bc_wide[,c("class","percent_tall_enough")],wide_en_bc_wide[,c("class","percent_wide_enough")], by="class")
tall_vs_wide$slope = tall_vs_wide$percent_tall_enough/tall_vs_wide$percent_wide_enough
tall_vs_wide = merge(tall_vs_wide,error_by_class[,c("class","num_apps_with_class")], by="class")

#############
######## Has redundant desc 
has_red_desc_class = as.data.frame(table(node$class,node$Has_Redundant_Description, useNA="no", exclude="na"))
has_red_desc_class = rename(has_red_desc_class, c("Var1"="class","Var2"="has_red_desc","Freq"="has_red_desc_count"))
has_red_desc_bc_wide = spread(has_red_desc_class, has_red_desc, has_red_desc_count)
has_red_desc_bc_wide$total = has_red_desc_bc_wide$True + has_red_desc_bc_wide$False
has_red_desc_bc_wide = merge(error_by_class, has_red_desc_bc_wide, by="class")
has_red_desc_bc_wide$percent_redun = has_red_desc_bc_wide$True/has_red_desc_bc_wide$total
View(has_red_desc_bc_wide)

############### Dulpicate/Shares Label
temp = node[,c("app_id","class","Num_Nodes_Share_Label")]
temp$shares_label = temp$Num_Nodes_Share_Label > 0
View(temp)
shares_label_class = as.data.frame(table(temp$class, temp$shares_label, useNA="no", exclude="na"))
shares_label_class = rename(shares_label_class, c("Var1"="class","Var2"="shares_label", "Freq"="shares_label_count"))

shares_label_bc_wide = spread(shares_label_class, shares_label, shares_label_count)
shares_label_bc_wide = rename(shares_label_bc_wide, c("TRUE"="True","FALSE"="False"))
shares_label_bc_wide$total = shares_label_bc_wide$False + shares_label_bc_wide$True
shares_label_bc_wide = merge(error_by_class, shares_label_bc_wide, by="class")
shares_label_bc_wide$percent_dup_label = shares_label_bc_wide$True/shares_label_bc_wide$total
View(shares_label_bc_wide)

#############
######## Editable Textview With Cont Desc
editable_txtview_w_cont_desc = as.data.frame(table(node$class,node$Editable_Textview_With_Cont_Desc, useNA="no", exclude="na"))
editable_txtview_w_cont_desc = rename(editable_txtview_w_cont_desc, c("Var1"="class","Var2"="is_ed_txt_w_cont_desc","Freq"="ed_txtvw_w_cont_desc_count"))
editable_txtvw_w_cont_desc_bc_wide = spread(editable_txtview_w_cont_desc, is_ed_txt_w_cont_desc, ed_txtvw_w_cont_desc_count)
editable_txtvw_w_cont_desc_bc_wide$total = editable_txtvw_w_cont_desc_bc_wide$True + editable_txtvw_w_cont_desc_bc_wide$False
editable_txtvw_w_cont_desc_bc_wide = merge(error_by_class, editable_txtvw_w_cont_desc_bc_wide, by="class")
editable_txtvw_w_cont_desc_bc_wide$percent_editable_txtvw_w_cont_desc = editable_txtvw_w_cont_desc_bc_wide$True/editable_txtvw_w_cont_desc_bc_wide$total
View(editable_txtvw_w_cont_desc_bc_wide)

############### Fully Overlaps
temp = node[,c("app_id","class","Num_Nodes_Overlap_With")]
temp$overlap = temp$Num_Nodes_Overlap_With > 0
View(temp)
overlap_class = as.data.frame(table(temp$class, temp$overlap, useNA="no", exclude="na"))
overlap_class = rename(overlap_class, c("Var1"="class","Var2"="overlaps", "Freq"="overlaps_count"))

overlaps_bc_wide = spread(overlap_class, overlaps, overlaps_count)
overlaps_bc_wide = rename(overlaps_bc_wide, c("TRUE"="True","FALSE"="False"))
overlaps_bc_wide$total = overlaps_bc_wide$False + overlaps_bc_wide$True
overlaps_bc_wide = merge(error_by_class, overlaps_bc_wide, by="class")
overlaps_bc_wide$percent_overlapping = overlaps_bc_wide$True/overlaps_bc_wide$total
View(overlaps_bc_wide)

####################
#### PLOTS
####################
####### For percents, higher percent should be higher percent BAD

###
### Fully Overlaps
h=hist(overlaps_bc_wide$percent_overlapping,
       ylab="num classes", ylim=c(0,12000), breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), xlab="Percent Fully Overlapping", ylab="Percent Classes", main="Percent of Widgets of a Class with Error")


##### Editable Textview w/ Cont Description
################
h=hist(editable_txtvw_w_cont_desc_bc_wide$percent_editable_txtvw_w_cont_desc,
       ylab="num classes", breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), xlab="Percent Elements Editable Textview w/ Cont Desc", ylab="Percent Classes", main="Percent of Widgets of a Class with Error")



##### Duplicate/Shared Label
################
h=hist(shares_label_bc_wide$percent_dup_label,
       ylab="num classes", ylim=c(0,10000))
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), xlab="Percent Shared/Duplicate Description", ylab="Percent Classes", main="Percent of Widgets of a Class with Error")

h_infreq_class = hist(shares_label_bc_wide[shares_label_bc_wide$class_count<=5,]$percent_dup_label,
                      ylab="num classes", ylim=c(0,12000), breaks=20)
h_infreq_class$density =h_infreq_class$counts/sum(h_infreq_class$counts)
sum(h_infreq_class$counts)
plot(h_infreq_class,freq=FALSE,ylim=c(0,1), xlab="Percent Duplicate Description", 
     ylab="Percent Classes", 
     main="Classes with 5 or fewer elements in the dataset")

h_freq_class = hist(shares_label_bc_wide[shares_label_bc_wide$class_count >=50,]$percent_dup_label,
                    ylab="num classes", ylim=c(0,12000), breaks=20)
h_freq_class$density =h_freq_class$counts/sum(h_freq_class$counts)
sum(h_freq_class$counts)
plot(h_freq_class,freq=FALSE,ylim=c(0,1), xlab="Percent Shared/Duplicate Description", 
     ylab="Percent Classes", 
     main="Classes with 50 or more elements in the dataset")


###
### Redundant Description
h=hist(has_red_desc_bc_wide$percent_redun,
        ylab="num classes", ylim=c(0,1200), breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), xlab="Percent Redundant Description", ylab="Percent Classes", main="Percent of Widgets of a Class with Error")

h_infreq_class = hist(has_red_desc_bc_wide[has_red_desc_bc_wide$class_count<=5,]$percent_redun,
                      ylab="num classes", ylim=c(0,12000), breaks=20)
h_infreq_class$density =h_infreq_class$counts/sum(h_infreq_class$counts)
sum(h_infreq_class$counts)
plot(h_infreq_class,freq=FALSE,ylim=c(0,1), xlab="Percent Redundant Description", 
     ylab="Percent Classes", 
     main="Classes with 5 or fewer elements in the dataset")

h_freq_class = hist(has_red_desc_bc_wide[has_red_desc_bc_wide$class_count >=50,]$percent_redun,
                    ylab="num classes", ylim=c(0,12000), breaks=20)
h_freq_class$density =h_freq_class$counts/sum(h_freq_class$counts)
sum(h_freq_class$counts)
plot(h_freq_class,freq=FALSE,ylim=c(0,1), xlab="Percent Redundant Description", 
     ylab="Percent Classes", 
     main="Classes with 50 or more elements in the dataset")

###
### Not Wide Enough
h =hist(wide_en_bc_wide$percent_not_wide_enough,
        ylab="num classes", ylim=c(0,12000), labels=TRUE)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE,
     xlab="Percent Not Wide Enough", 
     ylab="Percent Classes", main="Percent of Widgets of a Class with Error")

h_infreq_class = hist(wide_en_bc_wide[wide_en_bc_wide$class_count<=5,]$percent_not_wide_enough,
                      ylab="num classes", ylim=c(0,4000), breaks=20, labels=TRUE)
h_infreq_class$density =h_infreq_class$counts/sum(h_infreq_class$counts)
sum(h_infreq_class$counts)
plot(h_infreq_class,freq=FALSE,ylim=c(0,1), xlab="Percent Not Wide Enough", 
     ylab="Percent Classes", 
     main="Classes with 5 or fewer elements in the dataset")

h_freq_class = hist(wide_en_bc_wide[wide_en_bc_wide$class_count >=50,]$percent_not_wide_enough,
                    ylab="num classes", ylim=c(0,12000), breaks=20, labels=TRUE)
h_freq_class$density =h_freq_class$counts/sum(h_freq_class$counts)
sum(h_freq_class$counts)
plot(h_freq_class,freq=FALSE,ylim=c(0,1),  xlab="Percent Not Wide Enough", 
     ylab="Percent Classes", 
     main="Classes with 50 or more elements in the dataset")

nrow(wide_en_bc_wide[wide_en_bc_wide$class_count >=50 & wide_en_bc_wide$percent_not_wide_enough ==0,])
# amoung most frequent table of top 5 most frequent classes with errors, order by num False
View(wide_en_bc_wide[wide_en_bc_wide$class_count >=50 & wide_en_bc_wide$percent_not_wide_enough ==1,])

### Tall Enough
h=hist(tall_en_bc_wide$percent_not_tall_enough,
        ylab="num classes", ylim=c(0,12000))
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,0.8), xlab="Percent Elements Not Tall Enough", ylab="Percent Classes", main="Percent of Elements of a Class with Error")

h_infreq_class = hist(tall_en_bc_wide[tall_en_bc_wide$class_count<=5,]$percent_not_tall_enough,
                      ylab="num classes", ylim=c(0,12000), breaks=20)
h_infreq_class$density =h_infreq_class$counts/sum(h_infreq_class$counts)
sum(h_infreq_class$counts)
plot(h_infreq_class,freq=FALSE,ylim=c(0,1), xlab="Percent Not Tall Enough", 
     ylab="Percent Classes", 
     main="Classes with 5 or fewer elements in the dataset")

h_freq_class = hist(tall_en_bc_wide[tall_en_bc_wide$class_count >=50,]$percent_not_tall_enough,
                    ylab="num classes", ylim=c(0,12000), breaks=20)
h_freq_class$density =h_freq_class$counts/sum(h_freq_class$counts)
sum(h_freq_class$counts)
plot(h_freq_class,freq=FALSE,ylim=c(0,1), xlab="Percent Not Tall Enough", 
     ylab="Percent Classes", 
     main="Classes with 50 or more elements in the dataset")

nrow(tall_en_bc_wide[tall_en_bc_wide$class_count >=50 & tall_en_bc_wide$percent_not_tall_enough == 0,])


#####
### Speakable text
### 0 is good, 1 is bad
h =hist(sp_text_bc_wide$percent_speak_text_missing,
     ylab="num classes", ylim=c(0,12000), labels=TRUE)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Speaking Text Missing", ylab="Percent Classes", 
     main="Percent of Widgets of a Class with Speakable Text Missing")

## least frequent class dist
h_infreq_class = hist(sp_text_bc_wide[sp_text_bc_wide$class_count <=5,]$percent_speak_text_missing,
          ylab="num classes", ylim=c(0,12000), breaks=20)
h_infreq_class$density =h_infreq_class$counts/sum(h_infreq_class$counts)
sum(h_infreq_class$counts)
plot(h_infreq_class,freq=FALSE,ylim=c(0,1), labels=TRUE, 
     xlab="Percent Speaking Text Missing", 
     ylab="Percent Classes", 
     main="Classes with 5 or fewer elements in the dataset")

#most frequent class dist
h_freq_class = hist(sp_text_bc_wide[sp_text_bc_wide$class_count >=50,]$percent_speak_text_missing,
                      ylab="num classes", ylim=c(0,12000), breaks=20)
h_freq_class$density =h_freq_class$counts/sum(h_freq_class$counts)
sum(h_freq_class$counts)
plot(h_freq_class,freq=FALSE,ylim=c(0,1), labels=TRUE,
     xlab="Percent Speaking Text Missing", 
     ylab="Percent Classes", 
     main="Classes with 50 or more elements in the dataset")

# amoung most frequent table of top 5 most frequent classes with errors, order by num False
View(sp_text_bc_wide[sp_text_bc_wide$class_count>=50,])

# table of top 5 most likely error
View(sp_text_bc_wide[sp_text_bc_wide$class_count>=50 & sp_text_bc_wide$percent_speak_text_missing==1,])

##########################
####### Ad vs Not
### speakable text
summary(sp_text_bc_wide[sp_text_bc_wide$ad=="True",]$percent_speak_text_missing)
summary(sp_text_bc_wide[sp_text_bc_wide$ad=="False",]$percent_speak_text_missing)
boxplot(sp_text_bc_wide[sp_text_bc_wide$ad=="True",]$percent_speak_text_missing,sp_text_bc_wide[sp_text_bc_wide$ad=="False",]$percent_speak_text_missing)

h =hist(sp_text_bc_wide[sp_text_bc_wide$ad=="True",]$percent_speak_text_missing,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Speaking Text Missing", ylab="Percent Classes", 
     main="Percent of Widgets of an Ad Class with Speakable Text Missing")
h =hist(sp_text_bc_wide[sp_text_bc_wide$ad=="False",]$percent_speak_text_missing,
        ylab="num classes", labels=TRUE)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Speaking Text Missing", ylab="Percent Classes", 
     main="Percent of Widgets of a  Non Ad Class with Speakable Text Missing")

#####################
##### Ad vs Not
nrow(node[node$ad=="True",])
nrow(error_by_class[error_by_class$ad=="True",])



#####################
## Android vs Not
h =hist(sp_text_bc_wide[sp_text_bc_wide$android_widget=="True",]$percent_speak_text_missing,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Speaking Text Missing", ylab="Percent Classes", 
     main="Percent of Widgets of an And Class with Speakable Text Missing")

h =hist(sp_text_bc_wide[sp_text_bc_wide$android_widget=="False",]$percent_speak_text_missing,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Speaking Text Missing", ylab="Percent Classes", 
     main="Percent of Widgets of an Non-Android Class with Speakable Text Missing")

h =hist(wide_en_bc_wide[wide_en_bc_wide$android_widget=="True",]$percent_not_wide_enough,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Not Wide Enough", ylab="Percent Classes", 
     main="Percent of Widgets of an And Class Not Wide Enough")

h =hist(wide_en_bc_wide[wide_en_bc_wide$android_widget=="False",]$percent_not_wide_enough,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Not Wide Enough", ylab="Percent Classes", 
     main="Percent of Widgets of a Not And Class Not Wide Enough")

h =hist(tall_en_bc_wide[tall_en_bc_wide$android_widget=="True",]$percent_not_tall_enough,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Not Wide Enough", ylab="Percent Classes", 
     main="Percent of Widgets of a And Class Not Tall Enough")

h =hist(tall_en_bc_wide[tall_en_bc_wide$android_widget=="False",]$percent_not_tall_enough,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Not Wide Enough", ylab="Percent Classes", 
     main="Percent of Widgets of a Not And Class Not Tall Enough")

## red desc
h =hist(has_red_desc_bc_wide[has_red_desc_bc_wide$android_widget=="True",]$percent_redun,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Redun Desc", ylab="Percent Classes", 
     main="Percent of Widgets of a And Class")
h =hist(has_red_desc_bc_wide[has_red_desc_bc_wide$android_widget=="False",]$percent_redun,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Redun Desc", ylab="Percent Classes", 
     main="Percent of Widgets of a Non And Class")

## shares label
h =hist(shares_label_bc_wide[shares_label_bc_wide$android_widget=="True",]$percent_dup_label,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Shares Label", ylab="Percent Classes", 
     main="Percent of Widgets of a And Class")
h =hist(shares_label_bc_wide[shares_label_bc_wide$android_widget=="False",]$percent_dup_label,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Shares Label", ylab="Percent Classes", 
     main="Percent of Widgets of a Non And Class")

## editable text view w/ cont desc
h =hist(editable_txtvw_w_cont_desc_bc_wide[editable_txtvw_w_cont_desc_bc_wide$android_widget=="True",]$percent_editable_txtvw_w_cont_desc,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Edit TxtView w/ cont desc", ylab="Percent Classes", 
     main="Percent of Widgets of a And Class")
h =hist(editable_txtvw_w_cont_desc_bc_wide[editable_txtvw_w_cont_desc_bc_wide$android_widget=="False",]$percent_editable_txtvw_w_cont_desc,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Edit TxtView w/ cont desc", ylab="Percent Classes", 
     main="Percent of Widgets of a Non And Class")

## fully overlap
h =hist(overlaps_bc_wide[overlaps_bc_wide$android_widget=="True",]$percent_overlapping,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Fully Overlap", ylab="Percent Classes", 
     main="Percent of Widgets of a And Class")
h =hist(overlaps_bc_wide[overlaps_bc_wide$android_widget=="False",]$percent_overlapping,
        ylab="num classes", labels=TRUE, breaks=20)
h$density =h$counts/sum(h$counts)
plot(h,freq=FALSE,ylim=c(0,1.0), labels=TRUE, 
     xlab="Percent Fully Overlap", ylab="Percent Classes", 
     main="Percent of Widgets of a Non And Class")
