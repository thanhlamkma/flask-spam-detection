from enum import Enum
import aioredis
import json

class ModelAl(Enum):    
    NaiveBayes= 0
    SupportVectorMachine =1
    
class VectorAl(Enum):
    CountVectorizier =  0
    TfidfVectorizier = 1


def isnumber(value):
    return True if value < 2 else False 

async def check_key_exists():
    # Create a connection to Redis
    redis = await aioredis.from_url('redis://localhost:6379')

    # Search for keys that match the pattern
    val = await redis.get("ML_Setting")

    # Close the Redis connection
    await redis.close()
    try:

        key = json.loads(val)
        mod = key["mode-type"]
        vec = key ['vector-type']
        if isnumber(mod) and isnumber(vec):
            return True
    except:    
        return False

async def getcurrent():
    settingls = ['Navie Bayes', 'Support Vector Machine']
    try:
        redis = await aioredis.from_url('redis://localhost:6379')
        mod = await redis.get("ML_Setting")
        await redis.close()
        mod = json.loads(mod)        
        modtype = mod["mode-type"]
        vector = mod["vector-type"] #co the dung hoac khong    
        return settingls[modtype]
    except :
        return None
    
async def setcurrent(mod):
    try:
        if int(mod) > 2 :
            return 0       
        vec = 1    
        redis = await aioredis.from_url('redis://localhost:6379')
        setmode = json.dumps({"mode-type":ModelAl(mod).value,
                            "vector-type":VectorAl(vec).value})
        await redis.set("ML_Setting",setmode)
        await redis.close()
        return True
    except:
        return False


