import redis
import traceback
from workCms.status_restful_api import HttpCode
from workCms.core.conf import redis_host, redis_dbName_num, redis_passwd, redis_port


class Redis_str(object):
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_dbName_num, password=redis_passwd)

    # def __init__(self, **kwargs):
    #     self.k = kwargs["k"]
    #     self.v = kwargs["v"]
    #     self.k_tiem = kwargs["k_time"]
    def __init__(self, k=None, v=None, k_time=None):
        self.k = k
        self.v = v
        self.k_tiem = k_time

    def r_set(self):
        try:
            Redis_str.r.set(self.k, self.v)
            return HttpCode.success
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_get(self):
        try:
            rel = Redis_str.r.get(self.k)
            return rel.decode('utf-8')
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_append(self):
        try:
            Redis_str.r.append(self.k, self.v)
            return HttpCode.success
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_del(self):
        try:
            Redis_str.r.delete(self.k)
            return HttpCode.success
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_strlen(self):
        try:
            rel = Redis_str.r.strlen(self.k)
            return rel
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_setex(self):
        try:
            Redis_str.r.setex(self.k, self.k_tiem, self.v)
            return HttpCode.success
        except:
            print(traceback.format_exc())
            return HttpCode.serverError


class Redis_list(Redis_str):

    def r_lpush(self, v):
        try:
            Redis_str.r.lpush(self.k, v)
            return HttpCode.success
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_lindex(self, i):
        try:
            rel = Redis_str.r.lindex(self.k, i)
            return rel.decode('utf-8')
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_lpop(self):
        try:
            Redis_str.r.lpop(self.k)
            return HttpCode.success
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_lrange(self, s, end):
        v = []
        try:
            rel = Redis_str.r.lrange(self.k, s, end)
            for i in rel:
                v.append(i.decode('utf-8'))
            return v
        except:
            print(traceback.format_exc())
            return HttpCode.serverError

    def r_keyAll(self):
        try:
            rel = len(Redis_str.r.keys())
            return rel
        except:
            print(traceback.format_exc())
            return HttpCode.serverError
