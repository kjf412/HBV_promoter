git clone https://github.com/hyattpd/Prodigal.git
cd Prodigal/
make install
apt update
apt install -y sudo
sudo apt-get update
sudo apt-get install zlib1g-dev
pip install biopython
prodigal -i DATA.fasta -o DATA.gff -d gene.fasta -p meta -a HBV_protein.faa -f gff
