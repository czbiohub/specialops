
python - $1 <<END

import sys
txtfile=sys.argv[1]
count = -1
file = open(txtfile, 'r')
fileout = open ('output_file.csv', 'w')
for line in file.readlines():
   linestrip = line.rstrip('\n')
   newline = linestrip + "," + str(count) + "\n"
   #print(newline)
   count+=1
   fileout.write(newline)

END


csv=$(echo $1 | cut -f 1 -d '.')
echo $csv

awk -F , -v csv=$csv '{print ">"csv"_"$5"\n"$1}' output_file.csv > $csv.fasta
sed -i '1,4d'  $csv.fasta 
