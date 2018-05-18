## investigate classes of intered
## based on node_analysis.R base

#random number generator [min,max[
floor(runif(5, min=0, max=4422))

#############
### Size
###########

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
