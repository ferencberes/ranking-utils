package ciir.umass.edu.metric;

import java.util.HashMap;
import java.util.Map;

import ciir.umass.edu.learning.RankList;
import ciir.umass.edu.utilities.Sorter;

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
		if(rl.size() == 0)
			return 0;

		int l_size = k;
		if(k > rl.size() || k <= 0)
			l_size = rl.size();
		
		double[] labels_all = getLabels(rl);
		double[] cached_values_all = getCachedValues(rl);
		long[] vertex_ids_all = getDescription(rl);
		
		Map<Long, Double> labels_map = new HashMap<Long, Double>();
		Map<Long, Double> cached_map = new HashMap<Long, Double>();
		for(int i=0; i<vertex_ids_all.length; i++) {
			labels_map.put(vertex_ids_all[i], labels_all[i]);
			cached_map.put(vertex_ids_all[i], cached_values_all[i]);
		}
		
		int[] idx_labels = Sorter.sort(labels_all, false);
		double[] labels = new double[l_size];
		double[] cached_values = new double[l_size];
//		if(k<rl.size()){
//			//System.out.println("test");
//			//System.exit(2);
//			long[] labels_vertices = new long[l_size];
//			long[] cached_values_vertices = new long[l_size]; 
//			for(int i=0; i<l_size; i++) {
//				labels_vertices[i] = vertex_ids_all[idx_labels[i]];
//				cached_values_vertices[i] = vertex_ids_all[i];
//			}
//			double[][] full_lists = getExpandedLists(cached_values_vertices, labels_vertices, cached_map, labels_map);
//			cached_values = full_lists[0];
//			labels = full_lists[1];
//		} else {
			labels = labels_all;
			cached_values = cached_values_all;
//		}
		
		StatStorer labels_storer = getStatsAndSortedIndex(labels);
		StatStorer cached_storer = getStatsAndSortedIndex(cached_values);
		
//		System.out.println(printVector(labels));
//		System.out.println(printVector(cached_values));
		
//		System.out.println(labels.toString());
//		System.exit(2);
		
		return getCorrelation(cached_values, cached_storer, labels, labels_storer);
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
		StatStorer stats_for_cached = getStatsAndSortedIndex(cached_values);
		StatStorer stats_for_labels = getStatsAndSortedIndex(labels);
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
	
	private String printVector(double[] vec) {
		String out = "";
		for(int i=0; i<vec.length; i++) {
			out += vec[i] + ",";
		}
		out += "\n";
		return out;
	}
}
