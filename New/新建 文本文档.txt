tar -zxvf ncbi-blast-2.16.0+-x64-linux.tar.gz
vim ~/.bashrc
export PATH=/mnt/workspace/ncbi-blast-2.16.0+/bin/:$PATH
source ~/.bashrc


# method_1
makeblastdb -in EN2_Core_p.fasta -dbtype prot -out HBV_EN2_Core_p.db
makeblastdb -in EnhI_XP_X.fasta -dbtype prot -out HBV_EnhI_XP_X.db
makeblastdb -in SP1_L.fasta -dbtype prot -out HBV_SP1_L.db
makeblastdb -in SP2_M.fasta -dbtype prot -out HBV_SP2_M.db


blastn -db HBV_EN2_Core_p.db -query Human.fasta -out all_add.blast1  -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs" -evalue 1e -task dc-megablast
blastn -db HBV_EnhI_XP_X.db -query Human.fasta -out all_add.blast2  -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs" -evalue 1e -task dc-megablast
blastn -db HBV_SP1_L.db -query Human.fasta -out all_add.blast3  -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs" -evalue 1e -task dc-megablast
blastn -db HBV_SP2_M.db -query Human.fasta -out all_add.blast4  -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs" -evalue 1e -task dc-megablast

# method_1

