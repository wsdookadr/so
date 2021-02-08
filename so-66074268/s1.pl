#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
use Deep::Hash::Utils qw/reach/;

my $input = { bar => {cmd_opts => { gld_upf => ['abc' , 'def']} } };

my @output = ();

while (my @path = reach($input)) {
    for(my $i=0;$i<=$#path;$i++){
        if(defined $output[$i]) {
            if(ref($output[$i]) eq "") {
                if($output[$i] eq $path[$i]) {
                    next;
                };
                my $e1 = $output[$i];
                my $e2 = $path[$i];
                $output[$i] = [$e1,$e2];
            }elsif(ref($output[$i]) eq "ARRAY"){
                push @{$output[$i]}, $path[$i];
            };
        } else {
            $output[$i] = $path[$i];
        };
    };
}

print Dumper \@output;

