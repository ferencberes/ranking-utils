package ciir.umass.edu.metric;

import java.util.Random;

import ciir.umass.edu.learning.RankList;

public class WeightedCorrelationScorer extends MetricScorer {

	private Random gen = new Random();
	
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
		return getWeightedCorrelation(cached_values, getWeightedStatsAndSortedIndex(cached_values, false), labels, getWeightedStatsAndSortedIndex(labels, false));
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
		return swapChangeCalculator(cached_values, labels, size, false);
	}
		
	public double[][] swapChangeCalculator(double[] cached_values, double[] labels, int size, boolean is_ascending)
	{	
		StatStorer stats_for_cached = getWeightedStatsAndSortedIndex(cached_values, is_ascending);
		StatStorer stats_for_labels = getWeightedStatsAndSortedIndex(labels, is_ascending);
		double c_mean = stats_for_cached.getMean();
		double c_variance = stats_for_cached.getVariance();
		double l_variance = stats_for_labels.getVariance();
		int[] idx = stats_for_labels.getSorted_idx();
		double w_sum = 0.0;
		for(int i=0;i<size;i++) {
			w_sum += 1 / (i+1);
		}
		double denom = w_sum * Math.sqrt(c_variance * l_variance);
		//System.out.println(denom);
		System.out.println(printVector(labels));
		System.out.println(printVector(cached_values));
		
		double[][] changes = new double[size][];
		for(int i=0;i<size;i++) {
			changes[i] = new double[size];
		}
		for(int i=0;i<size;i++) {
			for(int j=i+1;j<size;j++) {
				//changes[j][i] = changes[i][j] = ((cached_values[idx[i]] - c_mean) / (i+1) - (cached_values[idx[j]] - c_mean) / (j+1)) * (labels[idx[i]] - labels[idx[j]]) / denom;
				if(cached_values[i] == cached_values[j]) {
					changes[j][i] = changes[i][j] = gen.nextFloat() * Math.pow(10, -5);
				} else if(labels[i] == labels[j]) {
					changes[j][i] = changes[i][j] = 0.0;
				} else {	
					changes[j][i] = changes[i][j] = ((cached_values[idx[i]] - c_mean) / (i+1) - (cached_values[idx[j]] - c_mean) / (j+1)) * (labels[idx[i]] - labels[idx[j]]) / denom;
				}
				System.out.println(changes[i][j]);
				System.exit(2);
			}
		}
		return changes;
	}
	
	protected double getWeightedCorrelation(double[] cached, StatStorer stats_for_cached, double[] labels, StatStorer stats_for_labels) {
		double c_mean = stats_for_cached.getMean();
		double c_variance = stats_for_cached.getVariance();
		int[] idx = stats_for_labels.getSorted_idx();
		double l_mean = stats_for_labels.getMean();
		double l_variance = stats_for_labels.getVariance();
		double sum = 0.0;
		double weight_sum = 0.0;
		for(int i=0; i<cached.length; i++) {
			weight_sum += (1.0 / (i+1));
			sum += ((cached[idx[i]]-c_mean) * (labels[idx[i]] - l_mean) * (1.0 / (i+1)));
		}
		return sum / (weight_sum * Math.sqrt(c_variance * l_variance));
	}
}
