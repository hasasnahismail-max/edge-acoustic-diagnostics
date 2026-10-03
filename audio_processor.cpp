#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>

class AudioProcessor {
public:
    static bool loadWAV(const std::string& filePath, std::vector<float>& audioData) {
        std::ifstream file(filePath, std::ios::binary);
        if (!file.is_open()) return false;

        file.seekg(44); // تخطي 44-byte WAV header
        int16_t sample;
        while (file.read(reinterpret_cast<char*>(&sample), sizeof(sample))) {
            audioData.push_back(sample / 32768.0f);
        }
        return !audioData.empty();
    }

    static std::vector<float> generateSyntheticSignal(size_t numSamples, int sampleRate) {
        std::vector<float> signal(numSamples);
        for (size_t i = 0; i < numSamples; ++i) {
            signal[i] = 0.5f * std::sin(2.0f * M_PI * 220.0f * i / sampleRate);
        }
        return signal;
    }
};
