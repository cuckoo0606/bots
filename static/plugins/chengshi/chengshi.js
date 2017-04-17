/* *
 *  * ---------------------------------------- *
 *   * 城市选择组件 v1.0
 *    * Author: VVG
 *     * QQ: 83816819
 *      * Mail: mysheller@163.com
 *       * http://www.cnblogs.com/NNUF/
 *        * ---------------------------------------- *
 *         * Date: 2012-07-10
 *          * ---------------------------------------- *
 *           * */

/* *
 *  * 全局空间 Vcity
 *   * */
var Vcity = {};
/* *
 *  * 静态方法集
 *   * @name _m
 *    * */
Vcity._m = {
    /* 选择元素 */
    $:function (arg, context) {
        var tagAll, n, eles = [], i, sub = arg.substring(1);
        context = context || document;
        if (typeof arg == 'string') {
            switch (arg.charAt(0)) {
                case '#':
                    return document.getElementById(sub);
                    break;
                case '.':
                    if (context.getElementsByClassName) return context.getElementsByClassName(sub);
                    tagAll = Vcity._m.$('*', context);
                    n = tagAll.length;
                    for (i = 0; i < n; i++) {
                        if (tagAll[i].className.indexOf(sub) > -1) eles.push(tagAll[i]);
                    }
                    return eles;
                    break;
                default:
                    return context.getElementsByTagName(arg);
                    break;
            }
        }
    },

    /* 绑定事件 */
    on:function (node, type, handler) {
           node.addEventListener ? node.addEventListener(type, handler, false) : node.attachEvent('on' + type, handler);
       },

    /* 获取事件 */
    getEvent:function(event){
                 return event || window.event;
             },

    /* 获取事件目标 */
    getTarget:function(event){
                  return event.target || event.srcElement;
              },

    /* 获取元素位置 */
    getPos:function (node) {
               var scrollx = document.documentElement.scrollLeft || document.body.scrollLeft,
               scrollt = document.documentElement.scrollTop || document.body.scrollTop;
               var pos = node.getBoundingClientRect();
               return {top:pos.top + scrollt, right:pos.right + scrollx, bottom:pos.bottom + scrollt, left:pos.left + scrollx }
           },

    /* 添加样式名 */
    addClass:function (c, node) {
                 if(!node)return;
                 node.className = Vcity._m.hasClass(c,node) ? node.className : node.className + ' ' + c ;
             },

    /* 移除样式名 */
    removeClass:function (c, node) {
                    var reg = new RegExp("(^|\\s+)" + c + "(\\s+|$)", "g");
                    if(!Vcity._m.hasClass(c,node))return;
                    node.className = reg.test(node.className) ? node.className.replace(reg, '') : node.className;
                },

    /* 是否含有CLASS */
    hasClass:function (c, node) {
                 if(!node || !node.className)return false;
                 return node.className.indexOf(c)>-1;
             },

    /* 阻止冒泡 */
    stopPropagation:function (event) {
                        event = event || window.event;
                        event.stopPropagation ? event.stopPropagation() : event.cancelBubble = true;
                    },
    /* 去除两端空格 */
    trim:function (str) {
             return str.replace(/^\s+|\s+$/g,'');
         }
};

/* 所有城市数据,可以按照格式自行添加（北京|beijing|bj），前16条为热门城市 */

Vcity.allCity = ['北京|beijing|bj','上海|shanghai|sh', '重庆|chongqing|cq',  '深圳|shenzhen|sz', '广州|guangzhou|gz', '杭州|hangzhou|hz',
    '南京|nanjing|nj', '苏州|shuzhou|sz', '天津|tianjin|tj', '成都|chengdu|cd', '南昌|nanchang|nc', '三亚|sanya|sy','青岛|qingdao|qd',
    '厦门|xiamen|xm', '西安|xian|xa','长沙|changsha|cs','合肥|hefei|hf','西藏|xizang|xz', '内蒙古|neimenggu|nmg', '安庆|anqing|aq', '阿泰勒|ataile|atl', '安康|ankang|ak',
    '阿克苏|akesu|aks', '包头|baotou|bt', '北海|beihai|bh', '百色|baise|bs','保山|baoshan|bs', '长治|changzhi|cz', '长春|changchun|cc', '常州|changzhou|cz', '昌都|changdu|cd',
    '朝阳|chaoyang|cy', '常德|changde|cd', '长白山|changbaishan|cbs', '赤峰|chifeng|cf', '大同|datong|dt', '大连|dalian|dl', '达县|daxian|dx', '东营|dongying|dy', '大庆|daqing|dq', '丹东|dandong|dd',
    '大理|dali|dl', '敦煌|dunhuang|dh', '鄂尔多斯|eerduosi|eeds', '恩施|enshi|es', '福州|fuzhou|fz', '阜阳|fuyang|fy', '贵阳|guiyang|gy',
    '桂林|guilin|gl',  '格尔木|geermu|gem', '呼和浩特|huhehaote|hhht', '哈密|hami|hm',
    '黑河|heihe|hh', '海拉尔|hailaer|hle', '哈尔滨|haerbin|heb', '海口|haikou|hk', '黄山|huangshan|hs', '邯郸|handan|hd',
    '汉中|hanzhong|hz', '和田|hetian|ht', '晋江|jinjiang|jj', '锦州|jinzhou|jz', '景德镇|jingdezhen|jdz',
    '嘉峪关|jiayuguan|jyg', '井冈山|jinggangshan|jgs', '济宁|jining|jn', '九江|jiujiang|jj', '佳木斯|jiamusi|jms', '济南|jinan|jn',
    '昆明|kunming|km', '康定|kangding|kd', '克拉玛依|kelamayi|klmy', '库尔勒|kuerle|kel', '库车|kuche|kc', '兰州|lanzhou|lz',
    '洛阳|luoyang|ly', '丽江|lijiang|lj', '林芝|linzhi|lz', '柳州|liuzhou|lz', '泸州|luzhou|lz', '连云港|lianyungang|lyg', '黎平|liping|lp',
    '连成|liancheng|lc', '拉萨|lasa|ls', '临沧|lincang|lc', '临沂|linyi|ly', '芒市|mangshi|ms', '牡丹江|mudanjiang|mdj', '满洲里|manzhouli|mzl', '绵阳|mianyang|my',
    '梅县|meixian|mx', '漠河|mohe|mh', '南充|nanchong|nc', '南宁|nanning|nn', '南阳|nanyang|ny', '南通|nantong|nt', '那拉提|nalati|nlt',
    '宁波|ningbo|nb', '攀枝花|panzhihua|pzh', '衢州|quzhou|qz', '秦皇岛|qinhuangdao|qhd', '庆阳|qingyang|qy', '齐齐哈尔|qiqihaer|qqhe',
    '石家庄|shijiazhuang|sjz',  '沈阳|shenyang|sy', '思茅|simao|sm', '铜仁|tongren|tr', '塔城|tacheng|tc', '腾冲|tengchong|tc', '台州|taizhou|tz',
    '通辽|tongliao|tl', '太原|taiyuan|ty', '威海|weihai|wh', '梧州|wuzhou|wz', '文山|wenshan|ws', '无锡|wuxi|wx', '潍坊|weifang|wf',  '乌兰浩特|wulanhaote|wlht',
    '温州|wenzhou|wz', '乌鲁木齐|wulumuqi|wlmq', '万州|wanzhou|wz', '乌海|wuhai|wh', '兴义|xingyi|xy', '西昌|xichang|xc',  '襄樊|xiangfan|xf',
    '西宁|xining|xn', '锡林浩特|xilinhaote|xlht', '西双版纳|xishuangbanna|xsbn', '徐州|xuzhou|xz',  '永州|yongzhou|yz', '榆林|yulin|yl', '延安|yanan|ya', '运城|yuncheng|yc',
    '银川|yinchuan|yc',  '盐城|yancheng|yc', '延吉|yanji|yj', '玉树|yushu|ys', '伊宁|yining|yn', '珠海|zhuhai|zh', 
    '张家界|zhangjiajie|zjj',  '郑州|zhengzhou|zz', '芷江|zhijiang|zj', '湛江|zhanjiang|zj',
    '阿城|acheng|ac', '双城|shuangcheng|sc', '尚志|shangzhi|sz', '五常|wuchang|wc', '讷河|nehe|nh', '鸡西|jixi|jx', '虎林|hulin|hl', '密山|mishan|ms', '鹤岗|hegang|hg',
   '双鸭山|shuangyashan|sys', '伊春|yichun|yc', '铁力|tieli|tl', '同江|tongjiang|tj', '富锦|fujin|fj', '七台河|qitaihe|qth', '海林|hailin|hl', '宁安|ningan|na', 
    '穆棱|muling|ml', '北安|beian|ba', '五大连池|wudalianchi|wdlc', '绥化|suihua|sh', '安达|anda|ad', '肇东|zhaodong|zd', '海伦|hailun|hl', '长春|changchun|cc', 
    '九台|jiutai|jt', '榆树|yushu|ys', '德惠|dehui|dh', '吉林|jilin|jl', '蛟河|jiaohe|jh', '桦甸|huadian|hd', '舒兰|shulan|sl', '磬石|qingshi|qs', '四平|siping|sp',
    '公主岭|gongzhuling|gzl', '双辽|shuangliao|sl', '辽源|liaoyuan|ly', '通化|tonghua|th', '梅河口|meihekou|mhk', '集安|jian|ja', '白山|baishan|bs', '临江|linjiang|lj', 
    '松原|songyuan|sy', '白城|baicheng|bc', '洮南|taonan|tn', '大安|daan|da', '图们|tumen|tm', '敦化|dunhua|dh', '珲春|hunchun|hc', '龙井|longjing|lj', '和龙|helong|hl',
    '焦作|jiaozuo|jz', '商丘|shangqiu|sq', '信阳|xinyang|xy', '周口|zhoukou|zk', '鹤壁|hebi|hb', '安阳|anyang|ay', '濮阳|puyang|py', '驻马店|zhumadian|zmd', 
    '开封|kaifeng|kf', '漯河|luohe|lh', '许昌|xuchang|xc', '新乡|xinxiang|xx', '济源|jiyuan|jy', '灵宝|lingbao|lb', '偃师|yanshi|ys', '邓州|dengzhou|dz', 
    '登封|dengfeng|df','三门峡|sanmenxia|smx', '新郑|xinzheng|xz', '禹州|yuzhou|yz', '巩义|gongyi|gy', '永城|yongcheng|yc', '长葛|changge|cg', '义马|yima|ym', 
    '林州|linzhou|lz', '汝阳|ruyang|ry', '荥阳|xingyang|xy', '平顶山|pingdingshan|pds', '卫辉|weihui|wh', '辉县|huixian|hx', '舞钢|wugang|wg', '新密|xinmi|xm', 
    '孟州|mengzhou|mz', '沁阳|qinyang|qy', '郏县|jiaxian|jx', '亳州|bozhou|bz', '芜湖|wuhu|wh', '马鞍山|maanshan|mas', '池州|chizhou|cz', '滁州|chuzhou|cz', 
    '淮南|huainan|hn', '淮北|huaibei|hb', '蚌埠|bengbu|bb', '宿州|suzhou|sz', '宣城|xuancheng|xc', '六安|liuan|la', '铜陵|tongling|tl', 
    '明光|minggaung|mg','天长|tainchang|tc', '宁国|ningguo|ng', '界首|jieshou|js', '桐城|tongcheng|tc', '泉州|quanzhou|qz','漳州|zhangzhou|zz', '南平|nanping|np', 
    '三明|sanming|sm', '龙岩|longyan|ly', '莆田|putian|pt', '宁德|ningde|nd','建瓯|jianou|jo', '武夷山|wuyishan|wys', '长乐|changle|cl', '福清|fuqing|fq', 
    '晋江|jinjiang|jj', '南安|nanan|na','福安|fuan|fa', '龙海|longhai|lh', '昭武|zhaowu|zw', '石狮|shishi|ss', '福鼎|fuding|fd', '建阳|jianyang|jy', 
    '漳平|zhangping|zp', '永安|yongan|ya', '白银|baiyin|by','武威|wuwei|ww', '金昌|jinchang|jc', '平凉|pingliang|pl', '张掖|zhangye|zy', '酒泉|jiuquan|jq', 
    '庆阳|qingyang|qy', '定西|dingxi|dx', '陇南|longnan|ln', 
    '天水|tianshui|ts', '玉门|yumen|ym', '临夏|linxia|lx', '合作|hezuo|hz', '甘南|gannan|gn', '安顺|anshun|as', '遵义|zunyi|zy', '六盘水|liupanshui|lps', '都匀|duyun|dy',
    '凯里|kaili|kl', '毕节|bijie|bj', '清镇|qingzhen|qz', '赤水|chishui|cs', '仁怀福泉|renhuaifuquan|rhfq', '万宁|wanning|wn', '文昌|wenchang|wc', '儋州|danzhou|dz',
    '琼海|qionghai|qh', '东方|dongfang|df', '五指山|wuzhishan|wzs', '保定|baoding|bd', '唐山|tangshan|ts', '邢台|xingtai|xt', '沧州|cangzhou|cz', '衡水|hengshui|hs',
    '廊坊|langfang|lf', '承德|chengde|cd', '迁安|qianan|qa', '鹿泉|luquan|lq', '南宫|nangong|ng', '任丘|renqiu|rq', '叶城|yecheng|yc', '辛集|xinji|xj', '涿州|zhuozhou|zz',
    '定州|dingzhou|dz', '晋州|jinzhou|jz', '霸州|bazhou|bz', '黄骅|huanghua|hh', '遵化|zunhua|zh', '张家口|zhangjiakou|zjk', '沙河|shahe|sh', '三河|sanhe|sh',
    '冀州|jizhou|jz', '武安|wuan|wa', '河间|hejian|hj', '深州|shenzhou|sz', '新乐|xinle|xl', '泊头|botou|bt', '安国|anguo|ag', '双滦|shuangluan|sl', '高碑店|gaobeidian|gbd',
    '武汉|wuhan|wh', '荆门|jingmen|jm', '咸宁|xianning|xn', '襄樊|xiangfan|xf', '荆州|jingzhou|jz', '黄石|huangshi|hs', '宜昌|yichang|yc', '随州|suizhou|sz', 
    '鄂州|ezhou|ez', '孝感|xiaogan|xg', '黄冈|huanggang|hg', '十堰|shiyan|sy', '枣阳|zaoyang|zy', '老河口|laohekou|lhk',  '仙桃|xiantao|xt', 
    '天门|tianmen|tm', '钟祥|zhongxiang|zx', '潜江|qianjiang|qj', '麻城|macheng|mc', '洪湖|honghu|hh', '汉川|hanchuan|hc', '赤壁|chibi|cb', '松滋|songzi|sz',  
    '丹江口|danjiangkou|djk', '武学|wuxue|wx', '广水|guangshui|gs', '石首|shishou|ss', '大治|dazhi|dz', '枝江|zhijiang|zj', '应城|yingcheng|yc', '宜城|yicheng|yc', 
    '当阳|dangyang|dy', '安陆|anlu|al', '宜都|yidu|yd', '利川|lichuan|lc', '郴州|chenzhou|cz', '益阳|yiyang|yy', '娄底|loudi|ld', '株洲|zhuzhou|zz', '衡阳|hengyang|hy', 
    '湘潭|xiangtan|xt', '岳阳|yueyang|yy', '常德|cahngde|cd', '昭阳|zhaoyang|zy', '永州|yongzhou|yz', '怀化|huaihua|hh', '浏阳|liuyang|ly', '醴陵|liling|ll', 
    '湘乡|xiangxiang|xx', '耒阳|leiyang|ly', '沅江|yuanjiang|yj', '涟源|lianyuan|ly', '常宁|changning|cn', '吉首|jishou|js', '津市|jinshi|js', '冷水江|lengshuijiang|lsj', 
    '临湘|linxiang|lx', '汨罗|miluo|ml', '武冈|wugang|wg', '韶山|shaoshan|ss', '安化|anhua|ah', '湘西|xaingxi|xx', '无锡|wuxi|wx','扬州|yangzhou|yz', 
    '徐州|xuzhou|xz', '苏州|suzhou|sz',  '盐城|yancheng|yc', '淮安|huaian|ha', '宿迁|suqian|sq', '镇江|zhenjiang|zj', '南通|nantong|nt', 
    '泰州|taizhou|tz', '兴化|xinghua|xh', '东台|dongtai|dt', '常熟|changshu|cs', '江阴|jiangyin|jy', '张家港|zhangjiagang|zjg', '通州|tongzhou|tz', '宜兴|yixing|yx', 
    '邳州|pizjou|pz', '海门|haimen|hm', '大丰|dafeng|df', '溧阳|liyang|ly', '泰兴|taixing|tx', '如市|rushi|rs', '昆山|kunshan|ks', '启东|qidong|qd', '江都|jiangdu|jd', 
    '丹阳|danyang|dy', '吴江|wujiang|wj', '靖江|jingjiang|jj', '扬中|yangzhong|yz', '新沂|xinyi|xy', '仪征|yizheng|yz', '太仓|taicang|tc', '姜堰|jiangyan|jy',
    '高邮|gaoyou|gy', '金坛|jintan|jt', '句容|jurong|jr', '灌南|guannan|gn',
    '赣州|ganzhou|gz', '上饶|shangrao|sr', '宜春|yichun|yc', '新余|xinyu|xy', '萍乡|pingxiang|px', '抚州|fuzhou|fz', '鹰潭|yingtan|yt', '吉安|jian|ja', 
    '丰城|fengcheng|fc', '樟树|zhangshu|zs', '德兴|dexing|dx', '瑞金|ruijin|rj', '高安|gaoan|ga', '乐平|leping|lp', '南康|nankang|nk', '贵溪|guixi|gx', '瑞昌|ruichang|rc', 
    '东乡|dongxaing|dx', '广丰|guangfeng|gf', '信州|xinzhou|xz', '三清|sanqing|sq', '葫芦岛|huludao|hld', '盘锦|panjin|pj', '鞍山|anshan|as', '铁岭|tieling|tl', 
    '本溪|benxi|bx', '丹东|dandong|dd', '抚顺|fushun|fs', '锦州|jinzhou|jz', '辽阳|liaoyang|ly', '阜新|fuxin|fx', '调兵山|diaobingshan|dbs', '朝阳市|chaoyangshi|cys', 
    '海城|haicheng|hc', '北票|beipiao|bp', '盖州|gaizhou|gz', '凤城|fengcheng|fc', '庄河|zhuanghe|zh', '凌源|lingyuan|ly', '开原|kaiyuan|ky', '兴城|xingcheng|xc', 
    '新民|xinmin|xm', '大石桥|dashiqiao|dsq', '东港|donggang|dg', '北宁|beining|bn', '瓦房店|wafangdian|wfd', '普兰店|pulandian|pld', '凌海|linghai|lh', '灯塔|dengta|dt', 
    '营口|yingkou|yk', '西宁|xining|xn', '格尔木|geermu|gem', '德令哈|delingha|dlh', '济南|jinan|jn', '威海|weihai|wh', '潍坊|weifang|wf', '菏泽|heze|hz', 
    '济宁|jining|jn', '莱芜|laiwu|lw', '烟台|yantai|yt', '淄博|zibo|zb', '枣庄|zaozhuang|zz', '泰安|taian|ta', '日照|rizhao|rz', '德州|dezhou|dz','聊城|liaocheng|lc',
    '滨州|binzhou|bz','乐陵|leling|ll','兖州|yanzhou|yz','诸城|zhucheng|zc','邹城|zoucheng|zc','滕州|tengzhou|tz','肥城|feicheng|fc','新泰|xintai|xt',
    '胶州|jiaozhou|jz','胶南|jiaonan|jn','即墨|jimo|jm','龙口|longkou|lk','平度|pingdu|pd','莱西|laixi|lx','阳泉|yangquan|yq','临汾|linfen|lf','晋中|jinzhong|jz',
    '忻州|xinzhou|xz','朔州|shuozhou|sz','吕梁|lvliang|ll','古交|gujiao|gj','高平|gaoping|gp','永济|yongji|yj','孝义|xiaoyi|xy','侯马|houma|hm','霍州|huozhou|hz',
    '介休|jiexiu|jx','河津|hejin|hj','汾阳|fenyang|fy','原平|yuanping|yp','潞城|lucheng|lc','咸阳|xianyang|xy','宝鸡|baoji|bj','铜川|tongchuan|tc','渭南|weinan|wn',
    '汉中|hanzhong|hz','商洛|sahngluo|sl','延安|yanan|ya','韩城|hancheng|hc','兴平|xingping|xp','华阴|huayin|hy','广安|guangan|ga','德阳|deyang|dy','乐山|leshan|ls',
    '巴中|bazhong|bz','内江|neijiang|nj','宜宾|yibin|yb','南充|nanchong|nc','都江堰|dujiangyan|djy','自贡|zigong|zg','泸州|luzhou|lz','广元|guangyuan|gy','达州|dazhou|dz',
    '资阳|ziyang|zy','锦阳|jinyang|jy','眉山|meishan|ms','遂宁|suining|sn','雅安|yaan|ya','阆中|langzhong|lz','广汉|guanghan|gh','绵竹|mianzhu|mz','万源|wanyuan|wy',
    '华蓥|huaying|hy','江油|jiangyou|jy','西昌|xichang|xc','彭州|pengzhou|pz','简阳|jianyang|jy','崇州|chongzhou|cz','什邡|shenfang|sf','峨眉山|emeishan|ems',
    '邛崃|qionglai|ql','双流|shuangliu|sl','玉溪|yuxi|yx','曲靖|qujing|qj', '昭通|zhaotong|zt','保山|baoshan|bs','丽江|lijiang|lj','临沧|lincang|lc','楚雄|chuxiong|cx',
    '开远|kaiyuan|ky','个旧|gejiu|gj','景洪|jinghong|jh','安宁|anning|an','宣威|xuanwei|xw','昭兴|zhaoxing|zx','湖州|huzhou|hz','嘉兴|jiaxing|jx','金华|jinhua|jh',
    '舟山|zhoushan|zs','衢州|quzhou|qz','丽水|lishui|ls','余姚|yuyao|yy','乐清|leqing|lq','临海|linhai|lh','温岭|wenling|wl','永康|yongkang|yk','瑞安|ruian|ra',
    '慈溪|cixi|cx','义乌|yiwu|yw','上虞|shangyu|sy','诸暨|zhuji|zj','海宁|haining|hn','桐乡|tongxiang|tx','兰溪|lanxi|lx','龙泉|longquan|lq','建德|jiande|jd',
    '富德|fude|fd','富阳|fuyang|fy','平湖|pinghu|ph','东阳|dongyang|dy','嵊州|shengzhou|sz','奉化|fenghua|fh','临安|linan|la','江山|jiangshan|js','汕头|shantou|st',
    '佛山|foshan|fs','韶关|shaoguan|sg','肇庆|zhaoqing|zq','江门|jiangmen|jm','茂名|maoming|mm','惠州|huizhou|hz','梅州|meizhou|mz','汕尾|shanwei|sw','河源|heyuan|hy',
    '阳江|yangjiang|yj','清远|qingyuan|qy','东莞|donggaun|dg','中山|zhongshan|zs','潮州|chaozhou|cz','揭阳|jieyang|jy','云浮|yunfu|yf','贺州|hezhou|hz','玉林|yulin|yl',
    '柳州|liuzhou|lz','梧州|wuzhou|wz','钦州|qinzhou|qz','百色|baise|bs','防城港|fangchenggang|fcg','贵港|guigang|gg','河池|hechi|hc','崇左|chongzuo|cz','来宾|laibin|lb',
    '东兴|dongxing|dx','桂平|guiping|gp','北流|beiliu|bl', '岑溪|cenxi|cx', '合山|heshan|hs', '凭祥|pingxiang|px', '宜州|yizhou|yz', '呼伦贝尔|hulunbeier|hlbe', 
    '赤峰|chifeng|cf', '扎兰屯|zhalantun|zlt',  '乌兰察布|wulanchabu|wlcb', '巴彦淖尔|bayannaoer|byne', '二连浩特|erlianhaote|elht', 
    '霍林郭勒|huolinguole|hlgl', '乌海|wuhai|wh', '阿尔山|aershan|aes', '乌兰浩特|wulanhaote|wlht', '锡林浩特|xilinhaote|xlht', '根河|genhe|gh', '满洲|manzhou|mz', 
    '额尔古纳|eerguna|eegn', '牙克石|yakeshi|yks', '临河|linhe|lh', '丰镇|fengzhen|fz', '通辽|tongliao|tl', '固原|guyuan|gy', '石嘴山|shizuishan|szs', 
    '青铜峡|qingtongxia|qtx', '中卫|zhongwei|zw', '吴忠|wuzhong|wz', '灵武|lingwu|lw', '日喀则|rikaze|rkz', '石河子|shihezi|shz', '喀什|kashen|ks', 
    '阿勒泰|aletai|alt', '阜康|fukang|fk', '库尔勒|kuerle|kel', '阿克苏|akesu|aks', '阿拉尔|alaer|ale', '哈密|hami|hm', '克拉玛依|kelamayi|klmy', '昌吉|changji|cj',
    '奎屯|kuitun|kt','米泉|miquan|mq' ];

/* 正则表达式 筛选中文城市名、拼音、首字母 */

Vcity.regEx = /^([\u4E00-\u9FA5\uf900-\ufa2d]+)\|(\w+)\|(\w)\w*$/i;
Vcity.regExChiese = /([\u4E00-\u9FA5\uf900-\ufa2d]+)/;

/* *
 *  * 格式化城市数组为对象oCity，按照a-h,i-p,q-z,hot热门城市分组：
 *   * {HOT:{hot:[]},ABCDEFGH:{a:[1,2,3],b:[1,2,3]},IJKLMNOP:{i:[1.2.3],j:[1,2,3]},QRSTUVWXYZ:{}}
 *    * */

(function () {
    var citys = Vcity.allCity, match, letter,
    regEx = Vcity.regEx,
    reg2 = /^[a-e]$/i, reg3 = /^[f-j]$/i, reg4 = /^[k-o]$/i; reg5 = /^[p-t]$/i; reg6 = /^[u-z]$/i;
if (!Vcity.oCity) {
    Vcity.oCity = {hot:{},ABCDE:{}, FGHIJ:{}, KLMNO:{}, PQRST:{}, UVWXYZ:{}};
    console.log(citys.length);
    for (var i = 0, n = citys.length; i < n; i++) {
        match = regEx.exec(citys[i]);
        letter = match[3].toUpperCase();
        if (reg2.test(letter)) {
            if (!Vcity.oCity.ABCDE[letter]) Vcity.oCity.ABCDE[letter] = [];
            Vcity.oCity.ABCDE[letter].push(match[1]);
        } else if (reg3.test(letter)) {
            if (!Vcity.oCity.FGHIJ[letter]) Vcity.oCity.FGHIJ[letter] = [];
            Vcity.oCity.FGHIJ[letter].push(match[1]);
        } else if (reg4.test(letter)) {
            if (!Vcity.oCity.KLMNO[letter]) Vcity.oCity.KLMNO[letter] = [];
            Vcity.oCity.KLMNO[letter].push(match[1]);
        }else if (reg5.test(letter)) {
            if (!Vcity.oCity.PQRST[letter]) Vcity.oCity.PQRST[letter] = [];
            Vcity.oCity.PQRST[letter].push(match[1]);
        }else if (reg6.test(letter)) {
            if (!Vcity.oCity.UVWXYZ[letter]) Vcity.oCity.UVWXYZ[letter] = [];
            Vcity.oCity.UVWXYZ[letter].push(match[1]);
        }
        /* 热门城市 前16条 */
        if(i<16){
            if(!Vcity.oCity.hot['hot']) Vcity.oCity.hot['hot'] = [];
            Vcity.oCity.hot['hot'].push(match[1]);
        }
    }
}
})();
/* 城市HTML模板 */
Vcity._template = [
'<p class="tip">热门城市(支持汉字/拼音)</p>',
    '<ul>',
    '<li class="on">热门城市</li>',
    '<li>A---E</li>',
    '<li>F---J</li>',
    '<li>K---O</li>',
    '<li>P---T</li>',
    '<li>U---Z</li>',
    '</ul>'
    ];

    /* *
     * 城市控件构造函数
     * @CitySelector
     * */

    Vcity.CitySelector = function () {


        this.initialize.apply(this, arguments);
    };

Vcity.CitySelector.prototype = {

    constructor:Vcity.CitySelector,

    /* 初始化 */

    initialize :function (options) {
        var input = options.input;
        this.input = Vcity._m.$('#'+ input);
        this.inputEvent();
    },

    /* *
     * @createWarp
     * 创建城市BOX HTML 框架
     * */

    createWarp:function(){


                   var inputPos = Vcity._m.getPos(this.input);
                   var div = this.rootDiv = document.createElement('div');
                   var that = this;

                   // 设置DIV阻止冒泡
                   Vcity._m.on(this.rootDiv,'click',function(event){
                       Vcity._m.stopPropagation(event);
                   });

                   // 设置点击文档隐藏弹出的城市选择框
                   Vcity._m.on(document, 'click', function (event) {
                       event = Vcity._m.getEvent(event);
                       var target = Vcity._m.getTarget(event);
                       if(target == that.input) return false;
                       //console.log(target.className);
                       if (that.cityBox)Vcity._m.addClass('hide', that.cityBox);
                       if (that.ul)Vcity._m.addClass('hide', that.ul);
                       if(that.myIframe)Vcity._m.addClass('hide',that.myIframe);
                   });
                   div.className = 'citySelector';
                   div.style.position = 'absolute';
                   div.style.left = inputPos.left + 'px';
                   div.style.top = inputPos.bottom + 'px';
                   div.style.zIndex = 999999;

                   // 判断是否IE6，如果是IE6需要添加iframe才能遮住SELECT框
                   var isIe = (document.all) ? true : false;
                   var isIE6 = this.isIE6 = isIe && !window.XMLHttpRequest;
                   if(isIE6){
                       var myIframe = this.myIframe =  document.createElement('iframe');
                       myIframe.frameborder = '0';
                       myIframe.src = 'about:blank';
                       myIframe.style.position = 'absolute';
                       myIframe.style.zIndex = '-1';
                       this.rootDiv.appendChild(this.myIframe);
                   }

                   var childdiv = this.cityBox = document.createElement('div');
                   childdiv.className = 'cityBox';
                   childdiv.id = 'cityBox';
                   childdiv.innerHTML = Vcity._template.join('');
                   var hotCity = this.hotCity =  document.createElement('div');
                   hotCity.className = 'hotCity';
                   childdiv.appendChild(hotCity);
                   div.appendChild(childdiv);
                   this.createHotCity();
               },

    /* *
     * @createHotCity
     * TAB下面DIV：hot,a-h,i-p,q-z 分类HTML生成，DOM操作
     * {HOT:{hot:[]},ABCDEFGH:{a:[1,2,3],b:[1,2,3]},IJKLMNOP:{},QRSTUVWXYZ:{}}
     **/

    createHotCity:function(){
                      var odiv,odl,odt,odd,odda=[],str,key,ckey,sortKey,regEx = Vcity.regEx,
                      oCity = Vcity.oCity;
                      for(key in oCity){
                          odiv = this[key] = document.createElement('div');
                          // 先设置全部隐藏hide
                          odiv.className = key + ' ' + 'cityTab hide';
                          sortKey=[];
                          for(ckey in oCity[key]){
                              sortKey.push(ckey);
                              // ckey按照ABCDEDG顺序排序
                              sortKey.sort();
                          }
                          for(var j=0,k = sortKey.length;j<k;j++){
                              odl = document.createElement('dl');
                              odt = document.createElement('dt');
                              odd = document.createElement('dd');
                              odt.innerHTML = sortKey[j] == 'hot'?'&nbsp;':sortKey[j];
                              odda = [];
                              for(var i=0,n=oCity[key][sortKey[j]].length;i<n;i++){
                                  str = '<a href="#">' + oCity[key][sortKey[j]][i] + '</a>';
                                  odda.push(str);
                              }
                              odd.innerHTML = odda.join('');
                              odl.appendChild(odt);
                              odl.appendChild(odd);
                              odiv.appendChild(odl);
                          }

                          // 移除热门城市的隐藏CSS
                          Vcity._m.removeClass('hide',this.hot);
                          this.hotCity.appendChild(odiv);
                      }
                      document.body.appendChild(this.rootDiv);
                      /* IE6 */
                      this.changeIframe();

                      this.tabChange();
                      this.linkEvent();
                  },

    /* *
     *  tab按字母顺序切换
     *  @ tabChange
     * */

    tabChange:function(){
                  var lis = Vcity._m.$('li',this.cityBox);
                  var divs = Vcity._m.$('div',this.hotCity);
                  var that = this;
                  for(var i=0,n=lis.length;i<n;i++){
                      lis[i].index = i;
                      lis[i].onclick = function(){
                          for(var j=0;j<n;j++){
                              Vcity._m.removeClass('on',lis[j]);
                              Vcity._m.addClass('hide',divs[j]);
                          }
                          Vcity._m.addClass('on',this);
                          Vcity._m.removeClass('hide',divs[this.index]);
                          /* IE6 改变TAB的时候 改变Iframe 大小*/
                          that.changeIframe();
                      };
                  }
              },

    /* *
     * 城市LINK事件
     *  @linkEvent
     * */

    linkEvent:function(){
                  var links = Vcity._m.$('a',this.hotCity);
                  var that = this;
                  for(var i=0,n=links.length;i<n;i++){
                      links[i].onclick = function(){
                          that.input.value = this.innerHTML;
                          Vcity._m.addClass('hide',that.cityBox);
                          /* 点击城市名的时候隐藏myIframe */
                          Vcity._m.addClass('hide',that.myIframe);
                      }
                  }
              },

    /* *
     * INPUT城市输入框事件
     * @inputEvent
     * */

    inputEvent:function(){
                   var that = this;
                   Vcity._m.on(this.input,'click',function(event){
                       event = event || window.event;
                       if(!that.cityBox){
                           that.createWarp();
                       }else if(!!that.cityBox && Vcity._m.hasClass('hide',that.cityBox)){
                           // slideul 不存在或者 slideul存在但是是隐藏的时候 两者不能共存
                           if(!that.ul || (that.ul && Vcity._m.hasClass('hide',that.ul))){
                               Vcity._m.removeClass('hide',that.cityBox);

                               /* IE6 移除iframe 的hide 样式 */
                               //alert('click');
                               Vcity._m.removeClass('hide',that.myIframe);
                               that.changeIframe();
                           }
                       }
                   });
                   Vcity._m.on(this.input,'focus',function(){
                       that.input.select();
                       if(that.input.value == '出发地') that.input.value = '';
                   });
                   Vcity._m.on(this.input,'blur',function(){
                       if(that.input.value == '') that.input.value = '';
                   });
                   Vcity._m.on(this.input,'keyup',function(event){
                       event = event || window.event;
                       var keycode = event.keyCode;
                       Vcity._m.addClass('hide',that.cityBox);
                       that.createUl();

                       /* 移除iframe 的hide 样式 */
                       Vcity._m.removeClass('hide',that.myIframe);

                       // 下拉菜单显示的时候捕捉按键事件
                       if(that.ul && !Vcity._m.hasClass('hide',that.ul) && !that.isEmpty){
                           that.KeyboardEvent(event,keycode);
                       }
                   });
               },

    /* *
     * 生成下拉选择列表
     * @ createUl
     * */

    createUl:function () {
                 //console.log('createUL');
                 var str;
                 var value = Vcity._m.trim(this.input.value);
                 // 当value不等于空的时候执行
                 if (value !== '') {
                     var reg = new RegExp("^" + value + "|\\|" + value, 'gi');
                     // 此处需设置中文输入法也可用onpropertychange
                     var searchResult = [];
                     for (var i = 0, n = Vcity.allCity.length; i < n; i++) {
                         if (reg.test(Vcity.allCity[i])) {
                             var match = Vcity.regEx.exec(Vcity.allCity[i]);
                             if (searchResult.length !== 0) {
                                 str = '<li><b class="cityname">' + match[1] + '</b><b class="cityspell">' + match[2] + '</b></li>';
                             } else {
                                 str = '<li class="on"><b class="cityname">' + match[1] + '</b><b class="cityspell">' + match[2] + '</b></li>';
                             }
                             searchResult.push(str);
                         }
                     }
                     this.isEmpty = false;
                     // 如果搜索数据为空
                     if (searchResult.length == 0) {
                         this.isEmpty = true;
                         str = '<li class="empty">对不起，没有找到数据 "<em>' + value + '</em>"</li>';
                         searchResult.push(str);
                     }
                     // 如果slideul不存在则添加ul
                     if (!this.ul) {
                         var ul = this.ul = document.createElement('ul');
                         ul.className = 'cityslide';
                         this.rootDiv && this.rootDiv.appendChild(ul);
                         // 记录按键次数，方向键
                         this.count = 0;
                     } else if (this.ul && Vcity._m.hasClass('hide', this.ul)) {
                         this.count = 0;
                         Vcity._m.removeClass('hide', this.ul);
                     }
                     this.ul.innerHTML = searchResult.join('');

                     /* IE6 */                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          this.changeIframe();

                     // 绑定Li事件
                     this.liEvent();
                 }else{
                     Vcity._m.addClass('hide',this.ul);
                     Vcity._m.removeClass('hide',this.cityBox);

                     Vcity._m.removeClass('hide',this.myIframe);

                     this.changeIframe();
                 }
             },

    /* IE6的改变遮罩SELECT 的 IFRAME尺寸大小 */
    changeIframe:function(){
                     if(!this.isIE6)return;
                     this.myIframe.style.width = this.rootDiv.offsetWidth + 'px';
                     this.myIframe.style.height = this.rootDiv.offsetHeight + 'px';
                 },

    /* *
     * 特定键盘事件，上、下、Enter键
     * @ KeyboardEvent
     * */

    KeyboardEvent:function(event,keycode){
                      var lis = Vcity._m.$('li',this.ul);
                      var len = lis.length;
                      switch(keycode){
                          case 40: //向下箭头↓
                              this.count++;
                              if(this.count > len-1) this.count = 0;
                              for(var i=0;i<len;i++){
                                  Vcity._m.removeClass('on',lis[i]);
                              }
                              Vcity._m.addClass('on',lis[this.count]);
                              break;
                          case 38: //向上箭头↑
                              this.count--;
                              if(this.count<0) this.count = len-1;
                              for(i=0;i<len;i++){
                                  Vcity._m.removeClass('on',lis[i]);
                              }
                              Vcity._m.addClass('on',lis[this.count]);
                              break;
                          case 13: // enter键
                              this.input.value = Vcity.regExChiese.exec(lis[this.count].innerHTML)[0];
                              Vcity._m.addClass('hide',this.ul);
                              Vcity._m.addClass('hide',this.ul);
                              /* IE6 */
                              Vcity._m.addClass('hide',this.myIframe);
                              break;
                          default:
                              break;
                      }
                  },

    /* *
     * 下拉列表的li事件
     * @ liEvent
     * */

    liEvent:function(){
                var that = this;
                var lis = Vcity._m.$('li',this.ul);
                for(var i = 0,n = lis.length;i < n;i++){
                    Vcity._m.on(lis[i],'click',function(event){
                        event = Vcity._m.getEvent(event);
                        var target = Vcity._m.getTarget(event);
                        that.input.value = Vcity.regExChiese.exec(target.innerHTML)[0];
                        Vcity._m.addClass('hide',that.ul);
                        /* IE6 下拉菜单点击事件 */
                        Vcity._m.addClass('hide',that.myIframe);
                    });
                    Vcity._m.on(lis[i],'mouseover',function(event){
                        event = Vcity._m.getEvent(event);
                        var target = Vcity._m.getTarget(event);
                        Vcity._m.addClass('on',target);
                    });
                    Vcity._m.on(lis[i],'mouseout',function(event){
                        event = Vcity._m.getEvent(event);
                        var target = Vcity._m.getTarget(event);
                        Vcity._m.removeClass('on',target);
                    })
                }
            }
};
var test=new Vcity.CitySelector({input:'fromcity'});
var test2=new Vcity.CitySelector({input:'tocity'});

