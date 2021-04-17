#!/usr/bin/perl
use strict;
use warnings;

my $cnt = {};
while(my $line = <STDIN>) {
    if($. == 1) {
        next;
    }else {
        my @cols = split(m{\s+},$line);
        if(@cols == 6) {
            my $potential = $cols[3];
            my $id = $cols[0];
            $id =~ s{^\;}{};
            if(0.7 <= $potential) {
                $cnt->{$id}++;
            };
        };
    };
};

my @ids_found = sort { $a cmp $b } (keys %$cnt);

for my $id (@ids_found) {
    print "PART $id:\n";
    print "$cnt->{$id} (values 0.7 <=)\n";
};

