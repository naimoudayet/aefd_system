import re  # استيراد مكتبة التعبيرات النمطية للبحث داخل النصوص
import arabic_reshaper  # مكتبة لإعادة تشكيل النصوص العربية لتظهر بشكل صحيح
from bidi.algorithm import get_display  # مكتبة لترتيب النصوص ثنائية الاتجاه لتظهر من اليمين لليسار

# تعريف دالة لتطبيع الأفعال العربية وجعلها تتبع نمط "فَعَلَ"
def normalize_arabic_verb(verb):
    """
    Normalize an Arabic verb to conform to the format 'فَعَلَ'.
    Adds missing diacritics if needed.
    """
    # تعريف حركة الفتحة باستخدام Unicode ( َ )
    fatha = "\u064E"  # َ

    # إزالة المسافات الإضافية من الفعل وضمان احتوائه على ثلاثة أحرف جذرية
    verb = verb.strip()  # حذف المسافات الزائدة في بداية ونهاية النص
    root_letters = re.findall(r"[\u0621-\u064A]", verb)  # استخراج الأحرف العربية فقط باستخدام التعبيرات النمطية

    # التحقق من أن الفعل يحتوي على ثلاثة أحرف جذرية بالضبط
    if len(root_letters) != 3:
        raise ValueError(f"The verb '{verb}' does not have exactly 3 root letters.")  # رمي خطأ إذا كان الشرط غير محقق

    # إضافة الفتحة بعد كل حرف لتطبيع الفعل إلى صيغة "فَعَلَ"
    normalized_verb = f"{root_letters[0]}{fatha}{root_letters[1]}{fatha}{root_letters[2]}{fatha}"
    return normalized_verb  # إرجاع الفعل بعد تطبيعه


# تعريف دالة للتحقق من موقع الهمزة (أَ) في الفعل
def check_hamza_position(verb):
    """
    Check if the Hamza (أَ) is in the first, middle, or last position of the root.
    Returns a corresponding rule.
    """
    # تطبيع الفعل أولًا باستخدام الدالة السابقة
    normalized_verb = normalize_arabic_verb(verb)

    # استخراج أحرف الجذر الثلاثة بعد التطبيع
    root_letters = re.findall(r"[\u0621-\u064A]", normalized_verb)  # استخراج الأحرف فقط

    # تعريف الهمزة المحددة مع الفتحة "أَ"
    specific_hamza = "أ"

    # التحقق من موقع الهمزة بين أحرف الجذر
    if root_letters[0] == specific_hamza:
        return "مهموز الفاء"  # الهمزة في أول الجذر (الفاء)
    elif root_letters[1] == specific_hamza:
        return "مهموز العين"  # الهمزة في منتصف الجذر (العين)
    elif root_letters[2] == specific_hamza:
        return "مهموز اللام"  # الهمزة في آخر الجذر (اللام)
    else:
        return "لا تحتوي الكلمة على همزة من نوع أَ"  # لا يوجد همزة في الجذر


# استخدام مثال على الدالتين للتحقق من الأفعال
verbs = ['أَمَرَ', 'أَخَذَ', 'أَكَلَ', 'أَسَرَ', 'سَأَلَ', 'دَأَبَ', 'رَأَى', 'قَرَأَ', 'نَشَأَ', 'بَدَأَ', 'دَرَأَ']

# حلقة تمر على كل فعل في قائمة الأفعال
for verb in verbs:
    try:
        # استدعاء الدالة للتحقق من موقع الهمزة
        result = check_hamza_position(verb)
        
        # إعادة تشكيل النص ليظهر بشكل صحيح من اليمين إلى اليسار
        reshaped_verb = arabic_reshaper.reshape(verb)
        reshaped_result = arabic_reshaper.reshape(result)
        
        # طباعة الفعل والنتيجة مع عرض النص بشكل صحيح باستخدام get_display
        print(f"Verb: {get_display(reshaped_verb)} - Result: {get_display(reshaped_result)}")
    except ValueError as e:
        print(e)  # طباعة رسالة الخطأ إذا لم يحتوي الفعل على 3 أحرف جذرية
