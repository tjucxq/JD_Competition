#########################################################################
#   Copyright (C) 2013 All rights reserved.
#   
#   文件名称：Select.pl
#   创 建 者：刘禹 finallyly liuyusi0121@sogou-inc.com(ext 6141)
#   创建日期：2013年04月02日
#   描    述：
#
#   备    注：
#
#########################################################################

use strict;
use warnings;
use Time::HiRes;
# please add your code here!
my $tmStarted=Time::HiRes::time;
if(3!=scalar @ARGV)
{
    &PrintUsage();
    exit 1;
}
my %hash=();
my $line="";
my $linecount=1;
open FREF, "<$ARGV[0]" or die "can not open reffile:$!\n";
while(defined($line=<FREF>))
{
    chomp $line;
    my @vec=split /\t/,$line;
    $hash{$vec[0]}=1;
}
close FREF;
open FIN,"<$ARGV[1]" or die "can not open inputfile:$!\n";
open FOUT, ">$ARGV[2]" or die "can not create outputfile:$!\n";
while(defined($line=<FIN>))
{
    chomp $line;
    if(defined($hash{$linecount}))
    {
        print FOUT "$line\t$linecount\n";
    }
    $linecount++;
}
close FIN;
close FOUT;
print STDERR "$0 has finished,congratulations!\n";
print STDERR "Time elapsed:".(Time::HiRes::time-$tmStarted)."\n";
=pod
    Subroutine(s);
=cut
sub PrintUsage
{
    print STDERR "perl program.pl [IN] ref_file [IN] input_file [OUT] output_file\n";
}
