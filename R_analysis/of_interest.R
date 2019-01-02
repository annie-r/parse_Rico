## investigate classes of intered
## based on node_analysis.R base




#random number generator [min,max[
floor(runif(5, min=0, max=1124))

#############
### Size
###########
######
## Radio Button
###
#explore 10 random interfaces 

## not wide, not tall
no_wide_no_tall = node[node$class=="android.widget.RadioButton" & node$Element_Wide_Enough=="False" & node$Element_Tall_Enough=="False",]

# random numbers generated
#1570 1486   72 2055 1753  236 1215 1143 1291  337
View(no_wide_no_tall[c(150,1486,72,2055,1753,236,1215,1143,1291,337),])

yes_wide_no_tall = node[node$class=="android.widget.RadioButton" & node$Element_Wide_Enough=="True" & node$Element_Tall_Enough=="False",]
# 6195 rows
# rand 5
# 2824 5838 3915 5192 2391
View(yes_wide_no_tall[c(2824,5838,3915,5192,2391),])


yes_wide_yes_tall = node[node$class=="android.widget.RadioButton" & node$Element_Wide_Enough=="True" & node$Element_Tall_Enough=="True",]
nrow(yes_wide_yes_tall)
View(yes_wide_yes_tall[c(3183,3369,885,1253,1129),])


###
## Switch
###
no_wide_yes_tall = node[node$class=="android.widget.Switch" & node$Element_Wide_Enough=="False" & node$Element_Tall_Enough=="True",]
nrow(no_wide_yes_tall)
View(no_wide_yes_tall[c(13,7,27,14,18),])

yes_wide_no_tall = node[node$class=="android.widget.Switch" & node$Element_Wide_Enough=="True" & node$Element_Tall_Enough=="False",]
nrow(yes_wide_no_tall) #1148
View(yes_wide_no_tall[c(345, 878, 263, 714, 189),])

yes_wide_yes_tall = node[node$class=="android.widget.Switch" & node$Element_Wide_Enough=="True" & node$Element_Tall_Enough=="True",]
nrow(yes_wide_yes_tall)
#148
View(yes_wide_yes_tall[c(88,  83,   4, 115,  98),])

no_wide_no_tall = node[node$class=="android.widget.Switch" & node$Element_Wide_Enough=="False" & node$Element_Tall_Enough=="False",]
nrow(no_wide_no_tall) #948
View(no_wide_no_tall[c(85 ,438 ,412, 465, 121),])

###
## Checkbox
###
no_wide_yes_tall = node[node$class=="android.widget.CheckBox" & node$Element_Wide_Enough=="False" & node$Element_Tall_Enough=="True",]
nrow(no_wide_yes_tall) #1124
View(no_wide_yes_tall[c(512, 1059 , 710 , 941,  433),])

yes_wide_no_tall = node[node$class=="android.widget.Switch" & node$Element_Wide_Enough=="True" & node$Element_Tall_Enough=="False",]
nrow(yes_wide_no_tall) #1148
View(yes_wide_no_tall[c(345, 878, 263, 714, 189),])

yes_wide_yes_tall = node[node$class=="android.widget.Switch" & node$Element_Wide_Enough=="True" & node$Element_Tall_Enough=="True",]
nrow(yes_wide_yes_tall)
#148
View(yes_wide_yes_tall[c(88,  83,   4, 115,  98),])

no_wide_no_tall = node[node$class=="android.widget.Switch" & node$Element_Wide_Enough=="False" & node$Element_Tall_Enough=="False",]
nrow(no_wide_no_tall) #948
View(no_wide_no_tall[c(85 ,438 ,412, 465, 121),])


#####################
##### Missing Label
###################
apps_with_some = error_by_app[error_by_app$Num_Missing_Speakable_Text_Per_Node > 0 & error_by_app$Num_Missing_Speakable_Text_Per_Node < 1, c("app_id","Num_Missing_Speakable_Text_Per_Node")]
nrow(apps_with_some) #7810

## randomly look at 5 examples
View(apps_with_some[c(4169,523,7253,6008,1510),])
app_nodes = node[node$app_id=="com.nhn.android.mail" & node$Speakable_Text_Present =="True",]
View(app_nodes[c(43,21,46,138,6),])
app_nodes = node[node$app_id=="com.nhn.android.mail" & node$Speakable_Text_Present =="False",]
nrow(app_nodes)
View(app_nodes[c(19,2,19,6,24),])




app_nodes = node[node$app_id=="com.androidloard.optimizemaster" & node$Speakable_Text_Present =="True",]
nrow(app_nodes)
View(app_nodes[c(5,15,26,12),])
app_nodes = node[node$app_id=="com.androidloard.optimizemaster" & node$Speakable_Text_Present =="False",]
nrow(app_nodes)
View(app_nodes[c(19,2,6,24),])
