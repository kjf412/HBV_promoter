git clone https://github.com/hyattpd/Prodigal.git
apt update
apt install -y sudo
sudo apt-get update
sudo apt-get install zlib1g-dev
cd Prodigal/
make install

pip install biopython
prodigal -i DATA.fasta -o DATA.gff -d gene.fasta -p meta -a HBV_protein.faa -f gff

prodigal -i Human.fasta -o Human.gff -d Human_cds.fasta -p meta -a HBV_protein.faa -f gff
