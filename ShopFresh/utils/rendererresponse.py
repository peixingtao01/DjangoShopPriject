from rest_framework.renderers import JSONRenderer

class customrenderer(JSONRenderer):
    # 重写这个类
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data,dict):
                # 如果请求是字典
                msg1 = data.pop('msg','请求成功')#删除
                # msg:'qingqiu'，设置了一个新的
                # 这是本身有一个msg的键值对
                code = data.pop('code',0)
                # 删除字典中这两个东西
            else:
                msg1 = '请求bu成功'
                code = 0
            ret = {
                'msg':msg1,
                'code':code,
                'author':'duoyan3wei',
                'data':data
            }
            return super().render(ret,accepted_media_type,renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)