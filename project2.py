#!/bin/sh

import sys, random, copy

people = []

class Clique:
    def __init__(self, items):
        self.data = set(items)

    def __str__(self):
        return str(self.data)

    def fitness(self):
        return len(self.data)

    """ 
    Add all possible items to this set considered in order.
    TODO: add in random order?
    """
    def makeMaximal(self):
        r = range(0, len(people))
        random.shuffle(r)
        for p in r:
            if p not in self.data and people[p].isFriendsWithAll(self.data):
                self.data.add(p)

    """
    Remove all items in self.data that aren't in the clique,
    starting from random point
    """
    def validate(self):
        items = list(self.data)
        start = random.randint(0, len(items) - 1)
        for p in items[start:]:
            if not people[p].isFriendsWithAll(self.data):
                self.data.discard(p)

        itemsr = items[:start]
        itemsr.reverse()
        for p in itemsr:
            if not people[p].isFriendsWithAll(self.data):
                self.data.discard(p)


    """
    Add random items to the set that won't mess it up to badly
    """
    def mutate(self, n):
        candidates = []
        for p in range(0, len(people)):
            if p not in self.data:
                candidates += [(p, people[p].countFriendsWith(self.data))]
            
        candidates.sort(lambda a, b: a[1] - b[1])
        # add three highly ranked items
        for c in candidates[:n]:
            self.data.add(c[0])

        self.validate()

    def breed(self, other):
        self.merge(other)
        self.mutate(random.randint(0, 10))

    def merge(self, other):
        self.makeMaximal()
        other.makeMaximal()
        self.data |= other.data
        self.validate()

class Person:
    def __init__(self, index, friends):
        self.index = index
        self.friends = friends

    def countFriendsWith(self, clique):
        count = 0
        for c in clique:
            if self.isFriendsWith(people[c]):
                count += 1
            
        return count

    """
    Returns True if this Person is friends with all 
    the people in iterable 'clique'
    """
    def isFriendsWithAll(self, clique):
        for c in clique:
            if not self.isFriendsWith(people[c]):
                return False
        return True

    """
    Returns True if this Person is friends with Person 'other'
    """
    def isFriendsWith(self, other):
        if self.index == other.index:
            return True

        return self.friends[other.index] == 1


def load(filename):
    inputfile = open(filename)
    p = 0
    for line in inputfile:
        name, friendlist = line.strip().split(',',1)
        people.append(Person(p, [int(f) for f in friendlist.split(',')]))
        p += 1

if __name__ == "__main__":
    load(sys.argv[1])
    newpop = [Clique([p]) for p in random.sample(range(len(people)), 20)]
    for gen in range(100):
        pop = newpop
        pop.sort(lambda a, b: b.fitness() - a.fitness())
        print 'Generation %d: ' % gen + ' '.join(str(p.fitness()) for p in pop)
        pop = pop[:5]
        newpop = []
        chosen = set()
        while len(newpop) < 20:
            newc = copy.deepcopy(random.choice(pop))
            newc2 = random.choice(pop)
            if newc != newc2 and (newc, newc2) not in chosen:
                #print "adding ", (str(newc), str(newc2))
                newc.breed(newc2)
                #print "as ", str(newc)
                newpop.append(newc)
                chosen.add((newc, newc2))

    print "Results: "
    print ' '.join(str(p.fitness()) for p in pop[:3])



