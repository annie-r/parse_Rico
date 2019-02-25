##################
###### Libraries

library(plyr) #ddply, rename
library(tidyr) # create wide data table
library(tibble) #add_column

###################
##### Read in data
# unmodified
# node =read.table(file="node_6_1_2018.csv", header=TRUE,
#                     quote="'\"", sep=",",
#                    encoding="UTF-8", fill=FALSE)
## has unmutated class names
node =read.table(file="node_1.2.2019.13.18_unminified_1.8.2019.11.07.csv", header=TRUE,
                 quote="'\"", sep=",",
                 encoding="UTF-8", fill=FALSE)
node[node=="na"] <- NA

#Specialty Nodes, to account for different test exclusion criteria

not_na_size_node = node[node$Element_Tall_Enough!="na" & node$Element_Wide_Enough != "na",]
not_na_size_node = add_column(not_na_size_node, Element_Big_Enough = not_na_size_node$Element_Tall_Enough=="True" & not_na_size_node$Element_Wide_Enough=="True", .after="Element_Tall_Enough")
not_na_size_node = add_column(not_na_size_node, Element_NOT_Big_Enough = not_na_size_node$Element_Tall_Enough=="False" & not_na_size_node$Element_Wide_Enough=="False", .after="Element_Tall_Enough")
not_na_size_node = add_column(not_na_size_node, Element_NOT_Wide_Only = not_na_size_node$Element_Tall_Enough=="True" & not_na_size_node$Element_Wide_Enough=="False", .after="Element_Wide_Enough")
not_na_size_node = add_column(not_na_size_node, Element_NOT_Tall_Only = not_na_size_node$Element_Tall_Enough=="False" & not_na_size_node$Element_Wide_Enough=="True", .after="Element_Tall_Enough")



##### Format data
node$Num_Nodes_Overlap_With = as.numeric(as.character(node$Num_Nodes_Overlap_With))
node$Num_Nodes_Share_Label = as.numeric(as.character(node$Num_Nodes_Share_Label))
node = tibble::add_column(node, Element_Big_Enough = node$Element_Tall_Enough=="True" & node$Element_Wide_Enough=="True", .after="Element_Tall_Enough")
#### investigate errors by class
#########

#######
## Gather information by class
#####

# apps with class not na for size

bc_info_size = table(not_na_size_node$class)
bc_info_size = rename(as.data.frame(bc_info_size), c("Var1"="class","Freq"="class_count"))

tmp = not_na_size_node[, c("app_id","class")]
tmp = unique(tmp)
apps_with_class_size = as.data.frame(table(tmp$class))
apps_with_class_size = rename(apps_with_class_size, c("Var1"="class","Freq"="num_apps_with_class"))
bc_info_size = merge(bc_info_size,apps_with_class_size, by="class")
#View(bc_info_size)

# general
by_class_info = table(node$class)
by_class_info = plyr::rename(as.data.frame(by_class_info), c("Var1"="class","Freq"="class_count"))
#View(by_class_info)

# get the number of apps that have at least one element of a given class that is not na

tmp = node[,c("app_id","class")]
tmp = unique(tmp)
apps_with_class = as.data.frame(table(tmp$class))
apps_with_class = plyr::rename(apps_with_class, c("Var1"="class","Freq"="num_apps_with_class"))
View(apps_with_class)
by_class_info = merge(by_class_info,apps_with_class, by="class")
View(by_class_info)



### if "android widget" and "ad" column
and.widget.classes <- data.frame(unique(node[,c("class","android_widget", "ad")]))
View(and.widget.classes)

by_class_info <- merge(by_class_info, and.widget.classes, by="class")

###################################################################
##################### BY CLASS  Create Data Tables: Error By Class
################################################

############
############ Sp Text 


has_sp_txt_by_class <- as.data.frame(table(node$class,node$Speakable_Text_Present, useNA="no", exclude="na"))
View(sp_text_by_class)
has_sp_txt_by_class = plyr::rename(has_sp_txt_by_class, c("Var1"="class","Var2"="speakable_text_present","Freq"="has_sp_txt_count"))
has_sp_txt_bc_wide = tidyr::spread(has_sp_txt_by_class, speakable_text_present,has_sp_txt_count ) 
has_sp_txt_bc_wide$total = (has_sp_txt_bc_wide$False + has_sp_txt_bc_wide$True)

has_sp_txt_bc_wide = merge(by_class_info, has_sp_txt_bc_wide, by="class")
View(by_class_info)
View(sp_text_bc_wide)
has_sp_txt_bc_wide$percent_sp_txt_missing = has_sp_txt_bc_wide$False/has_sp_txt_bc_wide$total


##########
# ########## Wide Enough
wide_en_by_class = as.data.frame(table(not_na_size_node$class,not_na_size_node$Element_Wide_Enough, useNA="no", exclude="na"))
wide_en_by_class = rename(wide_en_by_class, c("Var1"="class","Var2"="wide_enough","Freq"="wide_enough_count"))
wide_en_bc_wide = spread(wide_en_by_class, wide_enough, wide_enough_count)
wide_en_bc_wide$total = (wide_en_bc_wide$False + wide_en_bc_wide$True)
wide_en_bc_wide = merge(bc_info_size, wide_en_bc_wide, by="class")
wide_en_bc_wide$percent_not_wide_enough = wide_en_bc_wide$False/wide_en_bc_wide$total
View(wide_en_bc_wide)

##########
# ########## Only NOT Wide Enough
not_wide_en_only_by_class = as.data.frame(table(not_na_size_node$class,not_na_size_node$Element_NOT_Wide_Only, useNA="no", exclude="na"))
not_wide_en_only_by_class = plyr::rename(not_wide_en_only_by_class, c("Var1"="class","Var2"="not_wide_enough_only","Freq"="not_wide_enough_only_count"))
not_wide_en_only_bc_wide = tidyr::spread(not_wide_en_only_by_class, not_wide_enough_only, not_wide_enough_only_count)
not_wide_en_only_bc_wide$total = (not_wide_en_only_bc_wide$"FALSE" + not_wide_en_only_bc_wide$"TRUE")
not_wide_en_only_bc_wide = merge(bc_info_size, not_wide_en_only_bc_wide, by="class")
not_wide_en_only_bc_wide$percent_not_wide_enough_only = not_wide_en_only_bc_wide$"TRUE"/not_wide_en_only_bc_wide$total
View(not_wide_en_only_bc_wide)

# ######################
########## Tall Enough
tall_en_by_class = as.data.frame(table(not_na_size_node$class,not_na_size_node$Element_Tall_Enough, useNA="no", exclude="na"))
tall_en_by_class = rename(tall_en_by_class, c("Var1"="class","Var2"="tall_enough","Freq"="tall_enough_count"))
tall_en_bc_wide = spread(tall_en_by_class, tall_enough, tall_enough_count)
tall_en_bc_wide$total = tall_en_bc_wide$True + tall_en_bc_wide$False
tall_en_bc_wide = merge(bc_info_size, tall_en_bc_wide, by="class")
## To match others, this is percent BAD
tall_en_bc_wide$percent_not_tall_enough = tall_en_bc_wide$False/tall_en_bc_wide$total
tall_en_bc_wide = tall_en_bc_wide[tall_en_bc_wide$total>0,]
View(tall_en_bc_wide)

# ######################
########## ONLY NOT Tall Enough
not_tall_en_only_by_class = as.data.frame(table(not_na_size_node$class,not_na_size_node$Element_NOT_Tall_Only, useNA="no", exclude="na"))
not_tall_en_only_by_class = rename(not_tall_en_only_by_class, c("Var1"="class","Var2"="not_tall_en_only","Freq"="not_tall_en_only_count"))
not_tall_en_only_bc_wide = spread(not_tall_en_only_by_class, not_tall_en_only, not_tall_en_only_count)
not_tall_en_only_bc_wide$total = not_tall_en_only_bc_wide$"TRUE" + not_tall_en_only_bc_wide$"FALSE"
not_tall_en_only_bc_wide = merge(bc_info_size, not_tall_en_only_bc_wide, by="class")
## To match others, this is percent BAD
not_tall_en_only_bc_wide$percent_not_tall_en_only = not_tall_en_only_bc_wide$"TRUE"/not_tall_en_only_bc_wide$total
not_tall_en_only_bc_wide = not_tall_en_only_bc_wide[not_tall_en_only_bc_wide$total>0,]


#########################
########### Big enough (how many PASS both height and width)
big_en_by_class = as.data.frame(table(not_na_size_node$class,not_na_size_node$Element_Big_Enough, useNA="no", exclude="na"))
big_en_by_class = rename(big_en_by_class, c("Var1"="class","Var2"="big_enough","Freq"="big_enough_count"))
big_en_bc_wide = spread(big_en_by_class, big_enough, big_enough_count)
big_en_bc_wide$total = big_en_bc_wide$"TRUE" + big_en_bc_wide$"FALSE"
big_en_bc_wide = merge(bc_info_size, big_en_bc_wide, by="class")
## To match others, this is percent BAD
big_en_bc_wide$percent_not_big_enough = big_en_bc_wide$"FALSE"/big_en_bc_wide$total
big_en_bc_wide = big_en_bc_wide[big_en_bc_wide$total>0,]
View(big_en_bc_wide)

#########################
########### NOT Big enough (how many fail BOTH height and width)
not_big_en_by_class = as.data.frame(table(not_na_size_node$class,not_na_size_node$Element_NOT_Big_Enough, useNA="no", exclude="na"))
not_big_en_by_class = rename(not_big_en_by_class, c("Var1"="class","Var2"="not_big_enough","Freq"="not_big_enough_count"))
not_big_en_bc_wide = spread(not_big_en_by_class, not_big_enough, not_big_enough_count)
not_big_en_bc_wide$total = not_big_en_bc_wide$"TRUE" + not_big_en_bc_wide$"FALSE"
not_big_en_bc_wide = merge(bc_info_size, not_big_en_bc_wide, by="class")
## To match others, this is percent BAD
not_big_en_bc_wide$percent_not_big_enough = not_big_en_bc_wide$"TRUE"/not_big_en_bc_wide$total
not_big_en_bc_wide = not_big_en_bc_wide[not_big_en_bc_wide$total>0,]



###### TALL VS WIDE
tall_vs_wide = merge(tall_en_bc_wide[,c("class","percent_not_tall_enough")],wide_en_bc_wide[,c("class","percent_not_wide_enough")], by="class")
tall_vs_wide$slope = tall_vs_wide$percent_not_tall_enough/tall_vs_wide$percent_not_wide_enough
tall_vs_wide = merge(tall_vs_wide,bc_info_size[,c("class","num_apps_with_class")], by="class")

#############
######## Has redundant desc 
has_red_desc_class = as.data.frame(table(node$class,node$Has_Redundant_Description, useNA="no", exclude="na"))
has_red_desc_class = rename(has_red_desc_class, c("Var1"="class","Var2"="has_red_desc","Freq"="has_red_desc_count"))
has_red_desc_bc_wide = spread(has_red_desc_class, has_red_desc, has_red_desc_count)
has_red_desc_bc_wide$total = has_red_desc_bc_wide$True + has_red_desc_bc_wide$False
has_red_desc_bc_wide = merge(by_class_info, has_red_desc_bc_wide, by="class")
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
shares_label_bc_wide = merge(by_class_info, shares_label_bc_wide, by="class")
shares_label_bc_wide$percent_dup_label = shares_label_bc_wide$True/shares_label_bc_wide$total
View(shares_label_bc_wide)

#############
######## Editable Textview With Cont Desc
editable_txtview_w_cont_desc = as.data.frame(table(node$class,node$Editable_Textview_With_Cont_Desc, useNA="no", exclude="na"))
editable_txtview_w_cont_desc = rename(editable_txtview_w_cont_desc, c("Var1"="class","Var2"="is_ed_txt_w_cont_desc","Freq"="ed_txtvw_w_cont_desc_count"))
editable_txtvw_w_cont_desc_bc_wide = spread(editable_txtview_w_cont_desc, is_ed_txt_w_cont_desc, ed_txtvw_w_cont_desc_count)
editable_txtvw_w_cont_desc_bc_wide$total = editable_txtvw_w_cont_desc_bc_wide$True + editable_txtvw_w_cont_desc_bc_wide$False
editable_txtvw_w_cont_desc_bc_wide = merge(by_class_info, editable_txtvw_w_cont_desc_bc_wide, by="class")
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
overlaps_bc_wide = merge(by_class_info, overlaps_bc_wide, by="class")
overlaps_bc_wide$percent_overlapping = overlaps_bc_wide$True/overlaps_bc_wide$total
View(overlaps_bc_wide)


##########################################
################# BY APP 
###################################

#####
############## Missing Speakable Text
has_sp_text = as.data.frame(table(node[,c("app_id","Speakable_Text_Present")]))
has_sp_text_wide = tidyr::spread(has_sp_text, Speakable_Text_Present, Freq)
has_sp_text_wide = plyr::rename(has_sp_text_wide, c("False"="Missing Speakable Text", "True"="Has Speakable Text"))
has_sp_text_wide$total = has_sp_text_wide$`Missing Speakable Text` + has_sp_text_wide$`Has Speakable Text` 
has_sp_text_wide$prop_missing_sp_text = has_sp_text_wide$`Missing Speakable Text`/has_sp_text_wide$total

######
############### Size

#### not tall enough
View(node)
tall_en = as.data.frame(table(not_na_size_node[,c("app_id","Element_Tall_Enough")]))
View(tall_en)
tall_en_ba_wide = spread(tall_en, Element_Tall_Enough,Freq )
tall_en_ba_wide = rename(tall_en_ba_wide, c("False"="Not Tall Enough", "True"="Tall Enough"))
tall_en_ba_wide$Total = tall_en_ba_wide$`Not Tall Enough` + tall_en_ba_wide$`Tall Enough`
tall_en_ba_wide$Prop_Not_Tall_Enough = tall_en_ba_wide$`Not Tall Enough`/tall_en_ba_wide$Total
View(tall_en_ba_wide)

#### not tall enough ONLY
not_tall_en_only = as.data.frame(table(not_na_size_node[,c("app_id","Element_NOT_Tall_Only")]))
not_tall_en_only_ba_wide = spread(not_tall_en_only, Element_NOT_Tall_Only,Freq )
not_tall_en_only_ba_wide = rename(not_tall_en_only_ba_wide, c("FALSE"="Tall Enough", "TRUE"="Not Tall Enough Only"))
not_tall_en_only_ba_wide$Total = not_tall_en_only_ba_wide$`Tall Enough` + not_tall_en_only_ba_wide$`Not Tall Enough Only`
not_tall_en_only_ba_wide$Prop_Not_Tall_Enough = not_tall_en_only_ba_wide$`Not Tall Enough Only`/not_tall_en_only_ba_wide$Total

#### not wide enough
View(not_na_size_node)
wide_en = as.data.frame(table(not_na_size_node[,c("app_id","Element_Wide_Enough")]))
wide_en_ba_wide = spread(wide_en, Element_Wide_Enough,Freq )
wide_en_ba_wide = rename(wide_en_ba_wide, c("False"="Not Wide Enough", "True"="Wide Enough"))
wide_en_ba_wide$Total = wide_en_ba_wide$`Not Wide Enough` + wide_en_ba_wide$`Wide Enough`
wide_en_ba_wide$Prop_Not_Wide_Enough = wide_en_ba_wide$`Not Wide Enough`/wide_en_ba_wide$Total
View(wide_en_ba_wide)

#### not wide enough ONLY
View(not_na_size_node)
not_wide_en_only = as.data.frame(table(not_na_size_node[,c("app_id","Element_NOT_Wide_Only")]))
not_wide_en_only_ba_wide = spread(not_wide_en_only, Element_NOT_Wide_Only,Freq )
not_wide_en_only_ba_wide = rename(not_wide_en_only_ba_wide, c("FALSE"="Wide Enough", "TRUE"="Only Not Wide Enough"))
not_wide_en_only_ba_wide$Total = not_wide_en_only_ba_wide$`Wide Enough` + not_wide_en_only_ba_wide$`Only Not Wide Enough`
not_wide_en_only_ba_wide$Prop_Not_Wide_Enough_Only = not_wide_en_only_ba_wide$`Only Not Wide Enough`/not_wide_en_only_ba_wide$Total
View(not_wide_en_only_ba_wide)

#### not not big enough (fails either width, height, or both)
View(not_na_size_node)
big_en = as.data.frame(table(not_na_size_node[,c("app_id","Element_Big_Enough")]))
big_en_ba_wide = spread(big_en, Element_Big_Enough,Freq )
big_en_ba_wide = rename(big_en_ba_wide, c("FALSE"="Not Big Enough", "TRUE"="Big Enough"))
big_en_ba_wide$Total = big_en_ba_wide$`Not Big Enough` + big_en_ba_wide$`Big Enough`
big_en_ba_wide$Prop_Not_Big_Enough = big_en_ba_wide$`Not Big Enough`/big_en_ba_wide$Total
View(big_en_ba_wide)

#### NOT big enough (fails both height and width), TRUE when BOTH FALSE
View(not_na_size_node)
not_big_en = as.data.frame(table(not_na_size_node[,c("app_id","Element_NOT_Big_Enough")]))
not_big_en_ba_wide = spread(not_big_en, Element_NOT_Big_Enough,Freq )
not_big_en_ba_wide = rename(not_big_en_ba_wide, c("TRUE"="Not Big Enough", "FALSE"="Big Enough"))
not_big_en_ba_wide$Total = not_big_en_ba_wide$`Not Big Enough` + not_big_en_ba_wide$`Big Enough`
not_big_en_ba_wide$Prop_Not_Big_Enough = not_big_en_ba_wide$`Not Big Enough`/not_big_en_ba_wide$Total
View(not_big_en_ba_wide)

######################
#############################
########## WITHIN APP BY-CLASS
#####################
###############################

#####
## Missing Label
app_class_count_lab = dplyr::group_by(node, app_id, class) %>%
  dplyr::summarise(Freq = n())
app_class_count_lab = plyr::rename(as.data.frame(app_class_count_lab), c("Freq"="total_element_count"))

has_sp_txt_bc_wa <-  node %>% dplyr::group_by(app_id, class,Speakable_Text_Present) %>%
 dplyr::summarise(Freq = n())

has_sp_txt_bc_wa = merge(has_sp_txt_bc_wa,app_class_count_lab, by=c("app_id","class"))
has_sp_txt_bc_wa_wide = tidyr::spread(has_sp_txt_bc_wa, Speakable_Text_Present,Freq ) 
has_sp_txt_bc_wa_wide[is.na(has_sp_txt_bc_wa_wide)] = 0
has_sp_txt_bc_wa_wide$prop_missing_sp_txt = has_sp_txt_bc_wa_wide$"False"/has_sp_txt_bc_wa_wide$total_element_count
View(has_sp_txt_bc_wa_wide)

#####
## SIZE


app_class_count = dplyr::group_by(not_na_size_node,app_id, class) %>%
  dplyr::summarise(Freq = n())
app_class_count <- plyr::rename(as.data.frame(app_class_count), c("Freq"="total_element_count"))


## Not Big Enough (either)
big_en_bc_wa <-  not_na_size_node %>% dplyr::group_by(app_id, class,Element_Big_Enough) %>%
  dplyr::summarise(Freq = n())

big_en_bc_wa = merge(big_en_bc_wa,app_class_count, by=c("app_id","class"))
big_en_bc_wa_wide = tidyr::spread(big_en_bc_wa, Element_Big_Enough,Freq ) 
big_en_bc_wa_wide[is.na(big_en_bc_wa_wide)] = 0
big_en_bc_wa_wide$prop_not_big_en_either = big_en_bc_wa_wide$"FALSE"/big_en_bc_wa_wide$total_element_count
View(big_en_bc_wa_wide)
## Not Big Enough (both dimen)
not_big_en_bc_wa <-  not_na_size_node %>% dplyr::group_by(app_id, class,Element_NOT_Big_Enough) %>%
  dplyr::summarise(Freq = n())

not_big_en_bc_wa = merge(not_big_en_bc_wa,app_class_count, by=c("app_id","class"))
not_big_en_bc_wa_wide = tidyr::spread(not_big_en_bc_wa, Element_NOT_Big_Enough,Freq ) 
not_big_en_bc_wa_wide[is.na(not_big_en_bc_wa_wide)] = 0

not_big_en_bc_wa_wide$prop_NOT_big_en = not_big_en_bc_wa_wide$"TRUE"/not_big_en_bc_wa_wide$total_element_count
View(not_big_en_bc_wa_wide)

## Not Tall Enough Only
not_tall_en_bc_wa = not_na_size_node %>% dplyr::group_by(app_id, class,Element_NOT_Tall_Only) %>%
  dplyr::summarise(Freq = n())

not_tall_en_bc_wa = merge(not_tall_en_bc_wa,app_class_count, by=c("app_id","class"))
not_tall_en_bc_wa_wide = spread(not_tall_en_bc_wa, Element_NOT_Tall_Only, Freq)
not_tall_en_bc_wa_wide[is.na(not_tall_en_bc_wa_wide)] = 0
not_tall_en_bc_wa_wide$prop_NOT_tall_only = not_tall_en_bc_wa_wide$"TRUE"/not_tall_en_bc_wa_wide$total_element_count


#############################################
##################### ANLAYSIS (PLOTS and SUB-TABLES)
############################################
####### For percents, higher percent should be higher percent BAD


######################
###### Label
#############

###
### Missing speakable text

## by app
h=hist(has_sp_text_wide$prop_missing_sp_text*100,
       ylab="Number of Apps",
       ylim=c(0,6000),
       xlab="Proportion Elements Missing Speakable Text",
       main = "Proportion of Elements in App Missing Label",
       breaks = c(1*10:10),
       labels=TRUE)

## top 1% reuse, 
top_one_per = nrow(has_sp_txt_bc_wide)*.01
View(has_sp_txt_bc_wide[order(has_sp_txt_bc_wide$num_apps_with_class, decreasing=TRUE),][1:top_one_per,])

## filter class, by app
## FAB, image button, image
tmp = has_sp_txt_bc_wa_wide[has_sp_txt_bc_wa_wide$class=="android.widget.ImageView" |
                              has_sp_txt_bc_wa_wide$class=="android.widget.ImageButton" | 
                              has_sp_txt_bc_wa_wide$class=="android.support.design.widget.FloatingActionButton",]
h=hist(tmp$prop_missing_sp_txt,
       ylab="Number of Apps",
       ylim=c(0,6000),
       xlab="Proportion Elements Missing Speakable Text",
       main = "ImageViews, ImageButtons, and FABS in App Missing Label",
       breaks = c(1*10:10),
       labels=TRUE)

h=hist(has_sp_txt_bc_wa_wide[has_sp_txt_bc_wa_wide$class=="android.widget.ImageView" ,]$prop_missing_sp_txt,
       ylab="Number of Apps",
       ylim=c(0,6000),
       xlab="Proportion Elements Missing Speakable Text",
       main = "ImageViews in App Missing Label",
       breaks = c(1*10:10),
       labels=TRUE)


h=hist(has_sp_txt_bc_wa_wide[has_sp_txt_bc_wa_wide$class=="android.widget.ImageButton" ,]$prop_missing_sp_txt,
       ylab="Number of Apps",
       ylim=c(0,6000),
       xlab="Proportion Elements Missing Speakable Text",
       main = "ImageButtons in App Missing Label",
       breaks = c(1*10:10),
       labels=TRUE)


h=hist(has_sp_txt_bc_wa_wide[has_sp_txt_bc_wa_wide$class=="android.support.design.widget.FloatingActionButton" ,]$prop_missing_sp_txt,
       ylab="Number of Apps",
       ylim=c(0,6000),
       xlab="Proportion Elements Missing Speakable Text",
       main = "FABS in App Missing Label",
       breaks = c(1*10:10),
       labels=TRUE)
######################
###### Size
#############

###
### Not Wide Enough

## by class
h =hist(wide_en_bc_wide$percent_not_wide_enough,
        ylab="Number of Classes", 
        ylim=c(0,10000), 
        xlab="Proportion Elements Not Wide Enough",
        main = "Proportion Not Wide Enough by Class",
        breaks = c(.1*0:10),
        labels=TRUE)

# popular, high error, sort by num apps
View(wide_en_bc_wide[wide_en_bc_wide$percent_not_wide_enough>=.90,])
View(wide_en_bc_wide[wide_en_bc_wide$percent_not_wide_enough<=.10,])
# popular, sort by num apps
View(wide_en_bc_wide)

## by app
h=hist(wide_en_ba_wide$Prop_Not_Wide_Enough,
       ylab="Number of Apps",
       ylim=c(0,6000),
       xlab="Proportion Elements Not Wide Enough",
       main = "Proportion of Elements in App Not Wide Enough",
       breaks = c(.1*0:10),
       labels=TRUE)

###
### Not WIDE Enough ONLY

## by class
h =hist(not_wide_en_only_bc_wide$percent_not_wide_enough_only,
        ylab="Number of Classes", 
        xlab="Proportion Elements Not Wide Enough Only",
        main = "Proportion Not Wide Enough Only by Class",
        breaks = c(.1*0:10),
        labels=TRUE)

## by app
h=hist(not_wide_en_only_ba_wide$Prop_Not_Wide_Enough_Only,
       ylab="Number of Apps",
       ylim=c(0,10000),
       xlab="Proportion Elements Not Wide Enough Only",
       main = "Proportion of Elements in App Not Wide Enough",
       breaks = c(.1*0:10),
       labels=TRUE)

View(not_wide_en_only_bc_wide[order(not_wide_en_only_bc_wide$num_apps_with_class, decreasing=TRUE),][1:107,])

## top 1% reuse, top error prone
top_one_per = nrow(not_wide_en_only_bc_wide)*.01 #105
View(not_wide_en_only_bc_wide[order(not_wide_en_only_bc_wide$num_apps_with_class, decreasing=TRUE),][1:top_one_per,])


##
### Not Tall Enough

## by class
h=hist(tall_en_bc_wide$percent_not_tall_enough,
       ylab="Number of Classes", 
       ylim=c(0,10000), 
       xlab="Proportion Elements Not Tall Enough",
       main = "Proportion of Elements of Class Not Tall Enough",
       breaks = c(.1*0:10),
       labels=TRUE)
h=hist(tall_en_bc_wide$percent_not_tall_enough)

# popular, high error, sort by num apps
View(tall_en_bc_wide[tall_en_bc_wide$percent_not_tall_enough>=.90,])
# popular, sort by num apps
View(tall_en_bc_wide)


## highest num apps, highest percent error

tall_en_high_cl_bc = tall_en_bc_wide[tall_en_high_cl_bc$num_apps_with_class>1000,c("class","num_apps_with_class","percent_not_tall_enough", "False", "True","total")]
View(tall_en_high_cl_bc)
  hist(tall_en_bc_wide[tall_en_bc_wide$num_apps_with_class >100,]$percent_not_tall_enough,
                    ylab="num classes",
                    breaks = c(.1*0:10)
          )

## by app
h=hist(tall_en_ba_wide$Prop_Not_Tall_Enough,
       ylab="Number of Apps", 
       ylim=c(0,6000), 
       xlab="Proportion Elements Not Tall Enough",
       main = "Proportion of Elements of App Not Tall Enough",
       breaks = c(.1*0:10),
       labels=TRUE)

##
### NOT tall enough ONLY
## by class
h=hist(not_tall_en_only_bc_wide$percent_not_tall_en_only,
       ylab="Number of Classes", 
       ylim=c(0,10000), 
       xlab="Proportion Elements Not Tall Enough Only",
       main = "Proportion of Elements of Class Not Tall Enough Only",
       breaks = c(.1*0:10),
       labels=TRUE)

## by app
h = hist(not_tall_en_only_ba_wide$Prop_Not_Tall_Enough,
         ylab="Number of Apps", 
         ylim=c(0,10000), 
         xlab="Proportion Elements Not Tall Enough Only",
         main = "Proportion of Elements of App Not Tall Enough Only",
         breaks = c(.1*0:10),
         labels=TRUE)

## top 1% reuse, top error prone
top_one_per = nrow(not_tall_en_only_bc_wide)*.01 #105
View(not_tall_en_only_bc_wide[order(not_tall_en_only_bc_wide$num_apps_with_class, decreasing=TRUE),][1:top_one_per,])


## case studies class by app
 


h=hist(not_tall_en_bc_wa_wide[not_tall_en_bc_wa_wide$class=="android.widget.Button",]$prop_NOT_tall_only*100,
       ylab="Number of Apps (out of 3,944)", 
       ylim=c(0,4000), 
       xlab="Percent Elements Not Tall Enough Only",
       main = "Button not Tall Enough Only By App",
       breaks = c(1*10:10),
       labels=TRUE)
h=hist(not_tall_en_bc_wa_wide[not_tall_en_bc_wa_wide$class=="android.widget.ImageButton",]$prop_NOT_tall_only*100,
       ylab="Number of Apps (out of 4,063)", 
       ylim=c(0,4000), 
       xlab="Percent of Elements Not Tall Enough Only",
       main = "Image Button not Tall Enough Only By App",
       breaks = c(1*10:10),
       labels=TRUE)

btn_not_tall_only = not_na_size_node[not_na_size_node$class=="android.widget.Button" & not_na_size_node$Element_NOT_Tall_Only==TRUE,]
#floor(runif(5, min=0, nrow(btn_not_tall_only)))
# 32353 26141 29422 17251 30318
View(btn_not_tall_only[c(32353, 26141, 29422, 17251, 30318),])
btn_not_not_tall_only = not_na_size_node[not_na_size_node$class=="android.widget.Button" & not_na_size_node$Element_NOT_Tall_Only==FALSE,]
#floor(runif(5, min=0, nrow(btn_not_not_tall_only)))
# 24482 88754 98263 50253 31375
View(btn_not_not_tall_only[c(24482, 88754, 98263, 50253, 31375),])




tmp = not_tall_en_bc_wa_wide[not_tall_en_bc_wa_wide$class=="android.widget.ImageButton" |
                               not_tall_en_bc_wa_wide$class=="android.widget.Button",]
library(plyr)
tmp = rename(tmp, c("TRUE"="True", "FALSE"="False"))
btn_not_tall_bc_wa_wide = cbind(aggregate(total_element_count~app_id, sum, data=tmp))
t =  cbind(aggregate(True~app_id, sum, data=tmp))
btn_not_tall_bc_wa_wide = merge(btn_not_tall_bc_wa_wide, t, by="app_id")
t =  cbind(aggregate(False~app_id, sum, data=tmp))
btn_not_tall_bc_wa_wide = merge(btn_not_tall_bc_wa_wide, t, by="app_id")
btn_not_tall_bc_wa_wide$prop_not_tall_en = btn_not_tall_bc_wa_wide$True/btn_not_tall_bc_wa_wide$total_element_count
#6291 apps
h=hist(btn_not_tall_bc_wa_wide$prop_not_tall_en,
       ylab="Number of Apps", 
       ylim=c(0,6500), 
       xlab="Proportion Elements Not Tall Enough Only",
       main = "(Image) Button not Tall Enough By App",
       breaks = c(.1*0:10),
       labels=TRUE)

h=hist(not_tall_en_bc_wa_wide[not_tall_en_bc_wa_wide$class=="android.widget.RelativeLayout",]$prop_NOT_tall_only,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Tall Enough Only",
       main = "Relative Layout not Tall Enough By App",
       breaks = c(.1*0:10),
       labels=TRUE)
h=hist(not_tall_en_bc_wa_wide[not_tall_en_bc_wa_wide$class=="android.widget.LinearLayout",]$prop_NOT_tall_only,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Tall Enough Only",
       main = "Linear Layout not Tall Enough By App",
       breaks = c(.1*0:10),
       labels=TRUE)

h=hist(not_tall_en_bc_wa_wide[not_tall_en_bc_wa_wide$class=="android.widget.ListView",]$prop_NOT_tall_only,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Tall Enough Only",
       main = "List View not Tall Enough By App",
       breaks = c(.1*0:10),
       labels=TRUE)


View(not_tall_en_only_bc_wide[order(not_tall_en_only_bc_wide$num_apps_with_class, decreasing=TRUE),][1:107,])

##
### Not Big Enough in either dimension

## by class
#hist
h=hist(big_en_bc_wide$percent_not_big_enough,
       ylab="Number of Classes", 
       ylim=c(0,10000), 
       xlab="Proportion Elements By Class Not Big Enough",
       main = "Proportion of Elements of Class Not Big Enough in Either Dimension",
       breaks = c(.1*0:10),
       labels=TRUE)

#by app
h=hist(big_en_ba_wide$Prop_Not_Big_Enough,
       ylab="Number of Apps", 
       ylim=c(0,10000), 
       xlab="Proportion Elements By App Not Big Enough",
       main = "Proportion of Elements of App Not Big Enough in Either Dimension",
       breaks = c(.1*0:10),
       labels=TRUE)

#by app of specific classes

h=hist(big_en_bc_wa_wide[big_en_bc_wa_wide$class=="android.widget.RadioButton",]$prop_not_big_en_either*100,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Big Enough (either)",
       main = "Radio Button not Big Enough By App",
       breaks = c(1*10:10),
       labels=TRUE)

h=hist(big_en_bc_wa_wide[big_en_bc_wa_wide$class=="android.widget.ImageButton",]$prop_not_big_en_either*100,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Big Enough (either)",
       main = "Image Button not Big Enough By App",
       breaks = c(1*10:10),
       labels=TRUE)

h=hist(big_en_bc_wa_wide[big_en_bc_wa_wide$class=="android.widget.Button",]$prop_not_big_en_either*100,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Big Enough (either)",
       main = "Button not Big Enough By App",
       breaks = c(1*10:10),
       labels=TRUE)

## top 1% reuse, top error prone
top_one_per = nrow(big_en_bc_wide)*.01 #105
View(big_en_bc_wide[order(big_en_bc_wide$num_apps_with_class, decreasing=TRUE),][1:top_one_per,])

#combine image button and button
tmp = big_en_bc_wa_wide[big_en_bc_wa_wide$class=="android.widget.ImageButton" |
                               big_en_bc_wa_wide$class=="android.widget.Button",]
library(plyr)
tmp = rename(tmp, c("TRUE"="True", "FALSE"="False"))
btn_big_bc_wa_wide = cbind(aggregate(total_element_count~app_id, sum, data=tmp))
t =  cbind(aggregate(True~app_id, sum, data=tmp))
btn_big_bc_wa_wide = merge(btn_big_bc_wa_wide, t, by="app_id")
t =  cbind(aggregate(False~app_id, sum, data=tmp))
btn_big_bc_wa_wide = merge(btn_big_bc_wa_wide, t, by="app_id")
btn_big_bc_wa_wide$prop_not_big_en_either = btn_big_bc_wa_wide$False/btn_big_bc_wa_wide$total_element_count

h=hist(btn_big_bc_wa_wide$prop_not_big_en_either*100,
       ylab="Number of Apps (out of 6291)", 
       ylim=c(0,4000), 
       xlab="Percent Elements Not Big Enough Either Dimen",
       main = "(Image) Button not Big Enough (either) By App",
       breaks = c(1*10:10),
       labels=TRUE)

# popular, high error, sort by num apps
View(big_en_bc_wide[big_en_bc_wide$percent_not_big_enough>=.90,])
# popular, sort by num apps
View(big_en_bc_wide)



## by app
h=hist(big_en_ba_wide$Prop_Not_Big_Enough,
       ylab="Number of Apps", 
       ylim=c(0,6000), 
       xlab="Proportion Elements Not Big Enough",
       main = "Proportion of Elements of App Not Big Enough",
       breaks = c(.1*0:10),
       labels=TRUE)

##
### Not Big Enough in both dimension
h=hist(not_tall_en_bc_wa_wide[not_tall_en_bc_wa_wide$class=="android.widget.ListView",]$prop_NOT_tall_only,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Tall Enough Only",
       main = "List View not Tall Enough By App",
       breaks = c(.1*0:10),
       labels=TRUE)

## by class
#hist
h=hist(not_big_en_bc_wide$percent_not_big_enough,
       ylab="Number of Classes", 
       ylim=c(0,10000), 
       xlab="Proportion Elements Not Big Enough",
       main = "Proportion of Elements of Class Not Big Enough in Both Dimension",
       breaks = c(.1*0:10),
       labels=TRUE)

#by app
h=hist(not_big_en_ba_wide$Prop_Not_Big_Enough,
       ylab="Number of Apps", 
       ylim=c(0,10000), 
       xlab="Proportion Elements Not Big Enough",
       main = "Proportion of Elements of App Not Big Enough in Both Dimension",
       breaks = c(.1*0:10),
       labels=TRUE)

# class prop not big enough by num apps
## filtered class, by app
h=hist(not_big_en_bc_wa_wide[not_big_en_bc_wa_wide$class=="android.widget.CheckBox",]$prop_NOT_big_en*100,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Big Enough",
       main = "CheckBox not Big Enough By App",
       breaks = c(1*10:10),
       labels=TRUE)

h=hist(not_big_en_bc_wa_wide[not_big_en_bc_wa_wide$class=="android.widget.ImageButton",]$prop_NOT_big_en*100,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Big Enough",
       main = "Image Button not Big Enough By App",
       breaks = c(1*10:10),
       labels=TRUE)
img_btn_not_big = not_na_size_node[not_na_size_node$class=="android.widget.ImageButton" & not_na_size_node$Element_NOT_Big_Enough==TRUE,]
#floor(runif(5, min=0, nrow(img_btn_not_big)))
# 7385  1740 34218 26858 34158 9348 15492
View(img_btn_not_big[c(7385,  1740, 34218, 26858, 34158,9348, 15492),])
img_btn_big = not_na_size_node[not_na_size_node$class=="android.widget.ImageButton" & not_na_size_node$Element_NOT_Big_Enough==FALSE,]
#floor(runif(5, min=0, nrow(img_btn_big)))
# 30499 94505 84581 44597 84531
View(img_btn_big[c(30499, 94505, 84581, 44597, 84531),])


h=hist(not_big_en_bc_wa_wide[not_big_en_bc_wa_wide$class=="android.widget.Button",]$prop_NOT_big_en*100,
       ylab="Number of Apps", 
       ylim=c(0,4000), 
       xlab="Proportion Elements Not Big Enough",
       main = "Button not Big Enough By App",
       breaks = c(1*10:10),
       labels=TRUE)


# popular, high error, sort by num apps
View(not_big_en_bc_wide[big_en_bc_wide$percent_not_big_enough>=.90,])
# popular, sort by num apps
View(not_big_en_bc_wide)

#popular, high error: top 1% (105) of classes of reuse, then order by error rate
top_one_per = nrow(not_big_en_bc_wide)*0.01
View(not_big_en_bc_wide[order(not_big_en_bc_wide$num_apps_with_class, decreasing=TRUE),][1:top_one_per,])


## WHERE CHECKBOXES AND SWITCHES SHOW UP!!!!
View(not_big_en_bc_wide[not_big_en_bc_wide$num_apps_with_class>50,])

## by app
h=hist(not_big_en_ba_wide$Prop_Not_Big_Enough,
       ylab="Number of Apps", 

       xlab="Proportion Elements Not Big Enough",
       main = "Proportion of Elements of App Not Big Enough in Both Dimensions",
       breaks = c(.1*0:10),
       labels=TRUE)



##################################################
############################################
################ CASE STUDIES 
##########################################
#######################################

###################################
############## Switches

######### size
no_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.widget.ToggleButton" & not_na_size_node$Element_NOT_Big_Enough==TRUE,]
# get rand 5, keep for rep
# floor(runif(5, min=0, nrow(no_wide_no_tall)))
#  1339  651 1424 4215  190
View(no_wide_no_tall[c(1339,651,1424,4215,190),])

no_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.SwitchCompat" & not_na_size_node$Element_NOT_Wide_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(no_wide_yes_tall)))
# 4 32 55 77 46
View(no_wide_yes_tall[c(4,32,55,77,46),])
View(no_wide_yes_tall[no_wide_yes_tall$app_id=="com.ichi2.anki",])

yes_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.SwitchCompat" & not_na_size_node$Element_NOT_Tall_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(yes_wide_no_tall)))
# more since a lot had problems finding
# 1063 1477  704 1350 1102, 608, 368
View(yes_wide_no_tall[c(1063,1477,704,1350,1102, 608,368),])

yes_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.SwitchCompat" & not_na_size_node$Element_Big_Enough==TRUE,]
floor(runif(5, min=0, nrow(yes_wide_yes_tall)))
#  1042  474 1083  467   95
View(yes_wide_yes_tall[c(1042,474,1083,467,95),])

###################################
############## Toggle Buttons

######### size
no_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.widget.ToggleButton" & not_na_size_node$Element_NOT_Big_Enough==TRUE,]
# get rand 5, keep for rep
# floor(runif(5, min=0, nrow(no_wide_no_tall)))
#  1339  651 1424 4215  190
View(no_wide_no_tall[c(1339,651,1424,4215,190),])

no_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.widget.ToggleButton" & not_na_size_node$Element_NOT_Wide_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(no_wide_yes_tall)))
# 70 71 14 26 55
View(no_wide_yes_tall[c(70,71,14,26,55),])

yes_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.widget.ToggleButton" & not_na_size_node$Element_NOT_Tall_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(yes_wide_no_tall)))
# 2109  241 2671  767 2728
View(yes_wide_no_tall[c(2109,241,2671,767,2728),])

yes_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.widget.ToggleButton" & not_na_size_node$Element_Big_Enough==TRUE,]
floor(runif(5, min=0, nrow(yes_wide_yes_tall)))
#  3845 1748 3653 1380 6262
View(yes_wide_yes_tall[c(3845,1748,916,1380,6262),])



###################################
############## CheckBoxes

######### size
no_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.AppCompatCheckBox" & not_na_size_node$Element_NOT_Big_Enough==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(no_wide_no_tall)))
#   167  249 1754 1655 4449
View(no_wide_no_tall[c(167,249,1754,1655,4449),])

no_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.widget.CheckBox" & not_na_size_node$Element_NOT_Big_Enough==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(no_wide_no_tall)))
#   2675 2159 4106 4749 1329
View(no_wide_no_tall[c(2675, 215,9, 4106, 4749),])

yes_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.AppCompatCheckBox" & not_na_size_node$Element_Big_Enough==TRUE,]
floor(runif(5, min=0, nrow(yes_wide_yes_tall)))
#  318 827 267 583 238
View(yes_wide_yes_tall[c(318,827,267,583,238),])

yes_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.widget.CheckBox" & not_na_size_node$Element_Big_Enough==TRUE,]
floor(runif(5, min=0, nrow(yes_wide_yes_tall)))
#  394 1739  790  196  840
View(yes_wide_yes_tall[c(394, 1739,  790,  196,  840),])


no_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.AppCompatCheckBox" & not_na_size_node$Element_NOT_Wide_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(no_wide_yes_tall)))
# 117  83 245 543 393
View(no_wide_yes_tall[c(117,83,245,543,393),])

no_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.widget.CheckBox" & not_na_size_node$Element_NOT_Wide_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(no_wide_yes_tall)))
# 760 983 486 535 975
View(no_wide_yes_tall[c(760, 983, 486, 535, 975),])

yes_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.AppCompatCheckBox" & not_na_size_node$Element_NOT_Tall_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(yes_wide_no_tall)))
# 3563  842 3029 1225 1468
View(yes_wide_no_tall[c(3563,842,3029,1225,1468),])

yes_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.widget.CheckBox" & not_na_size_node$Element_NOT_Tall_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(yes_wide_no_tall)))
# 236 3242 2740  226 1046
View(yes_wide_no_tall[c(236, 3242, 2740,  226, 1046),])

###################################
############## Radio Button

######### size
no_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.widget.ToggleButton" & not_na_size_node$Element_NOT_Big_Enough==TRUE,]
# get rand 5, keep for rep
# floor(runif(5, min=0, nrow(no_wide_no_tall)))
#  1339  651 1424 4215  190
View(no_wide_no_tall[c(1339,651,1424,4215,190),])

no_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.AppCompatRadioButton" & not_na_size_node$Element_NOT_Wide_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(no_wide_yes_tall)))
# 6 138  51 134  69
View(no_wide_yes_tall[c(6, 138 , 51, 134,  69),])


yes_wide_no_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.SwitchCompat" & not_na_size_node$Element_NOT_Tall_Only==TRUE,]
# get rand 5, keep for rep
floor(runif(5, min=0, nrow(yes_wide_no_tall)))
# more since a lot had problems finding
# 1063 1477  704 1350 1102, 608, 368
View(yes_wide_no_tall[c(1063,1477,704,1350,1102, 608,368),])

yes_wide_yes_tall = not_na_size_node[not_na_size_node$class=="android.support.v7.widget.SwitchCompat" & not_na_size_node$Element_Big_Enough==TRUE,]
floor(runif(5, min=0, nrow(yes_wide_yes_tall)))
#  1042  474 1083  467   95
View(yes_wide_yes_tall[c(1042,474,1083,467,95),])
