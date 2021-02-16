#!/usr/bin/python3
import string
import copy
#
# Note: this generates all the possible placements of
# _distinct_ labelled balls into urns.
#
class BinPartitions:

    def __init__(self, balls, num_bins):
        self.balls = balls
        self.bins = [{} for x in range(num_bins)]

    def print_bins(self, bins):
        L = []
        for b in bins:
            buf = ''.join(b.keys())
            L += [buf]
        print(",".join(L))

    def _gen_helper(self,balls,bins):
        if len(balls) == 0:
            self.print_bins(bins)
        else:
            A,B = balls[0],balls[1:]
            for i in range(len(bins)):
                new_bins = copy.deepcopy(bins)
                new_bins[i].update({A:1})
                self._gen_helper(B,new_bins)

    def get_all(self):
        self._gen_helper(self.balls,self.bins)

#BinPartitions(['A','B'],2).get_all()
#BinPartitions(string.ascii_uppercase[:3],3).get_all()
BinPartitions(string.ascii_uppercase[:6],3).get_all()
#gen()


