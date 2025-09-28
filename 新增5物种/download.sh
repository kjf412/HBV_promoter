# 处理Bat_primate.txt，文件放入Bat_primate文件夹

#cat Bat_primate.txt | xargs -I {} sh -c 'mkdir -p Bat_primate && datasets download virus genome accession {} --include genome,cds,protein --filename Bat_primate/{}.zip'



# 处理Donkey_dog_raccoon.txt，文件放入Donkey_dog_raccoon文件夹

#cat Donkey_dog_raccoon.txt | xargs -I {} sh -c 'mkdir -p Donkey_dog_raccoon && datasets download virus genome accession {} --include genome,cds,protein --filename Donkey_dog_raccoon/{}.zip'



# 处理Fish.txt，文件放入Fish文件夹

cat Fish.txt | xargs -I {} sh -c 'mkdir -p Fish && datasets download virus genome accession {} --include genome,cds,protein --filename Fish/{}.zip'



# 处理marmot.txt，文件放入marmot文件夹

cat marmot.txt | xargs -I {} sh -c 'mkdir -p marmot && datasets download virus genome accession {} --include genome,cds,protein --filename marmot/{}.zip'



# 处理poultry.txt，文件放入poultry文件夹

cat poultry.txt | xargs -I {} sh -c 'mkdir -p poultry && datasets download virus genome accession {} --include genome,cds,protein --filename poultry/{}.zip'







#cat Bat_primate.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
#cat Donkey_dog_raccoon.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
#cat Fish.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
#cat marmot.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
#cat poultry.txt | xargs -I {} datasets download virus genome accession {} --include genome,cds,protein --filename {}.zip
