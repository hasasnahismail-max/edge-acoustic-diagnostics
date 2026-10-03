#include <iostream>
#include <vector>
#include <cmath>
#include <complex>
#include <algorithm>

using namespace std;

// 1. خوارزمية التحويل الفوري للترددات (Cooley-Tukey FFT)
void computeFFT(vector<complex<double>>& x) {
    const size_t N = x.size();
    if (N <= 1) return;

    vector<complex<double>> even(N / 2);
    vector<complex<double>> odd(N / 2);
    for (size_t i = 0; i < N / 2; ++i) {
        even[i] = x[2 * i];
        odd[i] = x[2 * i + 1];
    }

    computeFFT(even);
    computeFFT(odd);

    for (size_t k = 0; k < N / 2; ++k) {
        complex<double> t = polar(1.0, -2.0 * M_PI * k / N) * odd[k];
        x[k] = even[k] + t;
        x[k + N / 2] = even[k] - t;
    }
}

// 2. هيكل نتيجة التشخيص والتحليل الطيفي
struct DiagnosticReport {
    double peakFreq;          // التردد المهيمن (الأعلى سعة)
    double spectralCentroid;  // مركز الكتلة الطيفية
    double rmsEnergy;         // طاقة الإشارة الكلية
    int healthScore;          // مؤشر صحة المحرك (من 100)
    string statusText;        // حالة النظام الهندسية
    vector<string> faults;    // قائمة الأعطال المكتشفة
    string recommendation;    // التوصية الفنية
};

// 3. دالة التحليل الطيفي والتشخيص الميكانيكي
DiagnosticReport analyzeAcousticSpectrum(const vector<double>& audioData, int sampleRate) {
    DiagnosticReport report;
    if (audioData.empty()) return report;

    // حساب طاقة الإشارة (RMS Energy)
    double sumSquares = 0.0;
    for (double val : audioData) {
        sumSquares += val * val;
    }
    report.rmsEnergy = sqrt(sumSquares / audioData.size());

    // تجهيز بيانات الـ FFT (ضبط الحجم ليكون قوة للرقم 2)
    size_t n = 1;
    while (n < audioData.size() && n < 4096) n *= 2;

    vector<complex<double>> fftInput(n, 0.0);
    for (size_t i = 0; i < min(audioData.size(), n); ++i) {
        fftInput[i] = audioData[i];
    }

    // تنفيذ التحويل الطيفي
    computeFFT(fftInput);

    // استخراج التردد المهيمن والخصائص الطيفية
    double maxAmp = 0.0;
    double peakFreq = 0.0;
    double totalPower = 0.0;
    double weightedFreqSum = 0.0;

    for (size_t i = 0; i < n / 2; ++i) {
        double freq = static_cast<double>(i) * sampleRate / n;
        double amp = abs(fftInput[i]);
        totalPower += amp;
        weightedFreqSum += freq * amp;
        if (amp > maxAmp) {
            maxAmp = amp;
            peakFreq = freq;
        }
    }

    report.peakFreq = peakFreq;
    report.spectralCentroid = (totalPower > 0) ? (weightedFreqSum / totalPower) : 0.0;

    // قواعد تقييم الأعطال الميكانيكية دقيقة الصياغة
    if (report.peakFreq >= 20.0 && report.peakFreq <= 480.0) {
        report.faults.push_back("Critical: Crankshaft Main Bearings Wear (تآكل سبايك الكرانك الرئيسية)");
        report.healthScore = 38;
        report.statusText = "CRITICAL DEVIATION DETECTED";
        report.recommendation = "Immediate shutdown advised. Inspect oil pan for metallic debris.";
    } else if (report.peakFreq >= 1200.0 && report.peakFreq <= 6000.0) {
        report.faults.push_back("Critical: Variable Geometry Turbocharger Imbalance (خلل في اتزان عمود التيربو)");
        report.healthScore = 24;
        report.statusText = "CRITICAL DEVIATION DETECTED";
        report.recommendation = "Check turbocharger radial play and lubrication lines.";
    } else {
        report.faults.push_back("Optimal Acoustic Performance (أداء سليم ضمن الحدود الهندسية القياسية)");
        report.healthScore = 94;
        report.statusText = "OPTIMAL PERFORMANCE";
        report.recommendation = "Acoustic signature matches nominal specifications. No action required.";
    }

    return report;
}
