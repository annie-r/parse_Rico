## By Nodes
library(plyr) #ddply, rename
library(tidyr) # create wide data table

#### BEWARE POS GOOD OR BAD CHANGES PER ERROR



summary(node)


node$android_widget = as.factor(node$android_widget)
nrow(node)
percent_andr_widget = nrow(node[node$android_widget=="True",])/nrow(node)

summary(node$android_widget)
percent_andr_widget
subset_vars = c("android_widget","Speakable_Text_Present")
sub_table <- node[subset_vars]
View(sub_table)


### simple stats


### Tables exploring if Android Widget has impact on different errors
barplot(table(node$Has_Redundant_Description,node$android_widget),beside=T, 
        legend.text = T, args.legend=list(title="Has Redundant Desc"),
        xlab="Android Widget",ylab="Num Nodes", axisnames = T )


barplot(table(node$Speakable_Text_Present,node$android_widget),beside=T, 
        legend.text = T, args.legend=list(title="Speakable_Text_Present"),
        xlab="Android Widget",ylab="Num Nodes", axisnames = T )
per_sp_text_and = nrow(node[node$android_widget=='True' & node$Speakable_Text_Present=="True",])/(nrow(node[node$android_widget=='True',]))
per_sp_text_and
per_sp_text_cust = nrow(node[node$android_widget=='False' & node$Speakable_Text_Present=="True",])/(nrow(node[node$android_widget=='False',]))
per_sp_text_cust 

summary(node$Speakable_Text_Present)


barplot(table(node$Element_Wide_Enough,node$android_widget),beside=T, 
        legend.text = T, args.legend=list(title="Element_Wide_Enough"),
        xlab="Android Widget",ylab="Num Nodes", axisnames = T )
barplot(table(node$Element_Tall_Enough,node$android_widget),beside=T, 
        legend.text = T, args.legend=list(title="Element_Tall_Enough"),
        xlab="Android Widget",ylab="Num Nodes", axisnames = T )
per_and = nrow(node[node$android_widget=='True' & node$Element_Wide_Enough=="True",])/(nrow(node[node$android_widget=='True',]))
per_and
per_cust = nrow(node[node$android_widget=='False' & node$Element_Wide_Enough=="True",])/(nrow(node[node$android_widget=='False',]))
per_cust 



barplot(table(node$Editable_Textview_With_Cont_Desc,node$android_widget),beside=T, 
        legend.text = T, args.legend=list(title="Editable_Textview_With_Cont_Desc"),
        xlab="Android Widget",ylab="Num Nodes", axisnames = T )
summary(node$Editable_Textview_With_Cont_Desc)


#### investigate errors by class
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

and.widget.classes <- data.frame(unique(node[,c("class","android_widget")]))
View(and.widget.classes)

error_by_class <- merge(error_by_class, and.widget.classes, by="class")
# 
# View(data.frame(table(node[node$android_widget=='True',]$class)))
# nrow(data.frame(table(node[node$android_widget=='True',]$class)))
# temp = node[node$android_widget=='True',]$class
# temp$android_widget = ifelse(temp$Freq>0, TRUE, FALSE)
# View(temp)
# temp <- rename(temp, c("Var1"="class", "Freq"="class_count"))
# error_by_class <- merge(error_by_class, temp, by="class")
nrow(error_by_class)
plot(error_by_class$class, error_by_class$percent_speak_text_pres)

## analysis by node type of errors
# create table of error counts by node class




#error_by_class <- merge(error_by_class,class_freq, by="class")
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
wide_en_bc_wide$percent_wide_enough = wide_en_bc_wide$True/wide_en_bc_wide$total
wide_en_bc_wide$prop_not_wide_enough = wide_en_bc_wide$False/wide_en_bc_wide$total
View(wide_en_bc_wide)

# ######################
########## Tall Enough
tall_en_by_class = as.data.frame(table(node$class,node$Element_Tall_Enough, useNA="no", exclude="na"))
tall_en_by_class = rename(tall_en_by_class, c("Var1"="class","Var2"="tall_enough","Freq"="tall_enough_count"))
tall_en_bc_wide = spread(tall_en_by_class, tall_enough, tall_enough_count)
tall_en_bc_wide$total = tall_en_bc_wide$True + tall_en_bc_wide$False
tall_en_bc_wide = merge(error_by_class, tall_en_bc_wide, by="class")
 
tall_en_bc_wide$percent_tall_enough = tall_en_bc_wide$True/tall_en_bc_wide$total
tall_en_bc_wide$prop_not_tall_enough = tall_en_bc_wide$False/tall_en_bc_wide$total
View(tall_en_bc_wide)

###### TALL VS WIDE
tall_vs_wide = merge(tall_en_bc_wide[,c("class","percent_tall_enough")],wide_en_bc_wide[,c("class","percent_wide_enough")], by="class")
tall_vs_wide$slope = tall_vs_wide$percent_tall_enough/tall_vs_wide$percent_wide_enough
tall_vs_wide = merge(tall_vs_wide,error_by_class[,c("class","num_apps_with_class")], by="class")


######## Has redundant desc 
has_red_desc_class = as.data.frame(table(node$class,node$Has_Redundant_Description, useNA="no", exclude="na"))
has_red_desc_class = rename(has_red_desc_class, c("Var1"="class","Var2"="has_red_desc","Freq"="has_red_desc_count"))
has_red_desc_bc_wide = spread(has_red_desc_class, has_red_desc, has_red_desc_count)
has_red_desc_bc_wide$total = has_red_desc_bc_wide$True + has_red_desc_bc_wide$False
has_red_desc_bc_wide = merge(error_by_class, has_red_desc_bc_wide, by="class")
## To match other errors, keep the percentage as percentage good. For this check, False is GOOD
# this is percent GOOD!!
has_red_desc_bc_wide$percent_not_redun = has_red_desc_bc_wide$False/has_red_desc_bc_wide$total
View(has_red_desc_bc_wide)

############### Shares Label
temp = node[,c("app_id","class","Num_Nodes_Share_Label")]
temp$shares_label = temp$Num_Nodes_Share_Label > 0
View(temp)
shares_label_class = as.data.frame(table(temp$class, temp$shares_label, useNA="no", exclude="na"))
shares_label_class = rename(shares_label_class, c("Var1"="class","Var2"="shares_label", "Freq"="shares_label_count"))

shares_label_bc_wide = spread(shares_label_class, shares_label, shares_label_count)
shares_label_bc_wide = rename(shares_label_bc_wide, c("TRUE"="True","FALSE"="False"))
shares_label_bc_wide$total = shares_label_bc_wide$False + shares_label_bc_wide$True
shares_label_bc_wide = merge(error_by_class, shares_label_bc_wide, by="class")
## To match other errors, keep the percentage as percentage good. For this check, False is GOOD
# this is percent GOOD
shares_label_bc_wide$percent_not_dup_label = shares_label_bc_wide$False/shares_label_bc_wide$total
View(shares_label_bc_wide)

####################
#### PLOTS
####################

##### Duplicate Lael
################
hist(shares_label_bc_wide$percent_not_dup_label)
hist(shares_label_bc_wide[shares_label_bc_wide$android_widget=="True",]$percent_not_dup_label, xlab="percent of nodes within class without duplicate label",ylab="number of classes", main="And Classes by Per Nodes within class with error")
hist(shares_label_bc_wide[shares_label_bc_wide$android_widget=="False",]$percent_not_dup_label, xlab="percent of nodes within class without duplicate label",ylab="number of classes", main="Not And Classes by Per Nodes within class with error")
View(shares_label_bc_wide[shares_label_bc_wide$android_widget=="True" & shares_label_bc_wide$percent_not_dup_label==0,])
View(shares_label_bc_wide[shares_label_bc_wide$android_widget=="True" & shares_label_bc_wide$percent_not_dup_label>0.48 & shares_label_bc_wide$percent_not_dup_label < 0.52,])

View(shares_label_bc_wide[shares_label_bc_wide$android_widget=="False" & shares_label_bc_wide$percent_not_dup_label==1,])
View(shares_label_bc_wide[shares_label_bc_wide$android_widget=="False" & shares_label_bc_wide$percent_not_dup_label==0,])



###
### Redundant Description
hist(has_red_desc_bc_wide$percent_not_redun)
hist(has_red_desc_bc_wide[has_red_desc_bc_wide$android_widget=="True",]$percent_not_redun, xlab="percent of nodes within class with no redundant lab",ylab="number of classes", main="And Classes by Per Nodes within class with error")
hist(has_red_desc_bc_wide[has_red_desc_bc_wide$android_widget=="False",]$percent_not_redun, xlab="percent of nodes within class with no redundant lab",ylab="number of classes", main="And Classes by Per Nodes within class with error")
View(has_red_desc_bc_wide[has_red_desc_bc_wide$android_widget=="True" & has_red_desc_bc_wide$percent_not_redun<0.5,])
View(has_red_desc_bc_wide[has_red_desc_bc_wide$percent_not_redun ==1,])

###
### Wide Enough

hist(wide_en_bc_wide$prop_not_wide_enough, labels=T, ylim=c(0,10000),
     xlab="proprtion of nodes within class not wide enough",
     ylab="number of classes", 
     main="Prop Node not Wide Enough by Class")

hist(wide_en_bc_wide[wide_en_bc_wide$android_widget=="True",]$percent_wide_enough, xlab="percent of nodes within class wide enough",ylab="number of classes", main="And Classes by Per Nodes within class with error")
hist(wide_en_bc_wide[wide_en_bc_wide$android_widget=="False",]$percent_wide_enough, xlab="percent of nodes within class wide enough",ylab="number of classes", main="And Classes by Per Nodes within class with error")
View(wide_en_bc_wide[wide_en_bc_wide$android_widget=="True" & wide_en_bc_wide$percent_wide_enough==0,])
View(wide_en_bc_wide[wide_en_bc_wide$android_widget=="False" & wide_en_bc_wide$percent_wide_enough==1,])



plot(error_by_class$percent_wide_enough)
hist(error_by_class$percent_wide_enough, xlab="percent of nodes within class",ylab="number of classes", main="Wide Enough")
## by android
View(error_by_class)
# histograms
hist(error_by_class[error_by_class$android_widget=='True',]$percent_wide_enough, xlab="percent of nodes within class",ylab="number of classes", main="Wide Enough")
hist(error_by_class[error_by_class$android_widget=='False',]$percent_wide_enough, xlab="percent of nodes within class",ylab="number of classes", main="Not Wide En. Not And")

#look for specific, high profile classes
View(error_by_class[error_by_class$percent_wide_enough==0,])
View(node[node$class=="android.widget.VerticalSeekBar",])

### Tall Enough
plot(error_by_class$percent_tall_enough)

hist(tall_en_bc_wide$prop_not_tall_enough, labels=T, ylim=c(0,10000),
     xlab="proportion elements not tall enough by class",
     ylab="number of classes", 
     main="Not Tall Enough by Class")

hist(tall_en_bc_wide$percent_tall_enough, xlab="percent of nodes within class",ylab="number of classes", main="Tall Enough")
summary(tall_en_bc_wide[tall_en_bc_wide$android_widget=="True",]$percent_tall_enough)
View(tall_en_bc_wide[tall_en_bc_wide$percent_tall_enough>0.45 & tall_en_bc_wide$percent_tall_enough < 0.55,])

## by android
# histograms
hist(tall_en_bc_wide[tall_en_bc_wide$android_widget=='True',]$percent_tall_enough,xlab="percent of nodes within class",ylab="number of classes", main="andr: tall Enough")
hist(tall_en_bc_wide[tall_en_bc_wide$android_widget=='False',]$percent_tall_enough, xlab="percent of nodes within class",ylab="number of classes", main="not andr: tall enough")

# high profile classes
View(tall_en_bc_wide[tall_en_bc_wide$android_widget=="True" & tall_en_bc_wide$percent_tall_enough==0,])
View(tall_en_bc_wide[tall_en_bc_wide$android_widget=="False" & tall_en_bc_wide$percent_tall_enough==0,])


#####
### Speakable text
### 0 is good, 1 is bad
hist(sp_text_bc_wide$percent_speak_text_missing,
   label=T, ylim=c(0,12000),
     xlab="Percent Elements with Missing Label", ylab="Number of Classes",
     main="Missing Label Prevalence by Class")
hist(sp_text_bc_wide[sp_text_bc_wide$percent_speak_text_missing>0,]$percent_speak_text_missing,
     ylab="num classes", main="sp text missing per class without 0")
View(sp_text_bc_wide[sp_text_bc_wide$percent_speak_text_missing==1,])
View(sp_text_bc_wide[ sp_text_bc_wide$percent_speak_text_missing> 0.48 & sp_text_bc_wide$percent_speak_text_missing< 0.52,])

### look for high profile cases


### look at 50% nodes by app
sp_text_err_by_app = node[node$class=="android.widget.ImageButton",c("app_id","Speakable_Text_Present")]
sp_text_err_by_app = as.data.frame(table(sp_text_err_by_app$app_id, sp_text_err_by_app$Speakable_Text_Present, useNA="no", exclude="na"))
sp_text_err_by_app = rename(sp_text_err_by_app, c("Var1"="app_id","Var2"="Speakable_Text_Present"))

sp_text_err_by_app = spread(sp_text_err_by_app, Speakable_Text_Present, Freq)
sp_text_err_by_app$percent_false = sp_text_err_by_app$False/(sp_text_err_by_app$True + sp_text_err_by_app$False)
hist(sp_text_err_by_app$percent_false, xlab = "percent ImageButton without speakable text", ylab="num of apps")
View(sp_text_err_by_app[sp_text_err_by_app$percent_false==0.5,])

## by android widget
hist(sp_text_bc_wide[sp_text_bc_wide$android_widget=="True",]$percent_speak_text_missing, 
     xlab="percent of nodes within class with speakable text missing",ylab="number of classes", main="And Classes by Per Nodes within class with error")
hist(sp_text_bc_wide[sp_text_bc_wide$android_widget=="False",]$percent_speak_text_missing, 
     xlab="percent of nodes within class with speakable text missing",ylab="number of classes", main="Not And Classes by Per Nodes within class with error")
View(sp_text_bc_wide[sp_text_bc_wide$android_widget=="True" & sp_text_bc_wide$percent_speak_text_missing==0,])
View(sp_text_bc_wide[sp_text_bc_wide$android_widget=="True" & sp_text_bc_wide$percent_speak_text_missing> 0.48 & sp_text_bc_wide$percent_speak_text_missing< 0.52,])
View(sp_text_bc_wide[sp_text_bc_wide$android_widget=="False" & sp_text_bc_wide$percent_speak_text_missing==1,])
View(sp_text_bc_wide[ sp_text_bc_wide$percent_speak_text_missing==0,])


## by android widget
nrow(error_by_class[error_by_class$android_widget=="True" & error_by_class$percent_speak_text_pres==0,])
View(error_by_class[error_by_class$android_widget=="False" & error_by_class$percent_speak_text_pres==0,])
View(error_by_class[error_by_class$percent_speak_text_pres==0,])
View(error_by_class[error_by_class$android_widget=="True" & error_by_class$percent_speak_text_pres==1,])
View(error_by_class[error_by_class$android_widget=="False" & error_by_class$percent_speak_text_pres==1 & 
                      error_by_class$class.count > 500,])
View(error_by_class[error_by_class$android_widget=="False" & error_by_class$percent_speak_text_pres==0 & 
                      error_by_class$class.count > 500,])
View(error_by_class[error_by_class$percent_speak_text_pres == 0,])

hist(error_by_class[error_by_class$android_widget=="False",]$percent_speak_text_pres, xlab="percent of nodes within class with speakable text present",ylab="number of classes", main="Non-Andr Classes by Per Nodes within class w/ error")
boxplot(percent_speak_text_pres ~ android_widget, error_by_class)
summary(error_by_class$percent_speak_text_pres)
summary(error_by_class[error_by_class$android_widget=="True",])

#cuml dist plot
and.class.per.sp.text.edcf=ecdf(error_by_class[error_by_class$android_widget=="True",]$percent_speak_text_pres)
plot(and.class.per.sp.text.edcf, xlab="Percent of Nodes with Speakable Text Present", main="CDF of Android class nodes for what percentage of nodes of that class have speakable text present")
cust.class.per.sp.text.edcf=ecdf(error_by_class[error_by_class$android_widget=="False",]$percent_speak_text_pres)
plot(cust.class.per.sp.text.edcf,xlab="Percent of Nodes with Speakable Text Present", main="CDF of non-android classes for per nodes w/ error in class")




View(table(node$class))
View(table(node[node$Speakable_Text_Present=='True',]$class))
table(node[node$Speakable_Text_Present==TRUE])
typeof(node$Speakable_Text_Present)
node$Speakable_Text_Present=as.factor(node$Speakable_Text_Present)
sapply(node,class)


sum(node$class)
# Diff in errors between android widgets and other
barplot(node$android_widget)
plot(node[node$Speakable_Text_Present==TRUE]$android_widget, xlim = )
barplot(node[node$Speakable_Text_Present==TRUE]$android_widget)




detach(node)

