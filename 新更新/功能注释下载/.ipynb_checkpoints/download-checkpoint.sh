cat cat_accessions.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
cat shrew_accessions.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
