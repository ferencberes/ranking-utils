# ranking-utils
learning to rank experiments

## About

This repository is based on the [RankLib](http://sourceforge.net/p/lemur/wiki/RankLib/ "") project.

I was experimenting with listwise methods optimized for correlation measures.

The following objects were added to the original project:

   * [CorrelationScorer](/trunk/src/ciir/umass/edu/metric/CorrelationScorer.java ""): Pearson's correlation
   * [WeightedCorrelationScorer](/trunk/src/ciir/umass/edu/metric/WeightedCorrelationScorer.java ""): weighted Pearson's correlation
   * [RankCorrelationScorer](/trunk/src/ciir/umass/edu/metric/RankCorrelationScorer.java ""): Spearman's correlation  
   * [WeightedRankCorrelationScorer](/trunk/src/ciir/umass/edu/metric/WeightedRankCorrelationScorer.java ""): weighted Spearman's correlation  