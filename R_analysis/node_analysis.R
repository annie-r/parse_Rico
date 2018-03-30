## By Nodes

node = read.csv("all_node.csv")
node = read.csv("all_node_webview.csv")
View(node)
View(node[node$class=="android.widget.ZoomButton",])
summary(node[node$class=="android.widget.ZoomButton",])

attach(node)
node$Num_Nodes_Overlap_With = as.numeric(node$Num_Nodes_Overlap_With)
node$Num_Nodes_Share_Label = as.numeric(node$Num_Nodes_Share_Label)

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
barplot(table(node$Editable_Textview_With_Cont_Desc,node$android_widget),beside=T, 
        legend.text = T, args.legend=list(title="Editable_Textview_With_Cont_Desc"),
        xlab="Android Widget",ylab="Num Nodes", axisnames = T )
summary(node$Editable_Textview_With_Cont_Desc)


#### investigate errors by class
error_by_class = table(node$class)
error_by_class = rename(as.data.frame(error_by_class), c("Var1"="class","Freq"="class_count"))
View(error_by_class)

library(plyr)
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

sp_text_by_class <- as.data.frame(table(node[node$Speakable_Text_Present=='True',]$class))
sp_text_by_class = rename(sp_text_by_class, c("Var1"="class","Freq"="has_sp_text_count"))
View(node)
View(sp_text_by_class)
error_by_class <- merge(error_by_class, sp_text_by_class, by="class")
View(error_by_class)
error_by_class$percent_speak_text_pres = error_by_class$has_sp_text_count/error_by_class$class_count

wide_enough_by_class = as.data.frame(table(node[node$Element_Wide_Enough=="True",]$class))
wide_enough_by_class = rename(wide_enough_by_class, c("Var1"="class", "Freq"="is_wide_enough_count"))
View(wide_enough_by_class)
error_by_class <- merge(error_by_class, wide_enough_by_class, by="class")
View(error_by_class)
error_by_class$percent_wide_enough = error_by_class$is_wide_enough_count/error_by_class$class_count

tall_enough_by_class = as.data.frame(table(node[node$Element_Tall_Enough=="True",]$class))
tall_enough_by_class = rename(tall_enough_by_class, c("Var1"="class", "Freq"="is_tall_enough_count"))
View(tall_enough_by_class)
error_by_class <- merge(error_by_class, tall_enough_by_class, by="class")
View(error_by_class)
error_by_class$percent_tall_enough = error_by_class$is_tall_enough_count/error_by_class$class_count

#### PLOTS

### Wide Enough
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
hist(error_by_class$percent_tall_enough, xlab="percent of nodes within class",ylab="number of classes", main="Tall Enough")
## by android
# histograms
hist(error_by_class[error_by_class$android_widget=='True',]$percent_tall_enough,xlab="percent of nodes within class",ylab="number of classes", main="andr: tall Enough")
hist(error_by_class[error_by_class$android_widget=='False',]$percent_tall_enough, xlab="percent of nodes within class",ylab="number of classes", main="not andr: tall enough")

# high profile classes
View(error_by_class[error_by_class$android_widget=="True" & error_by_class$percent_tall_enough==0,])

### Speakable text
plot(error_by_class$percent_speak_text_pres)
hist(error_by_class[error_by_class$android_widget=="True",]$percent_speak_text_pres, xlab="percent of nodes within class with speakable text present",ylab="number of classes", main="And Classes by Per Nodes within class with error")
hist(error_by_class[error_by_class$android_widget=="False",]$percent_speak_text_pres, xlab="percent of nodes within class with speakable text present",ylab="number of classes", main="And Classes by Per Nodes within class with error")


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

