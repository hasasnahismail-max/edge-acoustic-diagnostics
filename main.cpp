#include <iostream>
#include <vector>
#include <fstream>
#include <cstdint>
#include <cmath>
#include <complex>
#include <algorithm>
#include <iomanip>

using namespace std;

// 1. هيكل ترويسة ملف الصوت WAV القياسي
struct WAVHeader {
    char riff[4];          // "RIFF"
    uint32_t fileSize;     // حجم الملف الإجمالي
    char wave[4];          // "WAVE"
    char fmt[4];           // "fmt "
    uint32_t fmtSize;      // حجم الـ fmt chunk
    uint16_t audioFormat;  // نوع الترميز (1 = PCM)
    uint16_t numChannels;  // عدد القنوات (1 = أحادي, 2 = ستيريو)
    uint32_t sampleRate;   // معدل العينات (مثلاً 22050 أو 44100 هيرتز)
    uint32_t byteRate;     // عدد البايتس في الثانية
    uint16_t blockAlign;   // محاذاة البلوك
    uint16_t bitsPerSample;// عدد البتات لكل عينة (مثلاً 16-bit)
};

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

// 3. خوارزمية التحويل الفوري للترددات (Cooley-Tukey FFT)
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

// 4. دالة قراءة وتطبيع عينات الصوت الخام من ملف WAV
vector<double> loadAndNormalizeWAV(const string& filename, int& sampleRate) {
    ifstream file(filename, ios::binary);
    if (!file.is_open()) {
        return {};
    }

    WAVHeader header;
    file.read(reinterpret_cast<char*>(&header), sizeof(WAVHeader));
    sampleRate = header.sampleRate;

    char chunkId[4];
    uint32_t chunkSize = 0;
    while (file.read(chunkId, 4)) {
        file.read(reinterpret_cast<char*>(&chunkSize), 4);
        if (string(chunkId, 4) == "data") {
            break;
        }
        file.seekg(chunkSize, ios::cur);
    }

    vector<int16_t> pcmData(chunkSize / sizeof(int16_t));
    file.read(reinterpret_cast<char*>(pcmData.data()), chunkSize);
    file.close();

    vector<double> normalizedAudio;
    normalizedAudio.reserve(pcmData.size());
    for (int16_t sample : pcmData) {
        normalizedAudio.push_back(static_cast<double>(sample) / 32768.0);
    }

    return normalizedAudio;
}

// 5. محرك التحليل الطيفي والتشخيص الميكانيكي
DiagnosticReport analyzeAcousticSpectrum(const vector<double>& audioData, int sampleRate) {
    DiagnosticReport report;
    if (audioData.empty()) return report;

    double sumSquares = 0.0;
    for (double val : audioData) {
        sumSquares += val * val;
    }
    report.rmsEnergy = sqrt(sumSquares / audioData.size());

    size_t n = 1;
    while (n < audioData.size() && n < 4096) n *= 2;

    vector<complex<double>> fftInput(n, 0.0);
    for (size_t i = 0; i < min(audioData.size(), n); ++i) {
        fftInput[i] = audioData[i];
    }

    computeFFT(fftInput);

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

    // قواعد تقييم الأعطال الميكانيكية
    if (report.peakFreq >= 20.0 && report.peakFreq <= 480.0) {
        report.faults.push_back("Crankshaft Main Bearings Wear (تآكل سبايك الكرانك الرئيسية)");
        report.healthScore = 38;
        report.statusText = "CRITICAL DEVIATION DETECTED";
        report.recommendation = "Immediate shutdown advised. Inspect oil pan for metallic debris.";
    } else if (report.peakFreq >= 1200.0 && report.peakFreq <= 6000.0) {
        report.faults.push_back("Variable Geometry Turbocharger Imbalance (خلل في اتزان عمود التيربو)");
        report.healthScore = 24;
        report.statusText = "CRITICAL DEVIATION DETECTED";
        report.recommendation = "Check turbocharger radial play and lubrication lines.";
    } else {
        report.faults.push_back("Optimal Acoustic Performance (أداء سليم ضمن الحدود الهندسية)");
        report.healthScore = 94;
        report.statusText = "OPTIMAL PERFORMANCE";
        report.recommendation = "Acoustic signature matches nominal specifications. No action required.";
    }

    return report;
}

// 6. البرنامج الرئيسي (Main Execution Core)
int main(int argc, char* argv[]) {
    cout << "==================================================" << endl;
    cout << "  ZINO EDGE-ACOUSTIC DIAGNOSTIC ENGINE (C++ CORE) " << endl;
    cout << "==================================================" << endl;

    string filename = "engine_sample.wav";
    if (argc > 1) {
        filename = argv[1];
    }

    int sampleRate = 0;
    vector<double> audioData = loadAndNormalizeWAV(filename, sampleRate);

    // إذا لم يتم العثور على ملف WAV، يتم توليد إشارة اختبارية افتراضية للمحاكاة
    if (audioData.empty()) {
        cout << "[EADE Notice] Audio file not found. Generating synthetic signal..." << endl;
        sampleRate = 22050;
        audioData.resize(4096);
        for (size_t i = 0; i < audioData.size(); ++i) {
            audioData[i] = 0.5 * sin(2.0 * M_PI * 220.0 * i / sampleRate) + 0.02 * ((double)rand() / RAND_MAX - 0.5);
        }
    } else {
        cout << "[EADE Success] Loaded real WAV file successfully (" << audioData.size() << " samples)." << endl;
    }

    // تشغيل المحرك وتحليل الإشارة
    DiagnosticReport report = analyzeAcousticSpectrum(audioData, sampleRate);

    // طباعة التقرير الهندسي النهائي
    cout << fixed << setprecision(2);
    cout << "\n================ [INSPECTION REPORT] ================" << endl;
    cout << " System Status     : " << report.statusText << endl;
    cout << " Health Index      : " << report.healthScore << "%" << endl;
    cout << " Dominant Peak Freq: " << report.peakFreq << " Hz" << endl;
    cout << " Spectral Centroid : " << report.spectralCentroid << " Hz" << endl;
    cout << " Signal RMS Energy : " << report.rmsEnergy << endl;
    cout << "--------------------------------------------------" << endl;
    cout << " DETECTED FAULTS:" << endl;
    for (const auto& fault : report.faults) {
        cout << "  * " << fault << endl;
    }
    cout << "--------------------------------------------------" << endl;
    cout << " RECOMMENDATION    : " << report.recommendation << endl;
    cout << "==================================================" << endl;

    return 0;
}
