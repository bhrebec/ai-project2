#!/bin/sh

import sys, random, copy

people = []

class Clique:
    def __init__(self, items, exclude):
        self.data = set(items)
        self.exclude = set(exclude)

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
            if (p not in self.data and people[p].isFriendsWithAll(self.data) 
                    and p not in self.exclude):
                self.data.add(p)

    """
    Remove all items in self.data that aren't in the clique,
    starting from random point
    """
    def validate(self):
        items = list(self.data)
        start = random.randint(0, len(items) - 1)
        for p in items[start:]:
            if not people[p].isFriendsWithAll(self.data) or p in self.exclude:
                self.data.discard(p)

        itemsr = items[:start]
        itemsr.reverse()
        for p in itemsr:
            if not people[p].isFriendsWithAll(self.data) or p in self.exclude:
                self.data.discard(p)


    """
    Add random items to the set that won't mess it up to badly
    """
    def mutate(self, n):
        candidates = []
        for p in range(0, len(people)):
            if p not in self.data and p not in self.exclude:
                candidates += [(p, people[p].countFriendsWith(self.data))]
            
        candidates.sort(lambda a, b: a[1] - b[1])
        # add three highly ranked items
        for c in candidates[:n]:
            self.data.add(c[0])

        self.validate()

    def breed(self, other):
        self.merge(other)
        self.mutate(random.randint(0, 5))

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

def GAmaxclique(exclude, gens):
    newpop = [Clique([p], exclude) for p in random.sample(range(len(people)), 20)]
    for gen in range(gens):
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
    return pop[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python project2.py <input file> [<# of generations>]"

    gens = 20
    if len(sys.argv) > 2:
        gens = int(sys.argv[2])

    load(sys.argv[1])

    p1 = GAmaxclique([], gens)
    p2 = GAmaxclique(p1.data, gens)
    p3 = GAmaxclique(p1.data | p2.data, gens)

    print p1
    print p2
    print p3
    print
    print (p1.data & p2.data)
    print (p2.data & p3.data)
    print (p1.data & p3.data)
    print
    print len(p1.data), len(p2.data), len(p3.data)
    print "total: %d" % (len(p1.data) + len(p2.data) + len(p3.data))

    if raw_input('Accept results? (y/n)').lower() == 'y':
        d1 = open('Data1.dat', 'w')
        d2 = open('Data2.dat', 'w')
        d3 = open('Data3.dat', 'w')

        for p, d in zip([p1.data, p2.data, p3.data], [d1, d2, d3]):
            d.write('%d\n' % (len(p) + 1))
            d.write(''.join(['%d\n' % person for person in p]))
            d.close()

