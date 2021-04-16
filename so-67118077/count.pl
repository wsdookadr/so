#!/usr/bin/perl
use strict;
use warnings;

my $part = 0;
my @cnt_part;
while(my $line = <STDIN>) {
    if($. == 1) {
        next;
    }elsif($line =~ m{^\(PART (\d+)\)}) {
        $part = $1;
    }else {
        my @cols = split(m{\s+},$line);
        if(@cols == 6) {
            my $potential = $cols[3];
            if(0.7 <= $potential) {
                $cnt_part[$part]++;
            };
        };
    };
};

for(my $i=1;$i<=$#cnt_part;$i++){
    print "Part $i:\n";
    print "$cnt_part[$i] (values 0.7 <=)\n";
};

