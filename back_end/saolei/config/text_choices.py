from django.db.models import TextChoices


class MS_TextChoices:
    class Mode(TextChoices):
        STD = '00', ('标准')
        UPK = '01', ('upk')
        WQ = '04', ('win7')
        JSW = '05', ('竞速无猜')
        QWC = '06', ('强无猜')
        RWC = '07', ('弱无猜')
        ZWC = '08', ('准无猜')
        QKC = '09', ('强可猜')
        RKC = '10', ('弱可猜')
        BZD = '11', ('标准递归')

    class Level(TextChoices):
        BEGINNER = 'b', ('初级')
        INTERMEDIATE = 'i', ('中级')
        EXPERT = 'e', ('高级')
        CUSTOM_8_8_40 = 'c8_8_40', ('8x8 40雷')
        CUSTOM_16_16_100 = 'c16_16_100', ('16x16 100雷')
        CUSTOM_16_30_150 = 'c16_30_150', ('16x30 150雷')
        CUSTOM_24_30_200 = 'c24_30_200', ('24x30 200雷')

    class State(TextChoices):
        PLAIN = 'a', ('已上传但未审核')
        FROZEN = 'b', ('审核未通过，被冻结')
        OFFICIAL = 'c', ('已通过审核')
        IDENTIFIER = 'd', ('标识不匹配')
        EXTERNAL = 'e', ('外部网站审核')

    class Software(TextChoices):
        AVF = 'a', ('avf')
        EVF = 'e', ('evf')
        MVF = 'm', ('mvf')
        RMV = 'r', ('rmv')


class Saolei_TextChoices:
    class SaoleiVideoState(TextChoices):
        NOTEXIST = 'n', ('不存在')
        PENDING = 'p', ('未审核')
        FROZEN = 'f', ('已冻结')
        OFFICIAL = 'o', ('正常')

    class SaoleiVideoImportState(TextChoices):
        NOTPLANNED = 'n', ('未计划')
        READY = 'r', ('准备就绪')
        QUEUEING = 'q', ('排队中')
        IMPORTING = 'i', ('导入中')
        IMPORTED = 'd', ('已导入')
        FAILED = 'f', ('导入失败')


class Medal_TextChoices:
    class Series(TextChoices):
        BREAKTHROUGH = 'breakthrough', ('破境')
        SPEED = 'speed', ('神速')
        MASTERY = 'mastery', ('通明')
        FLAGLESS_BREAKTHROUGH = 'flagless_breakthrough', ('盲扫破境')
        FLAGLESS_SPEED = 'flagless_speed', ('盲扫神速')
        FLAGLESS_MASTERY = 'flagless_mastery', ('盲扫通明')
        FLAGLESS_PRECISION = 'flagless_precision', ('盲扫·精工')
        FLAGGED_PRECISION = 'flagged_precision', ('标旗·精工')
        THREE_FLAGLESS_PRECISION = 'three_flagless_precision', ('三阶盲扫·精工')
        THREE_FLAGGED_PRECISION = 'three_flagged_precision', ('三阶标旗·精工')
        REGISTERED = 'registered', ('实名在册')
        REVIEWED = 'reviewed', ('录像过审')
        LEVELS = 'levels', ('扫雷新秀')
        LEVELS_NF = 'levels_nf', ('盲扫新秀')
        MODES = 'modes', ('走马观花')
        SAOLEI = 'saolei', ('旧迹新篇')
        SHAREHOLDER = 'shareholder', ('原始股东')

    class Kind(TextChoices):
        PB = 'pb', ('pb')
        COMPOSITE = 'composite', ('composite')
        ONCE = 'once', ('once')
        COUNT = 'count', ('count')
        BV_SET = 'bv_set', ('bv_set')
        CELL_MASK = 'cell_mask', ('cell_mask')
        EVENT_PLACE = 'event_place', ('event_place')
        GSC_STAT = 'gsc_stat', ('gsc_stat')
        GSC_PLACE = 'gsc_place', ('gsc_place')
        MANUAL = 'manual', ('manual')
        MIN_VIDEO_ID = 'min_video_id', ('min_video_id')

    class Direction(TextChoices):
        ASC = 'asc', ('asc')
        DESC = 'desc', ('desc')

    class Level(TextChoices):
        BEGINNER = 'b', ('b')
        INTERMEDIATE = 'i', ('i')
        EXPERT = 'e', ('e')

    class Style(TextChoices):
        ANY = 'any', ('any')
        NF = 'nf', ('nf')
        FL = 'fl', ('fl')


class Tournament_TextChoices:
    class Subclass(TextChoices):
        GSC = 'g', ('GSC比赛')
        WEEKLY = 'w', ('周赛')

    class State(TextChoices):
        PENDING = 'p', ('审核中')
        NORMAL = 'n', ('正常')
        CANCELLED = 'c', ('已取消')
        AWARDED = 'a', ('已颁奖')

    class WeeklyFormat(TextChoices):
        CLASSIC = 'c', ('2高5中')
