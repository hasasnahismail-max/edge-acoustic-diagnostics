#include <iostream>
#include <vector>
#include <fstream>
#include <cstdint>
#include <cmath>

using namespace std;

// هيكل ترويسة ملف الصوت WAV القياسي
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

// دالة قراءة وتطبيع عينات الصوت الخام من ملف WAV بجودة عالية
vector<double> loadAndNormalizeWAV(const string& filename, int& sampleRate) {
    ifstream file(filename, ios::binary);
    if (!file.is_open()) {
        cerr << "[EADE Error] Could not open audio file: " << filename << endl;
        return {};
    }

    WAVHeader header;
    file.read(reinterpret_cast<char*>(&header), sizeof(WAVHeader));
    sampleRate = header.sampleRate;

    // البحث عن مقطع البيانات "data" داخل الملف
    char chunkId[4];
    uint32_t chunkSize = 0;
    while (file.read(chunkId, 4)) {
        file.read(reinterpret_cast<char*>(&chunkSize), 4);
        if (string(chunkId, 4) == "data") {
            break;
        }
        file.seekg(chunkSize, ios::cur);
    }

    // قراءة البيانات وتحويلها إلى نطاق عشري [-1.0, 1.0]
    vector<int16_t> pcmData(chunkSize / sizeof(int16_t));
    file.read(reinterpret_cast<char*>(pcmData.data()), chunkSize);
    file.close();

    vector<double> normalizedAudio;
    normalizedAudio.reserve(pcmData.size());
    for (int16_t sample : pcmData) {
        normalizedAudio.push_back(static_cast<double>(sample) / 32768.0);
    }

    cout << "[EADE Success] Loaded " << normalizedAudio.size() << " samples at " << sampleRate << " Hz." << endl;
    return normalizedAudio;
}
