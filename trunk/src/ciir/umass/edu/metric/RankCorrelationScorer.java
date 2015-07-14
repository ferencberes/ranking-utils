package ciir.umass.edu.metric;

import ciir.umass.edu.learning.RankList;
import ciir.umass.edu.utilities.Sorter;

public class RankCorrelationScorer extends CorrelationScorer {
	public RankCorrelationScorer()
	{
		this.k = 10;
	}
	
	public RankCorrelationScorer(int k)
	{
		this.k = k;
	}
	
	public RankCorrelationScorer clone()
	{
		return new RankCorrelationScorer();
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
		return getCorrelation(cached_values_ranked, getStatsAndSortedIndex(cached_values_ranked, true), labels_ranked, getStatsAndSortedIndex(labels_ranked, true));
	}
	
//	public double score(RankList rl) // TEST for score conversion
//	{
//		k = rl.size();
//		double[] labels = new double[]{2.0, 3.0, 2.0, 2.0};
//		int[] idx_labels = Sorter.sort(labels, false);
//		double[] cached_values = new double[]{1.0, 0.5, 0.5, 0.2};
//		int[] idx_cached = Sorter.sort(cached_values, false);
//		double[] labels_ranked = convertCentralityToRank(labels, idx_labels); // it contains averaged positions as ranks
//		double[] cached_values_ranked = convertCentralityToRank(cached_values, idx_cached); // it contains averaged positions as ranks
//		System.exit(1);
//		
//		return getCorrelation(cached_values_ranked, getStatsAndSortedIndex(cached_values_ranked), labels_ranked, getStatsAndSortedIndex(labels_ranked));
//	}
	
	public String name()
	{
		return "RANKCORREL@"+k;
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
