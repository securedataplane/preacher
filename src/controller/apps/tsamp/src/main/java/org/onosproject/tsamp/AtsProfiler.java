/**
 * Kashyap Thimmaraju
 * kashyap.thimmaraju@sect.tu-berlin.de
 * AtsProfiler is a class to profile the
 * performance of the ATS detector.
 * startTime
 * stopTime
 * totalDetections
 * totalDetectionTime
 * totalDetectionRate=totalDetections/totalDetectionTime
 */
package org.onosproject.tsamp;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class AtsProfiler {
    int id;
    Instant startTime;
    Instant stopTime;
    int totalDetections;
    long totalDetectionTime;
    double totalDetectionRate;
    List<Double> detectionRateList;
    List<Double> detectionTimeList;

    public List<Double> getDetectionRateList() {
        return detectionRateList;
    }

    public void setDetectionRateList() {
        this.detectionRateList.add(getTotalDetections(), getTotalDetectionRate());
    }

    public List<Double> getDetectionTimeList() {
        return detectionTimeList;
    }

    public void setDetectionTimeList(long detectionTime) {
        this.detectionTimeList.add(getTotalDetections(), (double) detectionTime);
    }

    /*
     * profilerId is provided
     * to distinguish between
     * different threads/detectors.
     */
    public AtsProfiler(int profilerId) {
        this.id = profilerId;
        totalDetections = 0;
        totalDetectionTime = 0;
        totalDetectionRate = 0;
        detectionRateList = new ArrayList<Double>();
        detectionTimeList = new ArrayList<Double>();
        setDetectionRateList();
        setDetectionTimeList(0);
    }

    /*
     * The DetectionRate is computed
     * by taking the sum of total detections
     * made divided by the total time
     * spent in detections multiplied
     * by 1000 to get to seconds.
     */
    public void computeDetectionRate() {
        long detectionTime = Duration.between(getStartTime(), getStopTime()).toMillis();
        setTotalDetections(getTotalDetections() + 1);
        setTotalDetectionTime(getTotalDetectionTime() + detectionTime);
        setTotalDetectionRate((double) getTotalDetections() / getTotalDetectionTime() * 1000);
        setDetectionRateList();
        setDetectionTimeList(detectionTime);
    }

    /*
     * AtsProfiler handles adding the detection rate
     * for its detector into the static profileTable
     * used in TrajectorySampling.
     * This has been modified to add only the detection time
     * of that one detection instead of the total detection time.
     */
    public void addToProfileTable(Map<Integer, List<Double>> profileTable) {
        if (profileTable.isEmpty()) {
            profileTable.put(this.id, getDetectionTimeList());
//            profileTable.put(this.id, getDetectionRateList());
        }
        if (profileTable.containsKey(this.id)) {
            profileTable.replace(this.id, getDetectionTimeList());
//            profileTable.replace(this.id, getDetectionRateList());
        } else {
            profileTable.put(id, getDetectionTimeList());
//            profileTable.put(id, getDetectionRateList());
        }
    }

    public String toString() {
        String stringValue = "";
        int i = 0;
        stringValue += "\nDetectorId: " + this.id;
        stringValue += "\nTotal Detections: " + getTotalDetections();
        stringValue += "\nTotal Detection Time(ms): " + getTotalDetectionTime();
        stringValue += "\nTotal Detection Rate: " + String.format("%.4f", getTotalDetectionRate());
        stringValue += "\nDetection History:";
        for (double detectRate : getDetectionRateList()) {
            stringValue += "\nDetection: " + i + ", ";
            stringValue += "Avg. Detection Rate: " + String.format("%.4f", detectRate);
            i++;
        }
        return stringValue;
    }

    public Instant getStartTime() {
        return startTime;
    }

    public void setStartTime(Instant startTime) {
        this.startTime = startTime;
    }

    public Instant getStopTime() {
        return stopTime;
    }

    public void setStopTime(Instant stopTime) {
        this.stopTime = stopTime;
    }

    public int getTotalDetections() {
        return totalDetections;
    }

    public void setTotalDetections(int detections) {
        this.totalDetections = detections;
    }

    public long getTotalDetectionTime() {
        return totalDetectionTime;
    }

    public void setTotalDetectionTime(long detectionTime) {
        this.totalDetectionTime = detectionTime;
    }

    public double getTotalDetectionRate() {
        return totalDetectionRate;
    }

    public void setTotalDetectionRate(double totalDetectionRate) {
        this.totalDetectionRate = totalDetectionRate;
    }
}
