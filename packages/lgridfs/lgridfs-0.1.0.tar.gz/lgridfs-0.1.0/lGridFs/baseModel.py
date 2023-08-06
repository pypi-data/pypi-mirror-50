"""

试图采用mongodb 最原始的，文件流的上传下载处理方式,gridfs

但是在实际的文档阅读中发现，这种使用方式不支持分片上传的功能(即使用方式上，对比web端通过分片的方式上传)。

原本的方式只能通过流的方式来上传下载

先准备使用形如注册，分片上传，结束上传

同理，如果是文件流的形式发送到这个封装中，也是可以实现写入的

"""
from typing import Union
from datetime import datetime

from bson import ObjectId
from pymongo.results import InsertOneResult
from motor.motor_asyncio import AsyncIOMotorCollection,AsyncIOMotorDatabase,AsyncIOMotorCursor


__author__ = "北月" # or bigpangl

class MongodbFile(object):
    """

    模拟文件的追加写入

    一种是，允许分片上传，不控制片的多少。

    另一种，直接写入整个文件的二进制，但是要自行负责分片。

    """
    def __init__(self,fileid:Union[bytes,str,ObjectId],_files:AsyncIOMotorCollection,_chunks:AsyncIOMotorCollection,status:bool):
        if isinstance(fileid,bytes):
            fileid=fileid.decode("utf-8")
        if isinstance(fileid,str):
            fileid = ObjectId(fileid)
        self.fileid:ObjectId = fileid
        self._files:AsyncIOMotorCollection = _files
        self._chunks:AsyncIOMotorCollection = _chunks

        self.status = status

    async def write(self,index:int,content:bytes)->bool:
        """
        追加写入,content 的大小不能超过16M，原生的gridfs 系统是采用255K 的数据来分片
        :param index:
        :param content:
        :return:
        """
        if len(content)>1024*1024*16:
            raise Exception("单行中写入的数据量太大")
        if not self.status:
            await self._chunks.insert_one({"files_id":self.fileid,"n":index,"data":content})
            return True
        else:
            raise Exception("文件已经上传完毕，不允许上传")

    async def finish_upload(self):
        """
        结束上传时将修改文件的状态
        :return:
        """
        await self._files.find_one_and_update({"_id": self.fileid},{"$set":{"status":True}})
        self.status = True

    def read_like_stream(self):
        self.cursor:AsyncIOMotorCursor = self._chunks.find({"files_id":self.fileid}).sort("n", 1)
        return self

    async def get_by_n(self,index:int)->bytes:
        """
        根据需要来获取数据
        :param index:
        :return:
        """
        data_use = "".encode("utf-8")
        data = await self._chunks.find_one({"files_id":self.fileid,"n":index})
        if data:
            data_use = data.get("data",data_use)
        return data_use

    def __aiter__(self):
        return self

    async def __anext__(self):
        await self.cursor.fetch_next
        data:dict = self.cursor.next_object()
        if data:
            data_use = data.get("data","".encode("utf-8"))
            return data_use
        else:
            raise StopAsyncIteration

class PersonGridFs(object):
    """

    文件系统，对接mongodb的注册，上传部分

    """
    def __init__(self,db:AsyncIOMotorDatabase,bucket_name=None):
        self._db = db
        if bucket_name is None:
            bucket_name = "fs"
        self._files = db[f"{bucket_name}.files"]
        self._chunks = db[f"{bucket_name}.chunks"]

    async def registe_file(self,filename:str,length:int)->ObjectId:
        """
        注册文件
        :param filename:
        :param length:
        :return:
        """
        result:InsertOneResult = await self._files.insert_one({"filename":filename,"length":length,"uploadDate":datetime.now(),"status":False})
        return result.inserted_id

    async def delete_fileid(self,fileid:ObjectId)->bool:
        """
        删除文件
        :param fileid:
        :return:
        """
        assert isinstance(fileid,ObjectId),Exception("fileid should be ObjectId type")
        await self._chunks.delete_many({"files_id":fileid})
        await self._files.delete_many({"_id":fileid})
        return True

    async def get_file(self,fileid:Union[bytes,str,ObjectId])->MongodbFile:
        """
        获取文件数据
        :param fileid:
        :return:
        """
        if isinstance(fileid,bytes):
            fileid = fileid.decode("utf-8")
        if isinstance(fileid,str):
            fileid = ObjectId(fileid)
        data = await self._files.find_one({"_id":fileid})
        if not data:
            raise Exception(f"ID{str(fileid)},尚未注册到mongodb 中")
        mf = MongodbFile(fileid,self._files,self._chunks,data.get("status",False))
        return mf
