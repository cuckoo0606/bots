#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
import pymongo
from bson import ObjectId
from framework.data.mongo import db, Document, DBRef


def check(user_id):
    '''
        用户: 1688013【钟羽生】
        relation:/admin/5891979913485105cfe0c85f/5891994013485105cfe0c875/589199f813485105cfe0c87d/5895390313485105cfe0fcb4/5897ddbe13485105cfe13442

        查询红利(不算佣金)
        有显示两次扣或加, 也有没有记录的(因为订单相同, 算在他人帐上)
    '''
    # user = db.user.find_one({ '_id': ObjectId(user_id) })
    # relation = user.relation + '/'

    # where = {}
    # where['relation'] = {'$regex': relation}
    # where['status'] = 110
    # where['created'] = {"$lt" : datetime.datetime(2017,02,25)}

    # # 所有下级单号
    # orders = db.order.find(where)
    # print "所有下级的下单总数"
    # print orders.count()

    # # 记录重复的单号与id
    # li = []
    # for i in orders:
    #     if db.order.count({ "no": i.no }) > 1:
    #         li.append({ "_id": i._id, "no": i.no })

    # # 重复的订单
    # print li


    li =[
        {'_id': ObjectId('58aeb3de1633ee084f604e05'), 'no': 'R20170223060518867'},
        {'_id': ObjectId('58aeb2870cc9d7764ecb0a86'), 'no': 'R20170223055935894'},
        {'_id': ObjectId('58adb50dbb4b27694e906bb8'), 'no': 'R20170222115805783'},
        {'_id': ObjectId('58ad7c78d305bc8c4e6998ef'), 'no': 'R20170222075640809'},
        {'_id': ObjectId('58ac62b2bb4b27694e8fb4a2'), 'no': 'R20170221115426599'},
        {'_id': ObjectId('58ac56ee5c8f30334e10ebb0'), 'no': 'R20170221110414983'},
        {'_id': ObjectId('58ac2422d944f4a64e8ebee3'), 'no': 'R20170221072730205'},
        {'_id': ObjectId('58ac00b6eab630e04ebdfabe'), 'no': 'R20170221045622322'},
        {'_id': ObjectId('58aae5f41633ee084f5e3833'), 'no': 'R20170220084956006'}, 
        {'_id': ObjectId('58aa80fbfbe15f294ec653a6'), 'no': 'R20170220013907328'},
        {'_id': ObjectId('58aa77f18e9a38864e919142'), 'no': 'R20170220010033592'},
        {'_id': ObjectId('58aa2f9cfbe15f294ec625ab'), 'no': 'R20170220075156183'},
        {'_id': ObjectId('58a96c26f9cf34ec0e86de2d'), 'no': 'R20170219055758736'},
        {'_id': ObjectId('58a9311a59b8c7960e59dcde'), 'no': 'R20170219014602465'},
        {'_id': ObjectId('58a915d145b74eaf0e22f9aa'), 'no': 'R20170219114937962'},
        {'_id': ObjectId('58a900d8617434f20e5773bd'), 'no': 'R20170219102008045'},
        {'_id': ObjectId('58a8884aae391c750fef0544'), 'no': 'R20170219014546409'},
        {'_id': ObjectId('58a87c9545b74eaf0e22e555'), 'no': 'R20170219125549543'},
        {'_id': ObjectId('58a8773759b8c7960e59be6f'), 'no': 'R20170219123255047'},
        {'_id': ObjectId('58a83faeae391c750feef314'), 'no': 'R20170218083558419'},
        {'_id': ObjectId('58a83d0d586567a90e3380d9'), 'no': 'R20170218082445333'},
        {'_id': ObjectId('58a718260c936b0177ace0c6'), 'no': 'R20170217113502234'},
        {'_id': ObjectId('58a71605bd599fd3310bb629'), 'no': 'R20170217112557248'},
        {'_id': ObjectId('58a6ff39c6d8795b777a9a99'), 'no': 'R20170217094841678'},
        {'_id': ObjectId('58a66dbc06229a132fb38fc2'), 'no': 'R20170217112756522'},
        {'_id': ObjectId('58a65229a815c94522633a3c'), 'no': 'R20170217093017536'},
        {'_id': ObjectId('58a5234335ed5a6e5412ee17'), 'no': 'R20170216115755571'},
        {'_id': ObjectId('58a5076b1938e468547a4e53'), 'no': 'R20170216095907265'},
        {'_id': ObjectId('58a502c82dfe4cb055aebe79'), 'no': 'R20170216093920474'},
        {'_id': ObjectId('58a4ff1c252025a755c7add7'), 'no': 'R20170216092340440'},
        {'_id': ObjectId('58a48eda8a646884544c7767'), 'no': 'R20170216012442326'},
        {'_id': ObjectId('58a446dcb3d971b27977bcb9'), 'no': 'R20170215081732764'},
        {'_id': ObjectId('58a3932c039aab0f22d9c7d8'), 'no': 'R20170215073052027'},
        {'_id': ObjectId('58a161d6667aca247c7d9d0b'), 'no': 'R20170213033550958'},
        {'_id': ObjectId('58a13955e4cb69c17c2db603'), 'no': 'R20170213124301657'},
        {'_id': ObjectId('58a129565a68d68f7ba89086'), 'no': 'R20170213113446517'},
        {'_id': ObjectId('58a119e76b1ce9b30717467e'), 'no': 'R20170213102855528'},
        {'_id': ObjectId('589ddee96b1ce9b307171b1f'), 'no': 'R20170210114025553'}]

    for i in li:
        # 在删除的重复books表里查找(总共3W8条数据)
        books_bak = db.books_bak.find({ "type": 9, "args": i['_id'] })
        
        try:
            # 如果有结果, 就是相同订单重复计算
            if books_bak.count() > 0:
                for b in books_bak:
                    if b.user == ObjectId(user_id):
                        print '重复计算的资金表: {0}, 需要调整{1}元, 订单id: {2}, 单号: {3}'.format(str(b._id), b.amount*-1, i['_id'], i['no'])
                    else:
                        print '其他用户的资金表: {0}'.format(str(b._id))
            else:
                books = db.books.find({ "type": 9, "args": i['_id'] })
                if books.count() > 0:
                    print "重点订单: 订单id: {0}, 单号: {1}".format(i['_id'], i['no'])
                else:
                    print '没有计算的订单id: {0}, 单号: {1}'.format(str(i['_id']), i['no'])
                    # 将订单设置为未计算
                    # db.books.update({ "_id": i['_id'] }, {"$unset": { "position_process":1 }})
        except Exception, e:
            import pdb
            pdb.set_trace()
            print e


if __name__ == '__main__':
    user_id = "5897ddbe13485105cfe13442"
    check(user_id)

'''
重复计算的资金表: 58aeb43285b02a3cd8dc1d3b, 需要调整25.6元, 订单id: 58aeb3de1633ee084f604e05, 单号: R20170223060518867
重复计算的资金表: 58aeb2e085b02a3cd8dc1740, 需要调整8.0元, 订单id: 58aeb2870cc9d7764ecb0a86, 单号: R20170223055935894
没有计算的订单id: 58adb50dbb4b27694e906bb8, 单号: R20170222115805783   -10
没有计算的订单id: 58ad7c78d305bc8c4e6998ef, 单号: R20170222075640809   -20
没有计算的订单id: 58ac62b2bb4b27694e8fb4a2, 单号: R20170221115426599   -10
没有计算的订单id: 58ac56ee5c8f30334e10ebb0, 单号: R20170221110414983   80
没有计算的订单id: 58ac2422d944f4a64e8ebee3, 单号: R20170221072730205   8
没有计算的订单id: 58ac00b6eab630e04ebdfabe, 单号: R20170221045622322   -10
没有计算的订单id: 58aae5f41633ee084f5e3833, 单号: R20170220084956006    0
没有计算的订单id: 58aa80fbfbe15f294ec653a6, 单号: R20170220013907328   40
重复计算的资金表: 58aa784413485122c3d2960e, 需要调整-20.0元, 订单id: 58aa77f18e9a38864e919142, 单号: R20170220010033592
没有计算的订单id: 58aa2f9cfbe15f294ec625ab, 单号: R20170220075156183   -100
其他用户的资金表: 58a96c6d13485122c3d0620c
重复计算的资金表: 58a96c6d13485122c3d0620d, 需要调整2.0元, 订单id: 58a96c26f9cf34ec0e86de2d, 单号: R20170219055758736
没有计算的订单id: 58a9311a59b8c7960e59dcde, 单号: R20170219014602465    8
重复计算的资金表: 58a9162013485122c3cf763b, 需要调整-500.0元, 订单id: 58a915d145b74eaf0e22f9aa, 单号: R20170219114937962
重复计算的资金表: 58a9a9dd13485122c3d104a8, 需要调整400.0元, 订单id: 58a900d8617434f20e5773bd, 单号: R20170219102008045
其他用户的资金表: 58a9315113485122c3cfba08
重复计算的资金表: 58a9315113485122c3cfba09, 需要调整-78.0元, 订单id: 58a8884aae391c750fef0544, 单号: R20170219014546409
重复计算的资金表: 58a925a513485122c3cf9d34, 需要调整80.0元, 订单id: 58a87c9545b74eaf0e22e555, 单号: R20170219125549543
重复计算的资金表: 58a9204213485122c3cf8e60, 需要调整80.0元, 订单id: 58a8773759b8c7960e59be6f, 单号: R20170219123255047
重复计算的资金表: 58a9204213485122c3cf8e70, 需要调整80.0元, 订单id: 58a8773759b8c7960e59be6f, 单号: R20170219123255047
重复计算的资金表: 58a83ff113485122c3ce18e7, 需要调整-200.0元, 订单id: 58a83faeae391c750feef314, 单号: R20170218083558419
没有计算的订单id: 58a83d0d586567a90e3380d9, 单号: R20170218082445333   16
重复计算的资金表: 58a7187013485122c3cbede4, 需要调整-19.0元, 订单id: 58a718260c936b0177ace0c6, 单号: R20170217113502234
没有计算的订单id: 58a71605bd599fd3310bb629, 单号: R20170217112557248   -30
没有计算的订单id: 58a6ff39c6d8795b777a9a99, 单号: R20170217094841678   下单失败(5000)
没有计算的订单id: 58a66dbc06229a132fb38fc2, 单号: R20170217112756522   -1700
重点订单: 订单id: 58a65229a815c94522633a3c, 单号: R20170217093017536   -10
其他用户的资金表: 58a5238d13485170df3913b2
重复计算的资金表: 58a5238d13485170df3913a9, 需要调整8.0元, 订单id: 58a5234335ed5a6e5412ee17, 单号: R20170216115755571
没有计算的订单id: 58a5076b1938e468547a4e53, 单号: R20170216095907265   -2000
没有计算的订单id: 58a502c82dfe4cb055aebe79, 单号: R20170216093920474   -100
没有计算的订单id: 58a4ff1c252025a755c7add7, 单号: R20170216092340440    0
没有计算的订单id: 58a48eda8a646884544c7767, 单号: R20170216012442326   -100
没有计算的订单id: 58a446dcb3d971b27977bcb9, 单号: R20170215081732764   -100
重复计算的资金表: 58a43d2d13485176f57f6298, 需要调整80.0元, 订单id: 58a3932c039aab0f22d9c7d8, 单号: R20170215073052027
没有计算的订单id: 58a161d6667aca247c7d9d0b, 单号: R20170213033550958   -10
重复计算的资金表: 58a13996134851066343c7dd, 需要调整1600.0元, 订单id: 58a13955e4cb69c17c2db603, 单号: R20170213124301657
重复计算的资金表: 58a129981348510663439a43, 需要调整8.0元, 订单id: 58a129565a68d68f7ba89086, 单号: R20170213113446517
重复计算的资金表: 58a1c2eb1348510663459f7d, 需要调整80.0元, 订单id: 58a119e76b1ce9b30717467e, 单号: R20170213102855528
没有计算的订单id: 589ddee96b1ce9b307171b1f, 单号: R20170210114025553   -980
'''