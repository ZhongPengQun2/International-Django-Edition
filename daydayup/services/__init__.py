# coding: utf-8
import requests
from models.user import User
from models.word import Word, UserLearnedWords, Collections, UserLearnedChineseWords


def user_has_learned_this_word(user_id=None, word_id=None):
    return UserLearnedWords.query.filter(UserLearnedWords.user_id==user_id, UserLearnedWords.word_id==word_id).exists()


def user_learned_words_paged(user_id=None, page_num=1, page_size=20):
    learned_word_with_ids = UserLearnedWords.query.filter(
        UserLearnedWords.user_id == user_id).with_entities(UserLearnedWords.word_id).all()
    learned_word_ids = [x[0] for x in learned_word_with_ids]

    f = Word.query.filter(Word.id.in_(learned_word_ids))
    total = f.count()

    return total, int(f.count() / float(page_size) + 1), f.limit(
        page_size).offset((page_num - 1) * page_size)


def user_learned_chinese_words_paged(user_id=None, page_num=1, page_size=20):
    learned_word_with_ids = UserLearnedChineseWords.query.filter(
        UserLearnedChineseWords.user_id == user_id).with_entities(UserLearnedChineseWords.cn_word_id).all()
    learned_word_ids = [x[0] for x in learned_word_with_ids]

    f = Word.query.filter(Word.id.in_(learned_word_ids))
    total = f.count()

    return total, int(f.count() / float(page_size) + 1), f.limit(
        page_size).offset((page_num - 1) * page_size)


def user_collected_words_paged(user_id=None, page_num=1, page_size=20):
    collected_word_with_ids = Collections.query.filter(
        Collections.user_id == user_id).with_entities(Collections.word_id).all()
    word_ids = [x[0] for x in collected_word_with_ids]

    f = Word.query.filter(Word.id.in_(word_ids))
    total = f.count()
    return total, int(f.count() / float(page_size) + 1), f.limit(
        page_size).offset((page_num - 1) * page_size)


def  add_a_word_to_db(spell=u'', pronunciation=u'', unit=u'', meaning=u'', speak=u'', short_meaning=u''):
    word = Word(spell=spell, pronunciation=pronunciation, unit=unit, meaning=meaning, speak=speak, short_meaning=short_meaning)
    word.save()
    return word


def get_a_word_detail(spell=u""):
    word = Word.query.filter(Word.spell == spell).one_or_none()
    if not word:
        word = Word.query.filter()[0]
    return word


def translate_english_to_chinese(english_word):
    meaning = None
    r = requests.get("https://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&q=%s" % english_word)
    result = r.json()
    if result.get('basic'):
        meaning = '\n'.join(result.get('basic').get('explains'))
    return meaning


def word_image(word_spell):
    import PIL
    from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont

    word = Word.query.filter(Word.spell == word_spell).one_or_none()
    if not word:
        return
    img_width = 800
    img_height = 512
    im = Image.new("RGB", (img_width, img_height), (24, 24, 24))
    
    draw = ImageDraw.Draw(im)  # 创建 Draw 对象
    # font = ImageFont.load_default()
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/BigCaslon.ttf', 40)
    
    # 填充文字
    draw.text((img_width/2, img_height/2), word.spell, font=font, fill="#BBBBBB")
    draw.text((img_width/2 - 60, img_height/2 - 60), word.meaning, font=font, fill="#BBBBBB")
    
    im.save('/root/international/daydayup/static/images/%s.png'%word.id)
