git clone https://github.com/hyattpd/Prodigal.git
<<<<<<< HEAD
cd Prodigal/
make install
=======
>>>>>>> 40cf540577e968b8b6965a7476c68bd37e086b66
apt update
apt install -y sudo
sudo apt-get update
sudo apt-get install zlib1g-dev
<<<<<<< HEAD
pip install biopython
prodigal -i DATA.fasta -o DATA.gff -d gene.fasta -p meta -a HBV_protein.faa -f gff
=======
cd Prodigal/
make install

pip install biopython
prodigal -i DATA.fasta -o DATA.gff -d gene.fasta -p meta -a HBV_protein.faa -f gff

prodigal -i Human.fasta -o Human.gff -d Human_cds.fasta -p meta -a HBV_protein.faa -f gff
>>>>>>> 40cf540577e968b8b6965a7476c68bd37e086b66
