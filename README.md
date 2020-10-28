# CS 143 Programming Assignment: Alexander Chen, Daniel Cisneros, Fred Kelly, Veronica Tang

Q7)

Place CustomTopo.py in the /home/mininet directory on the virtual machine. Then run "$ sudo mn --custom CustomTopo.py --topo custom --test pingall --link tc".

Q8)

Copy firewall.py and firewall-policies.csv into ~/pox/pox/misc on the virtual machine. Then, on two separate terminals, first run "$ pox.py forwarding.l2_learning misc.firewall &"
to start the controller, and then run "sudo mn --topo single,3 --controller remote --mac". Neither h1 nor h3 should be able to ping h2. 

Q9)

Copy dijkstra.py and delay.csv into ~/pox/pox/misc on the virtual machine. Copy topo.py into /home/mininet on the virtual machine. On two separate terminals, first run
"pox.py misc.dijkstra &" to start the controller, and then run "sudo mn --custom topo.py --topo custom --controller remote --mac --link tc". Pingall should confirm that all hosts
can ping to each other. Pinging between h13 and h17 will reveal a RTT of around 81ms, which is as expected since the shortest path from h13 to h17 has a delay of 40ms, and this is
traversed twice when pinging. 
