#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <cstdint>

class AudioProcessor {
public:
    static bool loadWAV(const std::string& filePath, std::vector<float>& audioData) {
        std::ifstream file(filePath, std::ios::binary);
        if (!file.is_open()) return false;

        // قراءة الهيدر للتحقق من عدد القنوات
        file.seekg(22);
        uint16_t numChannels = 0;
        file.read(reinterpret_cast<char*>(&numChannels), sizeof(numChannels));

        file.seekg(44); // الانتقال للعينات الصوتية
        int16_t sample1, sample2;

        if (numChannels == 2) {
            // تحويل Stereo إلى Mono عبر أخذ متوسط القناتين
            while (file.read(reinterpret_cast<char*>(&sample1), sizeof(sample1)) &&
                   file.read(reinterpret_cast<char*>(&sample2), sizeof(sample2))) {
                float monoSample = ((sample1 + sample2) / 2.0f) / 32768.0f;
                audioData.push_back(monoSample);
            }
        } else {
            // قراءة Mono مباشرة
            int16_t sample;
            while (file.read(reinterpret_cast<char*>(&sample), sizeof(sample))) {
                audioData.push_back(sample / 32768.0f);
            }
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
