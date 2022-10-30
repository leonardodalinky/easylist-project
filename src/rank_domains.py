
from os import PathLike
from typing import Optional, Union
from datetime import datetime
from filter_parser import Rules


top_level_domain = [
    'top','com','xyz','xin','vip','win','red','net','org','wang',
    'gov','edu','mil','co','biz','name','info','mobi','pro',
    'travel','club','museum','int','aero','post','rec','asia',
    'ac','ad','ae','af','ag','ai','al','am','an',
    'ao','aq','ar','as','at','au','aw','az','ba',
    'bb','bd','be','bf','bg','bh','bi','bj','bm',
    'bn','bo','br','bs','bt','bv','bw','by','bz',
    'ca','cc','cd','cf','cg','ch','ci','ck','cl',
    'cm','cn','co','cr','cu','cv','cx','cy','cz',
    'de','dj','dk','dm','do','dz','ec','ee','eg',
    'er','es','et','eu','fi','fj','fk','fm','fo',
    'fr','ga','gd','ge','gf','gg','gh','gi','gl',
    'gm','gn','gp','gq','gr','gs','gt','gu','gw',
    'gy','hk','hm','hn','hr','ht','hu','id','ie',
    'il','im','in','io','iq','ir','is','it','je',
    'jm','jo','jp','ke','kg','kh','ki','km','kn',
    'kr','kw','ky','kz','la','lb','lc','li','lk',
    'lr','ls','lt','lu','lv','ly','ma','mc','md',
    'me','mg','mh','mk','ml','mm','mn','mo','mp',
    'mq','mr','ms','mt','mu','mv','mw','mx','my',
    'mz','na','nc','ne','nf','ng','ni','nl','no',
    'np','nr','nu','nz','om','pa','pe','pf','pg',
    'ph','pk','pl','pm','pn','pr','ps','pt','pw',
    'py','qa','re','ro','ru','rw','rs','sa','sb',
    'sc','sd','se','sg','sh','si','sk','sl','sm',
    'sn','so','sr','st','sv','sy','sz','tc','td',
    'tf','tg','th','tj','tk','tl','tm','tn','to',
    'tr','tt','tv','tw','tz','ua','ug','uk','us',
    'uy','uz','va','vc','ve','vg','vi','vn','vu',
    'wf','ws','ye','yt','yu','za','zm','zw','cs',
    'eh','kp','ax','bv','gb','sj','um','tp','su',
    'cs','dd','zr','fun',
    'fans','ren','club','city','fun','host',
    'art','firm','nom','store','web','icu','shop','game','trip','top','energy','citic','baidu', 'cat','jobs','coop','tel','xxx','arpa','root','site','ltd','tech','uno','cyou','cool','online','love','homes','space','ink','rest','group','buzz','run','cloud','cam','rest','press','world','live','life','today','center','bar','pub','fit','work','wiki','technology','zone','link','website','design','fashion','bet','plus','email','email','video','pink','men','one','moe','review','lol','movie','best','tools','app','fish','blog','rocks','sex','coupons','click','international','bid','how','monster'
]


def rules_from_file(file_path: Union[str, PathLike]):
    index, commit_hash, posix_time = file_path.split('/')[-1].split('.')[0].split('_')
    utc_time = datetime.utcfromtimestamp(int(posix_time))
    rules = Rules.from_file(file_path, utc_time)
    return rules

def get_domains_from_rules(rules: Rules):
    domains = []
    for item in rules:
        if not item.domain == '':
            domains.append(item.domain)
    return domains

def domains_cleaning(domains):
    cleaning_data = {}
    for domain in domains:
        if domain.find(':') > 0:
            domain = ":".join(domain.split(":")[:-1])
        domain_levels = domain.split('.')[::-1]
        secondory_domain = ""
        bz = True
        for i in range(len(domain_levels)): 
            domain_item = domain_levels[i]
            if not domain_item in top_level_domain:
                bz = False
                if (not i == 0) and (domain_item.find('*') == -1):
                    secondory_domain = ".".join(domain_levels[:i+1][::-1])
                    if not secondory_domain in cleaning_data:
                        cleaning_data[secondory_domain] = 1
                    else:
                        cleaning_data[secondory_domain] += 1
                break
        if bz:
            if len(domain_levels)>1:
                if not domain in cleaning_data:
                    cleaning_data[domain] = 1
                else:
                    cleaning_data[domain] += 1
    return cleaning_data

# 读入文件名，输出文件名
def rank_domains(rules_file_path: Union[str, PathLike], rank_file_path: Union[str, PathLike]):
    rules = rules_from_file(rules_file_path) 
    domains = get_domains_from_rules(rules)
    clean_domains = domains_cleaning(domains)
    print("\nThere are "+str(len(domains))+" rules.")
    print("Including "+str(len(clean_domains))+" domain names.\n")
    file = open(rank_file_path, "w")
    domains_rank = sorted(clean_domains.items(), key= lambda x:x[1], reverse=True) 
    for item in domains_rank:
        file.write(item[0]+","+str(item[1]))
        file.write('\n')
    file.close()