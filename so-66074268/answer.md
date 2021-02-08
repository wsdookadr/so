> also, what are the concepts that are being used in this code? are there any books/courses i can take for this?

The code mentioned by you from the [`Deep::Hash::Utils`](https://metacpan.org/pod/Deep::Hash::Utils) CPAN module is mainly handling nested data structures.

A couple of places to read about these:
- the official docs: [perldsc](https://perldoc.perl.org/perldsc) ; [perlreftut](https://perldoc.perl.org/perlreftut) ; [perlref](https://perldoc.perl.org/perlref) ; 
- [Modern Perl](http://onyxneon.com/books/modern_perl/modern_perl_2016_letter.pdf) by chromatic has a section on Nested Data Structures around page 60
- [Intermediate Perl: Beyond The Basics of Learning Perl 2nd edition](https://www.amazon.com/Intermediate-Perl-Beyond-Basics-Learning/dp/1449393098/) has a section about Nested Data Structures around page 44. 

In the most basic case, in these nested data structures, every node has one of the following types:
- scalar
- hashref
- arrayref

In turn, the values in the array pointed to by an arrayref can be of type scalar/hashref/arrayref.
The same goes for the values of the hash pointed to by an arrayref, it can be of type scalar/hashref/arrayref.

This induces a [tree-like](https://en.wikipedia.org/wiki/Tree_(data_structure)) structure. The algorithm for traversing such a tree is [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)
where some additional logic is required to check the type of the node and depending on the type decide how to proceed further down the tree.

To make a parallel, all of this is not that much different from traversing a filesystem hierarchy (see [link1](https://stackoverflow.com/a/25175976/827519), [link2](https://stackoverflow.com/a/6338531/827519)).

A [bigger list called perlres](https://github.com/thibaultduponchelle/perlres) on Perl resources is available.

---

In this specific case, the function `reach` from [`Deep::Hash::Utils`](https://metacpan.org/pod/Deep::Hash::Utils) acts as an iterator, and it returns all paths descending from the root down to each leaf.
Whenever a `@path` to a leaf is found, its elements are compared side-by-side with another list called `@output`, and there are three cases:
- there's no element on that position, so we store it
- the elements are equal, so we skip them
- the elements are different, so we merge them together in a list


```perl
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

```

OUTPUT:

```
$VAR1 = [
          'bar',
          'cmd_opts',
          'gld_upf',
          [
            'abc',
            'def'
          ]
        ];
```
