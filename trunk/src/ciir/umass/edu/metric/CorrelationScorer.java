package ciir.umass.edu.metric;

import ciir.umass.edu.learning.RankList;

public class CorrelationScorer extends MetricScorer {

	public CorrelationScorer()
	{
		this.k = 10;
	}
	
	public CorrelationScorer(int k)
	{
		this.k = k;
	}
	
	public CorrelationScorer clone()
	{
		return new CorrelationScorer();
	}
	
	public double score(RankList rl)
	{
		
		k = rl.size();
//		if(rl.size() == 0)
//			return 0;
//
//		int l_size = k;
//		if(k > rl.size() || k <= 0)
//			l_size = rl.size();
		// TODO: handle at k version of correlation!!!
		
		double[] labels = getLabels(rl);
		double[] cached_values = getCachedValues(rl);
//		System.out.println(labels.toString());
//		System.exit(2);
		
		return getCorrelation(cached_values, getStatsAndOrigiList(cached_values), labels, getStatsAndOrigiList(labels));
	}	
	
	public String name()
	{
		return "CORREL@"+k;
	}
	
	public double[][] swapChange(RankList rl)
	{
		int size = rl.size();
		// TODO: handle at k version of correlation!!!
//		int size = (rl.size() > k) ? k : rl.size();
		
		double[] labels = getLabels(rl);
		double[] cached_values = getCachedValues(rl);
		StatStorer stats_for_cached = getStatsAndOrigiList(cached_values);
		StatStorer stats_for_labels = getStatsAndOrigiList(labels);
		double c_variance = stats_for_cached.getVariance();
		double l_variance = stats_for_labels.getVariance();
		double denom = size * Math.sqrt(c_variance * l_variance);
		
		double[][] changes = new double[rl.size()][];
		for(int i=0;i<rl.size();i++)
			changes[i] = new double[rl.size()];
		for(int i=0;i<size;i++)
			for(int j=i+1;j<rl.size();j++)
				changes[j][i] = changes[i][j] = ((cached_values[i] - cached_values[j]) * (labels[i] - labels[j])) / denom;

		return changes;
	}
	
	private double getCorrelation(double[] cached, StatStorer stats_for_cached, double[] labels, StatStorer stats_for_labels) {
		double c_mean = stats_for_cached.getMean();
		double c_variance = stats_for_cached.getVariance();
		double l_mean = stats_for_labels.getMean();
		double l_variance = stats_for_labels.getVariance();
		double sum = 0.0;
		for(int i=0; i<cached.length; i++) {
			sum += (cached[i]-c_mean) * (labels[i] - l_mean);
		}
		return sum / (cached.length * Math.sqrt(c_variance * l_variance));
	}
}
