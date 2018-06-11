#DESeq2 Script Originally Written by Stephanie Christenson, 2015

setwd("~/Box Sync/mBAL-study/")
library( "DESeq2" )
library( "Rsamtools" )
library( "biomaRt" )
library( "GenomicAlignments" )
library( "gplots")
library( "plyr")

#sample sheet:
#genes are in rows
#columns are in columns
#need to cut out all numbers after decimal points
#in excel sheet
#make another column next to the ESL column
#click data
#click on convert text to data
#click on "fixed path", then "next"
#then click on where to cut off numbers, then click "finish"

#condition sheet
#samples are in rows
#the type of experimental conditions in columns

#this binds all of the .tab files together
temp<-list.files(pattern="mBAL")
import.list<-llply(temp, read.table)
data<-do.call("cbind", import.list)
rownames(data)<-data[,1]
#remove the first colum
data<-data[,-1]
#starting with 2nd column, get rid of every 4th
c<-1:ncol(data)
raw<-data[,!(c%%4==2)]
##starting with 2nd column, get rid of every 3rd
c<-1:ncol(raw)
raw<-raw[,!(c%%3==2)]
#starting with 1st column, keep every 2nd
c<-1:ncol(raw)
raw<-raw[,(c%%2==1)]
colnames(raw)<-temp
#remove 1st 4 rows
raw<-raw[-(1:4),]
write.csv( as.data.frame(raw), file="mBAL-genecounts.csv")

#optional section to remove rRNA genes up front
#raw<-read.csv("mBAL-genecounts.csv", row.names=1, header=TRUE)
#dim(raw)
#rRNAgenes<-array(read.csv("_rRNA-ENSEMBL-geneIDs.csv", header=FALSE) $V1)
#rawrRNAsubt<-raw[!(row.names(raw)%in%rRNAgenes),]
#dim(rawrRNAsubt)
#rRNAgenecounts<-raw[(row.names(raw)%in%rRNAgenes),]
#write.csv( as.data.frame(rRNAgenecounts), file="mBAL-rRNA-genes.csv")
#write.csv( as.data.frame(rawrRNAsubt), file="mBAL-genecounts-no-rRNA.csv")
#to select columns, column in front: 
#rRNAgenecounts<-raw[,(col.names(raw)%in%rRNAgenes)]

#CONVERT TO PROTEIN CODING GENES ONLY

#adding gene names (note, with strsplit ,2 would keep the second part of the split)
genenames<- sapply( strsplit( rownames(raw), split="\\." ), "[", 1 )
#The following chunk of code uses the ENSEMBL mart, 
#querying with the ENSEMBL gene id and requesting the Entrez gene id 
#and HGNC gene symbol.
library( "biomaRt" )
listMarts(host="www.ensembl.org")
mart = useMart(biomart="ENSEMBL_MART_ENSEMBL",dataset="hsapiens_gene_ensembl", host="www.ensembl.org")
genemap <- getBM( attributes = c("ensembl_gene_id", "entrezgene", "hgnc_symbol", "gene_biotype", "description"),
                  filters = "ensembl_gene_id",
                  values = genenames,
                  mart)
#create an index in which you are rearranging ensmbl gene ids from genemap into same order as they are in genenames
idx <- match(genenames, genemap$ensembl_gene_id )
#create new list called gene attributes (ga)

entrez <- genemap$entrezgene[ idx ]
hgnc_symbol <- genemap$hgnc_symbol[ idx ]
description <- genemap$description[ idx ]
gene_biotype <- genemap$gene_biotype[ idx ]
ensembl <- genemap$ensembl_gene_id[ idx ]

ga<-cbind(hgnc_symbol,description,gene_biotype,ensembl,entrez)
#make ga into a data frame from a matrix
ga<-as.data.frame(ga)
ga$gene_biotype<-as.character(ga$gene_biotype)

#pc = protein coding
pc<-ga[ga$gene_biotype=="protein_coding",]
pc<-pc[!(is.na(pc$ensembl)),]

#make an index for protein coding genes

rownames(rawrRNAsubt)<-genenames
idxpc<- match(pc$ensembl,rownames(raw))
rawrRNAsubtpc<-raw[idxpc,]
rownames(rawrRNAsubtpc)<-make.unique(as.character(pc$hgnc_symbol))

write.csv( as.data.frame(rawrRNAsubtpc), file="mBAL-protein-coding-genes.csv")

#####----------------------------------

genecountspc<-read.csv("mBAL-protein-coding-genes.csv", header=TRUE)
genecountspc<-as.matrix(genecountspc)

rownames(genecountspc)<-genecountspc[,1]
genecountspc<-genecountspc[,-1]
genecountspc <- apply(genecountspc, c(1,2), function(x) { (as.integer(x))})

#FILTERING 1
#script to capture genes present in at least 50% of samples but you may want to start higher than that.
###"microbes" is a matrix with samples in columns, genes in rows
## Determine which probes are present for each sample
# c means concatonate

mabsent <- c()

for (i in 1:ncol(genecountspc)) {
  ## Zero spot =absent
  absent <- as.numeric(genecountspc[,i]) < 1
  ## Add the sample to an "absent" matrix with all other samples
  mabsent <- cbind(mabsent, absent)
}

## Determine which probes are present
mpresent <- mabsent==0

## Find which probes are present in at least 50% of the samples
mfilter<- apply(mpresent,1,sum) > ncol(genecountspc)*.5
mpresent50<-genecountspc[mfilter=="TRUE",]

dim(mpresent50)

#for the protein coding genes, remove mt genes
idxmt <- grep("MT-",rownames(mpresent50))
mpresent50nomt<-mpresent50[-idxmt,]

dim(mpresent50nomt)

#FILTERING 2
#block inserted by KKalantar to remove genes which have outlier values for < 10% of samples.

mremove <- c()
mpresentoutlier <- c()
rownames_mpresentoutlier <- c()
for (i in 1:nrow(mpresent50nomt)) {
  # number of outliers less than threshold, but greater than 0 = 
  bpo<-length(boxplot.stats(mpresent50nomt[i,])$out)
  remove <- as.numeric(0 < bpo && bpo < ncol(mpresent50nomt)*0)
  # Add the sample to a "remove" matrix with all other samples
  mremove <- cbind(mremove, remove)
  if(remove==0){
    mpresentoutlier<- rbind(mpresentoutlier, mpresent50nomt[i,])
    rownames_mpresentoutlier <- cbind(rownames_mpresentoutlier, row.names(mpresent50nomt)[i])
  }
}

row.names(mpresentoutlier)<-rownames_mpresentoutlier
dim(mpresentoutlier)


# READ IN THE METADATA

metadata<-read.csv(as.matrix("mBAL-metadata.csv", header=TRUE))#add in meta data
rownames(metadata)<-metadata[,1]
metadata<-metadata[,-1]

#DESEQ FUNCTION
#design designates the column of condition (infxn) 

dds<-DESeqDataSetFromMatrix(countData= mpresent50nomt, colData= metadata, design=~infxn+batch)
dds<-DESeq(dds)
res<-results(dds)
res<-res[order(res$padj),]

#To run results when asking for a specific contrast (e.g. infxn versus none) put the column name first then the "disease" predictor, then the "control" predictor
resInfxn<-results(dds, contrast=c("effective_group", "yes", "no"))

#attr(resInfxn,"filterThreshold")
#plot(attr(resInfxn,"filterNumRej"),type="b",ylab="number of rejections")
#resInfxnNoFilt<-results(dds,contrast=c("infxn", "No infxn", "infxn"), independentFiltering=FALSE)  
#addmargins(table(filtering=(resInfxn$padj<.1),noFiltering=(resInfxnNoFilt$padj<.1)))

#SPOT CHECK how many genes at P < 0.05 
sum( resInfxn$pvalue < 0.05, na.rm=TRUE ) 
#Without filtering
#sum( resInfxnNoFilt$pvalue < 0.01, na.rm=TRUE ) 

#FDR = MULTIPLE TEST CORRECTION WHICH IS NECESSARY

#how many genes at fdr<0.02
sum( resInfxn$padj < 0.02, na.rm=TRUE ) 

#how many genes at fdr<0.01
sum( resInfxn$padj < 0.01, na.rm=TRUE ) 

#Reorder results by log2foldchange
resInfxn<- resInfxn[ order( resInfxn$log2FoldChange ), ] 
#resInfxnNoFilt<- resInfxnNoFilt[ order( resInfxnNoFilt$log2FoldChange ), ]

write.table(resInfxn, "mBAL-infxn-v-none.tab", sep="\t")

#pull out just FDR<0.05
resInfxnSig.1 <- resInfxn[ which(resInfxn$padj < 0.05 ), ]

##Normalized Counts
#Corrected for size factors
normcounts<-counts(dds, normalized = TRUE)
rownames(normcounts)<-rownames(mpresent50nomt)
colnames(normcounts)<-colnames(mpresent50nomt)
write.csv( as.data.frame(normcounts), file="NormCounts_mBAL_infxn-v-none.csv" )

#regularized log transformation, not to be used for differential expression, just for clustering/visualization---get the DE from the results files

##### RLD #####

rld <- rlog( dds )
#assay makes things into a matrix
rldassay<-assay(rld)

##### VST, a faster less accurate option

#vst <- getVarianceStabilizedData(dds)
#rldassay<-vst
#rld <- rlog( dds )
#rldassay<-assay(rld)


rownames(rldassay)<-rownames(normcounts)
colnames(rldassay)<-colnames(normcounts)
write.csv( as.data.frame(rldassay), file="RLECounts_mBAL_infxn-v-none.csv" )

#rldassay<-read.csv("RLECounts_mBAL_infxn-v-none.csv", row.names=1, header=TRUE)

#THIS SECTION MAKES THE PLOTS

#dev.off() resets the graphics mode
dev.off()
library("RColorBrewer")


library("gplots")
select <- order(rowMeans(counts(dds,normalized=TRUE)),decreasing=TRUE)[1:30]
hmcol <- colorRampPalette(brewer.pal(9, "GnBu"))(100)
heatmap.2(counts(dds,normalized=TRUE)[select,], col = hmcol,
          Rowv = FALSE, Colv = FALSE, scale="none",
          dendrogram="none", trace="none", margin=c(3,3))
#this just gives you the highest base means aross samples (quality plot)
heatmap.2(assay(rld)[select,], col = hmcol,
          Rowv = FALSE, Colv = FALSE, scale="none",
          dendrogram="none", trace="none",cexRow=0.6, margin=c(2, 2))


distsRL <- dist(t(assay(rld)))
mat <- as.matrix(distsRL)
rownames(mat) <- colnames(mat) <- with(colData(dds),
                                       paste(effective_group))
hc <- hclust(distsRL)
heatmap.2(mat, Rowv=as.dendrogram(hc),
          symm=TRUE, trace="none",
          col = rev(hmcol), margin=c(5, 5))
#PCA PLOT

library(ggplot2)
data <- plotPCA(rld, intgroup=c("effective_group"), returnData=TRUE)
percentVar <- round(100 * attr(data, "percentVar"))
ggplot(data, aes(as.numeric(PC1), as.numeric(PC2), color=effective_group)) +
  geom_point(size=3) +
  geom_text(aes(label=name),hjust=.5, vjust=0)+
  xlab(paste0("PC1: ",percentVar[1],"% variance")) +
  ylab(paste0("PC2: ",percentVar[2],"% variance"))


#This is usually how I make color palettes for my heatmaps
brewer=rgb(colorRamp(c ("blue", "white", "red"), space="rgb", interpolate="linear")(0:255/255), maxColorValue=255)

#find these rownames from the results in the normalized counts file (rldassay) and create an index
sigind<-match(rownames(resInfxnSig.1), rownames(rldassay))
#this creqtes the data object
set<-rldassay[sigind,]
#Top Table heatmap without colorbars 
#t(set) transposes to allow for centering and scaling
sett<-t(set)
sets<-scale(sett, center=T, scale=T)                   
setst<-t(sets)
rm(sett)                   
brewer=rgb(colorRamp(c("darkblue", "blue3", "blue2",  'blue', "white",  "red", "red3", "red4", "darkred"), space="rgb", interpolate="linear")(0:255/255), maxColorValue=255)
#brewer=rgb(colorRamp(c ("blue", "white", "darkred"), space="rgb", interpolate="linear")(0:255/255), maxColorValue=255)

dev.off()
#Colorbar for viral infection
status<- dds$effective_group
f.status<- factor(status)
vec.status<- rainbow(nlevels(f.status),start=.6,end=0)
status.colour <- rep(0,length(f.status))
#creates different colors for infxn/no infxn heatmap
for(i in 1:length(f.status))
  status.colour[i] <- vec.status[ f.status[i]==levels(f.status) ]

# Make Heatmap 

heat.c<-heatmap.2(setst, col = brewer, cexRow=0.5, ColSideColors=status.colour, scale="none", symbreaks=T, trace="none", margin=c(7,5))
pdf("mBAL-heatmap-infxn-v-none.pdf")





