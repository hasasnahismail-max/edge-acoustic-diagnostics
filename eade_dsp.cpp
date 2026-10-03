#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>

class EADEDSP {
public:
    // تطبيق Hann Window لتنعيم الإشارة الصوتية وتقليل التسريب الطيفي
    static void applyHannWindow(std::vector<float>& signal) {
        size_t N = signal.size();
        if (N == 0) return;
        
        for (size_t i = 0; i < N; ++i) {
            float multiplier = 0.5f * (1.0f - std::cos(2.0f * M_PI * i / (N - 1)));
            signal[i] *= multiplier;
        }
    }

    // حساب طاقة الإشارة الجذرية RMS
    static float calculateRMS(const std::vector<float>& signal) {
        if (signal.empty()) return 0.0f;
        float sumSquare = 0.0f;
        for (float sample : signal) {
            sumSquare += sample * sample;
        }
        return std::sqrt(sumSquare / signal.size());
    }
};
