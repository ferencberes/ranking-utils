package ciir.umass.edu.metric;

import ciir.umass.edu.learning.RankList;

public class WeightedCorrelationScorer extends MetricScorer {

	public WeightedCorrelationScorer()
	{
		this.k = 10;
	}
	
	public WeightedCorrelationScorer(int k)
	{
		this.k = k;
	}
	
	public WeightedCorrelationScorer clone()
	{
		return new WeightedCorrelationScorer();
	}
	
	public double score(RankList rl)
	{
		
		k = rl.size();
		
		double[] labels = getLabels(rl);
		double[] cached_values = getCachedValues(rl);
		return getWeightedCorrelation(cached_values, getWeightedStatsAndSortedIndex(cached_values), labels, getWeightedStatsAndSortedIndex(labels));
	}	
	
	public String name()
	{
		return "W_CORREL@"+k;
	}
	
	public double[][] swapChange(RankList rl)
	{
		int size = rl.size();
		double[] labels = getLabels(rl);
		double[] cached_values = getCachedValues(rl);
		StatStorer stats_for_cached = getWeightedStatsAndSortedIndex(cached_values);
		StatStorer stats_for_labels = getWeightedStatsAndSortedIndex(labels);
		double c_mean = stats_for_cached.getMean();
		double c_variance = stats_for_cached.getVariance();
		double l_variance = stats_for_labels.getVariance();
		int[] idx = stats_for_labels.getSorted_idx();
		double w_sum = 0.0;
		for(int i=0;i<size;i++) {
			w_sum += 1 / (i+1);
		}
		double denom = w_sum * Math.sqrt(c_variance * l_variance);
		
		double[][] changes = new double[rl.size()][];
		for(int i=0;i<rl.size();i++)
			changes[i] = new double[rl.size()];
		for(int i=0;i<size;i++)
			for(int j=i+1;j<rl.size();j++)
				changes[j][i] = changes[i][j] = ((cached_values[idx[i]] - c_mean) / (i+1) - (cached_values[idx[j]] - c_mean) / (j+1)) * (labels[idx[i]] - labels[idx[j]]) / denom;
		return changes;
	}
	
	private double getWeightedCorrelation(double[] cached, StatStorer stats_for_cached, double[] labels, StatStorer stats_for_labels) {
		double c_mean = stats_for_cached.getMean();
		double c_variance = stats_for_cached.getVariance();
		int[] idx = stats_for_labels.getSorted_idx();
		double l_mean = stats_for_labels.getMean();
		double l_variance = stats_for_labels.getVariance();
		double sum = 0.0;
		double weight_sum = 0.0;
		for(int i=0; i<cached.length; i++) {
			weight_sum += (1 / (i+1));
			sum += (cached[idx[i]]-c_mean) * (labels[idx[i]] - l_mean) * (1 / (i+1));
		}
		return sum / (weight_sum * Math.sqrt(c_variance * l_variance));
	}
}
