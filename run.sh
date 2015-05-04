
for ((i = 0 ; i < 2 ; i++)) ; do
for ((j = 0 ; j < 10 ; j++)) ; do
for ((k = 0 ; k < 10 ; k++)) ; do
    sed -i "s/REACTION_TIME:.*\$/REACTION_TIME: ${i}.${j}${k}/" config.conf
    echo -ne "Reaction Time: ${i}.${j}${k} " >> results.out
    python car_net_sim.py 60 | grep "Collisions" >> results.out
done
done
done
