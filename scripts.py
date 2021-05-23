import random
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson

COMMENDATIONS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!"
]

def get_schoolkid(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        return schoolkid
    except ObjectDoesNotExist:
        raise ValueError(f'Ученик с именем {schoolkid_name} не найден! Уточните имя и попробуйте снова.')
    except MultipleObjectsReturned:
        raise ValueError(f'Найдено больше одного ученика с именем {schoolkid_name}. Уточните имя и попробуйте снова.')

def fix_bad_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    return Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)

def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    return Chastisement.objects.filter(schoolkid=schoolkid).delete()

def create_commendation(schoolkid_name, subject_name):
    schoolkid = get_schoolkid(schoolkid_name)
    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__contains=subject_name,
    ).order_by('-date').first()

    if not last_lesson:
        return print(f'Уроков по предмету {subject_name} не найдено! Попробуйте указать другой предмет.')


    commendation_text = random.choice(COMMENDATIONS)
    Commendation.objects.create(
        text=commendation_text,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher,
        created=last_lesson.date,
    )