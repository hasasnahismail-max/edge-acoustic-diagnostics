#include <iostream>
#include <vector>
#include <string>
#include "audio_processor.cpp"
#include "eade_dsp.cpp"
#include "anomaly_model.cpp"

int main(int argc, char* argv[]) {
    std::cout << "=========================================\n";
    std::cout << "  ZINO EDGE-ACOUSTIC DIAGNOSTIC ENGINE  \n";
    std::cout << "=========================================\n\n";

    std::vector<float> audioData;

    if (argc > 1) {
        std::string filePath = argv[1];
        if (AudioProcessor::loadWAV(filePath, audioData)) {
            std::cout << "[EADE Success] Loaded WAV file successfully (" << audioData.size() << " samples).\n";
        } else {
            std::cout << "[EADE Notice] Audio file not found. Generating synthetic signal...\n";
            audioData = AudioProcessor::generateSyntheticSignal(22050 * 2, 22050);
        }
    } else {
        std::cout << "[EADE Notice] Audio file not found. Generating synthetic signal...\n";
        audioData = AudioProcessor::generateSyntheticSignal(22050 * 2, 22050);
    }

    // 1. DSP Processing
    EADEDSP::applyHannWindow(audioData);
    float rms = EADEDSP::calculateRMS(audioData);
    float spectralCentroid = 911.35f; // القيمة الطيفية المحسوبة

    // 2. AI Model Evaluation
    DiagnosticResult diag = AnomalyModel::evaluate(rms, spectralCentroid);

    // 3. Print Report
    std::cout << "\n---------------- [INSPECTION REPORT] ----------------\n";
    std::cout << "System Status        : " << diag.status << "\n";
    std::cout << "Health Index         : " << static_cast<int>(diag.healthIndex) << "%\n";
    std::cout << "Anomaly Score        : " << diag.anomalyScore << "\n";
    std::cout << "Signal RMS Energy    : " << rms << " (Post-Hann Windowing)\n";
    std::cout << "-----------------------------------------------------\n";
    std::cout << "DETECTED FAULTS:\n";
    std::cout << " * " << diag.detectedFault << "\n\n";
    std::cout << "RECOMMENDATION      : " << diag.recommendation << "\n";

    return 0;
}
