import re

class DataProcessor():
    def __init__(self, input: str):
        self.input = input

    def filter_text(self, s: str) -> str:
        res = ''
        l_str = s.split(' ')
        for x in l_str:
            if len(x) > 2 and set(".,:;!_*-+()/#¤%&)").isdisjoint(x):
                res += x + ' '
        return res[:-1]

    def getPost(self, s: str) -> str:
        s = self.filter_text(s)
        if len(s) < 4:
            return ''
        key_words = ('инженер',
        'информационн',
        'программист',
        'ведущий',
        'строительн', 
        'бизнес-аналитик', 
        'бизнес', 
        'аналитик', 
        'рекрутер', 
        'конференц-менеджер', 
        'с', 
        'веб',
        'разработчик', 
        'cистемный',
        'развити',
        'тестировщик',
        'архитектор',
        'мерчандайзер',
        'автоматизац',
        'соцсет',
        'по',
        'продуктов',
        'куратор',
        'проектн',
        'эксперт',
        'бухгалтер',
        'развити',
        'продавец',
        'поддержк',
        'общественност',
        'производст',
        'данным',
        'стратеги',
        'управляющий',
        'бренд',
        'дизайнер',
        'технический',
        'программист',
        'аналитик',
        'техник',
        'менеджер',
        'данн',
        'закупк',
        'seo',
        'копирайтер',
        'it',
        'специалист',
        'коммуникаци',
        'партнер',
        'безопасност',
        'монтажник',
        'digital',
        'маркетин',
        'менеджер',
        'специалист',
        'продажам',
        'проект',
        'бренд',
        'логистик',
        'консультант',
        'офис-менеджер',
        'инженер-конструктор',
        'корпоративн',
        'руководитель',
        'координатор',
        'строительст',
        'тестировщ',
        'HR',
        'магазина',
        'писатель',
        'клиент',
        'мобильный',
        'Главн',
        'работ',
        'архитектор',
        'продукта',
        'интернет',
        'маркетолог',
        'генеральный',
        'разработчик',
        'психолог',
        'маркетинг',
        'персонал',
        'коуч',
        'логист',
        'UX/UI',
        'поисков',
        'экономист',
        'кадров',
        'представ',
        'фотограф',
        'продукт',
        'менеджер',
        'учителъ',
        'директор',
        'финанс',
        'связ',
        'директор',
        'производственн',
        'проду',
        'арт',
        'маркетолог',
        'инженер',
        'мерч')
        for x in key_words:
            if x in s.lower():
                return s
        return ''
    
    def filter_site(self, s: str) -> str:
        res = ''
        l_str = s.split(' ')
        for x in l_str:
            if len(x) > 2 and '.' in x:
                res += x
        return res

    def getSite(self, s: str) -> str:
        s = self.filter_site(s)
        if len(s) < 5:
            return ''
        key_words = ('.creditcard', '.run', '.pro', '.holdings', '.finance', '.life', '.ua', '.ee', '.science', '.ch', '.mx', '.country', '.hosting', '.mp', '.trade', '.loans', '.lr', '.legal', '.schule', '.cloud', '.apartments', '.voto', '.yoga', '.ps', '.bt', '.desi', '.fm', '.car', '.restaurant', '.sz', '.soy', '.dog', '.top', '.xxx', '.is', '.lb', '.ceo', '.ao', '.ky', '.gi', '.as', '.flowers', '.delivery', '.website', '.express', '.pt', '.gift', '.be', '.claims', '.gives', '.sarl', '.tn', '.mw', '.et', '.ax', '.moscow', '.shop', '.cricket', '.su', '.name', '.ink', '.media', '.gh', '.bw', '.gold', '.tatar', '.cf', '.vn', '.kiwi', '.spor', '.cc', '.рф', '.juegos', '.blog', '.wine', '.wtf', '.auto', '.webcam', '.cafe', '.gl', '.horse', '.exposed', '.rocks', '.singles', '.pl', '.theater', '.wien', '.africa', '.study', '.shopping', '.givin', '.rentals', '.luxury', '.fishing', '.gs', '.photography', '.cool', '.email', '.insure', '.style', '.accountant', '.taxi', '.cheap', '.fit', '.pics', '.gy', '.ad', '.salon', '.br', '.bj', '.foundation', '.education', '.tc', '.one', '.doctor', '.kid', '.in', '.training', '.fund', '.productions', '.kn', '.kg', '.expert', '.onl', '.vin', '.menu', '.republican', '.codes', '.kz', '.fj', '.security', '.soccer', '.gg', '.cz', '.li', '.ooo', '.ventures', '.tennis', '.pictures', '.tw', '.diamonds', '.gifts', '.systems', '.vote', '.tienda', '.surgery', '.co', '.sexy', '.theatre', '.tv', '.casino', '.gm', '.adult', '.cars', '.promo', '.lol', '.catering', '.rodeo', '.charit', '.ma', '.fail', '.tips', '.fyi', '.bs', '.aw', '.mz', '.football', '.space', '.graphics', '.онлайн', '.land', '.care', '.christmas', '.vc', '.moda', '.money', '.supplies', '.discount', '.jewelry', '.cn', '.press', '.om', '.town', '.lighting', '.kh', '.school', '.dance', '.download', '.glass', '.lease', '.marketing', '.bg', '.movie', '.zone', '.sm', '.games', '.maison', '.cl', '.coupons', '.photo', '.vg', '.hockey', '.market', '.direct', '.international', '.villas', '.uz', '.дети', '.supply', '.sl', '.dj', '.tickets', '.nu', '.audio', '.cash', '.vip', '.ro', '.kim', '.tk', '.exchange', '.studio', '.fish', '.vision', '.ph', '.store', '.date', '.de', '.loan', '.uno', '.builders', '.army', '.il', '.net', '.mo', '.pr', '.cards', '.fashion', '.tl', '.mobi', '.aq', '.eg', '.repair', '.hk', '.mk', '.florist', '.site', '.es', '.fo', '.dental', '.lux', '.voyage', '.sex', '.company', '.zm', '.immobilien', '.institute', '.estate', '.ni', '.game', '.academy', '.bike', '.pink', '.group', '.np', '.fun', '.az', '.sucks', '.ck', '.zw', '.photos', '.ae', '.computer', '.pn', '.jm', '.consulting', '.jobs', '.za', '.properties', '.protection', '.bar', '.ge', '.link', '.cr', '.tech', '.coffee', '.xyz', '.tz', '.band', '.london', '.mu', '.pet', '.construction', '.ls', '.reisen', '.pk', '.guru', '.na', '.ke', '.city', '.watch', '.gr', '.navy', '.ai', '.holiday', '.wiki', '.love', '.tg', '.gmbh', '.how', '.se', '.gn', '.management', '.reviews', '.cologne', '.community', '.sp', '.show', '.tt', '.house', '.so', '.design', '.contractors', '.win', '.au', '.sg', '.camp', '.dm', '.sn', '.st', '.vi', '.click', '.forsale', '.futbol', '.works', '.center', '.rest', '.nf', '.furniture', '.shiksha', '.tires', '.lk', '.accountants', '.family', '.technology', '.рус', '.church', '.tirol', '.asi', '.support', '.vet', '.jo', '.rehab', '.vu', '.sb', '.ki', '.report', '.domains', '.surf', '.farm', '.bet', '.ms', '.engineer', '.casa', '.credit', '.bayern', '.cooking', '.af', '.bio', '.clinic', '.mba', '.airforce', '.bid', '.am', '.gf', '.recipes', '.partners', '.degree', '.vodka', '.shoes', '.ve', '.hiphop', '.hr', '.memorial', '.rw', '.ie', '.enterprises', '.bi', '.moe', '.university', '.ba', '.md', '.parts', '.ly', '.mt', '.app', '.poker', '.radio', '.cx', '.ht', '.inf', '.cy', '.re', '.camera', '.jp', '.pag', '.eu', '.guitars', '.mc', '.world', '.hospital', '.sr', '.agency', '.ye', '.lv', '.москва', '.green', '.sv', '.fi', '.black', '.sa', '.cruises', '.bo', '.global', '.attorney', '.viajes', '.digital', '.today', '.gd', '.pub', '.help', '.lt', '.news', '.club', '.party', '.cg', '.trading', '.auction', '.blue', '.healthcare', '.coach', '.coop', '.ga', '.blackfriday', '.career', '.college', '.ir', '.sk', '.boutique', '.kw', '.limo', '.best', '.s', '.ll', '.beer', '.forex', '.red', '.tours', '.wedding', '.brussels', '.stream', '.bn', '.work', '.chat', '.py', '.film', '.realty', '.do', '.je', '.buzz', '.no', '.id', '.gripe', '.tools', '.voting', '.art', '.condos', '.tube', '.limited', '.sy', '.vegas', '.dz', '.travel', '.hn', '.cab', '.nz', '.garden', '.to', '.rip', '.deals', '.gt', '.cleaning', '.racing', '.td', '.ug', '.careers', '.services', '.орг', '.cd', '.mortgage', '.solar', '.diet', '.business', '.berlin', '.bd', '.qpon', '.mv', '.events', '.build', '.pizza', '.toys', '.industries', '.earth', '.energy', '.gp', '.observer', '.sale', '.bingo', '.mom', '.vacations', '.engineering', '.gent', '.clothing', '.equipment', '.rs', '.dating', '.plumbing', '.us', '.nr', '.cm', '.miami', '.ws', '.social', '.flights', '.tattoo', '.dk', '.guide', '.nc', '.fitness', '.democrat', '.uy', '.bank', '.fr', '.actor', '.tax', '.сайт', '.rich', '.software', '.ltd', '.qa', '.ru', '.dentist', '.uk', '.ski', '.tel', '.bargains', '.pa', '.host', '.property', '.th', '.rent', '.mg', '.bm', '.ar', '.si', '.network', '.haus', '.hm', '.hu', '.al', '.tm', '.plus', '.cu', '.sd', '.my', '.gallery', '.kr', '.org', '.bh', '.kaufen', '.gratis', '.paris', '.live', '.ci', '.im', '.cat', '.fans', '.ng', '.team', '.it', '.at', '.gu', '.video', '.investments', '.ca', '.nl', '.courses', '.directory', '.aer', '.online', '.lawyer', '.ec', '.solutions', '.associates', '.tr', '.lu', '.immo', '.men', '.kitchen', '.golf', '.irish', '.broker', '.cam', '.io', '.fk', '.tj', '.pe', '.faith', '.capital', '.review', '.ninja', '.financial')
        for x in key_words:
            if x in s:
                return s
        return ''
    
    def getEmail(self, s: str) -> str:
        s = self.filter_site(s)
        if len(s) < 5:
            return ''
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if EMAIL_REGEX.match(s):
            return s
        else:
            return ''
    
    def filter_num(self, s: str) -> str:
        res = ''
        l_str = s.split(' ')
        for x in l_str:
            if not set("+()-1234567890").isdisjoint(x):
                res += x
        return res

    def getNum(self, s: str) -> str:
        s = self.filter_num(s)
        NUM_REGEX = re.compile(r'^((\+?7|8)[ \-]? ?)?((\(\d{3}\))|(\d{3}))?([ \-])?(\d{3}[\- ]?\d{2}[\- ]?\d{2})$')
        if NUM_REGEX.match(s):
            return s
        else:
            return ''

    def getName(self, s: str) -> str:
        NAME_REGEX = re.compile(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?')
        if NAME_REGEX.match(s):
            return s
        else:
            return ''
    
    def dataExtract(self) -> tuple:
        company = ''
        name = ''
        post = ''
        num1 = ''
        num2 = ''
        email = ''
        site = ''
        str_list = self.input.split('\n')
        print(str_list)
        for s in str_list:
            if self.getPost(s) != '':
                post = self.getPost(s)
            elif self.getNum(s) != '':
                if num1 == '':
                    num1 = self.getNum(s)
                else:
                    num2 = self.getNum(s)
            elif self.getSite(s) != '':
                if self.getEmail(s) != '':
                    email = self.getEmail(s)
                else:
                    site = self.getSite(s)
            if self.getName(s) != '':
                name = self.getName(s)

        t = (company, name, post, num1, num2, email, site)
        return t