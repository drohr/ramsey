ramsey :fork_and_knife:
======
Fabric hack that runs [foodcritic](http://acrmp.github.io/foodcritic/) on your invidual cookbooks and outputs test data in junit xml. 

Makes life easier when doing tests in your CI tool, like [Atlassian Bamboo](http://www.atlassian.com/software/bamboo/) or [Jenkins](http://jenkins-ci.org/).

```bash
$ ls cookbooks/
build-essential  redis
$ fab ramsey
Done with testcase for build-essential
Done with testcase for redis
```

Not much testing done, works for me, might not work for you.
