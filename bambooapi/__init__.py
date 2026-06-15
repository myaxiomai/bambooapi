import json
import mimetypes
import os
import re
from urllib.parse import parse_qs


BAMBOO_DOCS_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ - API docs</title>
<script>
var _t=localStorage.getItem('bam-theme');
if(_t) document.documentElement.setAttribute('data-theme',_t);
</script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#fff;--bg2:#f7f6f2;--bg3:#ededea;
  --txt:#1a1a1a;--txt2:#666;--txt3:#999;
  --bdr:rgba(0,0,0,0.08);--bdr2:rgba(0,0,0,0.14);
  --green:#2E9D45;--r:8px;
  --get-t:#E6F1FB;--post-t:#EAF3DE;--put-t:#FAEEDA;--del-t:#FCEBEB;
  --get-b:#185FA5;--post-b:#3B6D11;--put-b:#854F0B;--del-b:#A32D2D;
  --ok-bg:#EAF3DE;--ok-txt:#27500A;
  --lk:#185FA5;
}
@media(prefers-color-scheme:dark){:root{
  --bg:#1e1e1e;--bg2:#252525;--bg3:#2c2c2c;
  --txt:#f0efeb;--txt2:#999;--txt3:#666;
  --bdr:rgba(255,255,255,0.08);--bdr2:rgba(255,255,255,0.15);
  --get-t:#0c2240;--post-t:#162408;--put-t:#2a1804;--del-t:#2a0c0c;
  --ok-bg:#162408;--ok-txt:#97C459;--lk:#85B7EB;
}}
[data-theme=light]{
  --bg:#fff;--bg2:#f7f6f2;--bg3:#ededea;--txt:#1a1a1a;--txt2:#666;--txt3:#999;
  --bdr:rgba(0,0,0,0.08);--bdr2:rgba(0,0,0,0.14);
  --get-t:#E6F1FB;--post-t:#EAF3DE;--put-t:#FAEEDA;--del-t:#FCEBEB;
  --ok-bg:#EAF3DE;--ok-txt:#27500A;--lk:#185FA5;
}
[data-theme=dark]{
  --bg:#1e1e1e;--bg2:#252525;--bg3:#2c2c2c;--txt:#f0efeb;--txt2:#999;--txt3:#666;
  --bdr:rgba(255,255,255,0.08);--bdr2:rgba(255,255,255,0.15);
  --get-t:#0c2240;--post-t:#162408;--put-t:#2a1804;--del-t:#2a0c0c;
  --ok-bg:#162408;--ok-txt:#97C459;--lk:#85B7EB;
}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--txt);display:flex;flex-direction:column;height:100vh;overflow:hidden}
header{background:var(--green);height:46px;display:flex;align-items:center;gap:10px;padding:0 16px;flex-shrink:0}
.hl{display:flex;align-items:center;gap:8px}
.htitle{color:#fff;font-size:15px;font-weight:500;letter-spacing:.01em}
.hsub{color:rgba(255,255,255,.6);font-size:12px}
.hr{margin-left:auto;display:flex;align-items:center;gap:8px}
.hpill{background:rgba(255,255,255,.16);color:rgba(255,255,255,.9);font-size:11px;padding:2px 9px;border-radius:20px;font-weight:500}
.hbtn{background:rgba(255,255,255,.16);border:none;color:#fff;font-size:11px;padding:2px 9px;border-radius:20px;cursor:pointer;font-weight:500}
.wrap{display:flex;flex:1;overflow:hidden}
nav{width:200px;min-width:200px;border-right:1px solid var(--bdr);background:var(--bg2);overflow-y:auto;padding:6px 0}
.tile{padding:10px 10px 10px 13px;cursor:pointer;border-left:3px solid transparent;transition:background .12s}
.tile:hover{background:var(--bg3)}
.tile.sel-GET{background:var(--get-t);border-left-color:var(--get-b)}
.tile.sel-POST{background:var(--post-t);border-left-color:var(--post-b)}
.tile.sel-PUT{background:var(--put-t);border-left-color:var(--put-b)}
.tile.sel-DELETE{background:var(--del-t);border-left-color:var(--del-b)}
.tile-top{display:flex;align-items:center;gap:6px;margin-bottom:3px}
.tile-path{font-size:11px;font-family:monospace;color:var(--txt);word-break:break-all;line-height:1.3}
.tile-sum{font-size:11px;color:var(--txt2);line-height:1.4}
main{flex:1;overflow-y:auto;padding:24px 28px}
.dtop{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:10px}
.dpath{display:flex;align-items:center;gap:10px}
.dpathcode{font-size:17px;font-family:monospace;font-weight:500;color:var(--txt)}
.tbtn{font-size:12px;padding:6px 14px;border-radius:var(--r);cursor:pointer;border:1px solid var(--bdr2);background:var(--bg2);color:var(--txt)}
.tbtn.on{background:var(--green);color:#fff;border-color:var(--green)}
.ddesc{font-size:13px;color:var(--txt2);margin-bottom:20px;line-height:1.6}
.slabel{font-size:12px;font-weight:500;color:var(--txt);margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid var(--bdr)}
.prow{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid var(--bdr)}
.pname{font-size:12px;font-family:monospace;color:var(--txt);min-width:90px}
.pill{font-size:11px;padding:1px 7px;border-radius:4px}
.pt{background:var(--bg3);color:var(--txt2)}
.pr-GET{background:#B5D4F4;color:#0C447C}
.pr-POST{background:#C0DD97;color:#27500A}
.pr-PUT{background:#FAC775;color:#633806}
.pr-DELETE{background:#F7C1C1;color:#791F1F}
.pinput{flex:1;font-size:12px;padding:4px 8px;border-radius:4px;border:1px solid var(--bdr2);background:var(--bg);color:var(--txt);font-family:monospace}
.bblock{background:var(--bg2);border-radius:var(--r);padding:10px 14px;font-family:monospace;font-size:12px;color:var(--txt2);line-height:1.8}
textarea.binput{width:100%;font-size:12px;font-family:monospace;padding:10px;border-radius:var(--r);border:1px solid var(--bdr2);background:var(--bg);color:var(--txt);resize:vertical;min-height:90px}
.ebtn{font-size:13px;padding:8px 22px;border-radius:var(--r);cursor:pointer;border:none;font-weight:500;color:#fff;margin-bottom:20px;cursor:pointer}
.ebtn.GET{background:#185FA5}.ebtn.POST{background:#3B6D11}.ebtn.PUT{background:#854F0B}.ebtn.DELETE{background:#A32D2D}
.rsec{border-top:1px solid var(--bdr);padding-top:18px}
.rmeta{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.scode{font-size:12px;font-weight:500;padding:2px 9px;border-radius:4px}
.s2xx{background:var(--ok-bg);color:var(--ok-txt)}
.s4xx{background:#FAEEDA;color:#633806}[data-theme=dark] .s4xx{background:#2a1804;color:#EF9F27}
@media(prefers-color-scheme:dark){.s4xx{background:#2a1804;color:#EF9F27}}
.s5xx{background:#FCEBEB;color:#791F1F}[data-theme=dark] .s5xx{background:#2a0c0c;color:#F09595}
@media(prefers-color-scheme:dark){.s5xx{background:#2a0c0c;color:#F09595}}
.serr{background:#FCEBEB;color:#791F1F}[data-theme=dark] .serr{background:#2a0c0c;color:#F09595}
@media(prefers-color-scheme:dark){.serr{background:#2a0c0c;color:#F09595}}
.rtime{font-size:11px;color:var(--txt3)}
.cblock{background:var(--bg2);border-radius:var(--r);padding:10px 14px;font-family:monospace;font-size:12px;color:var(--txt2);white-space:pre;overflow-x:auto;margin-bottom:12px}
.slb{font-size:11px;color:var(--txt3);margin-bottom:4px}
.sgap{margin-bottom:16px}
.badge{display:inline-block;font-size:11px;font-weight:500;padding:2px 6px;border-radius:4px;letter-spacing:.04em;min-width:46px;text-align:center}
.blg{font-size:12px;padding:4px 10px;min-width:52px}
.GET{background:#185FA5;color:#E6F1FB}
.POST{background:#3B6D11;color:#EAF3DE}
.PUT{background:#854F0B;color:#FAEEDA}
.DELETE{background:#A32D2D;color:#FCEBEB}
</style>
</head>
<body>
<header>
  <div class="hl">
    <svg width="26" height="26" viewBox="0 0 100 100" aria-hidden="true">
      <circle cx="50" cy="50" r="37" fill="none" stroke="white" stroke-width="9"/>
    </svg>
    <span class="htitle">__TITLE__</span>
    <span class="hsub">API docs</span>
  </div>
  <div class="hr">
    <span class="hpill">v__VERSION__</span>
    <button class="hbtn" id="thbtn" onclick="toggleTheme()">Light</button>
  </div>
</header>
<div class="wrap">
  <nav id="sidebar"></nav>
  <main id="detail"><p style="padding:24px;color:var(--txt2);">Loading...</p></main>
</div>
<script>
var routes=[],sel=0,tryOpen=false,lastRes=null;

function isDark(){
  var t=document.documentElement.getAttribute('data-theme');
  if(t==='dark') return true;
  if(t==='light') return false;
  return window.matchMedia('(prefers-color-scheme:dark)').matches;
}
function toggleTheme(){
  var next=isDark()?'light':'dark';
  document.documentElement.setAttribute('data-theme',next);
  localStorage.setItem('bam-theme',next);
  document.getElementById('thbtn').textContent=isDark()?'Light':'Dark';
}
function initTheme(){
  document.getElementById('thbtn').textContent=isDark()?'Light':'Dark';
}

function badge(m,lg){
  return '<span class="badge'+(lg?' blg':'')+' '+m+'">'+m+'</span>';
}

function renderSidebar(){
  document.getElementById('sidebar').innerHTML=routes.map(function(r,i){
    var on=i===sel;
    return '<div class="tile'+(on?' sel-'+r.method:'')+'" onclick="bsel('+i+')">'+
      '<div class="tile-top">'+badge(r.method,false)+
      '<span class="tile-path">'+r.path+'</span></div>'+
      '<div class="tile-sum">'+r.summary+'</div></div>';
  }).join('');
}

function resolvedPath(r){
  var p=r.path;
  (r.params||[]).forEach(function(param){
    var el=document.getElementById('pi_'+param.name);
    p=p.replace('{'+param.name+'}',el&&el.value?el.value:'{'+param.name+'}');
  });
  var qparts=[];
  (r.queryParams||[]).forEach(function(param){
    var el=document.getElementById('qp_'+param.name);
    if(el&&el.value)qparts.push(encodeURIComponent(param.name)+'='+encodeURIComponent(el.value));
  });
  if(qparts.length)p+='?'+qparts.join('&');
  return p;
}

function buildCurl(r){
  var url=window.location.origin+resolvedPath(r);
  var cmd='curl -X '+r.method+' "'+url+'"';
  if(r.body!==null){
    var ta=document.getElementById('binput');
    var bv=ta?ta.value:'{}';
    cmd+=' -H "Content-Type: application/json" -d \''+bv+'\'';
  }
  return cmd;
}

function esc(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function renderDetail(){
  var r=routes[sel];
  var h='<div class="dtop"><div class="dpath">'+badge(r.method,true)+
    '<code class="dpathcode">'+r.path+'</code></div>'+
    '<button class="tbtn'+(tryOpen?' on':'')+'" onclick="btoggle()">'+
    (tryOpen?'Cancel':'Try it out')+'</button></div>'+
    '<p class="ddesc">'+esc(r.summary)+'.</p>';

  if(r.params&&r.params.length){
    h+='<div class="sgap"><div class="slabel">Path parameters</div>';
    r.params.forEach(function(p){
      h+='<div class="prow"><code class="pname">'+p.name+'</code>'+
        '<span class="pill pt">'+p.type+'</span>'+
        '<span class="pill pr-'+r.method+'">required</span>'+
        (tryOpen?'<input id="pi_'+p.name+'" class="pinput" type="text" placeholder="'+p.name+' value"/>':'')+'</div>';
    });
    h+='</div>';
  }

  if(r.queryParams&&r.queryParams.length){
    h+='<div class="sgap"><div class="slabel">Query parameters</div>';
    r.queryParams.forEach(function(p){
      h+='<div class="prow"><code class="pname">'+p.name+'</code>'+
        '<span class="pill pt">'+p.type+'</span>'+
        '<span class="pill pt" style="color:var(--txt3)">optional</span>'+
        (tryOpen?'<input id="qp_'+p.name+'" class="pinput" type="text" placeholder="'+p.name+'"/>':'')+'</div>';
    });
    h+='</div>';
  }
  if(r.body!==null){
    h+='<div class="sgap"><div class="slabel">Request body '+
      '<span style="font-weight:400;color:var(--txt2);font-size:11px;margin-left:6px;">application/json</span></div>';
    if(tryOpen){
      h+='<textarea id="binput" class="binput" placeholder="Enter JSON body">{}</textarea>';
    } else {
      h+='<div class="bblock">Send a JSON body with this request.</div>';
    }
    h+='</div>';
  }

  if(tryOpen){
    h+='<button class="ebtn '+r.method+'" onclick="bexec()">Execute</button>';
  }

  if(lastRes){
    var sc=lastRes.status;
    var cls=typeof sc==='number'&&sc<300?'s2xx':typeof sc==='number'&&sc<500?'s4xx':typeof sc==='number'?'s5xx':'serr';
    h+='<div class="rsec"><div class="slabel" style="margin-top:0;">Response</div>'+
      '<div class="rmeta"><span class="scode '+cls+'">'+sc+'</span>'+
      '<span class="rtime">'+lastRes.time+'ms</span></div>'+
      '<div class="slb">Response body</div>'+
      '<div class="cblock">'+esc(lastRes.body)+'</div>'+
      '<div class="slb">Curl</div>'+
      '<div class="cblock">'+esc(lastRes.curl)+'</div></div>';
  } else if(!tryOpen){
    h+='<div class="rsec"><div class="slabel" style="margin-top:0;">Responses</div>';
    var resKeys=Object.keys(r.responses||{});
    if(!resKeys.length)resKeys=['200'];
    resKeys.forEach(function(code){
      var desc=(r.responses&&r.responses[code]&&r.responses[code].description)||'Successful Response';
      var n=parseInt(code,10);
      var cls=n<300?'s2xx':n<500?'s4xx':'s5xx';
      h+='<div style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'+
        '<span class="scode '+cls+'">'+code+'</span>'+
        '<div style="font-size:12px;color:var(--txt2);padding-top:2px;">'+esc(desc)+'</div></div>';
    });
    h+='</div>';
  }

  document.getElementById('detail').innerHTML=h;
}

function bsel(i){sel=i;tryOpen=false;lastRes=null;renderSidebar();renderDetail();}
function btoggle(){tryOpen=!tryOpen;lastRes=null;renderSidebar();renderDetail();}

function bexec(){
  var r=routes[sel];
  var path=resolvedPath(r);
  var opts={method:r.method,headers:{}};
  if(r.body!==null){
    var ta=document.getElementById('binput');
    opts.headers['Content-Type']='application/json';
    opts.body=ta?ta.value:'{}';
  }
  var curl=buildCurl(r);
  var t0=Date.now();
  fetch(path,opts).then(function(res){
    var status=res.status;
    return res.text().then(function(txt){
      var pretty=txt;
      try{pretty=JSON.stringify(JSON.parse(txt),null,2);}catch(e){}
      lastRes={status:status,body:pretty,time:Date.now()-t0,curl:curl};
      renderDetail();
    });
  }).catch(function(err){
    lastRes={status:'ERR',body:String(err),time:Date.now()-t0,curl:curl};
    renderDetail();
  });
}

function loadSpec(){
  fetch('/openapi.json').then(function(res){return res.json();}).then(function(data){
    var paths=data.paths||{};
    routes=[];
    Object.keys(paths).forEach(function(path){
      Object.keys(paths[path]).forEach(function(method){
        var op=paths[path][method];
        var params=(op.parameters||[])
          .filter(function(p){return p.in==='path';})
          .map(function(p){return{name:p.name,type:(p.schema&&p.schema.type)||'string'};});
        var hasBody=['POST','PUT','PATCH'].indexOf(method.toUpperCase())>=0;
        var queryParams=(op.parameters||[])
          .filter(function(p){return p.in==='query';})
          .map(function(p){return{name:p.name,type:(p.schema&&p.schema.type)||'string'};});
        routes.push({
          method:method.toUpperCase(),
          path:path,
          summary:op.summary||path,
          params:params,
          body:hasBody?[]:null,
          responses:op.responses||({}),
          queryParams:queryParams
        });
      });
    });
    if(routes.length){renderSidebar();renderDetail();}
    else{document.getElementById('detail').innerHTML='<p style="padding:24px;color:var(--txt2);">No routes found in spec.</p>';}
  }).catch(function(){
    document.getElementById('detail').innerHTML='<p style="padding:24px;color:var(--txt2);">Could not load /openapi.json.</p>';
  });
}

initTheme();
loadSpec();
</script>
</body>
</html>"""


class Response:
    def __init__(self, body, status=200, headers=None):
        self.body = body
        self.status = status
        self._headers = []
        if headers:
            if isinstance(headers, dict):
                for k, v in headers.items():
                    self._headers.append((k.lower().encode(), str(v).encode()))
            else:
                for item in headers:
                    k, v = item
                    if isinstance(k, str):
                        k = k.lower().encode()
                    if isinstance(v, str):
                        v = v.encode()
                    self._headers.append((k, v))

    @property
    def headers(self):
        return self._headers

    def header(self, name, value):
        """Add a response header. Returns self for chaining.

        Example:
            return Response({"ok": True}).header("X-Request-Id", "abc123")
        """
        self._headers.append((name.lower().encode(), str(value).encode()))
        return self


class Request:
    def __init__(self, scope, receive):
        self.scope = scope
        self.receive = receive
        self.method = scope["method"]
        self.path = scope["path"]
        self.headers = {
            k.decode("utf-8").lower(): v.decode("utf-8")
            for k, v in scope.get("headers", [])
        }
        qs = scope.get("query_string", b"").decode("utf-8")
        parsed = parse_qs(qs, keep_blank_values=True) if qs else {}
        self.query_params = {k: v[0] for k, v in parsed.items()}

    async def body(self):
        chunks = []
        more = True
        while more:
            event = await self.receive()
            chunks.append(event.get("body", b""))
            more = event.get("more_body", False)
        return b"".join(chunks)

    async def json(self):
        raw = await self.body()
        if not raw:
            return None
        return json.loads(raw)


class Bamboo:
    def __init__(self, title="Bamboo", version="0.1.0"):
        self.title = title
        self.version = version
        self.routes = []
        self._static_mounts = []
        self._error_handlers = {}
        self.middlewares = []

    def middleware(self, func):
        self.middlewares.append(func)
        return func

    def route(self, method, path, responses=None, query=None):
        pattern = self.compile_path(path)
        def decorator(func):
            self.routes.append((method.upper(), path, pattern, func, responses, query))
            return func
        return decorator

    def get(self, path, responses=None, query=None):
        return self.route("GET", path, responses=responses, query=query)

    def post(self, path, responses=None, query=None):
        return self.route("POST", path, responses=responses, query=query)

    def put(self, path, responses=None, query=None):
        return self.route("PUT", path, responses=responses, query=query)

    def delete(self, path, responses=None, query=None):
        return self.route("DELETE", path, responses=responses, query=query)

    def compile_path(self, path):
        segments = [s for s in path.split("/") if s != ""]
        regex_parts = []
        for segment in segments:
            if segment.startswith("{") and segment.endswith("}"):
                name = segment[1:-1]
                regex_parts.append(r"(?P<%s>[^/]+)" % name)
            else:
                regex_parts.append(re.escape(segment))
        if regex_parts:
            regex = "^/" + "/".join(regex_parts) + "/?$"
        else:
            regex = "^/?$"
        return re.compile(regex)

    def openapi(self):
        paths = {}
        for method, path, pattern, handler, responses, query in self.routes:
            param_names = re.findall(r"{([^}]+)}", path)
            parameters = [
                {
                    "name": name,
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
                for name in param_names
            ]
            if query:
                for qname, qtype in query.items():
                    parameters.append({
                        "name": qname,
                        "in": "query",
                        "required": False,
                        "schema": {"type": qtype},
                    })
            doc = (handler.__doc__ or "").strip()
            summary = doc.splitlines()[0] if doc else handler.__name__
            if responses:
                op_responses = {
                    str(code): {"description": desc}
                    for code, desc in responses.items()
                }
            else:
                op_responses = {"200": {"description": "Successful Response"}}
            operation = {
                "summary": summary,
                "responses": op_responses,
            }
            if parameters:
                operation["parameters"] = parameters
            paths.setdefault(path, {})[method.lower()] = operation
        return {
            "openapi": "3.0.0",
            "info": {"title": self.title, "version": self.version},
            "paths": paths,
        }

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        request = Request(scope, receive)
        method = request.method
        path = request.path

        if method == "GET" and path == "/openapi.json":
            await self.send_json(send, self.openapi())
            return

        if method == "GET" and path == "/docs":
            docs = BAMBOO_DOCS_HTML.replace(
                "__TITLE__", self.title
            ).replace(
                "__VERSION__", self.version
            )
            await self.send_html(send, docs)
            return

        # Static file serving
        if method == "GET":
            for prefix, directory in self._static_mounts:
                if path == prefix or path.startswith(prefix + "/"):
                    import os, mimetypes
                    rel = path[len(prefix):]
                    safe = os.path.normpath(rel).lstrip("/\\")
                    file_path = os.path.join(directory, safe)
                    if not os.path.isfile(file_path):
                        await self.send_json(send, {"error": "not found"}, 404)
                        return
                    mime, _ = mimetypes.guess_type(file_path)
                    mime = mime or "application/octet-stream"
                    with open(file_path, "rb") as f:
                        body = f.read()
                    await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", mime.encode()), (b"content-length", str(len(body)).encode())]})
                    await send({"type": "http.response.body", "body": body})
                    return

        for route_method, route_path, pattern, handler, _responses, _query in self.routes:
            if route_method != method:
                continue
            match = pattern.match(path)
            if match:
                params = match.groupdict()
                try:
                    async def endpoint(req, _params=params, _handler=handler):
                        return await _handler(req, **_params)
                    chain = endpoint
                    for mw in reversed(self.middlewares):
                        chain = self._wrap(mw, chain)
                    result = await chain(request)
                    if isinstance(result, Response):
                        await self.send_response(send, result)
                    else:
                        await self.send_json(send, result)
                except Exception as _exc:
                    await self._dispatch_error(send, request, 500, exc=_exc)
                return

        await self.send_json(send, {"error": "not found"}, 404)

    def _wrap(self, middleware, next_handler):
        async def wrapped(request):
            return await middleware(request, next_handler)
        return wrapped

    async def send_json(self, send, data, status=200):
        body = json.dumps(data).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json; charset=utf-8"),
                (b"content-length", str(len(body)).encode()),
            ],
        })
        await send({"type": "http.response.body", "body": body})

    async def send_html(self, send, html, status=200):
        body = html.encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"text/html; charset=utf-8"),
                (b"content-length", str(len(body)).encode()),
            ],
        })
        await send({"type": "http.response.body", "body": body})

    async def send_response(self, send, response):
        body = json.dumps(response.body).encode("utf-8")
        headers = [
            (b"content-type", b"application/json; charset=utf-8"),
            (b"content-length", str(len(body)).encode()),
        ]
        headers.extend(response.headers)
        await send({
            "type": "http.response.start",
            "status": response.status,
            "headers": headers,
        })
        await send({"type": "http.response.body", "body": body})

    def error_handler(self, status_code):
        """Register a custom handler for a given HTTP status code.

        The handler receives (request) for 404, or (request, exc) for 500.

        Example::

            @app.error_handler(404)
            async def not_found(request):
                return {"error": "nothing here", "path": request.path}

            @app.error_handler(500)
            async def server_error(request, exc):
                return {"error": "something broke", "detail": str(exc)}
        """
        def decorator(func):
            self._error_handlers[status_code] = func
            return func
        return decorator

    async def _dispatch_error(self, send, request, status_code, exc=None):
        """Call the registered error handler, or fall back to default JSON."""
        import inspect
        handler = self._error_handlers.get(status_code)
        if handler:
            sig = inspect.signature(handler)
            params = list(sig.parameters.keys())
            if len(params) >= 2 and exc is not None:
                result = await handler(request, exc)
            else:
                result = await handler(request)
            if isinstance(result, Response):
                await self.send_response(send, result)
            else:
                await self.send_json(send, result, status_code)
        else:
            if status_code == 404:
                await self._dispatch_error(send, request, 404)
            elif status_code == 500:
                await self.send_json(send, {"error": "internal server error"}, 500)
            else:
                await self.send_json(send, {"error": "error"}, status_code)

    def static(self, url_prefix, directory):
        """Register a directory to serve static files from a URL prefix."""
        import os
        self._static_mounts.append((
            url_prefix.rstrip("/"),
            os.path.abspath(directory),
        ))
