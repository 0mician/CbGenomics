############################
#### Libraries and setup ###
############################

library(ggplot2)
library(reshape2)

setwd(dir = "/home/sid/Dev/CbGenomics/data/")
blast <- read.csv("blast_proteins.csv", check.names = FALSE, header=TRUE) 

# creating dataframe for heatmap
# labels extracted from list in bash with: "while read p; do echo "\"$p\","; done < heatmap_list.txt"
labels <- c("CBO0123",
            "CBO0124",
            "CBO0125",
            "CbC4_2296",
            "CbC4_2295",
            "CbC4_2294",
            "T258_2858",
            "T258_2857",
            "T258_2856",
            "CBO2797",
            "CBO2796",
            "CBO2795",
            "CbC4_1940",
            "CbC4_1939",
            "CbC4_1938",
            "U732_2593",
            "U732_2594",
            "U732_2595",
            "CLSPO_c19770",
            "CLSPO_c19780",
            "CLSPO_c19790",
            "CLSPO_c19800",
            "CLSPO_c19810",
            "CLSPO_c19820",
            "CBO1974",
            "CBO1975",
            "CBO1976",
            "CBO1977",
            "CBO1978",
            "CLK_1429",
            "CLK_1430",
            "CLK_1431",
            "CLK_1432",
            "CLOSPO_02139",
            "CLOSPO_02140",
            "CLOSPO_02141",
            "CLL_A3167",
            "CLL_A3168",
            "CLL_A3169",
            "CbC4_1573",
            "CbC4_1572",
            "CbC4_1571",
            "CbC4_1570",
            "CbC4_1569",
            "CbC4_1568",
            "CBO0204",
            "CbC4_0552",
            "CBO3432",
            "CLL_A0291",
            "CbC4_0273",
            "CBO1324",
            "CbC4_0666",
            "CBO2924",
            "CbC4_0502",
            "CBO0128",
            "CbC4_2292",
            "CLL_A0079",
            "CLL_A3162",
            "CBO3086",
            "CBO3085",
            "CBO3084",
            "CLL_A0078",
            "CDH90139.1",
            "D88151.1"
)

heat_protein <- data.frame(matrix(rep(0.0, 64*64), ncol = 64, nrow = 64))
rownames(heat_protein) <- labels
colnames(heat_protein) <- labels

for(i in 1:nrow(blast)) {
  heat_protein[as.character(blast$query[i]), as.character(blast$hit[i])] <- blast$perc_id[i]
}

heat_protein[lower.tri(heat_protein)] <- NA

heat_proteins.melt <- melt(heat_protein)
heat_proteins.melt$hit <- rep(labels, 64)
colnames(heat_proteins.melt) <- c("query", "perc_id", "target")
heat_proteins.melt <- heat_proteins.melt[, c("query", "target", "perc_id")]
heat_proteins.melt$target <- as.factor(heat_proteins.melt$target)
heat_proteins.melt$target <- factor(heat_proteins.melt$target, levels=heat_proteins.melt$target)

ggplot(data = heat_proteins.melt, aes(x = query  , y = target)) +
  theme_bw() +
  geom_tile(aes(fill = perc_id), colour = "grey90") +
  scale_fill_gradient(low = "white", high = "steelblue") +
  ggtitle("Heatmap of the 64 proteins identity") +
  xlab("Gene ID") +
  ylab("Gene ID") +
  theme(axis.text.x = element_text(angle=45, hjust=1, vjust=1),  
        legend.position="none",
        text = element_text(size=12),
        plot.title = element_text(size=16))
