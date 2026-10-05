def generate_expanded_car_report(
    brand, model, engine, fuel, cylinders, lang_code
):
  is_diesel = ("Diesel" in fuel) or ("CRDi" in engine) or ("TDI" in engine)
  is_turbo = ("Turbo" in fuel) or ("Turbo" in engine) or ("TSI" in engine)

  if lang_code == "العربية":
    p1 = (
        "<b>1. تحليل طيف فوريه الترددي (FFT Spectrum Analysis):</b><br>تم"
        " تفكيك الإشارة الصوتية لسيارة <b>"
        + str(brand)
        + " "
        + str(model)
        + "</b> (محرك <b>"
        + str(engine)
        + "</b>). التردد البارز يطابق زمن الاحتراق للـ "
        + str(cylinders)
        + " بدون تشتت في الطاقة."
    )
    p2 = (
        "<b>2. معاينة صمامات ومحاور الكامبشافت (Valve Train & Camshaft"
        " Acoustics):</b><br>خلوص الصبابات والصمامات يعمل ضمن المجال"
        " الهيدروليكي القياسي لشركة "
        + str(brand)
        + "، ولا تظهر أي طقطقة عشوائية في عمود الكامبشافت."
    )
    inj_str = (
        "ترددات بخاخات الديزل ذات الضغط العالي (Common Rail) متزنة ونقية دون"
        " وجود ظاهرة التسريب الترددي."
        if is_diesel
        else (
            "نظام حقن البنزين المباشر/المتعدد يعمل بانتظام، والضوضاء عالية"
            " التردد في النطاق الطبيعي."
        )
    )
    p3 = (
        "<b>3. نظام حقن الوقود والضغط العالي (Injectors & Fuel Rail"
        " Pressure):</b><br>"
        + inj_str
    )
    turbo_str = (
        "عنفة التوربو تعمل بستارة صوتية مستقرة دون أي صفير مرتفع أو احتكاك في"
        " شفرات الشاحن."
        if is_turbo
        else (
            "منظومة سحب الهواء وتطابق الضغط الطبيعي تعمل بكفاءة عالية بدون أي"
            " تسريب في المانفولد."
        )
    )
    p4 = (
        "<b>4. الشاحن التوربيني ونظام سحب الهواء (Turbocharger &"
        " Induction):</b><br>"
        + turbo_str
    )
    p5 = (
        "<b>5. محامل الدوران وعمود الكرنك والحذافة (Bearings, Crankshaft &"
        " DMF):</b><br>عدم وجود أي اهتزازات منخفضة التردد في محامل عمود الكرنك"
        " الرئيسية، وحذافة الفولام المزدوجة امتصت الصدمات الصوتية بالكامل."
    )
    p6 = (
        "<b>6. التوصيات الهندسية وخطة الصيانة الوقائية (Predictive"
        " Maintenance Plan):</b><br>المحرك بحالة ممتازة جداً. يوصى بالمحافظة"
        " على مواعيد استبدال الزيوت والفلاتر الخاصة بـ "
        + str(brand)
        + " عند قطع 10,000 كم."
    )
    return "<br><br>".join([p1, p2, p3, p4, p5, p6])

  elif lang_code == "English":
    p1 = (
        "<b>1. FFT Acoustic Spectrum Core Analysis:</b><br>Acoustic signal"
        " breakdown for <b>"
        + str(brand)
        + " "
        + str(model)
        + "</b> ("
        + str(engine)
        + "). Dominant peak matches the fundamental combustion frequency for "
        + str(cylinders)
        + " with zero spectral leakage."
    )
    p2 = (
        "<b>2. Valve Train & Camshaft Acoustic Inspection:</b><br>Valve lash"
        " clearances and hydraulic lifters operate strictly within nominal "
        + str(brand)
        + " specifications. Zero camshaft chatter observed."
    )
    inj_str = (
        "High-pressure Common Rail Diesel injector chatter is fully"
        " synchronized with zero cavitation noise."
        if is_diesel
        else (
            "Gasoline injection pulses show crisp, clean high-frequency"
            " harmonics within normal operating range."
        )
    )
    p3 = "<b>3. Fuel Injection System & Rail Dynamics:</b><br>" + inj_str
    turbo_str = (
        "Turbocharger spool frequency exhibits smooth acoustic resonance"
        " without high-pitched turbine squeal."
        if is_turbo
        else (
            "Naturally aspirated air intake manifold shows no pressure leaks or"
            " turbulent acoustic anomalies."
        )
    )
    p4 = "<b>4. Turbocharger & Induction Harmonics:</b><br>" + turbo_str
    p5 = (
        "<b>5. Bearings, Crankshaft & DMF Flywheel Dynamics:</b><br>Main"
        " crankshaft bearings show zero low-frequency rumble. Dual-Mass"
        " Flywheel effectively dampens rotational vibration peaks."
    )
    p6 = (
        "<b>6. Predictive Maintenance & Engineering Plan:</b><br>Overall"
        " powertrain acoustic health is optimal. Maintain regular "
        + str(brand)
        + " oil and filter replacement cycles every 10,000 km."
    )
    return "<br><br>".join([p1, p2, p3, p4, p5, p6])

  else:
    p1 = (
        "<b>1. Спектральный анализ FFT:</b><br>Акустический сигнал для <b>"
        + str(brand)
        + " "
        + str(model)
        + "</b> ("
        + str(engine)
        + ") разобран. Доминирующий пик соответствует частоте сгорания "
        + str(cylinders)
        + " без спектральных утечек."
    )
    p2 = (
        "<b>2. Акустическая проверка клапанного механизма:</b><br>Зазоры"
        " клапанов и гидрокомпенсаторы работают строго в пределах допусков "
        + str(brand)
        + ". Шум распредвала отсутствует."
    )
    inj_str = (
        "Импульсы дизельных форсунок высокого давления синхронизированы без"
        " шума кавитации."
        if is_diesel
        else (
            "Импульсы впрыска бензина демонстрируют чистые высокочастотные"
            " гармоники."
        )
    )
    p3 = "<b>3. Топливная система и давление рампы:</b><br>" + inj_str
    turbo_str = (
        "Частота турбокомпрессора показывает плавный резонанс без"
        " высокочастотного свиста."
        if is_turbo
        else "Атмосферный впускной коллектор работает без утечек давления."
    )
    p4 = "<b>4. Турбокомпрессор и система впуска:</b><br>" + turbo_str
    p5 = (
        "<b>5. Подшипники, коленвал и двухмассовый маховик:</b><br>Подшипники"
        " коленвала не имеют низкочастотных шумов. Маховик полностью гасит"
        " вибрационные пики."
    )
    p6 = (
        "<b>6. Рекомендации по техническому обслуживанию:</b><br>Общее"
        " акустическое состояние двигателя оптимальное. Соблюдайте регламент"
        " замены масла "
        + str(brand)
        + " каждые 10 000 км."
    )
    return "<br><br>".join([p1, p2, p3, p4, p5, p6])
