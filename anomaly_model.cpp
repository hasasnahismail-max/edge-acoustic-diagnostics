#include <iostream>
#include <vector>
#include <string>
#include <cmath>

struct DiagnosticResult {
    float healthIndex;
    float anomalyScore;
    std::string status;
    std::string detectedFault;
    std::string recommendation;
};

class AnomalyModel {
public:
    static DiagnosticResult evaluate(float rmsEnergy, float spectralCentroid) {
        DiagnosticResult result;
        
        // حساب درجة الشذوذ بناءً على مستويات الطاقة والتردد
        float energyAnomaly = std::abs(rmsEnergy - 0.15f) / 0.15f;
        result.anomalyScore = std::min(1.0f, energyAnomaly);
        
        // حساب مؤشر الصحة (كلما زاد الشذوذ قل المؤشر)
        result.healthIndex = std::max(0.0f, (1.0f - result.anomalyScore) * 100.0f);

        if (result.healthIndex < 50.0f) {
            result.status = "CRITICAL DEVIATION DETECTED";
            result.detectedFault = "Crankshaft Main Bearings Wear (تآكل سبائك العمود المرفقي)";
            result.recommendation = "Immediate shutdown advised. Inspect oil pan for metallic debris.";
        } else if (result.healthIndex < 80.0f) {
            result.status = "WARNING - MODERATE ANOMALY";
            result.detectedFault = "Minor Mechanical Vibration / Loose Belt";
            result.recommendation = "Schedule maintenance check within 24 operating hours.";
        } else {
            result.status = "SYSTEM HEALTHY";
            result.detectedFault = "None";
            result.recommendation = "Normal operating conditions. Continue routine monitoring.";
        }

        return result;
    }
};
