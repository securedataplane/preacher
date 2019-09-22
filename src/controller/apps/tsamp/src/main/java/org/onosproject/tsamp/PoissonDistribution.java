package org.onosproject.tsamp;

import java.util.Random;

public class PoissonDistribution extends Random {
    /**
     * This applet was written by Charles Stanton.
     * The source code was taken from the following site:
     * http://www.math.csusb.edu/faculty/stanton/probstat/poisson.html
     */
    private static final long serialVersionUID = 1L;

    public int nextPoisson(double lambda) {
        double elambda = Math.exp(-1 * lambda);
        double product = 1;
        int count =  0;
        int result = 0;
        while (product >= elambda) {
            product *= nextDouble();
            result = count;
            count++; // keep result one behind
            }
        return result;
        }
}