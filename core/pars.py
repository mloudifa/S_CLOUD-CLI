from urllib.parse import urlparse, parse_qs

def pars_url(url) -> dict:
    url_res = urlparse(url)
    domain = url_res.netloc.lower()
    path = url_res.path.lower()
    
    if "soundcloud.com" in domain:
        if "sets" in path:
            return {"type":"URL", "platform":"SoundCloud", "S_TYPE":"Playlist", "content": url}
        else:
            return {"type":"URL", "platform":"SoundCloud", "S_TYPE":"Single", "content": url}

    return {"type":"INVALID_PLATFORM", "url": url}
