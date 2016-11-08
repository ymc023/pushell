from django.contrib.auth import login, authenticate
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response


def Signin(request):
    if request.method=='POST':
        password = request.POST['password']
        username   = request.POST['username']



        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                from totp_auth import TotpAuth
                code = TotpAuth().secret
                request.session['username'] = username
                request.session['password'] = password
                request.session['code'] = code


                #login(request, user)
                return HttpResponseRedirect('/gauth/')
            else:
                return HttpResponse(({'success':'false'}))
        else:
            return HttpResponse('Wrong credentials')


    else:

        return render_to_response('login.html',RequestContext(request))


def GAuth(request):
    if request.method=='POST':


        code = request.POST['code']
        # try google


        user = authenticate(username=request.session['username'], password= request.session['password'])
        if user is not None:
            if user.is_active:

                login(request, user)
                return HttpResponse('success')
            else:
                return HttpResponse(({'success':'false'}))
        else:
            return HttpResponse(({'success':'false'}))


    else:

        return render_to_response('choose.html',RequestContext(request),locals())


    domain = urlparse.urlparse(request.url).netloc
    if not domain:
        domain = 'example.com'
    username = "%s@%s" % (current_user.id, domain)
    qrcode = current_user.totp.qrcode(username)
    stream = StringIO.StringIO()
    qrcode.save(stream)
    image = stream.getvalue()
    return Response(image, mimetype='image/png')