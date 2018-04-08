node_class_count = read.csv("nodeclasscount_uni.csv")
View(node_class_count)
node_class_count$count = as.numeric(node_class_count$count)
attach(node_class_count)

total_nodes = sum(node_class_count$count)
summary(node_class_count$count)
hist(node_class_count[count>3000 & count<200000,]$count)
boxplot(count)
node_class_count$percent_nodes = (node_class_count$count)/total_nodes
View(node_class_count)

sorted_df = node_class_count[order(-count),]
sorted_df$num = c(0:15030)
View(sorted_df)
plot(sorted_df[sorted_df$count > 5000,]$class, sorted_df[sorted_df$count > 5000,]$percent_nodes)

sorted_df$cumlsum = cumsum(sorted_df$percent_nodes)

detach(node_class_count)


## error by app

error_by_app = read.csv("app_errors.csv")

error_by_app$percent_default = num_talkback_android_default/num_talkback_nodes


attach(error_by_app)
View(error_by_app)


hist(error_by_app$Percent_Miss_Label)
plot(error_by_app$Num_Missing_Speakable_Test_Per_Node)

# set all as numeric
error_by_app$rating = as.numeric(paste(error_by_app$rating))
error_by_app$num_ratings = as.numeric(error_by_app$num_ratings)
error_by_app$Num_Missing_Speakable_Test_Per_Node[error_by_app$Num_Missing_Speakable_Test_Per_Node=='na'] <- NaN # is done by coeersion automatically in next step
error_by_app$Num_Missing_Speakable_Test_Per_Node = as.numeric(paste(error_by_app$Num_Missing_Speakable_Test_Per_Node))
error_by_app$Num_Not_Wide_Enough_Per_Node = as.numeric(paste(error_by_app$Num_Not_Wide_Enough_Per_Node))
error_by_app$Num_Not_Tall_Enough_Per_Node = as.numeric(paste(error_by_app$Num_Not_Tall_Enough_Per_Node))
error_by_app$Num_Editable_Textview_Cont_Desc_Per_Node = as.numeric(paste(error_by_app$Num_Editable_Textview_Cont_Desc_Per_Node))
error_by_app$Num_Fully_Overlapping_Clickable_Per_Node = as.numeric(paste(error_by_app$Num_Fully_Overlapping_Clickable_Per_Node))
error_by_app$Num_Clickable_Duplicate_Text_Per_Node = as.numeric(paste(error_by_app$Num_Clickable_Duplicate_Text_Per_Node))
error_by_app$Num_Non_Clickable_Duplicate_Text_Per_Node = as.numeric(paste(error_by_app$Num_Non_Clickable_Duplicate_Text_Per_Node))
error_by_app$Num_Redundant_Description_Per_Node = as.numeric(paste(error_by_app$Num_Redundant_Description_Per_Node))

hist(rating)
summary(rating)
boxplot(rating)

# histogram of each error in percentage form
hist(error_by_app$Num_Missing_Speakable_Test_Per_Node)
hist(error_by_app$Num_Not_Wide_Enough_Per_Node)
hist(error_by_app$Num_Not_Tall_Enough_Per_Node)
hist(error_by_app$Num_Editable_Textview_Cont_Desc_Per_Node)
hist(error_by_app$Num_Fully_Overlapping_Clickable_Per_Node)
hist(error_by_app$Num_Clickable_Duplicate_Text_Per_Node)
hist(error_by_app[Num_Redundant_Description_Per_Node>0,]$Num_Redundant_Description_Per_Node)



plot(error_by_app$percent_default, Num_Clickable_Duplicate_Text_Per_Node) #these aren't great comparison b/c percent default not all clickable
plot(error_by_app$percent_default, Num_Editable_Textview_Cont_Desc_Per_Node)
plot(error_by_app$percent_default, Num_Redundant_Description_Per_Node)
plot(error_by_app$percent_default, Num_Not_Tall_Enough_Per_Node)
plot(error_by_app$percent_default, Num_Not_Wide_Enough_Per_Node)

plot(error_by_app$rating,Num_Missing_Speakable_Test_Per_Node)
plot(error_by_app$rating, Num_Redundant_Description_Per_Node)

plot(error_by_app$category, Num_Missing_Speakable_Test_Per_Node)
plot(error_by_app$category, Num_Clickable_Duplicate_Text_Per_Node) #these aren't great comparison b/c percent default not all clickable
plot(error_by_app$category, Num_Editable_Textview_Cont_Desc_Per_Node)
plot(error_by_app$category, Num_Redundant_Description_Per_Node)
plot(error_by_app$category, Num_Not_Tall_Enough_Per_Node)
plot(error_by_app$category, Num_Not_Wide_Enough_Per_Node)

hist(error_by_app$percent_default)
summary(error_by_app[error_by_app$percent_default==0,]$percent_default)

plot(error_by_app$percent_default, Num_Missing_Speakable_Test_Per_Node)
sub = error_by_app[error_by_app$percent_default>0.9 & error_by_app$Num_Missing_Speakable_Test_Per_Node>0.9,]
View(sub[complete.cases(sub[,1]),])

plot(error_by_app[error_by_app$rating>4.7,]$percent_default, error_by_app[error_by_app$rating>4.7,]$Num_Missing_Speakable_Test_Per_Node)

hist(error_by_app[num_talkback_nodes<1000,]$num_talkback_nodes)
summary(error_by_app[num_talkback_nodes == 0 & rating>4,])
View(error_by_app)
View(error_by_app[error_by_app$num_talkback_nodes == 0 & error_by_app$rating>4,])


detach(error_by_app)
