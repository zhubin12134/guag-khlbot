

class URLGenerator:
    """
    kook_api_base_url = URLGenerator()
    kook_api_v3 = kook_api_base_url.v3
    print(kook_api_v3)  # 输出: https://www.kookapp.cn/api/v3
    print(kook_api_v3.products.info)
    assert isinstance(kook_api_v3, str)
    """

    __version__ = "v3"
    BASE_URL = 'https://www.kookapp.cn'


    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(f"'URLGenerator' object has no attribute '{name}'")
        
        if "_" in name:
            name = name.replace("_", "-")

        if name == 'end':
            return URLGenerator(f'{self.url}/')

        if name == 'str':
            return str(URLGenerator(f'{self.url}'))
        
        if name == 'api':
            return URLGenerator(f'{self.url}/api/v3')

        new_url = f'{self.url}/{name}'
        return URLGenerator(new_url)

    def __init__(self, url=None):
        self.url = url or self.BASE_URL

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url
    
    
kook_api = URLGenerator()

    
if __name__ == '__main__':
    url = kook_api.api.gateway.index
    print(url)  # 输出: https://www.kookapp.cn/api/v3
    print(url.products.info)
    print(type(url.str) is str)
    # assert isinstance(kook_api_v3, str)
    

