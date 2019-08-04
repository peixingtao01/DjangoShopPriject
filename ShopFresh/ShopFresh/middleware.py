from django.utils.deprecation import MiddlewareMixin
# 中间件的元类，所有自定义的中间件
class MiddlewareTest(MiddlewareMixin):
    def process_request(self,request):
        print('这是process_request')
    def process_view(self,request,view_func,view_args,view_kwargs):
        print('这是process_view')
    def process_exceptions(self,request,exception):
        print('这是process_exceptions')
    def process_template_response(self,request,response):
        print('这是process_template_response')
        return response
    def process_response(self,request,response):
        print('这是process_response')
        return response