# miscellaneous
Random unrefined projects for learning

Brief description of the projects:

**1. obstacle-avoidance**

This was made with the intention of developing an algorithm for avoiding static obstacles by an Unmanned aerial vehicle. 
I ended up implementing something like [this] paper which uses covariance confidence ellipses to judge the avoidance region and get
a vector to change course. 

![](https://github.com/nikhil-sethi/miscellaneous/blob/master/obstacle-avoidance/obs.gif)

**2. python-netlogo**

This is a very poor attempt at interfacing [Netlogo](an application for multiagent control) and python with a library called [nl4py].
The library itself is pretty sweet but not that mature. The interface was succesful and I did end up writing a flocking algorithm for
the agents as well. I ran into problems with the interface while getting data from netlogo to python. I ended up writing my own physical
environment in python and matplotlib itself as this was part of a larger project.

**3. vba_rc**

A very small vba script that fills a pre-existing text boxes of a Microsoft word template with appropriate data from Excel. It takes the 
rating of a student and fills in the answers to questions from an anwer bank.

**4. GA**

My first hands at optimization <3. I was trying to solve a very simple problem with a very complicated algorithm just for fun and learning.

**5. PSO**

Succesfully implemented a particle swarm optimizer for a college assignment. I got carried away and extended it to more than required 
by implementing stuff like OOP, multithreading, nearest neighbhour searching etc. The algo works well but the code is badly written. Best of luck
to whoever attempts to read.


  [this]:https://link.springer.com/content/pdf/10.1007/s10846-017-0543-4.pdf
  [Netlogo]:https://ccl.northwestern.edu/netlogo/
  [nl4py]:https://github.com/chathika/NL4Py
