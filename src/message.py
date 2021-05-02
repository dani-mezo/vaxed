import logging

welcome = [
    "Kellemes napot Viktória hercegnő!",
    "Szia Borsó!",
    "Remélem nem fáj a pocikád.",
    "Szia!",
    "Sziaaa.",
    "Sziaaaa.",
    "Sziaaaaa.",
    "Ööö csá.",
    "Halóóó. ..  Zzzz. ..  Halóóó.",
    "Halóóó.",
    "Jó reggelt Kisborsó, örülök hogy felébredtél.",
    "Facebook üzenetek mentése... Ne kapcsold ki!",
    "Köszönöm hogy ma reggel kedves voltál!",
    "Szép napot!",
    "Szervusz.",
    "Heló.",
    "Hi.",
    "Szia cica.",
    "Mornin'",
    "Hey.",
    "Hogy vagyunk ezen a pompás reggelen?",
    "Szia szivecske.",
    "'Jajj itt a Cicuka.'",
    "Jó újra itt látni téged.",
    "Hé fordulj egy pillanatra balra ...  ez az, SZIA.",
    "Kk.",
    "Kk csá.",
    "szia.",
    "Sziasztok.",
    "Betöltött az alkalmazás, üdvözlégy!",
    "A királylány szolgálatában!",
    "Bonzsúr.",
    "Szépséges estét hölgyem!",
    "Kellemes délutánt kisasszony!",
    "Helló belló.",
    "'What.'",
    "Szia hercegnő.",
    "Jónapot kívánok!",
    "Jónapot kívánok cica kisasszony!",
    "Szép délutánt Borsócska!"
]

comment = [
    "Légyszíves ne felejts el reggelizni.",
    "Miújság?",
    "Mi volt veled ma?",
    "Kérsz enni valamit?",
    "Milyen sütikére vágysz?",
    "Eszünk valamikor fagyit?"
    "Iszol már kávékát?",
    "Ne felejts el ebédelni.",
    "Milyen sütit sütünk?",
    "Mikor lesz már karácsony?",
    "Mit kérsz a szülinapodra?",
    "E heti alkalmazás indításunk nyertese pedig: Viktória!",
    "Jól áll a hajad.",
    "Tetszik ez a nadrág.",
    "Nem fázol?",
    "Tessék menni aludni, szép álmokat Borsócska.",
    "Nincs meleged?",
    "Igyál egy pohár vizet",
    "Főzzek neked teát?",
    "Mikor fogunk összeházasodni?",
    "Kérek szépen egy puszit.",
    "Megyek főzök pesztóstésztát.",
    "Kellene megint menni az IKEA-ba.",
    "Nem vagy álmoska?",
    "Gyere aludni jó? Alvááás.",
    "Gyere ide gyöngyike. ... PURRR.",
    "Naaa, nézz már oda!",
    "Fantasztikus, tényleg.",
    "Ah, megint dolgoznod kell?",
    "Túl sok időt ne tölts itt!",
    "De aranyos vagy hogy megsimogatsz!",
    "Gyere aludni.",
    "Jössz aludni?",
    "Alvááás.",
    "Megsimogattad ma már a cicát?",
    "Mikor megyünk már moziba?",
    "Szeretném ha figyelnél a hasikádra és nem ennél sokat.",
    "Miért dolgozol ilyenkor?!",
    "Ne fáradj el légyszives, nyomogasd meg a szemed.",
    "Gyönyörű szép vagy ma!",
    "Gyönyörű szép vagy ma! ... És máskor is!",
    "Csodaszép vagy ám.",
    "Mit fogsz ma ebédelni?",
    "Nem kérsz egy kávét? Sütit? Valamit?",
    "Ne legyél ma goromba, jó?",
    "Hová akarsz legközelebb elutazni?",
    "Mit csinálunk a hétvégén?",
    "Mikor vili?",
    "Tetszik a fölsőd.",
    "Hé nem jössz ide?..",
    "Na.",
    "Nagyon cuki amikor kirakod a fogacskádat.",
    "Klip-klap-klip-klap.. Prrrr.",
    "MAU. ... MAU. Ma..khmskas..u."
]

fun = ["😍", "😙", "😀", "😆", "😄", "😂", "😊", "🙂", "😁", "😱", "😘", "😚", "😍", "😝", "🤑", "😛", "😇", "😎", "😏",
       "❤", "😴", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🐱", "🍵", "☕", "🙏", "🙈", "🙉", "🙊", "🙃",
       "🤖", "🤗", "🤘", "🤙", "🤞", "🤷", "💰", "👽", "💛", "💙", "💜", "❤", "💚", "💓", "💗", "💕", "💞", "💘", "💖",
       "✨", "⭐", "🌟", "💫", "🎵", "🔥", "🎃", "👻", "🎅", "🎄", "🎁", "🔔", "🐱", "🐶", "🐭", "🐹", "🐰", "🐺", "🐸",
       "🐵", "🐒", "🐴", "🐎", "🐘", "🐼",  "🐦", "🐤", "🐥", "🐣", "🐔", "🐧", "🐢", "🐈", "🐩", "🐯", "🐨", "🐻", "🐆"
        "🐞", "🐌", "🐙", "🐠", "🐟", "🐳", "🐋", "🐬", "🐄", "🐏",  "🐃", "🐅", "🐇", "🐐", "🐓", "🐕", "🐖",
        "🐁", "🐲", "🐡", "🐊", "🐪" ]

sad = ["😓", "😥", "😩", "😔", "😞", "😖", "😨", "😰", "😣", "😢", "😭", "😂", "😲", "😱", "😫", "😠", "😡", "😤", "😪",
       "💥", "💥", "💢", "❗", "❓",  "🐫", "🐑", "🐍", "🐛", "🐝", "🐜", "🐀", "🐉", "🐂", "🐷", "🐽", "🐮", "🐗"]

SMALL_LINE = "-------------------"
DOUBLE_LINE = SMALL_LINE + SMALL_LINE
LONG_LINE = SMALL_LINE + SMALL_LINE + SMALL_LINE + SMALL_LINE
TASK = "------------ TASK {} - {} ------------"
TASK_END = "------------ TASK {} - {} - Befejezve ------------"
SMALL_ARROW = "---------->"
TASK1 = "------------------ TASK 1 - 100% Színezés ------------------"
TASK1_END = "------------ TASK 1 - 100% Színezés - Befejezve ------------"

class Message:
    @staticmethod
    def log_block(text, text2, log_method):
        log_method(LONG_LINE)
        log_method(LONG_LINE)
        for j in range(10):
            log_method('->')
            if j == 4:
                if len(text) > 20:
                    log_method('->  ' + text)
                else:
                    logging.info('->                             ' + text)
            if j == 5 and text2 is not None:
                log_method('->    ' + text2)
        log_method(LONG_LINE)
        log_method(LONG_LINE)
