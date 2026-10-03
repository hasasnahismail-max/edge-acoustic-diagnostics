#include <iostream>
#include <vector>
#include "audio_processor.cpp" // أو ربطه عبر Header مستقبلاً
#include "eade_dsp.cpp"

int main(int argc, char* argv[]) {
    std::cout << "===========================================\n";
    std::cout << " ZINO EDGE-ACOUSTIC DIAGNOSTIC ENGINE (C++ CORE)\n";
    std::cout << "===========================================\n";

    std::vector<float> audioData;
    int sampleRate = 22050;

    // إذا قام المستخدم بتمرير ملف صوتي، قم بتحميله، وإلا استخدم إشارة اصطناعية للاختبار
    if (argc > 1) {
        std::string filename = argv[1];
        audioData = AudioProcessor::loadWavFile(filename, sampleRate);
    }

    if (audioData.empty()) {
        std::cout << "[EADE Notice] Using synthetic engine test signal...\nÂn";
        // إشارة اصطناعية تحاكي ترددات احتكاك أو خلل في المحرك
        audioData.resize(4096);
        for (size_t i = 0; i < audioData.size(); ++i) {
            audioData[i] = 0.5f * sin(2.0 * 3.14159 * 220.0 * i / sampleRate) + 
                           0.2f * sin(2.0 * 3.14159 * 1600.0 * i / sampleRate);
        }
    }

    // تشغيل محرك التحليل الطيفي والتشخيص الهندسي
    EADEDSP::runDiagnostics(audioData, sampleRate);

    return 0;
}
