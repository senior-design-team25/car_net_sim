
for i in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 \
         1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 \
         2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9
do
sed -i "s/REACTION_TIME:.*\$/REACTION_TIME: ${i}/" config.conf
echo -ne "Reaction Time: ${i} " >> results.out
python car_net_sim.py 60 | grep "Collisions" >> results.out
done
