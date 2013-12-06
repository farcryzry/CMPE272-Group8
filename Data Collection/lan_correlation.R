
require("plyr")
require("reshape")

df=read.csv("language_correlation.csv")
lan.count=aggregate(df$pushes,list(lan=df$repository_language),sum)
lan.top20=as.character(lan.count$lan) #get the vector of top20 lan
df.top20=df[df$repository_language %in% lan.top20,] #filter by lan

#filter by actor (uses more than 1 lan)
x=table(df.top20$actor)>1
actor.vector=row.names(table(df.top20$actor)[x])
df.cleaned=df.top20[df.top20$actor %in% actor.vector,]

#get the actor profile. takes ~20 min
#actor.profile=mdply(actor.vector,get.actor.profile)

df.final<-cast(df.cleaned,actor~repository_language,mean)
df.final<-df.final[,seq(2,21)]#drop the first column
mask<-apply(df.final, 2, is.nan)
df.final[mask]<-0
correlation<-cor(df.final,method="spearman")
write.csv(correlation, file="lan_correlation_result.csv")


