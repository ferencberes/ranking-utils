package ciir.umass.edu.metric;

import ciir.umass.edu.learning.RankList;
import ciir.umass.edu.utilities.Sorter;

public class WeightedRankCorrelationScorer extends WeightedCorrelationScorer {
	public WeightedRankCorrelationScorer()
	{
		this.k = 10;
	}
	
	public WeightedRankCorrelationScorer(int k)
	{
		this.k = k;
	}
	
	public WeightedRankCorrelationScorer clone()
	{
		return new WeightedRankCorrelationScorer();
	}
	
	public double score(RankList rl)
	{
		k = rl.size();
		double[] labels = getLabels(rl);
		int[] idx_labels = Sorter.sort(labels, false);
		double[] cached_values = getCachedValues(rl);
		int[] idx_cached = Sorter.sort(cached_values, false);
		double[] labels_ranked = convertCentralityToRank(labels, idx_labels); // it contains averaged positions as ranks
		double[] cached_values_ranked = convertCentralityToRank(cached_values, idx_cached); // it contains averaged positions as ranks
		return getWeightedCorrelation(cached_values_ranked, getWeightedStatsAndSortedIndex(cached_values_ranked, true), labels_ranked, getWeightedStatsAndSortedIndex(labels_ranked, true));
	}	
	
	public String name()
	{
		return "W_RANKCORREL@"+k;
	}
	
	public double[][] swapChange(RankList rl)
	{
		int size = rl.size();
		double[] labels = getLabels(rl);
		int[] idx_labels = Sorter.sort(labels, false);
		double[] cached_values = getCachedValues(rl);
		int[] idx_cached = Sorter.sort(cached_values, false);
		double[] labels_ranked = convertCentralityToRank(labels, idx_labels); // it contains averaged positions as ranks
		double[] cached_values_ranked = convertCentralityToRank(cached_values, idx_cached); // it contains averaged positions as ranks
		return swapChangeCalculator(cached_values_ranked, labels_ranked, size, true);
	}
}
