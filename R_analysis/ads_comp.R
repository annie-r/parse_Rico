### compare ads
### set up from basic paper analysis
library(plyr) #ddply, rename
library(tidyr) # create wide data table

ads_comp = as.data.frame(table(node[,c("ad","Speakable_Text_Present")]))
ads_comp = spread(ads_comp, Speakable_Text_Present, Freq)
ads_comp = rename(ads_comp, c("False"="Missing_Label", "True"="Has_Label"))
ads_comp$prop_missing_label = ads_comp$Missing_Label/(ads_comp$Missing_Label+ads_comp$Has_Label)

### Wide Enough
tmp = as.data.frame(table(node[,c("ad","Element_Wide_Enough")]))
tmp = spread(tmp, Element_Wide_Enough, Freq)
tmp = rename(tmp, c("False"="Not_Wide_Enough", "True"="Wide_Enough"))
tmp$prop_not_wide_enough = tmp$Not_Wide_Enough/(tmp$Not_Wide_Enough+tmp$Wide_Enough)

ads_comp = merge(ads_comp, tmp, by="ad")

### Tall Enough
tmp = as.data.frame(table(node[,c("ad","Element_Tall_Enough")]))
tmp = spread(tmp, Element_Tall_Enough, Freq)
tmp = rename(tmp, c("False"="Not_Tall_Enough", "True"="Tall_Enough"))
tmp$prop_not_tall_enough = tmp$Not_Tall_Enough/(tmp$Not_Tall_Enough+tmp$Tall_Enough)

ads_comp = merge(ads_comp, tmp, by="ad")


### Editable_Textview_With_Cont_Desc
### WRONG!!!!!!!!!!!!!!!!!!!! ####
tmp = as.data.frame(table(node[,c("ad","Editable_Textview_With_Cont_Desc")]))
tmp = spread(tmp, Editable_Textview_With_Cont_Desc, Freq)
tmp = rename(tmp, c("False"="OK_Editable_TxtVw", "True"="Editable_TxtVw_w_Cont_Desc"))
tmp$prop_editable_txtvw_w_cont_desc = tmp$Editable_TxtVw_w_Cont_Desc/
  (tmp$Editable_TxtVw_w_Cont_Desc+tmp$OK_Editable_TxtVw)

ads_comp = merge(ads_comp, tmp, by="ad")

### Duplicate Label
tmp = as.data.frame(table(node[,c("ad","shares_label")]))
tmp = spread(tmp, shares_label, Freq)
tmp = rename(tmp, c("FALSE"="Not_Dup_Label", "TRUE"="Dup_Label")) 
tmp$prop_dup_label = tmp$Dup_Label/(tmp$Dup_Label + tmp$Not_Dup_Label)
ads_comp = merge(ads_comp, tmp, by="ad")


### Redundant Label
tmp = as.data.frame(table(node[,c("ad","Has_Redundant_Description")]))
tmp = spread(tmp, Has_Redundant_Description, Freq)
tmp = rename(tmp, c("False"="No_Redun_Desc", "True"="Redun_Desc")) 
tmp$prop_redun_label = tmp$Redun_Desc/(tmp$Redun_Desc + tmp$No_Redun_Desc)
ads_comp = merge(ads_comp, tmp, by="ad")


View(tmp)
View(ads_comp)

