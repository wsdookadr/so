To count the number of lines, for each part, that match some condition on a certain column, you can just loop over the line, skip the header, parse the part number, and use an array to count the number of lines matching for each part.

After this you can just loop over the counts recorded in the array and print them out in your specific format.

```perl
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
```

To run it, just pipe the entire file through the Perl script: 
```
cat in.txt | perl count.pl
```

and you get an output like this:

```
Part 1:
1 (values 0.7 <=)
Part 2:
2 (values 0.7 <=)
Part 3:
2 (values 0.7 <=)
```

If you want to also display the counts into words, you can use [`Lingua::EN::Numbers`](https://metacpan.org/pod/Lingua::EN::Numbers) (see [this program](https://github.com/wsdookadr/so/blob/master/so-67118077/count2.pl) ) and you get an output very similar to the one in your post:

```
Part 1:
1 (one values 0.7 <=)
Part 2:
2 (two values 0.7 <=)
Part 3:
2 (two values 0.7 <=)
```


All the code in this post is also [available here](https://github.com/wsdookadr/so/tree/master/so-67118077).


