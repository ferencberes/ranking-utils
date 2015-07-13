/*===============================================================================
 * Copyright (c) 2010-2012 University of Massachusetts.  All Rights Reserved.
 *
 * Use of the RankLib package is subject to the terms of the software license set 
 * forth in the LICENSE file included with this software, and also available at
 * http://people.cs.umass.edu/~vdang/ranklib_license.html
 *===============================================================================
 */

package ciir.umass.edu.metric;


import java.util.List;

import ciir.umass.edu.learning.RankList;
import ciir.umass.edu.utilities.Sorter;

/**
 * @author vdang
 * A generic retrieval measure computation interface. 
 */
public class MetricScorer {

	protected int k = 10;
	
	public MetricScorer() 
	{
		
	}
	public void setK(int k)
	{
		this.k = k;
	}
	public int getK()
	{
		return k;
	}
	public void loadExternalRelevanceJudgment(String qrelFile)
	{
		
	}
	public double score(List<RankList> rl)
	{
		double score = 0.0;
		for(int i=0;i<rl.size();i++)
			score += score(rl.get(i));
		return score/rl.size();
	}
	
	protected int[] getRelevanceLabels(RankList rl)
	{
		int[] rel = new int[rl.size()];
		for(int i=0;i<rl.size();i++)
			rel[i] = (int)rl.get(i).getLabel();
		return rel;
	}
	
	// NOTE: for correlation scorers
	protected long[] getDescription(RankList rl)
	{
		long[] rel = new long[rl.size()];
		for(int i=0;i<rl.size();i++)
			rel[i] = Long.parseLong(rl.get(i).getDescription().substring(2)); // it is supposed that description holds vertex ids. e.g.: # 15115660
		return rel;
	}
	
	// NOTE: for correlation scorers
	protected double[] getLabels(RankList rl)
	{
		double[] rel = new double[rl.size()];
		for(int i=0;i<rl.size();i++)
			rel[i] = rl.get(i).getLabel();
		return rel;
	}
	
	// NOTE: for correlation scorers
	protected double[] getCachedValues(RankList rl)
	{
		double[] rel = new double[rl.size()];
		for(int i=0;i<rl.size();i++)
			rel[i] = rl.get(i).getCached();
		return rel;
	}
	
	/**
	 * MUST BE OVER-RIDDEN
	 * @param rl
	 * @return
	 */
	public double score(RankList rl)
	{
		return 0.0;
	}
	public MetricScorer clone()
	{
		return null;
	}
	public String name()
	{
		return "";
	}
	public double[][] swapChange(RankList rl)
	{
		return null;
	}
	
	// NOTE: for correlation scorers
	protected StatStorer getStatsAndSortedIndex(double[] records)
	{
		int size = records.length;
		int[] idx = Sorter.sort(records, false);
		
		double sum = 0.0;
		for(int i=0;i<size;i++) {
			sum += records[i]; // TODO: inkabb itt kene osztani?
		}
		double mean = sum / size;
		double var_s = 0.0;
		for(int i=0;i<size;i++)
			var_s += Math.pow(records[i]-mean, 2);
		double variance = var_s / size;
		return new StatStorer(idx, mean, variance);
	}
	
	// NOTE: for correlation scorers
	protected StatStorer getWeightedStatsAndSortedIndex(double[] records)
	{
		int size = records.length;
		int[] idx = Sorter.sort(records, false);
		
		double sum = 0.0;
		double weight_sum = 0.0;
		for(int i=0;i<size;i++) {
			weight_sum += (1.0 / (i+1));
			sum += (records[idx[i]] * (1.0 / (i+1)));
		}
		double mean = sum / weight_sum;
		double var_s = 0.0;
		for(int i=0;i<size;i++)
			var_s += (Math.pow(records[idx[i]]-mean, 2) * (1.0 / (i+1)));
		double w_variance = var_s / weight_sum;
		return new StatStorer(idx, mean, w_variance);
	}
	
	// NOTE: for correlation scorers
	public class StatStorer {
		private int[] sorted_idx;
		private  double mean;
		private double variance;
	
		public StatStorer(int[] sorted, double m, double var) {
			this.sorted_idx = sorted;
			this.mean = m;
			this.variance = var;
		}

		public int[] getSorted_idx() {
			return sorted_idx;
		}
		public double getMean() {
			return mean;
		}
		public double getVariance() {
			return variance;
		}
	}
	
	protected String printVector(double[] vec) {
		String out = "";
		for(int i=0; i<vec.length; i++) {
			out += vec[i] + ",";
		}
		out += "\n";
		return out;
	}
}
