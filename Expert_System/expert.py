# Расширенная экспертная система (40 правил) диагностики респираторных и смежных заболеваний

RULES = [
    # ----- Основные диагнозы (прямые правила) -----
    # 1. Грипп
    (('temperature', True), ('muscle_ache', True), ('headache', True),
     ('diagnosis', 'Грипп'), 10),
    # 2. COVID-19 (потеря обоняния + температура или кашель)
    (('loss_of_smell', True), ('_temp_or_cough', True),
     ('diagnosis', 'COVID-19 (высокая вероятность)'), 10),
    # 3. Ангина
    (('temperature', True), ('sore_throat', True), ('cough', False),
     ('diagnosis', 'Ангина'), 9),
    # 4. Острый бронхит
    (('cough', True), ('wet_cough', True), ('_temp_or_fatigue', True),
     ('diagnosis', 'Острый бронхит'), 8),
    # 5. Аллергический ринит
    (('runny_nose', True), ('sneezing', True), ('temperature', False),
     ('muscle_ache', False),
     ('diagnosis', 'Аллергический ринит'), 7),
    # 6. ОРВИ (простуда)
    (('_runny_or_sneeze', True), ('temperature', False), ('fatigue', False),
     ('diagnosis', 'ОРВИ (простуда)'), 6),
    # 7. Синусит
    (('headache', True), ('runny_nose', True), ('duration_long', True),
     ('diagnosis', 'Синусит (воспаление пазух)'), 8),
    # 8. Мигрень/переутомление
    (('headache', True), ('fatigue', True), ('_no_resp', True),
     ('diagnosis', 'Мигрень или переутомление'), 5),
    # 9. Здоров
    (('temperature', False), ('cough', False), ('sore_throat', False),
     ('runny_nose', False), ('headache', False), ('fatigue', False),
     ('diagnosis', 'Симптомов не выявлено, вероятно здоров'), 1),

    # ----- OR-хелперы (промежуточные факты) -----
    # 10. _temp_or_cough (два правила)
    (('temperature', True), ('_temp_or_cough', True), 10),
    (('cough', True), ('_temp_or_cough', True), 9),
    # 11. _temp_or_fatigue
    (('temperature', True), ('_temp_or_fatigue', True), 8),
    (('fatigue', True), ('_temp_or_fatigue', True), 7),
    # 12. _runny_or_sneeze
    (('runny_nose', True), ('_runny_or_sneeze', True), 6),
    (('sneezing', True), ('_runny_or_sneeze', True), 5),
    # 13. _no_resp (нет респираторных симптомов)
    (('cough', False), ('runny_nose', False), ('sneezing', False),
     ('sore_throat', False), ('_no_resp', True), 4),
    # 14. COVID-19 через контакт + любой респираторный симптом
    (('contact_with_case', True), ('_any_resp', True),
     ('diagnosis', 'COVID-19 (контакт + респираторные симптомы)'), 9),
    # 15. _any_resp (4 правила)
    (('cough', True), ('_any_resp', True), 7),
    (('shortness_of_breath', True), ('_any_resp', True), 7),
    (('runny_nose', True), ('_any_resp', True), 6),
    (('loss_of_smell', True), ('_any_resp', True), 6),
    # 16. COVID-19 через одышку и температуру
    (('shortness_of_breath', True), ('temperature', True),
     ('diagnosis', 'COVID-19 (одышка + температура)'), 9),
    # 17. Боль в груди + одышка → срочно
    (('chest_pain', True), ('shortness_of_breath', True),
     ('diagnosis', 'Требуется срочная консультация врача (пневмония/осложнения)'), 11),
    # 18. Пневмония (основной путь)
    (('cough', True), ('temperature', True), ('shortness_of_breath', True),
     ('wet_cough', True),
     ('diagnosis', 'Пневмония (вероятна, требуется срочное обследование)'), 10),
    # 19. Пневмония (вариант с болью в груди)
    (('cough', True), ('temperature', True), ('chest_pain', True),
     ('diagnosis', 'Пневмония (боль в груди, требуется срочное обследование)'), 10),
    # 20. Туберкулёз (кровохарканье)
    (('prolonged_cough', True), ('blood_in_sputum', True),
     ('diagnosis', 'Туберкулёз (кровохарканье) — необходимо дообследование'), 10),
    # 21. Туберкулёз (общие симптомы)
    (('prolonged_cough', True), ('night_sweats', True), ('weight_loss', True),
     ('diagnosis', 'Туберкулёз (длительный кашель + ночная потливость + потеря веса)'), 9),
    # 22. Острый фарингит
    (('sore_throat', True), ('temperature', True), ('swollen_lymph_nodes', True),
     ('cough', False),
     ('diagnosis', 'Острый фарингит'), 8),
    # 23. Ларингит
    (('hoarseness', True), ('cough', True), ('temperature', False),
     ('diagnosis', 'Ларингит'), 7),
    # 24. Инфекционный мононуклеоз
    (('sore_throat', True), ('temperature', True), ('swollen_lymph_nodes', True),
     ('fatigue', True), ('duration_long', True),
     ('diagnosis', 'Инфекционный мононуклеоз (вероятен)'), 8),
    # 25. Коклюш
    (('prolonged_cough', True), ('whooping_sound', True),
     ('diagnosis', 'Коклюш (судорожный кашель со свистящим вдохом)'), 9),
    # 26. Бронхиальная астма
    (('cough', True), ('shortness_of_breath', True), ('wheezing', True),
     ('diagnosis', 'Бронхиальная астма (обострение)'), 9),
    # 27. ХОБЛ (обострение)
    (('prolonged_cough', True), ('smoker', True), ('shortness_of_breath', True),
     ('wet_cough', True),
     ('diagnosis', 'ХОБЛ (хроническая обструктивная болезнь лёгких, вероятно обострение)'), 8),
    # 28. ГЭРБ-ассоциированный кашель
    (('heartburn', True), ('cough', True), ('hoarseness', True),
     ('diagnosis', 'ГЭРБ-ассоциированный кашель (рефлюкс-ларингит)'), 7),
    # 29. Паническая атака
    (('stress_anxiety', True), ('dizziness', True), ('shortness_of_breath', True),
     ('chest_pain', True), ('temperature', False),
     ('diagnosis', 'Паническая атака (гипервентиляционный синдром)'), 8),
    # 30. Анемия
    (('fatigue', True), ('pale_skin', True), ('dizziness', True),
     ('temperature', False),
     ('diagnosis', 'Анемия (возможна, проверьте уровень гемоглобина)'), 6),
    # 31. Аллергический риноконъюнктивит
    (('itchy_eyes', True), ('runny_nose', True), ('sneezing', True),
     ('temperature', False),
     ('diagnosis', 'Аллергический риноконъюнктивит'), 7),
    # 32. Тонзиллит
    (('sore_throat', True), ('temperature', True), ('difficulty_swallowing', True),
     ('swollen_lymph_nodes', True),
     ('diagnosis', 'Тонзиллит (возможен бактериальный)'), 8),
    # 33. Обезвоживание
    (('fatigue', True), ('dizziness', True), ('dry_mouth', True),
     ('diagnosis', 'Обезвоживание (рекомендуется увеличить приём жидкости)'), 6),
    # 34. COVID-19 (лёгкое течение)
    (('loss_of_smell', True), ('headache', True), ('fatigue', True),
     ('diagnosis', 'COVID-19 (лёгкое течение)'), 9),
    # 35. Плеврит
    (('chest_pain', True), ('pain_on_breathing', True), ('cough', True),
     ('diagnosis', 'Плеврит (воспаление плевры)'), 9),
    # 36. Хронический бронхит курильщика
    (('smoker', True), ('cough', True), ('wet_cough', True),
     ('temperature', False),
     ('diagnosis', 'Хронический бронхит курильщика'), 5),
    # 37. Постназальный затёк
    (('postnasal_drip', True), ('cough', True),
     ('diagnosis', 'Постназальный затёк (синдром постназального затекания)'), 7),
    # 38. _any_chest_symptom (два OR-правила для будущего использования)
    (('chest_pain', True), ('_any_chest_symptom', True), 8),
    (('shortness_of_breath', True), ('_any_chest_symptom', True), 8),
    # 39. _any_systemic_symptom (два OR-правила)
    (('night_sweats', True), ('_any_systemic', True), 7),
    (('weight_loss', True), ('_any_systemic', True), 7),
    # 40. Неспецифическая инфекция (если есть температура и кашель, но ничего более специфичного)
    (('temperature', True), ('cough', True), ('_no_specific', True),
     ('diagnosis', 'Острая респираторная инфекция (неуточнённая)'), 4),
    # Вспомогательное правило для _no_specific (нет симптомов, характерных для других болезней)
    (('loss_of_smell', False), ('blood_in_sputum', False), ('whooping_sound', False),
     ('wheezing', False), ('hoarseness', False), ('swollen_lymph_nodes', False),
     ('pale_skin', False), ('dizziness', False), ('_no_specific', True), 2),
]


class ExpertSystem:
    def __init__(self):
        self.facts = {}
        self.rules = []
        self.asked = set()
        self.explanations = []

    def add_rule(self, *args):
        priority = args[-1]
        conclusion = args[-2]
        conditions = args[:-2]
        self.rules.append({
            'if': [(c[0], c[1]) for c in conditions],
            'then': conclusion,
            'priority': priority
        })

    def askable(self, fact):
        return fact in {
            'temperature', 'cough', 'wet_cough', 'sore_throat', 'muscle_ache',
            'headache', 'runny_nose', 'sneezing', 'fatigue', 'loss_of_smell',
            'shortness_of_breath', 'chest_pain', 'contact_with_case', 'duration_long',
            'prolonged_cough', 'night_sweats', 'weight_loss', 'blood_in_sputum',
            'swollen_lymph_nodes', 'hoarseness', 'difficulty_swallowing', 'ear_pain',
            'itchy_eyes', 'smoker', 'heartburn', 'stress_anxiety', 'dizziness',
            'pale_skin', 'dry_mouth', 'pain_on_breathing', 'whooping_sound',
            'wheezing', 'postnasal_drip'
        }

    def ask_user(self, fact):
        if fact in self.asked:
            return self.facts.get(fact)
        questions = {
            'temperature': 'Температура выше 38°C?',
            'cough': 'Есть кашель?',
            'wet_cough': 'Кашель влажный (с мокротой)?',
            'sore_throat': 'Болит горло?',
            'muscle_ache': 'Ломота в мышцах?',
            'headache': 'Головная боль?',
            'runny_nose': 'Насморк?',
            'sneezing': 'Частое чихание?',
            'fatigue': 'Сильная усталость, слабость?',
            'loss_of_smell': 'Потеря обоняния или вкуса?',
            'shortness_of_breath': 'Одышка или затруднённое дыхание?',
            'chest_pain': 'Боль или давление в груди?',
            'contact_with_case': 'Был контакт с подтверждённым больным COVID-19?',
            'duration_long': 'Симптомы длятся больше 7 дней?',
            'prolonged_cough': 'Кашель длится более 3 недель?',
            'night_sweats': 'Беспокоит ночная потливость?',
            'weight_loss': 'Наблюдается непреднамеренная потеря веса?',
            'blood_in_sputum': 'Есть кровь в мокроте?',
            'swollen_lymph_nodes': 'Увеличены лимфоузлы на шее?',
            'hoarseness': 'Осиплость голоса или хрипота?',
            'difficulty_swallowing': 'Затруднено глотание?',
            'ear_pain': 'Боль в ухе?',
            'itchy_eyes': 'Зуд в глазах?',
            'smoker': 'Вы курите (стаж более 10 пачка-лет)?',
            'heartburn': 'Беспокоит изжога или кислый привкус во рту?',
            'stress_anxiety': 'Испытываете сильный стресс или тревогу?',
            'dizziness': 'Кружится голова?',
            'pale_skin': 'Кожа выглядит бледнее обычного?',
            'dry_mouth': 'Ощущается сухость во рту?',
            'pain_on_breathing': 'Боль в груди усиливается при глубоком вдохе?',
            'whooping_sound': 'При кашле слышен свистящий вдох (как "петушиный крик")?',
            'wheezing': 'Слышны свистящие хрипы в груди (свистящее дыхание)?',
            'postnasal_drip': 'Есть ощущение стекания слизи по задней стенке горла?',
        }
        while True:
            ans = input(questions[fact] + ' (y/n): ').strip().lower()
            if ans in ('y', 'yes', 'да'):
                val = True
                break
            elif ans in ('n', 'no', 'нет'):
                val = False
                break
            print('Ответьте y или n')
        self.facts[fact] = val
        self.asked.add(fact)
        return val

    def evaluate_condition(self, fact, expected_value):
        val = self.facts.get(fact)
        if val is None:
            if self.askable(fact):
                val = self.ask_user(fact)
            else:
                return False
        return val == expected_value

    def rule_applicable(self, rule):
        for fact, expected in rule['if']:
            if not self.evaluate_condition(fact, expected):
                return False
        return True

    def find_applicable_rule(self):
        applicable = [r for r in self.rules if self.rule_applicable(r)]
        if not applicable:
            return None
        return max(applicable, key=lambda r: r['priority'])

    def infer(self):
        while True:
            rule = self.find_applicable_rule()
            if not rule:
                break
            fact, value = rule['then']
            if self.facts.get(fact) == value:
                break
            self.facts[fact] = value
            self.explanations.append(
                f"Применено правило (приоритет {rule['priority']}): "
                f"ЕСЛИ {rule['if']} ТО {fact} = {value}"
            )
            if fact == 'diagnosis':
                return value

        if 'diagnosis' in self.facts:
            return self.facts['diagnosis']
        for rule in sorted(self.rules, key=lambda r: r['priority']):
            if rule['then'][0] == 'diagnosis' and self.rule_applicable(rule):
                self.facts['diagnosis'] = rule['then'][1]
                self.explanations.append(f"Запасное правило: ЕСЛИ {rule['if']} ТО {rule['then']}")
                return rule['then'][1]
        return 'Не удалось определить состояние по заданным правилам.'

    def explain(self):
        if self.explanations:
            print('\n--- Ход рассуждений ---')
            for step in self.explanations:
                print(step)
        else:
            print('\nПравила не применялись.')


if __name__ == '__main__':
    while True:
        es = ExpertSystem()
        for rule in RULES:
            es.add_rule(*rule)

        print("Экспертная система диагностики заболеваний (40 правил)")
        print("=" * 60)
        print("Отвечайте y (да) или n (нет) на вопросы о симптомах.\n")
        diagnosis = es.infer()
        print(f"\n>>> Результат: {diagnosis}")
        es.explain()

        again = input("\nПройти ещё раз? (y/n): ").strip().lower()
        if again not in ('y', 'yes', 'да'):
            break

    input("\nНажмите Enter для выхода...")