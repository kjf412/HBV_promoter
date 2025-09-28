cat Bat_primate.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
cat Donkey_dog_raccoon.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
cat Fish.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
cat marmot.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
cat poultry.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
