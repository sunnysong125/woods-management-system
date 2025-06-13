"""
自定義中間件
"""
import logging

logger = logging.getLogger(__name__)

class CSRFDebugMiddleware:
    """CSRF調試中間件"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 記錄請求信息
        if request.method == 'POST':
            logger.info(f"POST請求到: {request.path}")
            logger.info(f"Origin: {request.META.get('HTTP_ORIGIN', 'None')}")
            logger.info(f"Referer: {request.META.get('HTTP_REFERER', 'None')}")
            logger.info(f"Host: {request.META.get('HTTP_HOST', 'None')}")
            logger.info(f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'None')}")
            logger.info(f"CSRF Token in headers: {request.META.get('HTTP_X_CSRFTOKEN', 'None')}")
            
            # 檢查cookies
            csrf_cookie = request.COOKIES.get('csrftoken', 'None')
            logger.info(f"CSRF Token in cookies: {csrf_cookie}")
            
            # 檢查POST數據中的CSRF token
            csrf_post = request.POST.get('csrfmiddlewaretoken', 'None')
            logger.info(f"CSRF Token in POST data: {csrf_post}")

        response = self.get_response(request)
        return response 