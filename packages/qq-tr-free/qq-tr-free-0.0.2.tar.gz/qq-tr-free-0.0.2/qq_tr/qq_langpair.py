'''
qq fanyi code

https://cloud.tencent.com/document/api/551/15619
'''
import logging
import pytest
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())
QQTR_CODES = ['zh', 'en', 'jp', 'kr', 'de', 'fr', 'es', 'it', 'tr', 'ru', 'pt', 'vi', 'id', 'ms', 'th', 'auto']  # NOQA # pylint: disable=C0301


def qq_langpair(srclang, tgtlang):
    '''
    convert srclang, tgtlang to a pair suitable for qq fanyi
    '''
    # LOGGER.debug(" inp: %s, %s", srclang, tgtlang)

    try:
        srclang = srclang.lower().strip()
    except Exception as exc:
        LOGGER.warning(exc)
        srclang = ''

    # LOGGER.debug(" inp: %s, %s", srclang, tgtlang)

    try:
        tgtlang = tgtlang.lower().strip()
    except Exception as exc:
        LOGGER.warning(exc)
        tgtlang = ''

    if srclang == '':
        srclang = 'auto'
    if tgtlang == '':
        tgtlang = 'auto'

    # LOGGER.debug(" inp0: %s, %s", srclang, tgtlang)

    if srclang == 'auto' and tgtlang == 'auto':
        tgtlang = 'zh'

    # LOGGER.debug(" inp1: %s, %s", srclang, tgtlang)

    if srclang != 'auto' and tgtlang == 'auto':
        tgtlang = 'zh'

    if srclang in ['cn', 'chinese', 'zhong', 'zhongwen']:
        srclang = 'zh'
    if tgtlang in ['cn', 'chinese', 'zhong', 'zhongwen']:
        tgtlang = 'zh'

    if srclang[:3] in ['ger', 'deu', ]:
        srclang = 'de'
    if tgtlang in  ['ger', 'deu', ]:
        tgtlang = 'de'
    # LOGGER.debug('out: %s, %s', srclang, tgtlang)

    if srclang not in QQTR_CODES:
        src_score = process.extractOne(srclang, QQTR_CODES, scorer=fuzz.UWRatio)
        srclang0 = srclang
        srclang = src_score[0]

        # LOGGER.warning(" %s not recognized, guessing to be %s ", srclang0, srclang)

    if tgtlang not in QQTR_CODES:
        tgt_score = process.extractOne(tgtlang, QQTR_CODES, scorer=fuzz.UWRatio)
        tgtlang0 = tgtlang
        tgtlang = tgt_score[0]
        # LOGGER.warning(" %s not recognized, guessing to be %s ", tgtlang0, tgtlang)

    return srclang, tgtlang


@pytest.mark.parametrize(
    "inpair, outpair", [
        (('auto', 'auto'), ('auto', 'zh')),
        (('en', 'auto'), ('en', 'zh')),
        (('', ''), ('auto', 'zh')),
        (('en', ''), ('en', 'zh')),
        ((1, ''), ('auto', 'zh')),  # srclang strip() exception ==> '' >> 'auto'
        (('', 1), ('auto', 'zh')),  # tgtlan strip() exception ==> '' >> 'auto'
        (('en', 'cn'), ('en', 'zh')),
        (('EN', 'cn'), ('en', 'zh')),
        (('EN', 'Cn'), ('en', 'zh')),
        (('chinese', 'en'), ('zh', 'en')),
        (('chinese', 'En'), ('zh', 'en')),
        # process.extractOne("enn", QQTR_CODES, scorer=fuzz.UWRatio)
        (('chinese', 'enn'), ('zh', 'en')),
        (('enn', 'chinese'), ('en', 'zh')),
        (('enn', 'zh CHT'), ('en', 'zh')),
        (('enn', 'ger'), ('en', 'de')),
        (('german', 'en'), ('de', 'en')),
    ]
)
def test_pairs(inpair, outpair, caplog):
    '''test_pairs'''
    caplog.set_level(logging.DEBUG)
    assert qq_langpair(*inpair) == outpair
