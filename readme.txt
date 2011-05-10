AI Project 2
============

Members
-------

* Todd Burkemper
* Brian Hrebec
* Thomas Shaddox

Operation
---------

We use a genetic algorithm to estimate the maximal three cliques in the provided friend network. The genetic algorithm actually runs thrice: once for the entire friend set, then once for the friend set *omitting the people in the clique found by the first run*, then finally for the friend set *omitting the people in the first two cliques*.

Clearly, the result is three cliques which are guaranteed to be pairwise disjoint.

The Genetic Algorithm
---------------------

We begin each generation with a population of 20 cliques. Each clique is created by choosing a random individual from the provided list of people and building a clique around that individual. Initially, each clique will only contain that single individual, and will therefore have a fitness of 1.

At the end of each generation, we choose the 5 fittest (largest) cliques from our population to survive. To fill out the remaining 15 spots in our new population, we randomly choose pairs of cliques, breed them, and add the resulting offspring to the new population.

Breeding consists of maximizing each parent clique, merging them into a child clique, then (potentially) mutating the child:

1. Maximizing a clique is done by simply adding to the clique each and every individual that can possibly be added such that the clique property is maintained.

2. Merging two cliques is as simple as computing the union of the two sets, and then randomly iterating over the individual members of the resulting clique and removing the ones which violate the clique property.

3. Mutation consists of finding candidate individuals (individuals which are friends with a large number of people currently in the clique) and attempting to add them to the clique. If and only if the clique property is maintained, the candidate becomes a new member. Each mutation chooses a number of candidates between zero and five (zero of course representing a breeding with no mutation whatsoever).
